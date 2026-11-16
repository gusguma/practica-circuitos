import heapq

def crear_nodo(posicion, g=float('inf'), h=0.0, padre=None):
    """
    Crea un nodo para el algoritmo A*.

    posicion: coordenadas (fila, columna).
    g: coste acumulado desde el origen.
    h: estimacion del coste hasta el destino.
    padre: nodo anterior en el camino.
    """
    nodo = {
        "posicion": posicion,
        "padre": padre,
        "g": g,
        "h": h,
        "f": g + h
    }
    return nodo


def calcular_heuristica(posicion_actual, posicion_destino):
    """
    Calcula la distancia Manhattan entre dos posiciones.
    """
    distancia_filas = abs(posicion_actual[0] - posicion_destino[0])
    distancia_columnas = abs(posicion_actual[1] - posicion_destino[1])
    return distancia_filas + distancia_columnas


def reconstruir_camino(nodo_meta):
    """
    Reconstruye el camino desde el nodo inicial
    hasta el nodo meta.
    Recibe:
        nodo_meta: ultimo nodo encontrado por A*.
    Devuelve:
        Lista de posiciones (fila, columna).
    """
    camino = []
    nodo = nodo_meta

    while nodo is not None:
        camino.append(nodo["posicion"])
        nodo = nodo["padre"]
    camino.reverse()
    return camino


def es_valida(mapa, posicion, origen, destino):
    """
    Comprueba si una posicion es valida para una conexion.
    Permite pasar por casillas libres y por los
    pines de origen y destino de la conexion actual.
    """
    fila, columna = posicion
    alto = len(mapa)
    ancho = len(mapa[0])

    # Comprobar los limites del tablero.
    if fila < 0 or fila >= alto:
        return False
    if columna < 0 or columna >= ancho:
        return False
    # Los pines de origen y destino estan permitidos.
    if posicion == origen or posicion == destino:
        return True
    # El resto del recorrido solo puede utilizar
    # casillas libres.
    return mapa[fila][columna] == "0"


def sucesores(mapa, posicion, origen, destino):
    """
    Obtiene las posiciones a las que podemos movernos
    desde una casilla del tablero.

    Solo permite movimientos horizontales y verticales,
    siempre que la posicion sea valida.
    """
    fila, columna = posicion
    posibles_movimientos = [
        [1, 0],   # Abajo
        [-1, 0],  # Arriba
        [0, 1],   # Derecha
        [0, -1]   # Izquierda
    ]
    resultado = []
    for movimiento in posibles_movimientos:
        nueva_fila = fila + movimiento[0]
        nueva_columna = columna + movimiento[1]
        nueva_posicion = (nueva_fila, nueva_columna)
        if es_valida(mapa, nueva_posicion, origen, destino):
            resultado.append(nueva_posicion)
    return resultado


def find_path(mapa, origen, destino):
    """
    Busca el camino mas corto entre dos posiciones
    utilizando el algoritmo A*.
    Devuelve una lista de posiciones si encuentra
    un camino, o una lista vacia si no existe.
    """
    if origen is None or destino is None:
        return []
    # Crear el nodo inicial.
    h = calcular_heuristica(origen, destino)
    nodo_inicial = crear_nodo(origen, g=0, h=h)
    # Nodos pendientes de explorar.
    abiertos = []
    contador = 0

    heapq.heappush(abiertos,(nodo_inicial["f"], contador, nodo_inicial))
    # Mejor coste conocido para cada posicion.
    mejores_costes = {origen: 0}
    # Posiciones que ya hemos explorado.
    cerrados = set()
    while abiertos:
        # Recuperar el nodo con menor f.
        _, _, nodo_actual = heapq.heappop(abiertos)
        posicion_actual = nodo_actual["posicion"]
        # Ignorar nodos con costes antiguos.
        if nodo_actual["g"] > mejores_costes[posicion_actual]:
            continue
        if posicion_actual in cerrados:
            continue
        # Comprobar si hemos llegado al destino.
        if posicion_actual == destino:
            return reconstruir_camino(nodo_actual)
        # Marcar la posicion como explorada.
        cerrados.add(posicion_actual)
        # Obtener los posibles movimientos.
        for nueva_posicion in sucesores(mapa, posicion_actual, origen, destino):
            if nueva_posicion in cerrados:
                continue
            # Cada movimiento tiene coste 1.
            nuevo_g = nodo_actual["g"] + 1
            # Comprobar si hemos encontrado
            # un camino mejor hasta esta posicion.
            if nueva_posicion not in mejores_costes or nuevo_g < mejores_costes[nueva_posicion]:
                mejores_costes[nueva_posicion] = nuevo_g
                nuevo_h = calcular_heuristica(nueva_posicion, destino)
                nuevo_nodo = crear_nodo(nueva_posicion,g=nuevo_g,h=nuevo_h,padre=nodo_actual)
                contador += 1
                heapq.heappush(abiertos,(nuevo_nodo["f"], contador, nuevo_nodo))
    # No existe un camino valido.
    return []
