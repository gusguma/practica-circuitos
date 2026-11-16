# Práctica 1 — Algoritmo A* para interconexión de circuitos

## 1. Objetivo

El algoritmo A* permite encontrar un camino entre dos pines de la placa cuadriculada sin atravesar circuitos, otros pines o casillas prohibidas. Además, el módulo `conexiones.py` aplica A* sucesivamente a las parejas de pines y reserva las casillas interiores de cada ruta. **A* resuelve una conexión individual; la interconexión múltiple se realiza con una estrategia secuencial propia**, cuyo resultado depende del orden de las parejas.

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

## 7. Interconexión múltiple con `conexiones.py`

Para conectar varias parejas de pines se utiliza `conectar_pines(mapa, conexiones)`; esta función **no forma parte de la plantilla de los cuadernos**, sino que organiza llamadas sucesivas al A* explicado en clase.

1. Se crea `mapa_trazado` copiando cada fila del mapa original (`fila[:]`). De este modo el dato de entrada no se altera.
2. Se recorren, en el orden del fichero, las tuplas `(pin_origen, pin_destino)`.
3. Se localizan las coordenadas de los extremos mediante `buscar_pin()`.
4. Se llama a `find_path()` para calcular una ruta válida en el mapa actualizado.
5. Si existe ruta, se guarda y se marcan con `"X"` sus posiciones interiores (`camino[1:-1]`), reservándolas para las siguientes búsquedas. Los pines extremos se conservan.
6. Si no hay ruta, se registra la conexión como pendiente.

La función devuelve `mapa_trazado`, `rutas` y `pendientes`. El valor `"X"` usado para una pista ya trazada comparte la condición de **no transitable** con otros obstáculos, aunque conceptualmente su origen sea diferente.

## 8. Pruebas de las 16 conexiones actuales

Se han ejecutado `main.py` y un script local `pruebas_conexiones.py` en PyCharm. El estudiante ha aportado las salidas siguientes:

| Comprobación | Resultado comunicado |
| --- | --- |
| Conexiones definidas y realizadas | 16 de 16 |
| Conexiones pendientes | 0 |
| Extremos de cada ruta | Correctos (`True`) |
| Movimientos entre casillas adyacentes | Correctos (`True`) |
| Casillas interiores libres en el mapa original | `True` |
| Sin reutilizar casillas interiores entre pistas | `True` |
| Longitud total de las rutas | 208 movimientos |
| Suma de distancias Manhattan | 208 movimientos |
| Prueba de optimalidad para estas parejas | `True` |
| Ejecución | Código de salida 0 |

**Justificación de la longitud mínima para el conjunto actual.** Cada una de las 16 parejas se encuentra separada por una distancia Manhattan de 13 movimientos; por tanto, cualquier trazado de esas mismas parejas necesita al menos `16 × 13 = 208` movimientos. Puesto que hemos encontrado 16 rutas válidas, sin compartir casillas interiores, cuya suma es 208, **la longitud total es mínima para este conjunto fijo de 16 conexiones** con movimientos ortogonales y coste unitario. No es una garantía general para cualquier conjunto de conexiones ni para otros diseños de placa.

La comprobación automática de cruces compara las posiciones interiores de las pistas. En nuestra cuadrícula, con movimientos ortogonales y extremos distintos, esta prueba, junto con las comprobaciones de adyacencia y de casillas transitables, permite verificar que las pistas del conjunto actual no se intersectan en casillas.

## 9. Limitaciones actuales y trabajo pendiente

- Se han conectado **las 16 parejas provisionales del fichero**, que utilizan 32 de los 64 pines existentes. El diseño final todavía debe determinar qué conexiones adicionales se requieren para cumplir el enunciado. Los terminales de alimentación `S1` y `S2` aún no forman parte de la lista de conexiones.
- La estrategia secuencial bloquea las casillas ya utilizadas; **no prueba órdenes alternativos ni retrocede sobre rutas anteriores** cuando una conexión queda pendiente. La igualdad con la cota Manhattan es una prueba de óptimo **solo en el conjunto evaluado**, no una propiedad del método general.
- Para robustez adicional queda por validar de forma explícita que las coordenadas recibidas por `find_path()` estén dentro de la matriz y sean las correspondientes a los pines designados.
- La zona opcional reservada para disipación térmica todavía no se ha añadido; se elegirá después de estudiar las conexiones completas, se introducirá en el mapa de entrada y se recalcularán todas las rutas.
- Conviene conservar una captura de la ejecución en PyCharm, tanto de `main.py` como de las pruebas automáticas, como evidencia del informe acumulativo.

## 10. Relación con los materiales del profesor

- **Clase 3:** representación del soporte y lectura de códigos de casillas.
- **Clase 5:** búsqueda A*, nodos, abiertos, evaluación `f=g+h`, movimientos y Manhattan.
- **Clase 7:** plantilla de interconexión con diccionarios, `heapq`, reconstrucción de caminos y `find_path`.

La reserva secuencial de pistas en `conexiones.py` constituye una ampliación propia para utilizar A* en varias conexiones. El documento describe el comportamiento implementado y seguirá actualizándose con el proyecto.
