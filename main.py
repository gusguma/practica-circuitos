
"""
Practica 1 - Conexion de circuitos.
Ejemplo de busqueda de una ruta mediante A*.
"""

from tablero import cargar_tablero, buscar_pin
from astar import find_path

# Cargar el tablero y las conexiones.
mapa, conexiones = cargar_tablero(
    "datos/DefinicionConexionesCircuito.txt"
)

# Seleccionar una conexion del fichero.
pin_origen = "A5"
pin_destino = "Bd"

# Obtener las coordenadas de ambos pines.
origen = buscar_pin(mapa, pin_origen)
destino = buscar_pin(mapa, pin_destino)

# Ejecutar A*.
camino = find_path(mapa, origen, destino)

# Mostrar los resultados.
print("Soporte:", len(mapa), "x", len(mapa[0]))
print("Conexiones definidas:", len(conexiones))
print("Conexion:", pin_origen, "-", pin_destino)

if camino:
    print("Camino encontrado:", camino)
    print("Longitud:", len(camino) - 1)
else:
    print("No existe un camino valido.")
