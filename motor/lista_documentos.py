"""
lista_documentos.py
Define la lista enlazada que almacena todos los documentos de la colección.

La colección completa se guarda como:
    doc_1 → doc_2 → doc_3 → None

Cada nodo apunta a la raíz del árbol de un documento.
No usa listas [] de Python internamente.
"""

from __future__ import annotations
from typing import Optional
from motor.nodo_arbol import NodoArbol


class NodoColeccion:
    """
    Eslabón de la lista enlazada de documentos.
    Guarda la raíz del árbol de un documento y apunta al siguiente.
    """

    def __init__(self, raiz: NodoArbol):
        self.raiz: NodoArbol = raiz
        self.siguiente: Optional[NodoColeccion] = None


class ListaDocumentos:
    """
    Lista enlazada que contiene todos los documentos de la colección.
    No usa listas [] de Python internamente.
    """

    def __init__(self):
        self.cabeza: Optional[NodoColeccion] = None

    def agregar(self, raiz: NodoArbol) -> None:
        """Agrega un documento al final de la lista."""
        nuevo = NodoColeccion(raiz)
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
        """Permite usar 'for raiz in lista_documentos'."""
        actual = self.cabeza
        while actual is not None:
            yield actual.raiz
            actual = actual.siguiente
