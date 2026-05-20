"""
nodo_arbol.py
Define el nodo del árbol y la lista enlazada de hijos.

Cada campo de un documento JSON se representa como un NodoArbol.
Los hijos de cada nodo se guardan en una ListaHijos (lista enlazada propia).
"""

from __future__ import annotations
from typing import Any, Optional


class NodoArbol:
    """
    Un nodo dentro del árbol de un documento.

    Nodo HOJA   → tiene clave y valor simple (str, int, bool, None).
    Nodo OBJETO → tiene clave, valor=None, y sus hijos son los sub-campos.

    Ejemplo:
        {"nombre": "Ana", "direccion": {"barrio": "Laureles"}}

        NodoArbol("documento")
          ├── NodoArbol("nombre",    "Ana")       ← hoja
          └── NodoArbol("direccion", None)        ← objeto
                └── NodoArbol("barrio", "Laureles") ← hoja
    """

    def __init__(self, clave: str, valor: Any = None):
        self.clave: str = clave
        self.valor: Any = valor
        self.hijos: ListaHijos = ListaHijos()

    def es_hoja(self) -> bool:
        """Retorna True si el nodo no tiene hijos."""
        return self.hijos.esta_vacia()


class NodoHijo:
    """
    Eslabón de la lista enlazada de hijos.
    Guarda un NodoArbol y un puntero al siguiente hermano.
    """

    def __init__(self, nodo: NodoArbol):
        self.nodo: NodoArbol = nodo
        self.siguiente: Optional[NodoHijo] = None


class ListaHijos:
    """
    Lista enlazada de los hijos de un NodoArbol.
    No usa listas [] de Python internamente.
    """

    def __init__(self):
        self.cabeza: Optional[NodoHijo] = None

    def agregar(self, nodo: NodoArbol) -> None:
        """Agrega un hijo al final de la lista."""
        nuevo = NodoHijo(nodo)
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
        """Permite usar 'for hijo in lista_hijos'."""
        actual = self.cabeza
        while actual is not None:
            yield actual.nodo
            actual = actual.siguiente
