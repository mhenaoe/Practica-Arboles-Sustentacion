# Diagrama de Clases

## Diagrama UML

```mermaid
classDiagram

    class DoublyNode {
        +Any value
        +DoublyNode next
        +DoublyNode prev
        +__repr__() str
    }

    class DoublyLinkedList {
        +DoublyNode head
        +int size
        +append(value) None
        +remove(value) bool
        +pop(index) Any
        +extend(otra_lista) None
        +find(condition) Any
        +is_empty() bool
        +__iter__()
        +__len__() int
        +__repr__() str
    }

    class Node {
        +str key
        +Any value
        +DoublyLinkedList children
        +is_leaf() bool
        +__repr__() str
    }

    class GeneralTree {
        +Node root
        +add_child(parent, child) None
        +__repr__() str
    }

    class NodoColeccion {
        +GeneralTree arbol
        +NodoColeccion siguiente
    }

    class ListaDocumentos {
        +NodoColeccion cabeza
        +agregar(arbol) None
        +esta_vacia() bool
        +__iter__()
    }

    class DocumentCollection {
        +ListaDocumentos documentos
        +load(data) None
        +load_from_file(ruta_archivo) None
        +find(filtro) list
        +to_json() list
    }

    DoublyLinkedList *-- DoublyNode : contiene nodos
    Node *-- DoublyLinkedList : children
    GeneralTree *-- Node : root
    NodoColeccion *-- GeneralTree : arbol
    NodoColeccion --> NodoColeccion : siguiente
    ListaDocumentos *-- NodoColeccion : cabeza
    DocumentCollection *-- ListaDocumentos : documentos
```

---

## Descripción de las relaciones

| Relación | Tipo | Descripción |
|----------|------|-------------|
| `DoublyLinkedList` → `DoublyNode` | Composición `*--` | La lista contiene y gestiona sus propios nodos |
| `Node` → `DoublyLinkedList` | Composición `*--` | Cada nodo del árbol tiene su propia lista de hijos |
| `GeneralTree` → `Node` | Composición `*--` | El árbol contiene y es dueño de su raíz |
| `NodoColeccion` → `GeneralTree` | Composición `*--` | Cada eslabón de la colección contiene un árbol |
| `NodoColeccion` → `NodoColeccion` | Asociación `-->` | Auto-referencia: el puntero `siguiente` al próximo eslabón |
| `ListaDocumentos` → `NodoColeccion` | Composición `*--` | La lista gestiona sus eslabones de documentos |
| `DocumentCollection` → `ListaDocumentos` | Composición `*--` | La colección contiene y gestiona la lista de documentos |

---

## Flujo entre clases (de abajo hacia arriba)

```
DoublyNode          ← eslabón base, usado por DoublyLinkedList
    ↑
DoublyLinkedList    ← lista doble, usada como children en Node
    ↑
Node                ← nodo del árbol, tiene key, value y children
    ↑
GeneralTree         ← árbol completo, tiene un Node raíz
    ↑
NodoColeccion       ← eslabón de la colección, contiene un GeneralTree
    ↑
ListaDocumentos     ← cadena de NodoColeccion  →  →  → None
    ↑
DocumentCollection  ← clase principal que usa todo lo anterior
```

---

## Dónde vive cada clase

| Clase | Archivo |
|-------|---------|
| `DoublyNode` | `motor/estructuras.py` |
| `DoublyLinkedList` | `motor/estructuras.py` |
| `Node` | `motor/estructuras.py` |
| `GeneralTree` | `motor/estructuras.py` |
| `NodoColeccion` | `motor/lista_documentos.py` |
| `ListaDocumentos` | `motor/lista_documentos.py` |
| `DocumentCollection` | `motor/coleccion.py` |
