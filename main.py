
from tablero import cargar_tablero
from conexiones import conectar_pines

mapa, conexiones = cargar_tablero(
    "datos/DefinicionConexionesCircuito.txt"
)

mapa_trazado, rutas, pendientes = conectar_pines(
    mapa, conexiones
)

longitud_total = 0

print("RESULTADO DE LAS CONEXIONES")

for origen, destino, camino in rutas:
    longitud = len(camino) - 1
    longitud_total += longitud

    print(origen, "-", destino, ":", longitud, "movimientos")

print("\nConexiones realizadas:", len(rutas))
print("Conexiones pendientes:", len(pendientes))
print("Longitud total:", longitud_total)

if pendientes:
    print("Pendientes:", pendientes)