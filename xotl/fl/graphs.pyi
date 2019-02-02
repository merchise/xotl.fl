from typing import AbstractSet, List, MutableMapping, Set
from typing import Generic, TypeVar


T = TypeVar('T')


class Graph(Generic[T]):
    nodes: MutableMapping[T, Set[T]]

    def add_edge(self, from_: T, to_: T) -> None:
        ...

    def add_many(self, from_: T, to_: AbstractSet[T]) -> None:
        ...

    def get_topological_order(self) -> List[T]:
        ...

    def get_sccs(self) -> List[AbstractSet[T]]:
        ...
