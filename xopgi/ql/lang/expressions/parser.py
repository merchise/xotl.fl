#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import List, Union, Deque
from collections import deque

from xoutil.objects import setdefaultattr
from ply import lex, yacc

from .base import (
    AST,
    Identifier,
    Literal,
    Lambda,
    Application,
    Let,
    Letrec
)

from ..builtins import StringType, CharType, NumberType


class ParserError(SyntaxError):
    pass


tokens = [
    'IDENTIFIER',
    'BASE16_INTEGER',
    'BASE10_INTEGER',
    'BASE8_INTEGER',
    'BASE2_INTEGER',
    'COLON',
    'DOT_OPERATOR',
    'SPACE',
    'PADDING',
    'LPAREN',
    'RPAREN',
    'CHAR',
    'STRING',
    'PLUS',
    'MINUS',
    'STAR',
    'SLASH',
    'BACKSLASH',
    'ARROW',
    'DOUBLESLASH',
    'PERCENT',
    'OPERATOR',
    'TICK_OPERATOR',
    'ANNOTATION',
    'FLOAT',
    'EQ',
]

# Reserved keywords: pairs of (keyword, regexp).  If the regexp is None, it
# defaults to '\b{keyword}\b' (case-sensitive).
reserved = [
    ('let', None),

    # We need the KEYWORD_IN to match the preceding spaces to avoid the lexer
    # to issue a 'SPACE'.  Otherwise, in an expression like 'let id x = x in
    # ...'; the body of the last equation ('x') is a full expression; and the
    # parser would be in a state `expr . SPACE KEYWORD_IN ...`; at which it
    # will try to match the application.
    ('in', r'\s+in\b'),
]


for keyword, regexp in reserved:
    tk = f'KEYWORD_{keyword.upper()}'

    def tkdef(t):
        setdefaultattr(t.lexer, 'col', 0)
        t.value = t.value.strip()
        t.lexer.col += len(keyword)
        return t

    tkdef.__doc__ = regexp or rf'\b{keyword}\b'
    tkdef.__name__ = tkname = f't_{tk}'

    globals()[tkname] = tkdef
    tokens.append(tk)


t_IDENTIFIER = r'[A-Za-z]\w*'
t_BASE10_INTEGER = '[0-9][0-9_]*'
t_BASE16_INTEGER = '0[xX][0-9a-fA-F][0-9a-fA-F_]*'
t_BASE8_INTEGER = '0[oO][0-7][0-7_]*'
t_BASE2_INTEGER = '0[bB][01][01_]*'

t_COLON = r':'


def t_STRING(t):
    r'\"([^\n]|\\["])*\"'
    # eval is safe because t.value must match the regular expression.  Notice
    # that you must use `string_repr`:func: to get a string representation
    # that work in our language.
    t.value = eval(t.value)
    return t


def string_repr(s):
    result = ['"']
    for ch in s:
        if ch == "'":
            result.append(ch)
        elif ch == '"':
            result.append('\\')
            result.append(ch)
        else:
            result.append(repr(ch)[1:-1].replace(r'\\', '\\'))
    result.append('"')
    return ''.join(result)


def t_CHAR(t):
    r"'([^\n]|(\\[ntr])|(\\[xuU][a-f\d]+))'"
    value = t.value[1:-1]
    if len(value) > 1:
        assert value.startswith('\\')
        # \x..., \u...
        value = eval(f"'{value}'")
    t.value = value
    return t


# We need to treat space specially in this grammar because it can have a
# semantical value: the application of expressions 'e1 e2'.
#
# We want to emit a SPACE token only when application is **not impossible**.
#
# We disallow to break applications with a new line; so 'f \n a' won't a emit
# SPACE token but a PADDING (because \n).
#
# In the malformed expression '+ a b' the first space is ignore and the second
# is emitted; but in the well-formed expression '(+) a b' both spaces are
# emitted.
#
# In expressions like 'let x ...' the space after the keyword is not ignored
# but required.
def t_SPACE(t):
    r'[ \t\n]+'
    if '\n' in t.value:
        if t.lexpos + len(t.value) != len(t.lexer.lexdata):
            t.type = 'PADDING'
            t.lexer.lineno += t.value.count('\n')
            return t
        else:
            return  # the end of the file matches no token.
    elif not t.lexpos or t.lexpos + len(t.value) == len(t.lexer.lexdata):
        return  # This removes the token entirely.
    else:
        # In the expression:
        #
        #    e0   (   e1   e2   )   e3
        #       ^   !    ^    !   ^
        #
        # The run of spaces marked with '^' are important and must be kept,
        # but the spaces above the '!' are just padding and can be ignored
        # (don't create a token for them).
        #
        before = t.lexer.lexdata[t.lexpos - 1]
        after = t.lexer.lexdata[t.lexpos + len(t.value)]
        common = '=<>`.,:+-%@!$*^/'
        if before in common + '(' or after in common + ')':
            return  # This removes the token entirely.
        else:
            return t


def t_LPAREN(t):
    r'\('
    return t


def t_RPAREN(t):
    r'\)'
    return t


def t_FLOAT(t):
    r'([0-9_]*\.[0-9]+([eE][-+]\d+)?|[0-9][0-9_]*[eE][-+]\d+)'
    if t.value.startswith('_'):
        raise lex.LexError(f'Illegal float representation {t.value!r}', t.lexpos)
    t.value = t.value.replace('_', '')
    return t


# PLUS, MINUS, EQ and DOT are treated specially to disambiguate (binary + from
# unary +, etc); DOT is right associative.

def t_PLUS(t):
    r'(?<![/\.\-\+\*<>\$%\^&!@\#=\|])\+(?![/\.\-\+\*<>\$%\^&!@\#=\|])'
    return t


def t_MINUS(t):
    r'(?<![/\.\-\+\*<>\$%\^&!@\#=\|])\-(?![/\.\-\+\*<>\$%\^&!@\#=\|])'
    return t


def t_STAR(t):
    r'(?<![/\.\-\+\*<>\$%\^&!@\#=\|])\*(?![/\.\-\+\*<>\$%\^&!@\#=\|])'
    return t


def t_DOUBLESLASH(t):
    r'(?<![/\.\-\+\*<>\$%\^&!@\#=\|])\/\/(?![/\.\-\+\*<>\$%\^&!@\#=\|])'
    return t


def t_SLASH(t):
    r'(?<![/\.\-\+\*<>\$%\^&!@\#=\|])\/(?![/\.\-\+\*<>\$%\^&!@\#=\|])'
    return t


def t_ARROW(t):
    r'(?<![/\.\-\+\*<>\$%\^&!@\#=\|])\-\>(?![/\.\-\+\*<>\$%\^&!@\#=\|])'
    return t


def t_BACKSLASH(t):
    r'(?<![/\.\-\+\*<>\$%\^&!@\#=\|])\\(?![/\.\-\+\*<>\$%\^&!@\#=\|])'
    return t


def t_PERCENT(t):
    r'(?<![/\.\-\+\*<>\$%\^&!@\#=\|])%(?![/\.\-\+\*<>\$%\^&!@\#=\|])'
    return t


def t_EQ(t):
    r'(?<![/\.\-\+\*<>\$%\^&!@\#=\|])=(?![/\.\-\+\*<>\$%\^&!@\#=\|])'
    return t


# Don't merge this with OPERATOR, we need it to make sure is
# right-associative.
def t_DOT_OPERATOR(t):
    r'\.(?![/\.\-\+\*<>\$%\^&!@\#=\|])'
    return t


def t_TICK_OPERATOR(t):
    r'`[A-Za-z]\w*`'
    t.value = t.value[1:-1]
    return t


# Emit the ANNOTATION only if the '@' surrounded by a possible number and a
# possible string/char/identifier.
def t_ANNOTATION(t):
    r'(?<=[0-9a-fA-F_])@(?=[\'"A-Za-z])'
    return t


def t_OPERATOR(t):
    r'[/\.\-\+\*<>\$%\^&!@\#=\|]+'
    return t


lexer = lex.lex(debug=False)


precedence = (
    ('right', 'ARROW', ),

    ('left', 'KEYWORD_LET', ),
    ('left', 'KEYWORD_IN', ),

    ('left', 'TICK_OPERATOR', ),
    ('left', 'OPERATOR', ),

    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'SLASH', 'DOUBLESLASH', 'PERCENT'),

    ('right', 'DOT_OPERATOR', ),

    # Application has the highest priority, and is left associative:
    # 'a b c' means '(a b) c'.
    ('left', 'SPACE', ),
)


def p_standalone_expr(prod):
    '''st_expr : expr
               | PADDING expr
    '''
    count = len(prod)
    prod[0] = prod[count - 1]


def p_literals_and_basic(prod):
    '''expr :  number
             | concrete_number
             | string
             | char
             | identifier
             | enclosed_expr
             | letexpr
    '''
    prod[0] = prod[1]


def p_char(prod):
    'char : CHAR'
    prod[0] = Literal(prod[1], CharType)


def p_string(prod):
    'string : STRING'
    prod[0] = Literal(prod[1], StringType)


def p_variable(prod):
    'identifier : IDENTIFIER'
    prod[0] = Identifier(prod[1])


def p_paren_expr(prod):
    'enclosed_expr : LPAREN expr RPAREN'
    prod[0] = prod[2]


def p_infix_application(prod):
    'expr : expr TICK_OPERATOR expr'
    prod[0] = Application(Application(Identifier(prod[2]), prod[1]), prod[3])


def p_application(prod):
    'expr : expr SPACE expr'
    prod[0] = Application(prod[1], prod[3])


def p_application_after_paren(prod):
    '''expr : enclosed_expr expr
            | expr enclosed_expr
    '''
    prod[0] = Application(prod[1], prod[2])


def p_compose(prod):
    r'''
    expr : expr DOT_OPERATOR expr
    '''
    e1, e2 = prod[1], prod[3]
    prod[0] = Application(Application(Identifier('.'), e1), e2)


def p_operators_as_expressios(prod):
    '''enclosed_expr : LPAREN DOT_OPERATOR RPAREN
                     | LPAREN operator RPAREN
    '''
    operator = prod[2]
    prod[0] = Identifier(operator)


def p_user_operator_expr(prod):
    r'''expr : expr operator expr

    '''
    e1, operator, e2 = prod[1], prod[2], prod[3]
    prod[0] = Application(Application(Identifier(operator), e1), e2)


def p_operator(prod):
    r'''
    operator :  PLUS
              | MINUS
              | STAR
              | SLASH
              | DOUBLESLASH
              | PERCENT
              | ARROW
              | OPERATOR

    '''
    prod[0] = prod[1]


def p_integer(prod):
    '''number : BASE10_INTEGER
              | BASE16_INTEGER
              | BASE8_INTEGER
              | BASE2_INTEGER
    '''
    value = prod[1]
    value = value.replace('_', '')  # We separators anywhere: 1000 = 10_00
    base = 10
    if value.startswith('0'):
        mark = value[1:2]
        if mark in ('x', 'X'):
            base = 16
        elif mark in ('b', 'B'):
            base = 2
        elif mark in ('o', 'O'):
            base = 8
        elif not mark or mark in '0123456789':
            pass
        else:
            assert False, 'Invalid integer mark'
    val = int(value, base)
    prod[0] = Literal(val, NumberType)


def p_pos_number(prod):
    '''number : PLUS number'''
    prod[0] = prod[2]


def p_neg_number(prod):
    '''number : MINUS number'''
    number = prod[2]
    assert isinstance(number, Literal)
    number.value = -number.value
    prod[0] = number


def p_float(prod):
    'number : FLOAT'
    prod[0] = Literal(float(prod[1]), NumberType)


def p_concrete_number(prod):
    '''concrete_number :  number ANNOTATION string
                        | number ANNOTATION char
                        | number ANNOTATION identifier
    '''
    number = prod[1]
    assert isinstance(number, Literal)
    number.annotation = prod[3]
    prod[0] = number


def p_empty(prod):
    '''empty : '''
    pass


def p_lambda_definition(prod):
    '''expr : BACKSLASH parameters ARROW expr
    '''
    params = prod[2]
    assert params
    prod[0] = build_lambda(params, prod[4])


def p_parameters(prod):
    '''parameters : IDENTIFIER _parameters
    '''
    names = prod[2]
    names.insert(0, prod[1])
    prod[0] = names


def p__params(prod):
    '_parameters : SPACE IDENTIFIER _parameters'
    names = prod[3]
    names.insert(0, prod[2])
    prod[0] = names


def p_empty__parameters(prod):
    '''_parameters : empty
    '''
    prod[0] = []


# Patterns and Equations.  In the final AST, an expression like:
#
#     let id x = x in ...
#
# would actually be like
#
#     let id = \x -> x
#
# with some complications if pattern-matching is allowed:
#
#     let length [] = 0
#         lenght (x:xs) = 1 + length xs
#     in  ...
#
# For now, we allow only the SIMPLEST of all definitions (we don't have a
# 'case' keyword to implement pattern matching.)  But, in any case, having the
# names of productions be 'pattern' and 'equations' is fit.
#
#
# The Pattern and Equation definitions are purposely not part of the AST, but
# more concrete syntactical object in the source code.  In the final AST, the
# let expressions shown above are indistinguishable.


class Pattern:
    def __init__(self, cons, params=None):
        self.cons = cons
        self.params = params or []

    def __repr__(self):
        return f'<pattern {self.cons!r} {self.params!r}>'

    def __str__(self):
        if self.params:
            return f'{self.cons} {self.parameters}'
        else:
            return self.cons

    @property
    def parameters(self):
        return ' '.join(self.params)


def p_pattern(prod):
    '''pattern : parameters'''
    cons, *params = prod[1]
    prod[0] = Pattern(cons, params)


class Equation:
    def __init__(self, pattern: Pattern, body: AST) -> None:
        self.pattern = pattern
        self.body = body

    def __repr__(self):
        return f'<equation {self.pattern!s} = {self.body!r}>'


def p_equation(prod):
    '''equation : pattern EQ expr
    '''
    prod[0] = Equation(prod[1], prod[3])


class Equations(list):
    pass


def p_equation_set(prod):
    '''equations : equation _equation_set
    '''
    result = prod[2]
    result.append(prod[1])
    prod[0] = Equations(result)


def p_equation_set2(prod):
    '''
    _equation_set : PADDING equation _equation_set
    '''
    result = prod[3]
    result.append(prod[2])
    prod[0] = result


def p_equation_set3(prod):
    '''
    _equation_set : empty
    '''
    prod[0] = []


def p_let_expr(prod):
    '''letexpr : KEYWORD_LET SPACE equations KEYWORD_IN SPACE st_expr

    '''
    #
    # We need to decide if we issue a Let or a Letrec: if any of declared
    # names appear in the any of the bodies we must issue a Letrec, otherwise
    # issue a Let.
    #
    # Also we need to convert function-patterns into Lambda abstractions:
    #
    #    let id x = ...
    #
    # becomes:
    #
    #    led id = \x -> ...
    #
    # For the time being (we don't have pattern matching yet), each symbol can
    # be defined just once.
    #
    def to_lambda(equation: Equation):
        'Convert (if needed) an equation to the equivalent one using lambdas.'
        if equation.pattern.params:
            return Equation(
                Pattern(equation.pattern.cons),
                build_lambda(equation.pattern.params, equation.body)
            )
        else:
            return equation

    equations = [to_lambda(eq) for eq in prod[3]]
    conses = [eq.pattern.cons for eq in equations]
    names = set(conses)
    if len(names) != len(conses):
        raise SyntaxError('Several definitions for the same name')
    if any(set(find_free_names(eq.body)) & names for eq in equations):
        klass = Letrec
    else:
        klass = Let
    body = prod[6]
    prod[0] = klass({eq.pattern.cons: eq.body for eq in equations}, body)


def p_error(prod):
    raise ParserError('Invalid expression')


parser = yacc.yacc(debug=True, start='st_expr')


def build_lambda(params: List[str], body: AST) -> Lambda:
    '''Create a Lambda from several parameters.

    Example:

       >>> build_lambda(['a', 'b'], Identifier('a'))
       Lambda('a', Lambda('b', Identifier('a')))

    '''
    assert params
    result = body
    for param in reversed(params):
        result = Lambda(param, result)
    return result  # type: ignore


def find_free_names(expr: AST) -> List[str]:
    '''Find all names that appear free in `expr`.

    Example:

      >>> set(find_free_names(parse('let id x = x in map id xs')))  # doctest: +LITERAL_EVAL
      {'map', 'xs'}

    Names can be repeated:

      >>> find_free_names(parse('twice x x')).count('x')
      2

    '''
    POPFRAME = None  # remove a binding from the 'stack'
    result: List[str] = []
    bindings: Deque[str] = deque([])
    nodes: Deque[Union[None, AST]] = deque([expr])
    while nodes:
        node = nodes.pop()
        if node is POPFRAME:
            bindings.pop()
        elif isinstance(node, Identifier):
            if node.name not in bindings:
                result.append(node.name)
        elif isinstance(node, Literal):
            if isinstance(node.annotation, AST):
                nodes.append(node)
        elif isinstance(node, Application):
            nodes.extend([
                node.e1,
                node.e2,
            ])
        elif isinstance(node, Lambda):
            bindings.append(node.varname)
            nodes.append(POPFRAME)
            nodes.append(node.body)
        elif isinstance(node, (Let, Letrec)):
            # This is tricky; the bindings can be used recursively in the
            # bodies of a letrec:
            #
            #    letrec f1 = ....f1 ... f2 ....
            #           f2 = ... f1 ... f2 ....
            #           ....
            #    in ... f1 ... f2 ...
            #
            # So we must make all the names in the bindings bound and then
            # look at all the definitions.
            #
            # We push several POPFRAME at the to account for that.
            bindings.extend(node.bindings.keys())
            nodes.extend(POPFRAME for _ in node.bindings.keys())
            nodes.extend(node.bindings.values())
            nodes.append(node.body)
        else:
            assert False, f'Unknown AST node: {node!r}'
    return result