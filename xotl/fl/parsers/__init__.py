#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from xoutil.objects import setdefaultattr
from xoutil.future.datetime import TimeSpan

from ply import lex, yacc

from xotl.fl.types import (
    TypeVariable,
    TypeCons,
    ListTypeCons,
    TypeScheme,
)
from xotl.fl.types import TypeEnvironment  # noqa
from xotl.fl.expressions import (
    AST,
    Identifier,
    Literal,
    Application,
    ConcreteLet,
    ConsPattern,
    Equation,
    DataType,
    DataCons,
    build_lambda,
)

from xotl.fl.builtins import (
    StringType,
    CharType,
    NumberType,
    UnitType,
    DateType,
    DateTimeType,
    DateIntervalType,
)


class ParserError(Exception):
    pass


tokens = [
    'UPPER_IDENTIFIER',
    'LOWER_IDENTIFIER',
    'UNDER_IDENTIFIER',
    'BASE16_INTEGER',
    'BASE10_INTEGER',
    'BASE8_INTEGER',
    'BASE2_INTEGER',
    'COLON',
    'COMMA',
    'DOT_OPERATOR',
    'SPACE',
    'PADDING',
    'NEWLINE',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
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
    'DATETIME',
    'DATE',
    'DATETIME_INTERVAL',
    'DATE_INTERVAL',
    'PIPE',
]

# Reserved keywords: pairs of (keyword, regexp).  If the regexp is None, it
# defaults to '\b{keyword}\b' (case-sensitive).
reserved = [
    ('data', None),

    # These are just to avoid the expression to (re)define them.
    ('class', None),
    ('instance', None),

    ('where', r'\s+where\b'),
    ('let', None),

    ('forall', None),

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
        value = t.value
        lines = value.count('\n')
        t.value = value.strip()
        t.lexer.lineno += lines
        return t

    tkdef.__doc__ = regexp or rf'\b{keyword}\b'
    tkdef.__name__ = tkname = f't_{tk}'

    globals()[tkname] = tkdef
    tokens.append(tk)


t_COLON = r':'


# t_NL and tNLE remove runs of empty spaces at the beginning or end of the
# code, this simplifies the treatment of t_SPACE.  t_STRING needs to appear
# before t_SPACE to ensure the tokenizer captures all spaces in a string as
# part of the string.
def t_NL(t):
    r'^\s+'
    value = t.value
    lines = value.count('\n')
    t.lexer.lineno += lines
    # A program that starts:
    #
    #         +----  column 0
    #         |
    #         v
    # line 0: \n
    # line 1:       \n
    # line 2:     id ....
    #
    # t_NL will match up to the space before 'id'.  So we start at that level
    # of indentation.  If 'id' would start the line, then the last char of
    # 'value' would a '\n' and last would be the empty string.
    #
    # Beware that _indent_level is only set here if there are spaces at the
    # beginning of the program.
    last = value.split('\n')[-1]
    _set_min_indentation_level(t, len(last))
    _set_indentation_level(t, len(last))


def _get_indentation_level(t):
    '''Return the indentation level of the token `t`.'''
    return setdefaultattr(t.lexer, '_indentation_level', 0)


def _set_indentation_level(t, level):
    t.lexer._indentation_level = level
    return t


def _get_min_indentation_level(t):
    '''Return the indentation level of the token `t`.'''
    return setdefaultattr(t.lexer, '_min_indentation_level', 0)


def _set_min_indentation_level(t, level):
    t.lexer._min_indentation_level = level
    return t


def t_NLE(t):
    r'\s+$'


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
            result.append(repr(ch)[1:-1])
    result.append('"')
    return ''.join(result)


def t_CHAR(t):
    r"'(\\[ntr\\']|\\[xuU][a-f\d]+|[^\n])'"
    value = t.value[1:-1]
    if len(value) > 1:
        assert value.startswith('\\')
        # \x..., \u...
        value = eval(f"'{value}'")
    t.value = value
    return t


def t_BASE2_INTEGER(t):
    '-?0[bB][01][01_]*'
    return t


def t_BASE8_INTEGER(t):
    '-?0[oO][0-7][0-7_]*'
    return t


def t_BASE16_INTEGER(t):
    '-?0[xX][0-9a-fA-F][0-9a-fA-F_]*'
    return t


def t_FLOAT(t):
    r'-?([0-9_]*\.[0-9]+([eE][-+]\d+)?|[0-9][0-9_]*[eE][-+]\d+)'
    value = t.value
    if value.startswith('-') or value.startswith('+'):
        sign, value = value[0], value[1:]
    else:
        sign = ''
    if value.startswith('_'):
        raise lex.LexError(f'Illegal float representation {value!r}', t.lexpos)
    t.value = sign + value.replace('_', '')
    return t


# Integers were pushed to the bottom because the tokenizer would make of '0b0'
# the tokens BASE10_INTEGER IDENTIFIER BASE10_INTEGER.
def t_BASE10_INTEGER(t):
    r'-?[0-9][0-9_]*'
    return t


# We need to treat space specially in this grammar because it can have a
# semantical value: the application of expressions 'e1 e2'.
#
# We want to emit a SPACE token only when application is **not impossible**.
#
# We disallow to break applications with a new line; so 'f \n a' won't a emit
# SPACE token but a PADDING (because \n).
#
# SPACE won't be emitted around any operator.  But after a right parenthesis
# or before an left parenthesis, it will be kept.  In the malformed expression
# '+ a b' the first space is ignore and the second is emitted; but in the
# well-formed expression '(+) a b' both spaces are emitted.
#
# In expressions like 'let x ...' the space after the keyword is not ignored
# but required.
#
# See more details in the file ``indentation.rst``.
def t_SPACE(t):
    r'[ \t\n]+'
    if '\n' in t.value:
        value = t.value
        lines = value.count('\n')
        last = value.split('\n')[-1]
        level = len(last)
        _set_indentation_level(t, level)
        if lines > 1 or level == _get_min_indentation_level(t):
            t.type = 'NEWLINE'
        else:
            t.type = 'PADDING'
        t.lexer.lineno += lines
        return t
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
        common = '=<>`.,:+-%@!$*^/|,'
        if before in common + '[(' or after in common + ')]':
            return  # This removes the token entirely.
        else:
            return t


def t_LPAREN(t):
    r'\('
    return t


def t_RPAREN(t):
    r'\)'
    return t


def t_LBRACKET(t):
    r'\['
    return t


def t_RBRACKET(t):
    r'\]'
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


def t_DATETIME(t):
    r'<\d{4,}-\d\d-\d\d[ T]\d\d:\d\d(:\d\d)?(\.\d+)?>'
    import dateutil.parser
    val = t.value[1:-1]
    res = dateutil.parser.parse(val)
    t.value = res
    return t


def t_DATE(t):
    r'<\d{4,}-\d\d-\d\d>'
    import dateutil.parser
    val = t.value[1:-1]
    res = dateutil.parser.parse(val).date()
    t.value = res
    return t


def t_DATETIME_INTERVAL(t):
    (r'<from[ \t]+\d{4,}-\d\d-\d\d[ T]\d\d:\d\d(:\d\d)?(\.\d+)?'
     r'[ \t]+to[ \t]+\d{4,}-\d\d-\d\d[ T]\d\d:\d\d(:\d\d)?(\.\d+)?>')
    raise NotImplementedError


def t_DATE_INTERVAL(t):
    r'<from[ \t]+\d{4,}-\d\d-\d\d[ \t]+to[ \t]+\d{4,}-\d\d-\d\d>'
    import dateutil.parser
    source = t.value[1:-1]
    _, start, _, end = source.split()
    start = dateutil.parser.parse(start)
    end = dateutil.parser.parse(end)
    t.value = TimeSpan(start, end)
    return t


_OPERATOR_MAP = {
    '.': 'DOT_OPERATOR',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'STAR',
    '/': 'SLASH',
    '//': 'DOUBLESLASH',
    '->': 'ARROW',
    '\\': 'BACKSLASH',
    '%': 'PERCENT',
    '=': 'EQ',
    '|': 'PIPE',
    ',': 'COMMA',
}


def t_OPERATOR(t):
    r'[/\.\-\+\*<>\$%\^&!@\#=\\\|,]+'
    t.type = _OPERATOR_MAP.get(t.value, 'OPERATOR')
    return t


def t_IDENTIFIER(t):
    r'[A-Za-z_]\w*'
    value = t.value
    if value.startswith('_'):
        t.type = 'UNDER_IDENTIFIER'
    elif value[0].isupper():
        t.type = 'UPPER_IDENTIFIER'
    else:
        assert value[0].islower()
        t.type = 'LOWER_IDENTIFIER'
    return t


lexer = lex.lex(debug=False)


precedence = (
    ('right', 'ARROW', ),

    ('left', 'KEYWORD_LET', ),
    ('left', 'KEYWORD_IN', ),

    ('left', 'KEYWORD_WHERE', ),

    ('left', 'TICK_OPERATOR', ),
    ('left', 'OPERATOR', ),

    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'SLASH', 'DOUBLESLASH', 'PERCENT'),

    ('right', 'DOT_OPERATOR', ),

    # Application has the highest priority, and is left associative:
    # 'a b c' means '(a b) c'.
    ('left', 'SPACE', ),
)


def p_application(prod):
    'expr_factor : expr_factor SPACE expr_factor'
    prod[0] = Application(prod[1], prod[3])


# XXX: The only infix op at level 9 is DOT and it is right-associative.
def p_expressions_precedence_rules(prod):
    '''
    expr_term9 : expr_factor infixr_operator_9 expr_term9
               | expr_factor

    expr_term7 : expr_term7 infixl_operator_7 expr_term9
               | expr_term9

    expr_term6 : expr_term6 infixl_operator_6 expr_term7
               | expr_term7

    expr_term2 : expr_term2 infixl_operator_2 expr_term6
               | expr_term6

    expr_term1 : expr_term2 infixr_operator_2 expr_term1
               | expr_term2

    expr_term0 : expr infixl_operator_0 expr_term0
               | expr_term1

    '''
    rhs = prod[1:]
    if len(rhs) > 1:
        e1, op, e2 = prod[1:]
        prod[0] = Application(Application(Identifier(op), e1), e2)
    else:
        prod[0] = prod[1]


def p_standalone_definitions(prod):
    '''
    st_expr : expr

    expr : expr_term0

    expr_factor : literal
                | identifier
                | enclosed_expr
                | letexpr
                | where_expr
                | lambda_expr
                | simple_list_expr
                | simple_tuple_expr

    st_type_expr : type_expr

    '''
    count = len(prod)
    prod[0] = prod[count - 1]


def p_literals(prod):
    '''literal : number
             | concrete_number
             | string
             | char
             | date
             | datetime
             | date_interval
             | datetime_interval
    '''
    prod[0] = prod[1]


def p_tuple_expr(prod):
    '''simple_tuple_expr : LPAREN _list_items RPAREN
    '''
    lst = prod[2]
    if lst:
        assert len(lst) > 1, 'There is no way to build a 1-tuple'
        cons = ',' * (len(lst) - 1)
        result = Identifier(cons)
        for item in lst:
            result = Application(result, item)
    else:
        result = Literal((), UnitType)
    prod[0] = result


def p_list_expr(prod):
    '''simple_list_expr : LBRACKET _list_items RBRACKET
    '''
    lst = prod[2]
    result = Identifier('[]')
    for item in reversed(lst):
        result = Application(Application(Identifier(':'), item), result)
    prod[0] = result


def p_list_items(prod):
    '''_list_items : expr _list_items_cont
       _list_items_cont : COMMA expr _list_items_cont
    '''
    last = len(prod) - 1
    lst = prod[last]
    lst.insert(0, prod[last - 1])
    prod[0] = lst


def p_list_items_empty(prod):
    '''_list_items : empty
       _list_items_cont : empty
    '''
    prod[0] = []


def p_date(prod):
    '''date : DATE
    '''
    prod[0] = Literal(prod[1], DateType)


def p_datetime(prod):
    '''datetime : DATETIME
    '''
    prod[0] = Literal(prod[1], DateTimeType)


def p_date_interval(prod):
    '''date_interval : DATE_INTERVAL
    '''
    prod[0] = Literal(prod[1], DateIntervalType)


def p_datetime_interval(prod):
    '''datetime_interval : DATETIME_INTERVAL
    '''
    prod[0] = prod[1]


def p_char(prod):
    'char : CHAR'
    prod[0] = Literal(prod[1], CharType)


def p_string(prod):
    'string : STRING'
    prod[0] = Literal(prod[1], StringType)


def p_variable(prod):
    '''identifier : _identifier

    '''
    prod[0] = Identifier(prod[1])


def p_bare_identifier(prod):
    '''_identifier : UNDER_IDENTIFIER
                   | UPPER_IDENTIFIER
                   | LOWER_IDENTIFIER

    '''
    prod[0] = prod[1]


def p_paren_expr(prod):
    'enclosed_expr : LPAREN expr RPAREN'
    prod[0] = prod[2]


def p_application_after_paren(prod):
    '''expr_factor : enclosed_expr expr_factor
                   | expr_factor enclosed_expr
    '''
    prod[0] = Application(prod[1], prod[2])


def p_operators_as_expressios(prod):
    '''enclosed_expr : _enclosed_operator
    '''
    prod[0] = Identifier(prod[1])


def p_enclosed_operator(prod):
    '''_enclosed_operator : LPAREN _st_operator RPAREN'''
    prod[0] = prod[2]


# The user may use '->' for a custom operator; that's why need the ARROW in
# the infix_operator_2 rule.  The _st_operator is for *standard* operators,
# i.e non-names converted to operators; we use this to allow providing the
# builtin type for operators (builtins.py; and nametype_decl below).
def p_operator(prod):
    '''
    infixr_operator_9 : DOT_OPERATOR

    infixl_operator_7 : STAR
                     | SLASH
                     | DOUBLESLASH
                     | PERCENT

    infixl_operator_6 : PLUS
                     | MINUS

    infixr_operator_2 : COLON

    infixl_operator_2 : OPERATOR
                      | ARROW

    infixl_operator_0 : TICK_OPERATOR

    _st_operator : infixl_operator_2
                 | infixr_operator_2
                 | infixl_operator_6
                 | infixl_operator_7
                 | infixr_operator_9
                 | COMMA

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
    if value.startswith('-'):
        sign = -1
        value = value[1:]
    else:
        sign = 1
        if value.startswith('+'):
            value = value[1:]
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
    val = sign * int(value, base)
    prod[0] = Literal(val, NumberType)


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
    '''lambda_expr : BACKSLASH patterns ARROW expr
    '''
    params = prod[2]
    assert params
    prod[0] = build_lambda(params, prod[4])


def p_pattern(prod):
    '''
    pattern : identifier
    pattern : literal
    pattern : cons_pattern
    pattern : list_cons_pattern
    pattern : tuple_cons_pattern
    pattern : empty_list_pattern
    pattern : empty_tuple_pattern
    '''
    prod[0] = prod[1]


def p_list_cons_for_param(prod):
    '''list_cons_pattern : pattern COLON pattern
    '''
    prod[0] = ConsPattern(':', [prod[1], prod[3]])


def p_param_pattern(prod):
    '''cons_pattern : LPAREN _identifier SPACE patterns RPAREN'''
    prod[0] = ConsPattern(prod[2], prod[4])


def p_empty_list_as_pattern(prod):
    '''empty_list_pattern : LBRACKET RBRACKET'''
    # Instead of having the Literal([], ...) make the param a name.
    prod[0] = Identifier('[]')


def p_unit_value_as_pattern(prod):
    '''empty_tuple_pattern : LPAREN RPAREN'''
    # Instead of having the Literal((), ...) make the param a name.
    prod[0] = Literal((), UnitType)


def p_tuple_cons_pattern(prod):
    '''tuple_cons_pattern : LPAREN patterns_comma_sep RPAREN
    '''
    items = prod[2]
    assert len(items) > 1
    prod[0] = ConsPattern(',' * (len(items) - 1), items)


def p_patterns(prod):
    '''patterns : pattern _patterns
       patterns_comma_sep : pattern _patterns_comma
       _patterns : SPACE pattern _patterns
       _patterns_comma : COMMA pattern _patterns_comma
    '''
    last = len(prod) - 1
    lst = prod[last]
    pattern = prod[last - 1]
    lst.insert(0, pattern)
    prod[0] = lst


def p_patterns_empty(prod):
    '''_patterns : empty
       _patterns_comma : empty
    '''
    prod[0] = []


def p_equation(prod):
    '''equation : _identifier _patterns EQ expr
       equation : _enclosed_operator _patterns EQ expr
    '''
    prod[0] = Equation(prod[1], prod[2], prod[4])


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


# We need to have st_expr in the body of the letexpr because having 'expr'
# directly creates problems: 'let ... in f x' would be regarded as '(let
# ... in f) x'.  So st_expr can never be at the left of SPACE in any rule.
def p_let_expr(prod):
    '''
    letexpr : KEYWORD_LET SPACE equations KEYWORD_IN SPACE st_expr

    '''
    prod[0] = ConcreteLet(prod[3], prod[6]).ast


def p_where_expr(prod):
    '''
    where_expr : expr KEYWORD_WHERE SPACE equations
    where_expr : expr KEYWORD_WHERE PADDING equations
    '''
    prod[0] = ConcreteLet(prod[4], prod[1]).ast


def p_error(prod):
    raise ParserError(f'While trying to match: {prod}')


def p_type_expr(prod):
    '''type_expr : type_scheme type_function_expr
                 | type_scheme type_term'''
    scheme, type_ = prod[1], prod[2]
    if scheme:
        prod[0] = TypeScheme(scheme, type_)
    else:
        prod[0] = type_


def p_type_scheme_empty(prod):
    'type_scheme : empty'


def p_type_scheme(prod):
    'type_scheme : KEYWORD_FORALL SPACE _type_scheme_generics'
    generics = prod[3]
    assert generics
    prod[0] = generics


def p_type_scheme_generics(prod):
    '_type_scheme_generics : _identifier SPACE _type_scheme_generics'
    lst = prod[3]
    lst.insert(0, prod[1])
    prod[0] = lst


def p_last_type_scheme_generic(prod):
    '_type_scheme_generics : _identifier DOT_OPERATOR'
    prod[0] = [prod[1]]


def p_type_function_expr(prod):
    '''type_function_expr : type_term ARROW _maybe_padding type_function_expr
                          | type_term
    '''
    count = len(prod)
    if count > 2:
        prod[0] = TypeCons('->', [prod[1], prod[count - 1]], binary=True)
    else:
        prod[0] = prod[1]


def p_type_term(prod):
    '''type_term : type_app_expression
                 | type_factor'''
    prod[0] = prod[1]


def p_type_application_expr(prod):
    'type_app_expression : type_factor _app_args_non_empty'
    cons = prod[1]
    args = tuple(prod[2])
    if isinstance(cons, TypeVariable):
        f = TypeCons(cons.name)
    else:
        assert isinstance(cons, TypeCons)
        f = cons
    prod[0] = TypeCons(f.cons, f.subtypes + args, binary=f.binary)


def p_type_application_args(prod):
    '''_app_args : SPACE type_factor _app_args
       _app_args_non_empty : SPACE type_factor _app_args
    '''
    args = prod[3]
    args.insert(0, prod[2])
    prod[0] = args


def p_type_application_args_empty(prod):
    '_app_args : empty'
    prod[0] = []


def p_type_variable(prod):
    '''type_variable : LOWER_IDENTIFIER'''
    prod[0] = TypeVariable(prod[1])


def p_type_cons(prod):
    '''type_cons : UPPER_IDENTIFIER'''
    prod[0] = TypeCons(prod[1])


def p_type_factor_identifier(prod):
    '''type_factor : type_variable
                   | type_cons

    '''
    prod[0] = prod[1]


def p_type_factor_paren(p):
    '''type_factor : LPAREN _maybe_padding type_expr _maybe_padding RPAREN'''
    p[0] = p[3]


def p_type_factor_bracket(prod):
    'type_factor : LBRACKET _maybe_padding type_expr _maybe_padding RBRACKET'
    prod[0] = ListTypeCons(prod[3])


def p_maybe_padding(prod):
    '''_maybe_padding : PADDING
                      | empty
    '''
    pass


def p_program(prod):
    '''program : definitions
    '''
    prod[0] = prod[1]


class Definition:
    def __init__(self, name: str, body: AST) -> None:
        self.name = name
        self.body = body


class Definitions(list):
    pass


def p_definitions(prod):
    '''definitions : definition _definition_set
    '''
    lst: Definitions = prod[2]
    lst.insert(0, prod[1])
    prod[0] = lst


def p_definition_set(prod):
    '''_definition_set : NEWLINE definition _definition_set
    '''
    lst: Definitions = prod[3]
    lst.insert(0, prod[2])
    prod[0] = lst


def p_definition_set2(prod):
    '''_definition_set : empty
    '''
    prod[0] = []


def p_definition(prod):
    '''definition : nametype_decl
                  | valuedef
                  | datatype_definition
    '''
    prod[0] = prod[1]


def p_valuedef(prod):
    '''valuedef : equation
    '''
    prod[0] = prod[1]


def p_nametype_decl(prod):
    '''nametype_decl : _identifier COLON COLON st_type_expr
    '''
    name = prod[1]
    type_ = prod[4]
    scheme = TypeScheme.from_typeexpr(type_)
    prod[0] = {name: scheme}  # type: TypeEnvironment


def p_nametype_decl_operators(prod):
    '''nametype_decl : LPAREN _st_operator RPAREN COLON COLON st_type_expr
    '''
    name = prod[2]
    type_ = prod[6]
    scheme = TypeScheme.from_typeexpr(type_)
    prod[0] = {name: scheme}  # type: TypeEnvironment


def p_datatype_definition(prod):
    '''datatype_definition : _datatype_lhs EQ _data_rhs
    '''
    name, args, type_ = prod[1]
    defs = prod[3]
    prod[0] = DataType(name, type_, defs)


def p_datatype_lhs(prod):
    '''_datatype_lhs : KEYWORD_DATA SPACE UPPER_IDENTIFIER _cons_params
    '''
    name = prod[3]
    args = prod[4]
    type_ = TypeCons(name, [TypeVariable(n) for n in args])
    prod[0] = (name, args, type_)


def p_datatype_cons_params(prod):
    '''_cons_params : SPACE LOWER_IDENTIFIER _cons_params
    '''
    arg = prod[2]
    args = prod[3]
    args.insert(0, arg)
    prod[0] = args


def p_datatype_cons_params_empty(prod):
    '''_cons_params : empty
    '''
    prod[0] = []


def p_datatype_body(prod):
    '''_data_rhs : data_cons _data_conses
       _data_conses : _maybe_padding PIPE data_cons _data_conses
    '''
    count = len(prod)
    lst = prod[count - 1]
    lst.insert(0, prod[count - 2])
    prod[0] = lst


def p_datatype_conses_empty(prod):
    '_data_conses : empty'
    prod[0] = []


def p_data_cons(prod):
    '''data_cons : _data_cons'''
    name, args = prod[1]
    prod[0] = DataCons(name, args)


def p_bare_data_cons(prod):
    '''_data_cons : UPPER_IDENTIFIER _cons_args'''
    prod[0] = (prod[1], prod[2])


def p_data_cons_args(prod):
    '''_cons_args : SPACE cons_arg _cons_args
    '''
    count = len(prod)
    lst = prod[count - 1]
    lst.insert(0, prod[count - 2])
    prod[0] = lst


def p_data_cons_args_empty(prod):
    '''_cons_args : empty
    '''
    prod[0] = []


def p_cons_arg(prod):
    '''cons_arg : type_variable
       cons_arg : type_cons
       cons_arg : _cons_arg_factor
    '''
    prod[0] = prod[1]


def p_cons_arg_factor(prod):
    '''_cons_arg_factor : LPAREN type_expr RPAREN
    '''
    prod[0] = prod[2]


def p_cons_arg_factor_list(prod):
    '''_cons_arg_factor : LBRACKET type_expr RBRACKET
    '''
    prod[0] = ListTypeCons(prod[2])


type_parser = yacc.yacc(debug=False, start='st_type_expr',
                        tabmodule='type_parsertab')

expr_parser = yacc.yacc(debug=False, start='st_expr',
                        tabmodule='expr_parsertab')

program_parser = yacc.yacc(debug=True, start='program',
                           tabmodule='program_parsertab')
