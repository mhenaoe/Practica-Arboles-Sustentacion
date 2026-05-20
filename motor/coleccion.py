"""
coleccion.py
Clase principal DocumentCollection.

Agrupa todo el sistema y expone tres métodos públicos:
  - load(data)            recibe una lista de dicts y carga la colección
  - load_from_file(path)  lee un archivo .json y llama a load()
  - find(filtro)          busca documentos que cumplan el filtro
  - to_json()             reconstruye toda la colección como lista de dicts
"""

import json
from motor.lista_documentos import ListaDocumentos
from motor.conversion import _documento_a_arbol, _raiz_a_dict
from motor.consultas import _cumple_filtro


class DocumentCollection:
    """
    Colección de documentos almacenados como árboles en una lista enlazada.
    Simula el comportamiento básico de una colección en MongoDB.

    Uso:
        collection = DocumentCollection()
        collection.load(lista_de_dicts)
        collection.find({"ciudad": "Medellín"})
        collection.to_json()
    """

    def __init__(self):
        self.documentos: ListaDocumentos = ListaDocumentos()

    def load(self, data: list) -> None:
        """
        Recibe una lista de dicts Python y convierte cada uno en un árbol.
        Agrega cada árbol a la lista enlazada interna.
        """
        for documento in data:
            arbol = _documento_a_arbol(documento)
            self.documentos.agregar(arbol)

    def load_from_file(self, ruta_archivo: str) -> None:
        """Lee un archivo .json y carga sus documentos."""
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
        self.load(data)

    def find(self, filtro: dict) -> list:
        """
        Retorna todos los documentos que cumplen el filtro.

        Ejemplos de filtros válidos:
            {"ciudad": "Medellín"}
            {"edad": {"$gt": 25}}
            {"ciudad": "Bogotá", "edad": {"$gte": 18}}
            {"direccion.barrio": "Laureles"}
        """
        if self.documentos.esta_vacia():
            print("La colección está vacía.")
            return []

        resultados: list = []
        for raiz in self.documentos:
            if _cumple_filtro(raiz, filtro):
                resultados.append(_raiz_a_dict(raiz))

        if not resultados:
            print("No se encontraron documentos que cumplan la consulta.")

        return resultados

    def to_json(self) -> list:
        """Reconstruye y retorna toda la colección como lista de dicts."""
        resultado: list = []
        for raiz in self.documentos:
            resultado.append(_raiz_a_dict(raiz))
        return resultado
