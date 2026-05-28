# Mini Motor Documental — Árboles y Listas Enlazadas

Proyecto integrador EDD - 20261

Sistema de almacenamiento y consulta de documentos JSON, inspirado en MongoDB. Cada documento se convierte en un árbol, los árboles se encadenan en una lista enlazada, y se pueden hacer consultas con filtros y operadores.

---

## Estructura del proyecto

```
Practica_Arboles_Sustentacion/
├── coleccion.json          ← datos de ejemplo (5 documentos)
├── pruebas.py              ← archivo principal para ejecutar
├── explicacion.md          ← modelo de clases y análisis de complejidad
├── README.md               ← este archivo
└── motor/
    ├── estructuras.py      ← DoublyLinkedList, Node, GeneralTree
    ├── conversion.py       ← JSON → árbol  y  árbol → JSON
    ├── consultas.py        ← operadores y filtros de búsqueda
    ├── lista_documentos.py ← lista enlazada de documentos
    └── coleccion.py        ← DocumentCollection (clase principal)
```

---

## Cómo ejecutar

Desde la carpeta raíz del proyecto:

```bash
python pruebas.py
```

---

## Cómo usar el sistema

```python
from motor.coleccion import DocumentCollection

collection = DocumentCollection()
collection.load_from_file("coleccion.json")  # carga desde archivo
# o también: collection.load([{...}, {...}])  # carga desde lista

# Consultas
collection.find({"ciudad": "Medellín"})
collection.find({"edad": {"$gt": 25}})
collection.find({"edad": {"$gte": 18, "$lte": 30}})
collection.find({"ciudad": "Bogotá", "edad": {"$gte": 30}})
collection.find({"direccion.barrio": "Laureles"})

# Reconstruir el JSON original desde los árboles
collection.to_json()
```

---

## Operadores de consulta soportados

| Operador | Significado | Ejemplo |
|----------|-------------|---------|
| `$eq` | igual a | `{"edad": {"$eq": 25}}` |
| `$ne` | diferente de | `{"ciudad": {"$ne": "Bogotá"}}` |
| `$gt` | mayor que | `{"edad": {"$gt": 25}}` |
| `$gte` | mayor o igual que | `{"edad": {"$gte": 18}}` |
| `$lt` | menor que | `{"edad": {"$lt": 30}}` |
| `$lte` | menor o igual que | `{"edad": {"$lte": 30}}` |

---

## Restricciones cumplidas

- Los hijos de cada nodo del árbol se almacenan en una `DoublyLinkedList` propia — no se usan listas `[]` de Python.
- La colección se almacena en una `ListaDocumentos` propia (lista enlazada simple) — no se usan listas `[]` de Python.
- Los diccionarios de Python solo se usan para leer el JSON inicial, representar el filtro de consulta y reconstruir el JSON de salida.
- Todas las clases y funciones incluyen type hints.
- El sistema maneja casos borde: ruta inexistente, tipo incompatible con operador, colección vacía, sin resultados.

---

## Autora

Mariana Henao Echeverri
