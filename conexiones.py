from tablero import buscar_pin
from astar import find_path

def conectar_pines(mapa, conexiones):
    """
    Calcula las rutas entre los pines mediante A Star. Cada conexión se identifica mediante un número
    de dos caracteres en el tablero resultante.
    Devuelve:
        mapa_trazado: tablero con las rutas.
        rutas: conexiones realizadas.
        pendientes: conexiones sin ruta.
    """
    # Copiar el tablero sin modificar el original.
    mapa_trazado = []
    for fila in mapa:
        mapa_trazado.append(fila[:])
    rutas = []
    pendientes = []
    numero_conexion = 1
    # Recorrer las conexiones definidas.
    for pin_origen, pin_destino in conexiones:
        origen = buscar_pin(mapa_trazado, pin_origen)
        destino = buscar_pin(mapa_trazado, pin_destino)
        # Buscar la ruta utilizando A*.
        camino = find_path(mapa_trazado, origen, destino)
        if camino:
            rutas.append((pin_origen, pin_destino, camino))
            # Identificador de dos caracteres.
            identificador = str(numero_conexion).rjust(2, "0")
            # Marcar las posiciones del camino.
            # No modificamos los pines de los extremos.
            for fila, columna in camino[1:-1]:
                mapa_trazado[fila][columna] = identificador
        else:
            pendientes.append((pin_origen, pin_destino))
        numero_conexion += 1
    return mapa_trazado, rutas, pendientes
