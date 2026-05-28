# Explicación del modelo de clases y análisis de complejidad

## ¿Qué hace el sistema?

Es un mini motor documental inspirado en MongoDB. Recibe documentos en formato JSON, los convierte en árboles, los almacena en una lista enlazada y permite hacer consultas sobre ellos con filtros y operadores.

---

## Archivos del proyecto

```
Practica_Arboles_Sustentacion/
├── coleccion.json          ← datos de entrada
├── pruebas.py              ← archivo que se ejecuta para probar
├── explicacion.md          ← este archivo
└── motor/
    ├── estructuras.py      ← DoublyLinkedList, Node, GeneralTree
    ├── conversion.py       ← JSON → árbol  y  árbol → JSON
    ├── consultas.py        ← operadores y filtros
    ├── lista_documentos.py ← lista enlazada de documentos
    └── coleccion.py        ← DocumentCollection (clase principal)
```

---

## Modelo de clases

El sistema tiene **7 clases** organizadas en 4 capas.

---

### Capa 1 — Estructuras base (`estructuras.py`)

#### `DoublyNode`

Un eslabón de la lista doblemente enlazada. Guarda un valor y dos punteros: uno al siguiente nodo y uno al anterior.

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `value` | `Any` | El dato guardado en este eslabón |
| `next` | `DoublyNode \| None` | Puntero al siguiente eslabón |
| `prev` | `DoublyNode \| None` | Puntero al eslabón anterior |

---

#### `DoublyLinkedList`

Lista doblemente enlazada. Se usa para guardar los **hijos de cada nodo del árbol**, cumpliendo la restricción de no usar listas `[]` de Python.

```
None ← [hijo_1] ↔ [hijo_2] ↔ [hijo_3] → None
```

| Método | Descripción |
|--------|-------------|
| `append(value)` | Agrega un elemento al final |
| `remove(value)` | Elimina un elemento por valor |
| `pop(index)` | Obtiene y elimina el elemento en la posición dada |
| `extend(otra)` | Agrega todos los elementos de otra lista |
| `find(condition)` | Retorna el primer elemento que cumple una función |
| `is_empty()` | Retorna `True` si la lista no tiene elementos |
| `__iter__` | Permite usar `for elemento in lista` |
| `__len__` | Permite usar `len(lista)` |

---

#### `Node`

Un nodo del árbol de un documento. Cada campo del JSON se convierte en un `Node`.

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `key` | `str` | Nombre del campo (ej: `"nombre"`, `"edad"`) |
| `value` | `Any` | Valor si es hoja (`"Ana"`, `25`). `None` si es objeto anidado. |
| `children` | `DoublyLinkedList` | Hijos del nodo (vacía si es hoja) |

Un nodo es **hoja** cuando `children` está vacía — guarda un valor simple (string, número, bool, null).
Un nodo es **objeto** cuando tiene hijos — representa un campo cuyo valor es un `{}` en el JSON.

Método `is_leaf()` → retorna `True` si `children` está vacía.

---

#### `GeneralTree`

El árbol completo de un documento. Solo guarda la raíz y expone `add_child()`.

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `root` | `Node \| None` | Nodo raíz del árbol (representa el documento completo) |

---

### Capa 2 — Lista de documentos (`lista_documentos.py`)

#### `NodoColeccion`

Eslabón de la lista enlazada de documentos. Es simple (un solo puntero hacia adelante).

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `arbol` | `GeneralTree` | El árbol completo de un documento |
| `siguiente` | `NodoColeccion \| None` | Puntero al siguiente documento |

#### `ListaDocumentos`

Lista enlazada **simple** que encadena todos los documentos de la colección.

```
[doc_1] → [doc_2] → [doc_3] → None
```

Es simple (no doble) porque para recorrer la colección nunca se necesita ir hacia atrás.

| Método | Descripción |
|--------|-------------|
| `agregar(arbol)` | Agrega un documento al final |
| `esta_vacia()` | Retorna `True` si no hay documentos |
| `__iter__` | Permite usar `for arbol in lista` |

---

### Capa 3 — Conversión (`conversion.py`) y Consultas (`consultas.py`)

Funciones auxiliares que no son clases pero son el núcleo de la lógica.

**conversion.py:**

| Función | Descripción |
|---------|-------------|
| `_json_a_nodo(clave, valor)` | Convierte un par clave-valor en un `Node`. Recursiva para objetos anidados. |
| `_documento_a_arbol(documento)` | Convierte un dict completo en un `GeneralTree` |
| `_arbol_a_json(nodo)` | Reconstruye el valor JSON desde un `Node`. Recursiva. |
| `_raiz_a_dict(arbol)` | Convierte un `GeneralTree` completo en un dict Python |

**consultas.py:**

| Función | Descripción |
|---------|-------------|
| `_obtener_valor_en_ruta(arbol, ruta)` | Navega el árbol siguiendo `"campo.subcampo"` |
| `_cumple_condicion(valor, condicion)` | Aplica operadores `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte` |
| `_cumple_filtro(arbol, filtro)` | Verifica que el documento cumpla TODAS las condiciones |

---

### Capa 4 — Clase principal (`coleccion.py`)

#### `DocumentCollection`

Agrupa todo el sistema. Es la única clase que el usuario usa directamente.

| Método | Descripción |
|--------|-------------|
| `load(data)` | Recibe una lista de dicts y convierte cada uno en árbol |
| `load_from_file(ruta)` | Lee un archivo `.json` y llama a `load()` |
| `find(filtro)` | Retorna los documentos que cumplen el filtro |
| `to_json()` | Reconstruye toda la colección como lista de dicts |

---

## Diagrama completo del sistema

```
coleccion.json
      │
      ▼  load_from_file()  →  json.load()  →  lista de dicts Python
      │
      ▼  _documento_a_arbol() por cada documento
      │
DocumentCollection
  └── documentos: ListaDocumentos
        │
        ├── NodoColeccion → NodoColeccion → NodoColeccion → None
        │     arbol             arbol             arbol
        │       │
        │   GeneralTree
        │     └── root: Node("documento")
        │               └── children: DoublyLinkedList
        │                     ├── Node("id",      1)           ← hoja
        │                     ├── Node("nombre",  "Ana")       ← hoja
        │                     ├── Node("edad",    25)          ← hoja
        │                     ├── Node("ciudad",  "Medellín")  ← hoja
        │                     └── Node("direccion", None)      ← objeto anidado
        │                               └── children: DoublyLinkedList
        │                                     ├── Node("barrio",        "Laureles")
        │                                     └── Node("codigo_postal", 50031)
        │
        ▼  find({"ciudad": "Medellín"})
        │
        │  por cada arbol:
        │    _cumple_filtro()
        │      └── _obtener_valor_en_ruta(arbol, "ciudad") → "Medellín"
        │      └── _cumple_condicion("Medellín", "Medellín") → True
        │    si cumple → _raiz_a_dict(arbol) → dict Python
        │
        ▼
  [{"id": 1, "nombre": "Ana", ...}, {"id": 3, "nombre": "Lucía", ...}]
```

---

## Análisis de complejidad

Variables usadas:
- **n** = número de documentos en la colección
- **m** = número total de nodos en un árbol (campos + sub-campos)
- **d** = profundidad de la ruta (ej: `"direccion.barrio"` → d = 2)
- **k** = número de condiciones en el filtro

---

### Carga de documentos — `load(data)`

Por cada documento se recorre el dict y se construye el árbol nodo por nodo.

- Construir un árbol: **O(m)**
- Para n documentos: **O(n × m)**

---

### Búsqueda por ruta — `_obtener_valor_en_ruta()`

Se baja nivel por nivel. En cada nivel se recorren los hijos buscando la clave.

- Por cada parte de la ruta se revisan hasta m hijos: **O(m)** por nivel
- Para ruta de profundidad d: **O(d × m)**
- En documentos pequeños con pocos campos por nivel: cercano a **O(d)**

---

### Consulta sobre toda la colección — `find(filtro)`

Se recorre la lista enlazada completa. Por cada documento se evalúan k condiciones, cada una con una búsqueda por ruta.

- Total: **O(n × k × d × m)**
- Caso más común (k=1, d=1): **O(n × m)**

---

### Conversión de árbol a JSON — `to_json()` / `_arbol_a_json()`

Se visita cada nodo del árbol exactamente una vez de forma recursiva.

- Por documento: **O(m)**
- Para toda la colección: **O(n × m)**
