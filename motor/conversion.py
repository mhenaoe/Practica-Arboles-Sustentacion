from typing import Any
from .estructuras import Node, GeneralTree


# -------------------------------------------------------------------
# JSON -> ARBOL
# -------------------------------------------------------------------

def _json_a_nodo(clave: str, valor: Any) -> Node:

    # objeto anidado
    if isinstance(valor, dict):

        nodo = Node(clave)

        for sub_clave, sub_valor in valor.items():

            hijo = _json_a_nodo(sub_clave, sub_valor)

            nodo.children.append(hijo)

    else:
        nodo = Node(clave, valor)

    return nodo


def _documento_a_arbol(documento: dict) -> GeneralTree:

    raiz = Node("documento")

    for clave, valor in documento.items():

        hijo = _json_a_nodo(clave, valor)

        raiz.children.append(hijo)

    return GeneralTree(raiz)


# -------------------------------------------------------------------
# ARBOL -> JSON
# -------------------------------------------------------------------

def _arbol_a_json(nodo: Node) -> Any:

    # hoja
    if nodo.is_leaf():
        return nodo.value

    resultado = {}

    for hijo in nodo.children:
        resultado[hijo.key] = _arbol_a_json(hijo)

    return resultado


def _raiz_a_dict(arbol: GeneralTree) -> dict:

    documento = {}

    for hijo in arbol.root.children:
        documento[hijo.key] = _arbol_a_json(hijo)

    return documento