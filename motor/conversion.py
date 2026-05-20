"""
conversion.py
Funciones para convertir entre JSON (dicts de Python) y árboles (NodoArbol).

JSON → árbol:   _json_a_nodo, _documento_a_arbol
Árbol → JSON:   _arbol_a_json, _raiz_a_dict
"""

from typing import Any
from motor.nodo_arbol import NodoArbol


# ---------------------------------------------------------------------------
# JSON → Árbol
# ---------------------------------------------------------------------------

def _json_a_nodo(clave: str, valor: Any) -> NodoArbol:
    """
    Convierte un par clave-valor de JSON en un NodoArbol.

    Si el valor es un dict (objeto anidado), crea un nodo sin valor
    y llama a sí misma recursivamente para cada sub-campo.

    Si el valor es simple (str, int, bool, None), crea una hoja.

    Ejemplo con "direccion": {"barrio": "Laureles", "codigo_postal": 50031}:
        → NodoArbol("direccion", None)
              ├── NodoArbol("barrio", "Laureles")
              └── NodoArbol("codigo_postal", 50031)
    """
    if isinstance(valor, dict):
        nodo = NodoArbol(clave, None)
        for sub_clave, sub_valor in valor.items():
            hijo = _json_a_nodo(sub_clave, sub_valor)
            nodo.hijos.agregar(hijo)
    else:
        nodo = NodoArbol(clave, valor)

    return nodo


def _documento_a_arbol(documento: dict) -> NodoArbol:
    """
    Convierte un documento JSON completo en un árbol.
    Crea un nodo raíz llamado "documento" y agrega cada campo como hijo.
    """
    raiz = NodoArbol("documento")
    for clave, valor in documento.items():
        hijo = _json_a_nodo(clave, valor)
        raiz.hijos.agregar(hijo)
    return raiz


# ---------------------------------------------------------------------------
# Árbol → JSON
# ---------------------------------------------------------------------------

def _arbol_a_json(nodo: NodoArbol) -> Any:
    """
    Reconstruye el valor JSON a partir de un NodoArbol.

    Hoja   → retorna el valor directamente.
    Objeto → retorna un dict construido recursivamente.
    """
    if nodo.es_hoja():
        return nodo.valor

    resultado: dict = {}
    for hijo in nodo.hijos:
        resultado[hijo.clave] = _arbol_a_json(hijo)
    return resultado


def _raiz_a_dict(raiz: NodoArbol) -> dict:
    """Convierte la raíz de un documento completo a un dict Python."""
    documento: dict = {}
    for hijo in raiz.hijos:
        documento[hijo.clave] = _arbol_a_json(hijo)
    return documento
