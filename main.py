from tablero import get_codigo_tablero, cargar_tablero, buscar_pin, mostrar_matriz

print(get_codigo_tablero("00"))
print(get_codigo_tablero("XX"))
print(get_codigo_tablero("A1"))
print(get_codigo_tablero("S1"))

mapa, conexiones = cargar_tablero(
    "datos/DefinicionConexionesCircuito.txt"
)

print("Filas del tablero:", len(mapa))
print("Columnas del tablero:", len(mapa[0]))
print("Numero de conexiones:", len(conexiones))

print("\nPrimera fila:")
print(mapa[0])

print("\nConexiones:")
for conexion in conexiones:
    print(conexion)

print("A1:", buscar_pin(mapa, "A1"))
print("B1:", buscar_pin(mapa, "B1"))
print("C1:", buscar_pin(mapa, "C1"))
print("D1:", buscar_pin(mapa, "D1"))
print("S1:", buscar_pin(mapa, "S1"))
print("Z9:", buscar_pin(mapa, "Z9"))

print("\nTABLERO COMPLETO:")
mostrar_matriz(mapa)
