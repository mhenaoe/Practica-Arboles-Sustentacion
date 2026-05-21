import json
from coleccion import DocumentCollection


def mostrar(titulo: str, resultado: list) -> None:

    print(f"\n{'='*60}")
    print(titulo)
    print('='*60)

    if resultado:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------
# CARGA
# ---------------------------------------------------------------

collection = DocumentCollection()

collection.load_from_file("coleccion.json")

print("\n*** MOTOR DOCUMENTAL BASADO EN ARBOLES ***")


# ---------------------------------------------------------------
# CONSULTA 1
# ---------------------------------------------------------------

resultado_1 = collection.find({
    "ciudad": "Medellín"
})

mostrar("CONSULTA 1 - ciudad == Medellín", resultado_1)


# ---------------------------------------------------------------
# CONSULTA 2
# ---------------------------------------------------------------

resultado_2 = collection.find({
    "edad": {"$gt": 25}
})

mostrar("CONSULTA 2 - edad > 25", resultado_2)


# ---------------------------------------------------------------
# CONSULTA 3
# ---------------------------------------------------------------

resultado_3 = collection.find({
    "direccion.barrio": "Laureles"
})

mostrar("CONSULTA 3 - direccion.barrio == Laureles", resultado_3)


# ---------------------------------------------------------------
# CONSULTA 4
# ---------------------------------------------------------------

resultado_4 = collection.find({
    "ciudad": {"$ne": "Bogotá"}
})

mostrar("CONSULTA 4 - ciudad != Bogotá", resultado_4)


# ---------------------------------------------------------------
# CONSULTA 5
# ---------------------------------------------------------------

resultado_5 = collection.find({
    "edad": {"$gte": 20, "$lte": 30}
})

mostrar("CONSULTA 5 - 20 <= edad <= 30", resultado_5)


# ---------------------------------------------------------------
# CONSULTA 6
# ---------------------------------------------------------------

resultado_6 = collection.find({
    "ciudad": "Bogotá",
    "edad": {"$gte": 30}
})

mostrar("CONSULTA 6 - multiples condiciones", resultado_6)


# ---------------------------------------------------------------
# CONSULTA 7
# ---------------------------------------------------------------

resultado_7 = collection.find({
    "direccion.codigo_postal": {"$gt": 100000}
})

mostrar("CONSULTA 7 - codigo postal > 100000", resultado_7)


# ---------------------------------------------------------------
# CONSULTA 8
# ---------------------------------------------------------------

resultado_8 = collection.find({
    "telefono": "123"
})

mostrar("CONSULTA 8 - ruta inexistente", resultado_8)


# ---------------------------------------------------------------
# TO JSON
# ---------------------------------------------------------------

print(f"\n{'='*60}")
print("TO_JSON()")
print('='*60)

print(
    json.dumps(
        collection.to_json(),
        ensure_ascii=False,
        indent=2
    )
)


# ---------------------------------------------------------------
# COLECCION VACIA
# ---------------------------------------------------------------

print(f"\n{'='*60}")
print("CASO BORDE - COLECCION VACIA")
print('='*60)

coleccion_vacia = DocumentCollection()

coleccion_vacia.find({
    "ciudad": "Medellín"
})