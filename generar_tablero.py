# Construccion de la placa de la Practica 1.
# Cada elemento de la matriz se representa con dos caracteres.

TAMANO_PLACA = 30
TAMANO_CIRCUITO = 6

mapa = []
for fila in range(TAMANO_PLACA):
    mapa.append(['00'] * TAMANO_PLACA)


def colocar_circuito(letra, fila_inicial, columna_inicial):
    # Tanto el interior del circuito como sus esquinas no permiten conexiones.
    for fila in range(fila_inicial, fila_inicial + TAMANO_CIRCUITO):
        for columna in range(columna_inicial, columna_inicial + TAMANO_CIRCUITO):
            mapa[fila][columna] = 'XX'

    # Cuatro pines en cada lado, sin utilizar las esquinas.
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


colocar_circuito('A', 3, 3)
colocar_circuito('B', 3, 21)
colocar_circuito('C', 21, 3)
colocar_circuito('D', 21, 21)

# Fuente de alimentacion, independiente de los circuitos.
mapa[0][14] = 'S1'
mapa[29][14] = 'S2'

# Conexiones iniciales entre pines enfrentados.
# Se completara el conjunto de conexiones en posteriores commits.
conexiones = []
for izquierda, derecha in [('A', 'B'), ('C', 'D')]:
    for indice in range(4):
        conexiones.append((izquierda + '5678'[indice], derecha + 'defg'[indice]))

for superior, inferior in [('A', 'C'), ('B', 'D')]:
    for indice in range(4):
        conexiones.append((superior + '9abc'[indice], inferior + '1234'[indice]))

with open('datos/DefinicionConexionesCircuito.txt', 'w', encoding='utf-8') as fichero:
    for fila in mapa:
        fichero.write(''.join(fila) + '\n')
    fichero.write('CONEXIONES:\n')
    for origen, destino in conexiones:
        fichero.write(origen + '-' + destino + '\n')

print('Placa:', len(mapa), 'x', len(mapa[0]))
print('Circuitos: A, B, C, D (6 x 6; 16 pines por circuito)')
print('Conexiones iniciales:', len(conexiones))