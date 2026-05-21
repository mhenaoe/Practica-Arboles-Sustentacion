from __future__ import annotations
from typing import Any, Optional


# -------------------------------------------------------------------
# LISTA DOBLEMENTE ENLAZADA
# -------------------------------------------------------------------

class DoublyNode:

    def __init__(
        self,
        value: Any,
        next: Optional["DoublyNode"] = None,
        prev: Optional["DoublyNode"] = None
    ):
        self.value = value
        self.next = next
        self.prev = prev

    def __repr__(self) -> str:
        return f"{self.value}"


class DoublyLinkedList:

    def __init__(self):
        self.head: Optional[DoublyNode] = None
        self.size: int = 0

    def append(self, value: Any) -> None:

        nuevo = DoublyNode(value)

        if self.head is None:
            self.head = nuevo
        else:
            actual = self.head

            while actual.next is not None:
                actual = actual.next

            actual.next = nuevo
            nuevo.prev = actual

        self.size += 1

    def remove(self, value: Any) -> bool:

        actual = self.head

        while actual is not None:

            if actual.value == value:

                # primer nodo
                if actual.prev is None:
                    self.head = actual.next

                    if self.head is not None:
                        self.head.prev = None

                else:
                    actual.prev.next = actual.next

                    if actual.next is not None:
                        actual.next.prev = actual.prev

                self.size -= 1
                return True

            actual = actual.next

        return False

    def pop(self, index: int = 0) -> Any:

        if self.head is None:
            return None

        actual = self.head
        contador = 0

        while actual is not None and contador < index:
            actual = actual.next
            contador += 1

        if actual is None:
            return None

        valor = actual.value
        self.remove(valor)

        return valor

    def extend(self, otra_lista: "DoublyLinkedList") -> None:

        for valor in otra_lista:
            self.append(valor)

    def find(self, condition) -> Any:

        actual = self.head

        while actual is not None:

            if condition(actual.value):
                return actual.value

            actual = actual.next

        return None

    def is_empty(self) -> bool:
        return self.head is None

    def __iter__(self):

        actual = self.head

        while actual is not None:
            yield actual.value
            actual = actual.next

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:

        valores = []

        for valor in self:
            valores.append(str(valor))

        return " <--> ".join(valores)


# -------------------------------------------------------------------
# NODO DEL ARBOL
# -------------------------------------------------------------------

class Node:

    def __init__(self, key: str, value: Any = None):

        self.key: str = key
        self.value: Any = value

        # hijos almacenados con lista enlazada propia
        self.children: DoublyLinkedList = DoublyLinkedList()

    def is_leaf(self) -> bool:
        return self.children.is_empty()

    def __repr__(self) -> str:
        return f"Node({self.key}: {self.value})"


# -------------------------------------------------------------------
# ARBOL GENERAL
# -------------------------------------------------------------------

class GeneralTree:

    def __init__(self, root: Optional[Node] = None):
        self.root = root

    def add_child(self, parent: Node, child: Node) -> None:
        parent.children.append(child)

    def __repr__(self) -> str:
        return repr(self.root) if self.root else "Empty tree"