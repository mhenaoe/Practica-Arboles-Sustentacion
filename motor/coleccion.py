import json

from .lista_documentos import ListaDocumentos
from .conversion import _documento_a_arbol, _raiz_a_dict
from .consultas import _cumple_filtro


class DocumentCollection:

    def __init__(self):

        self.documentos = ListaDocumentos()

    # ---------------------------------------------------------------
    # CARGA
    # ---------------------------------------------------------------

    def load(self, data: list) -> None:

        for documento in data:

            arbol = _documento_a_arbol(documento)

            self.documentos.agregar(arbol)

    def load_from_file(self, ruta_archivo: str) -> None:

        with open(ruta_archivo, "r", encoding="utf-8") as archivo:

            data = json.load(archivo)

        self.load(data)

    # ---------------------------------------------------------------
    # CONSULTAS
    # ---------------------------------------------------------------

    def find(self, filtro: dict) -> list:

        if self.documentos.esta_vacia():

            print("La colección está vacía.")

            return []

        resultados = []

        for arbol in self.documentos:

            if _cumple_filtro(arbol, filtro):

                resultados.append(_raiz_a_dict(arbol))

        if not resultados:
            print("No se encontraron documentos que cumplan la consulta.")

        return resultados

    # ---------------------------------------------------------------
    # RECONSTRUIR JSON
    # ---------------------------------------------------------------

    def to_json(self) -> list:

        resultado = []

        for arbol in self.documentos:

            resultado.append(_raiz_a_dict(arbol))

        return resultado