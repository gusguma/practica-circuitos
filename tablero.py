
def get_codigo_tablero(caracteres):
    """
    Convierte el código de una casilla del fichero a su representación interna.
    """
    if caracteres == "00":
        return "0"
    elif caracteres == "XX":
        return "X"
    else:
        return caracteres


def cargar_tablero(nombre_fichero):
    """
    Lee el fichero de definición del circuito.
    Devuelve:
        mapa: lista de listas con las casillas del tablero.
        conexiones: lista de tuplas con los pines a conectar.
    """
    mapa = []
    conexiones = []
    leyendo_tablero = True

    with open(nombre_fichero, "r", encoding="utf-8") as fichero:
        for linea in fichero:
            linea = linea.strip()
            if linea == "":
                continue
            if linea.upper() == "CONEXIONES:":
                leyendo_tablero = False
                continue
            if leyendo_tablero:
                fila = []
                for i in range(0, len(linea), 2):
                    caracteres = linea[i:i + 2]
                    codigo = get_codigo_tablero(caracteres)
                    fila.append(codigo)
                mapa.append(fila)
            else:
                origen, destino = linea.split("-")
                conexiones.append((origen, destino))
    return mapa, conexiones


def buscar_pin(mapa, pin):
    """
    Busca un pin dentro del tablero.
    Devuelve:
        Una tupla (fila, columna) si encuentra el pin.
        None si el pin no existe.
    """
    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            if mapa[fila][columna] == pin:
                return fila, columna
    return None


def mostrar_matriz(mapa):
    """
    Muestra el contenido del tablero en consola.
    """
    for fila in mapa:
        for casilla in fila:
            print(str(casilla).rjust(2), end=" ")
        print()
