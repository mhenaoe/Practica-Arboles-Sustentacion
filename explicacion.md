# Explicación del modelo de clases y análisis de complejidad

## Modelo de clases

El sistema tiene **5 clases principales** más funciones auxiliares.

---

### 1. `NodoArbol`
Representa un nodo dentro del árbol de un documento.

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `clave` | `str` | Nombre del campo (ej: `"nombre"`, `"edad"`) |
| `valor` | `Any` | Valor del campo si es hoja. `None` si es objeto anidado. |
| `hijos` | `ListaHijos` | Lista enlazada de hijos (vacía si es hoja) |

Un nodo es **hoja** cuando su campo `hijos` está vacío (valor simple: string, número, bool, null).  
Un nodo es **objeto** cuando tiene hijos (campo cuyo valor es un `{}` en el JSON).

---

### 2. `ListaHijos`
Lista enlazada de los hijos de un `NodoArbol`. Usa nodos internos `NodoHijo`.

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `cabeza` | `NodoHijo \| None` | Primer hijo |

Cada `NodoHijo` guarda un `NodoArbol` y un puntero `siguiente` al próximo hermano.

---

### 3. `NodoColeccion`
Nodo de la lista enlazada de documentos.

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `raiz` | `NodoArbol` | Raíz del árbol del documento |
| `siguiente` | `NodoColeccion \| None` | Puntero al siguiente documento |

---

### 4. `ListaDocumentos`
Lista enlazada que contiene todos los documentos de la colección.

```
doc_1 → doc_2 → doc_3 → None
```

Cada nodo apunta a la raíz del árbol de un documento.

---

### 5. `DocumentCollection`
Clase principal. Agrupa todo y expone los métodos públicos.

| Método | Descripción |
|--------|-------------|
| `load(data)` | Recibe una lista de dicts y carga la colección |
| `load_from_file(path)` | Lee un archivo `.json` y llama a `load()` |
| `find(filtro)` | Busca documentos que cumplan el filtro |
| `to_json()` | Reconstruye toda la colección como lista de dicts |

---

### Diagrama simplificado

```
DocumentCollection
  └── documentos: ListaDocumentos
        ├── NodoColeccion → NodoColeccion → NodoColeccion → None
        │     raiz               raiz               raiz
        │      │                  │                  │
        │   NodoArbol          NodoArbol          NodoArbol   ← raíz de cada documento
        │   (documento)        (documento)        (documento)
        │      │
        │   hijos: ListaHijos
        │      ├── NodoArbol(clave="id",     valor=1)      ← hoja
        │      ├── NodoArbol(clave="nombre", valor="Ana")  ← hoja
        │      └── NodoArbol(clave="direccion", valor=None) ← objeto
        │               └── hijos: ListaHijos
        │                     ├── NodoArbol(clave="barrio", valor="Laureles")
        │                     └── NodoArbol(clave="codigo_postal", valor=50031)
```

---

## Análisis de complejidad

Sea:
- **n** = número de documentos en la colección
- **m** = número de campos por documento (en promedio)
- **d** = profundidad de una ruta (ej: `"direccion.barrio"` → d = 2)
- **k** = número de condiciones en el filtro

---

### Carga de documentos — `load(data)`

Por cada documento se recorre el dict para construir el árbol.

- Construir un árbol: **O(m)** donde m = total de nodos del árbol
- Para n documentos: **O(n × m)**

---

### Búsqueda por ruta — `_obtener_valor_en_ruta(raiz, ruta)`

Se recorre el árbol nivel por nivel, buscando cada parte de la ruta entre los hijos.

- Por cada nivel se recorren los hijos: en el peor caso **O(m)** hijos
- Para una ruta de profundidad d: **O(d × m)**
- En la práctica, con documentos pequeños es casi **O(d)**

---

### Consulta sobre toda la colección — `find(filtro)`

Se recorre toda la lista enlazada y por cada documento se evalúa el filtro.

- Por cada documento: evaluar k condiciones, cada una con búsqueda por ruta O(d × m)
- Total: **O(n × k × d × m)**
- Caso simple con k=1 y d=1: **O(n × m)**

---

### Conversión de árbol a JSON — `to_json()` / `_arbol_a_json()`

Se visita **cada nodo** del árbol exactamente una vez.

- Por documento: **O(total de nodos del árbol)**
- Para toda la colección: **O(n × m)**
