from tablero import buscar_pin
from astar import find_path

def conectar_pines(mapa, conexiones):
    """
    Calcula las rutas para las conexiones definidas.

    Las casillas utilizadas se bloquean para impedir
    que las siguientes conexiones las atraviesen.

    Devuelve el mapa actualizado, las rutas encontradas
    y las conexiones pendientes.
    """
    # Copiar el tablero sin modificar el original.
    mapa_trazado = []

    for fila in mapa:
        mapa_trazado.append(fila[:])

    rutas = []
    pendientes = []

    # Recorrer las conexiones del fichero.
    for pin_origen, pin_destino in conexiones:
        origen = buscar_pin(mapa_trazado, pin_origen)
        destino = buscar_pin(mapa_trazado, pin_destino)
        camino = find_path(mapa_trazado, origen, destino)
        if camino:
            rutas.append((pin_origen, pin_destino, camino))
            # Reservar las casillas interiores del camino.
            for fila, columna in camino[1:-1]:
                mapa_trazado[fila][columna] = "X"
        else:
            pendientes.append((pin_origen, pin_destino))
    return mapa_trazado, rutas, pendientes
