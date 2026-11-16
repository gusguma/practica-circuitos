# Práctica 1 — Algoritmo A* para interconexión de circuitos

## 1. Objetivo

El algoritmo A* permite encontrar un camino entre dos pines de la placa cuadriculada sin atravesar circuitos, otros pines o casillas prohibidas. Se utiliza como base para la posterior interconexión de múltiples pares de pines. Esta fase resuelve **una única conexión por búsqueda**, no el problema global de rutas sin cruces.

La implementación parte del planteamiento de los cuadernos **Clase 5: `AStar-2Oct2026.ipynb`** y **Clase 7: `InterconexionCircuitos-Clase7-VEstudiantes.ipynb`**. En la Clase 5 se explica A* con clases `Nodo` y `Abiertos` y una función heurística Manhattan sobre una cuadrícula; para esta práctica se ha seguido la plantilla de la Clase 7, que propone `crearNodo`, `calcularHeuristica`, `reconstruirCamino` y `find_path`. Se han adaptado los nombres al estilo `snake_case` utilizado en el proyecto y la matriz se representa como **lista de listas**, como en la construcción del tablero.

## 2. Modelo del problema

- **Estado:** posición `(fila, columna)` de una casilla.
- **Estado inicial:** coordenadas del pin de origen obtenidas con `buscar_pin(mapa, identificador)`.
- **Meta:** coordenadas del pin de destino.
- **Operadores:** desplazarse una casilla arriba, abajo, izquierda o derecha.
- **Coste de cada movimiento:** 1.
- **Casillas transitables:** `"0"` y los dos extremos de la conexión actual. Las posiciones `"X"` y todos los demás pines no son transitables.
- **Salida:** una lista de coordenadas desde origen hasta destino; `[]` si no se encuentra ruta o falta alguno de los extremos.

La longitud de una ruta, expresada en movimientos, se obtiene mediante `len(camino) - 1` **solo si el camino no está vacío**. Una ruta de 14 casillas contiene 13 desplazamientos.

## 3. Función heurística

La distancia Manhattan calcula una cota inferior de los movimientos pendientes:

`h(n) = abs(fila_actual - fila_destino) + abs(columna_actual - columna_destino)`

La evaluación del nodo se obtiene como `f(n) = g(n) + h(n)`, donde `g(n)` es el coste acumulado. Esta heurística no sobreestima el coste real cuando los movimientos permitidos son ortogonales y cada uno cuesta 1. Por ello A* puede obtener una ruta mínima para **cada búsqueda individual**, aunque la presencia de obstáculos obligue a rodeos.

Ejemplos verificados en PyCharm:

| Conexión | Origen | Destino | Manhattan | Ruta A* |
| --- | --- | --- | ---: | ---: |
| A1 → B1 | `(3, 4)` | `(3, 22)` | 18 | 20 movimientos |
| A5 → Bd | `(4, 8)` | `(4, 21)` | 13 | 13 movimientos |

La primera ruta sube a la fila 2 para evitar los pines que impiden avanzar directamente por la fila 3 y después vuelve a bajar al destino. La segunda atraviesa directamente las casillas libres de la fila 4.

## 4. Funciones implementadas

### `crear_nodo(posicion, g=float('inf'), h=0.0, padre=None)`

Devuelve un diccionario con las claves `posicion`, `padre`, `g`, `h` y `f`. Para el nodo inicial se proporciona expresamente `g=0`. El valor infinito por defecto indica que todavía no se conoce un coste de llegada.

### `calcular_heuristica(posicion_actual, posicion_destino)`

Calcula la distancia Manhattan, explicada en la Clase 5 y aplicable a la función auxiliar propuesta en la Clase 7.

### `reconstruir_camino(nodo_meta)`

Sigue los enlaces `padre` hasta el nodo inicial, guarda las posiciones y utiliza `reverse()` para devolverlas desde el origen al destino.

### `es_valida(mapa, posicion, origen, destino)`

Comprueba que la posición está dentro de los límites; permite el origen y el destino y, para los demás puntos, exige que la casilla contenga `"0"`. No permite atravesar pines ajenos ni zonas `"X"`.

### `sucesores(mapa, posicion, origen, destino)`

Calcula las posiciones alcanzables mediante los desplazamientos `(1,0)`, `(-1,0)`, `(0,1)` y `(0,-1)`, descartando los movimientos no válidos.

### `find_path(mapa, origen, destino)`

Realiza la búsqueda con `heapq` como cola de prioridad de abiertos; usa un conjunto `cerrados` y un diccionario `mejores_costes`. Descarta entradas antiguas y reconstruye el camino al encontrar la meta. El contador auxiliar de la cola desempata prioridades sin comparar diccionarios. Si no existe camino devuelve `[]`.

## 5. Secuencia general de A*

1. Comprobar si el origen o el destino son `None`; en ese caso devolver `[]`.
2. Crear el nodo inicial con `g=0` y `h` igual a la distancia Manhattan a la meta.
3. Introducir el nodo en la cola de abiertos y registrar el coste conocido de su posición.
4. Extraer de abiertos el nodo con menor `f` y descartar entradas obsoletas o ya cerradas.
5. Si su posición coincide con el destino, reconstruir y devolver la ruta.
6. En otro caso, añadir la posición a cerrados, obtener sus sucesores y calcular `nuevo_g = g_actual + 1`.
7. Incorporar un sucesor a abiertos únicamente si no tenía coste previo o se ha encontrado un coste menor.
8. Repetir mientras haya abiertos; si se agotan, devolver `[]`.

## 6. Pruebas observadas

Las siguientes salidas han sido aportadas por el estudiante tras ejecutar `main.py` en PyCharm:

| Comprobación | Resultado comunicado |
| --- | --- |
| Nodo inicial `(3,4)`, `g=0`, `h=18` | `f=18` |
| Reconstrucción de tres nodos enlazados | `[(3,4), (3,5), (3,6)]` |
| Sucesores de A1 | `[(2,4)]` |
| Sucesores de `(0,0)` | `[(1,0), (0,1)]` |
| Camino A1–B1 | 20 movimientos |
| Camino A5–Bd | 13 movimientos |
| Casillas interiores del último camino evaluado | Todas `"0"` |
| Adyacencia del último camino evaluado | `True` |
| Pin `Z9` inexistente | `[]` |
| Tablero artificial bloqueado | `[]` |

La salida contiene dos impresiones de `Camino sin obstaculos: True`; se trata de una verificación duplicada. **Las validaciones automáticas con la variable `camino` se aplicaron a la última ruta asignada (`A5–Bd`)**, por lo que no deben contarse como una validación automática independiente de `A1–B1`.

El informe de pruebas acumulativo se mantiene en `documentacion/Informe_pruebas_Practica1.docx`; se incorporarán capturas y nuevas pruebas conforme avance el proyecto.

## 7. Limitaciones actuales y trabajo pendiente

- A* calcula la ruta mínima **para una pareja concreta** teniendo en cuenta el mapa actual. No garantiza por sí mismo que se puedan realizar todas las conexiones ni que su suma de longitudes sea mínima.
- La lista de 16 conexiones es provisional y no incluye todavía todos los pines ni los terminales de alimentación como extremos de rutas.
- La búsqueda actual no reserva las casillas utilizadas para otras rutas; esa funcionalidad corresponde al trazado múltiple.
- Para robustez adicional queda por validar de forma explícita que las coordenadas recibidas estén dentro de la matriz y sean realmente las de los pines designados. Las pruebas actuales se han realizado con coordenadas válidas obtenidas mediante `buscar_pin`.
- La zona opcional reservada para disipación térmica se estudiará cuando exista un trazado múltiple, incorporándola al mapa antes de la validación final.

Las comprobaciones específicas de pines de origen y destino y el uso de listas de listas son adaptaciones al formato de nuestro proyecto. Este documento describe el estado técnico del algoritmo y seguirá actualizándose cuando evolucione la implementación.
