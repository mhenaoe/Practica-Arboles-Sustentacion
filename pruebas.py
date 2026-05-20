"""
pruebas.py
Evidencia de ejecución con 8 consultas diferentes.

Ejecutar con:  python pruebas.py
"""

import json
from motor import DocumentCollection

# ---------------------------------------------------------------------------
# Utilidad de impresión bonita
# ---------------------------------------------------------------------------

def mostrar(titulo: str, resultado: list) -> None:
    print(f"\n{'='*55}")
    print(f"  {titulo}")
    print('='*55)
    if resultado:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    # Si está vacío, find() ya imprimió el mensaje correspondiente


# ---------------------------------------------------------------------------
# Cargar la colección desde el archivo JSON
# ---------------------------------------------------------------------------

collection = DocumentCollection()
collection.load_from_file("coleccion.json")

print("\n*** MOTOR DOCUMENTAL BASADO EN ÁRBOLES Y LISTAS ENLAZADAS ***")

# ---------------------------------------------------------------------------
# CONSULTA 1: Filtro de igualdad simple
# Buscar todos los documentos cuya ciudad sea "Medellín"
# ---------------------------------------------------------------------------
resultado_1 = collection.find({"ciudad": "Medellín"})
mostrar("CONSULTA 1 — ciudad == 'Medellín'", resultado_1)

# ---------------------------------------------------------------------------
# CONSULTA 2: Operador $gt (mayor que)
# Buscar personas con edad mayor a 25
# ---------------------------------------------------------------------------
resultado_2 = collection.find({"edad": {"$gt": 25}})
mostrar("CONSULTA 2 — edad > 25", resultado_2)

# ---------------------------------------------------------------------------
# CONSULTA 3: Ruta anidada
# Buscar documentos cuyo barrio sea "Laureles"
# ---------------------------------------------------------------------------
resultado_3 = collection.find({"direccion.barrio": "Laureles"})
mostrar("CONSULTA 3 — direccion.barrio == 'Laureles'", resultado_3)

# ---------------------------------------------------------------------------
# CONSULTA 4: Operador $ne (diferente de)
# Buscar personas que NO sean de Bogotá
# ---------------------------------------------------------------------------
resultado_4 = collection.find({"ciudad": {"$ne": "Bogotá"}})
mostrar("CONSULTA 4 — ciudad != 'Bogotá'", resultado_4)

# ---------------------------------------------------------------------------
# CONSULTA 5: Rango con $gte y $lte
# Buscar personas con edad entre 20 y 30 (inclusive)
# ---------------------------------------------------------------------------
resultado_5 = collection.find({"edad": {"$gte": 20, "$lte": 30}})
mostrar("CONSULTA 5 — 20 <= edad <= 30", resultado_5)

# ---------------------------------------------------------------------------
# CONSULTA 6: Múltiples condiciones combinadas
# Buscar personas de Bogotá con edad mayor o igual a 30
# ---------------------------------------------------------------------------
resultado_6 = collection.find({"ciudad": "Bogotá", "edad": {"$gte": 30}})
mostrar("CONSULTA 6 — ciudad == 'Bogotá' AND edad >= 30", resultado_6)

# ---------------------------------------------------------------------------
# CONSULTA 7: Ruta anidada con operador
# Buscar documentos cuyo código postal sea mayor a 100000
# ---------------------------------------------------------------------------
resultado_7 = collection.find({"direccion.codigo_postal": {"$gt": 100000}})
mostrar("CONSULTA 7 — direccion.codigo_postal > 100000", resultado_7)

# ---------------------------------------------------------------------------
# CONSULTA 8: Ruta que no existe (caso borde)
# ---------------------------------------------------------------------------
resultado_8 = collection.find({"telefono": "123"})
mostrar("CONSULTA 8 — campo 'telefono' no existe (caso borde)", resultado_8)

# ---------------------------------------------------------------------------
# to_json(): Reconstruir toda la colección desde los árboles
# ---------------------------------------------------------------------------
print(f"\n{'='*55}")
print("  to_json() — Colección completa reconstruida desde árboles")
print('='*55)
toda_la_coleccion = collection.to_json()
print(json.dumps(toda_la_coleccion, ensure_ascii=False, indent=2))

# ---------------------------------------------------------------------------
# CASO BORDE: Colección vacía
# ---------------------------------------------------------------------------
print(f"\n{'='*55}")
print("  CASO BORDE — Consulta sobre colección vacía")
print('='*55)
coleccion_vacia = DocumentCollection()
coleccion_vacia.find({"ciudad": "Medellín"})
