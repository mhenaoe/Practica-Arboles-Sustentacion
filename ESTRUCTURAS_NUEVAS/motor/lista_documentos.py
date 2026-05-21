from __future__ import annotations
from typing import Optional
from estructuras import GeneralTree


class NodoColeccion:

    def __init__(self, arbol: GeneralTree):

        self.arbol: GeneralTree = arbol
        self.siguiente: Optional["NodoColeccion"] = None


class ListaDocumentos:

    def __init__(self):

        self.cabeza: Optional[NodoColeccion] = None

    def agregar(self, arbol: GeneralTree) -> None:

        nuevo = NodoColeccion(arbol)

        if self.cabeza is None:
            self.cabeza = nuevo
            return

        actual = self.cabeza

        while actual.siguiente is not None:
            actual = actual.siguiente

        actual.siguiente = nuevo

    def esta_vacia(self) -> bool:
        return self.cabeza is None

    def __iter__(self):

        actual = self.cabeza

        while actual is not None:

            yield actual.arbol

            actual = actual.siguiente