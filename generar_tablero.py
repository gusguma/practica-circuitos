
# Practica 1 - Conexion de circuitos.
# Construccion del soporte y definicion de las conexiones.
# Cada casilla de la matriz se representa con dos caracteres.

TAMANO_PLACA = 30
TAMANO_CIRCUITO = 6

# Crear el soporte vacio de 30 x 30 casillas.
mapa = []

for fila in range(TAMANO_PLACA):
    mapa.append(['00'] * TAMANO_PLACA)


def colocar_circuito(letra, fila_inicial, columna_inicial):
    """
    Coloca un circuito integrado de 6 x 6 casillas.

    Cada circuito tiene 16 pines, distribuidos en
    cuatro pines por lado y dejando libres las esquinas.
    """

    # El interior y las esquinas del circuito se bloquean.
    for fila in range(fila_inicial, fila_inicial + TAMANO_CIRCUITO):
        for columna in range(columna_inicial, columna_inicial + TAMANO_CIRCUITO):
            mapa[fila][columna] = 'XX'

    # Identificadores de los 16 pines.
    etiquetas = '123456789abcdefg'
    indice = 0

    # Lado superior: pines 1 a 4.
    for desplazamiento in range(1, 5):
        mapa[fila_inicial][columna_inicial + desplazamiento] = letra + etiquetas[indice]
        indice += 1

    # Lado derecho: pines 5 a 8.
    for desplazamiento in range(1, 5):
        mapa[fila_inicial + desplazamiento][columna_inicial + 5] = letra + etiquetas[indice]
        indice += 1

    # Lado inferior: pines 9, a, b, c.
    for desplazamiento in range(1, 5):
        mapa[fila_inicial + 5][columna_inicial + desplazamiento] = letra + etiquetas[indice]
        indice += 1

    # Lado izquierdo: pines d, e, f, g.
    for desplazamiento in range(1, 5):
        mapa[fila_inicial + desplazamiento][columna_inicial] = letra + etiquetas[indice]
        indice += 1


# --------------------------------------------------
# COLOCACION DE LOS CIRCUITOS INTEGRADOS
# --------------------------------------------------

# Distribucion de los cuatro circuitos en el soporte.
# Se dejan cinco casillas de margen exterior.

colocar_circuito("A", 5, 5)
colocar_circuito("B", 5, 19)
colocar_circuito("C", 19, 5)
colocar_circuito("D", 19, 19)


# --------------------------------------------------
# FUENTE DE ALIMENTACION
# --------------------------------------------------

# Terminales de alimentacion independientes
# de los cuatro circuitos integrados.

mapa[0][14] = 'S1'
mapa[29][14] = 'S2'


# --------------------------------------------------
# DEFINICION DE LAS CONEXIONES
# --------------------------------------------------

# Las parejas de pines se definen antes de calcular
# las rutas. El algoritmo A* determinara los caminos.

conexiones = []

# Conexiones horizontales entre circuitos enfrentados.
for izquierda, derecha in [('A', 'B'), ('C', 'D')]:
    for indice in range(4):
        conexiones.append((
            izquierda + '5678'[indice],
            derecha + 'defg'[indice]
        ))

# Conexiones verticales entre circuitos enfrentados.
for superior, inferior in [('A', 'C'), ('B', 'D')]:
    for indice in range(4):
        conexiones.append((
            superior + '9abc'[indice],
            inferior + '1234'[indice]
        ))

# Conexiones del corredor superior.
conexiones += [
    ('A4', 'B1'),
    ('A3', 'B2'),
    ('A2', 'B3'),
    ('A1', 'B4')
]

# Conexiones del corredor inferior.
conexiones += [
    ('Cc', 'D9'),
    ('Cb', 'Da'),
    ('Ca', 'Db'),
    ('C9', 'Dc')
]

# Conexiones del corredor izquierdo.
conexiones += [
    ('Ag', 'Cd'),
    ('Af', 'Ce'),
    ('Ae', 'Cf')
]

# Conexiones del corredor derecho.
conexiones += [
    ('B8', 'D5'),
    ('B7', 'D6'),
    ('B6', 'D7'),
    ('B5', 'D8')
]

# Conexiones con los terminales de alimentacion.
conexiones += [
    ('S1', 'Ad'),
    ('S2', 'Cg')
]


# --------------------------------------------------
# GENERACION DEL FICHERO DE DEFINICION
# --------------------------------------------------

# El fichero contiene dos secciones:
# 1. Representacion de la placa y sus componentes.
# 2. Parejas de pines que deben conectarse.

with open(
    'datos/DefinicionConexionesCircuito.txt',
    'w',
    encoding='utf-8'
) as fichero:

    # Escribir las filas del tablero.
    for fila in mapa:
        fichero.write(''.join(fila) + '\n')

    # Escribir la seccion de conexiones.
    fichero.write('CONEXIONES:\n')

    for origen, destino in conexiones:
        fichero.write(origen + '-' + destino + '\n')


# --------------------------------------------------
# MOSTRAR RESUMEN DE LA GENERACION
# --------------------------------------------------

print('Soporte:', len(mapa), 'x', len(mapa[0]))
print('Circuitos: A, B, C, D')
print('Dimensiones de cada circuito:', TAMANO_CIRCUITO, 'x', TAMANO_CIRCUITO)
print('Pines por circuito: 16')
print('Total de pines de circuitos:', 4 * 16)
print('Terminales de alimentacion: S1 y S2')
print('Conexiones definidas:', len(conexiones))
print('Fichero generado: datos/DefinicionConexionesCircuito.txt')
