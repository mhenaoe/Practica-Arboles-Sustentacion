"""
consultas.py
Funciones para buscar documentos dentro de la colección.

Flujo de una consulta find({"direccion.barrio": "Laureles"}):
  1. _obtener_valor_en_ruta  → navega el árbol hasta encontrar el valor
  2. _cumple_condicion       → compara el valor con la condición (operadores $gt, etc.)
  3. _cumple_filtro          → verifica que el documento cumpla TODAS las condiciones
"""

from typing import Any, Optional
from motor.nodo_arbol import NodoArbol


def _obtener_valor_en_ruta(raiz: NodoArbol, ruta: str) -> Any:
    """
    Navega el árbol siguiendo una ruta separada por puntos.

    Ejemplo con ruta = "direccion.barrio":
      1. Divide: ["direccion", "barrio"]
      2. Busca "direccion" entre los hijos de la raíz
      3. Busca "barrio" entre los hijos de "direccion"
      4. "barrio" es hoja → retorna su valor

    Retorna None si la ruta no existe en el documento.
    """
    partes = ruta.split(".")
    actual = raiz

    for parte in partes:
        encontrado: Optional[NodoArbol] = None
        for hijo in actual.hijos:
            if hijo.clave == parte:
                encontrado = hijo
                break

        if encontrado is None:
            return None

        actual = encontrado

    return actual.valor if actual.es_hoja() else actual


def _cumple_condicion(valor: Any, condicion: Any) -> bool:
    """
    Verifica si un valor cumple una condición.

    Condición directa:      condicion = "Medellín"    → valor == "Medellín"
    Condición con operador: condicion = {"$gt": 25}   → valor > 25

    Operadores: $eq  $ne  $gt  $gte  $lt  $lte

    Retorna False si el tipo no permite la comparación (ej: "Ana" > 25).
    """
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


def _cumple_filtro(raiz: NodoArbol, filtro: dict) -> bool:
    """
    Verifica si un documento cumple TODAS las condiciones del filtro.
    Si alguna condición falla, retorna False de inmediato.
    """
    for ruta, condicion in filtro.items():
        valor = _obtener_valor_en_ruta(raiz, ruta)
        if not _cumple_condicion(valor, condicion):
            return False
    return True
