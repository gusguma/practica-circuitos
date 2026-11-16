# Practica 1 - Prueba de la zona de disipacion termica.
# Este archivo se utiliza para realizar pruebas locales.
from tablero import cargar_tablero
from conexiones import conectar_pines

# --------------------------------------------------
# CARGAR EL TABLERO
# --------------------------------------------------

mapa, conexiones = cargar_tablero('datos/DefinicionConexionesCircuito.txt')

# --------------------------------------------------
# DEFINIR LA ZONA TÉRMICA
# --------------------------------------------------

FILA_INICIAL = 13
COLUMNA_INICIAL = 13

ALTO = 3
ANCHO = 4

casillas_termicas = []

for fila in range(FILA_INICIAL, FILA_INICIAL + ALTO):
    for columna in range(COLUMNA_INICIAL, COLUMNA_INICIAL + ANCHO):
        casillas_termicas.append((fila, columna))

# --------------------------------------------------
# COMPROBAR LAS CASILLAS RESERVADAS
# --------------------------------------------------

zona_bloqueada = True

for fila, columna in casillas_termicas:
    if mapa[fila][columna] != 'X':
        zona_bloqueada = False
        print('Casilla no bloqueada:', fila, columna)

# --------------------------------------------------
# CALCULAR LAS CONEXIONES
# --------------------------------------------------

mapa_trazado, rutas, pendientes = conectar_pines(mapa, conexiones)

# --------------------------------------------------
# COMPROBAR QUE NO SE ATRAVIESA LA ZONA
# --------------------------------------------------

sin_rutas_en_zona = True
longitud_total = 0

for origen, destino, camino in rutas:
    longitud_total += len(camino) - 1
    for posicion in camino:
        if posicion in casillas_termicas:
            sin_rutas_en_zona = False
            print('Ruta dentro de la zona termica:',origen, '-', destino, posicion)

# --------------------------------------------------
# MOSTRAR RESULTADOS
# --------------------------------------------------

print('PRUEBA DE LA ZONA TERMICA')
print('Dimensiones de la zona:', ALTO, 'x', ANCHO)
print('Casillas reservadas:', len(casillas_termicas))
print('Todas las casillas bloqueadas:', zona_bloqueada)
print('Conexiones definidas:', len(conexiones))
print('Conexiones realizadas:', len(rutas))
print('Conexiones pendientes:', pendientes)
print('Ninguna ruta atraviesa la zona:', sin_rutas_en_zona)
print('Longitud total:', longitud_total)

# --------------------------------------------------
# RESULTADO FINAL
# --------------------------------------------------

zona_valida = (
    zona_bloqueada
    and len(casillas_termicas) == 12
    and sin_rutas_en_zona
    and len(rutas) == len(conexiones)
    and len(pendientes) == 0
)
print('ZONA TERMICA VALIDA:', zona_valida)
