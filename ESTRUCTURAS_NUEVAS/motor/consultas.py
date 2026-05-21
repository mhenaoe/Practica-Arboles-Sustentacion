from typing import Any, Optional
from estructuras import Node, GeneralTree


# -------------------------------------------------------------------
# BUSQUEDA POR RUTA
# -------------------------------------------------------------------

def _obtener_valor_en_ruta(arbol: GeneralTree, ruta: str) -> Any:

    partes = ruta.split(".")

    actual = arbol.root

    for parte in partes:

        encontrado: Optional[Node] = None

        for hijo in actual.children:

            if hijo.key == parte:
                encontrado = hijo
                break

        if encontrado is None:
            return None

        actual = encontrado

    return actual.value if actual.is_leaf() else actual


# -------------------------------------------------------------------
# OPERADORES
# -------------------------------------------------------------------

def _cumple_condicion(valor: Any, condicion: Any) -> bool:

    # igualdad simple
    if not isinstance(condicion, dict):
        return valor == condicion

    for operador, limite in condicion.items():

        try:

            if operador == "$eq":
                if not (valor == limite):
                    return False

            elif operador == "$ne":
                if not (valor != limite):
                    return False

            elif operador == "$gt":
                if not (valor > limite):
                    return False

            elif operador == "$gte":
                if not (valor >= limite):
                    return False

            elif operador == "$lt":
                if not (valor < limite):
                    return False

            elif operador == "$lte":
                if not (valor <= limite):
                    return False

        except TypeError:
            return False

    return True


# -------------------------------------------------------------------
# FILTRO COMPLETO
# -------------------------------------------------------------------

def _cumple_filtro(arbol: GeneralTree, filtro: dict) -> bool:

    for ruta, condicion in filtro.items():

        valor = _obtener_valor_en_ruta(arbol, ruta)

        if not _cumple_condicion(valor, condicion):
            return False

    return True