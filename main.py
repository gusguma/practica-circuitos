from tablero import cargar_tablero, mostrar_matriz
from conexiones import conectar_pines

# Cargar la definición del soporte.
mapa, conexiones = cargar_tablero("datos/DefinicionConexionesCircuito.txt")

# Calcular las rutas.
mapa_trazado, rutas, pendientes = conectar_pines(mapa, conexiones)

longitud_total = 0

print("RESULTADO DE LAS CONEXIONES")

for origen, destino, camino in rutas:
    longitud = len(camino) - 1
    longitud_total += longitud
    print(origen, "-", destino, ":", longitud, "movimientos")

print("\nConexiones realizadas:", len(rutas))
print("Conexiones pendientes:", len(pendientes))
print("Longitud total:", longitud_total)

# Mostrar la placa con todas las conexiones.
print("\nTABLERO CON LAS CONEXIONES")
mostrar_matriz(mapa_trazado)

# Mostrar que conexion representa cada numero.
print("\nLEYENDA DE LAS CONEXIONES")

numero = 1

for origen, destino in conexiones:
    identificador = str(numero).rjust(2, "0")
    print(identificador, ":", origen, "-", destino)
    numero += 1
