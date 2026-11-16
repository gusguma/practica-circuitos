# Práctica 1 — Búsqueda A* e interconexión de circuitos

## 1. Objetivo y relación con los cuadernos

Resolver automáticamente las rutas entre parejas de pines **previamente definidas**, utilizando A* para cada pareja y evitando que las pistas atraviesen circuitos, zonas bloqueadas u otras conexiones.

La base del algoritmo procede de los materiales de la asignatura:

- **Clase 5, `AStar-2Oct2026.ipynb`:** estados, nodos, abiertos y cerrados, función de evaluación y distancia Manhattan.
- **Clase 7, `InterconexionCircuitos-Clase7-VEstudiantes.ipynb`:** planteamiento del problema de circuitos, diccionarios para los nodos, `heapq` y funciones auxiliares de A*.

El proyecto utiliza nombres en `snake_case` y listas de listas para el tablero. `conexiones.py`, que coordina varias ejecuciones de A*, es una **ampliación propia** para gestionar el trazado múltiple; no sustituye a A* por otro algoritmo.

## 2. Modelo de búsqueda

| Concepto | Representación |
| --- | --- |
| Estado | `(fila, columna)` |
| Estado inicial | Coordenadas del pin de origen |
| Meta | Coordenadas del pin de destino |
| Acciones | Arriba, abajo, derecha e izquierda |
| Coste por acción | 1 movimiento |
| Casillas transitables | `"0"` y los dos extremos de la conexión actual |
| Casillas no transitables | `"X"`, pines ajenos y pistas previamente ocupadas |
| Solución individual | Lista de coordenadas origen → destino |
| Ausencia de ruta | Lista vacía `[]` |

La longitud de un camino encontrado se obtiene como `len(camino) - 1`, pues el número de desplazamientos es uno menos que el número de posiciones recorridas.

## 3. Heurística Manhattan

Con movimientos ortogonales de coste unitario:

```text
h(n) = abs(fila_actual - fila_destino) + abs(columna_actual - columna_destino)
f(n) = g(n) + h(n)
```

`g(n)` es el número de movimientos realizados desde el origen y `h(n)` estima los restantes sin considerar obstáculos. Manhattan es admisible y consistente en esta cuadrícula; A* encuentra una ruta de menor coste **para cada conexión individual con los obstáculos ya fijados**.

Esto no implica que el conjunto de rutas sea globalmente óptimo: una pista corta puede bloquear rutas posteriores y obligarlas a dar rodeos.

## 4. Funciones del módulo `astar.py`

| Función | Responsabilidad |
| --- | --- |
| `crear_nodo()` | Devuelve un diccionario con `posicion`, `padre`, `g`, `h` y `f` |
| `calcular_heuristica()` | Calcula la distancia Manhattan |
| `reconstruir_camino()` | Sigue los nodos `padre`, invierte la lista y devuelve la ruta origen → destino |
| `es_valida()` | Comprueba límites del mapa y si una casilla puede utilizarse |
| `sucesores()` | Genera posiciones adyacentes que cumplen las restricciones |
| `find_path()` | Ejecuta A* con `heapq`, abiertos, cerrados y mejores costes |

`find_path()` guarda en `abiertos` las posiciones pendientes, priorizadas por `f`. En `cerrados` registra posiciones expandidas y en `mejores_costes` conserva el menor valor `g` encontrado para cada posición. Cuando llega al destino reconstruye el recorrido. Cuando no encuentra una ruta devuelve `[]`.

## 5. Interconexión de varias parejas

La función `conectar_pines(mapa, conexiones)`, implementada en `conexiones.py`, aplica la siguiente estrategia secuencial:

1. Copia las filas del tablero original mediante `fila[:]` para no modificar el dato de entrada.
2. Recorre las parejas **en el orden en que aparecen en el fichero**.
3. Localiza origen y destino utilizando `buscar_pin()`.
4. Ejecuta `find_path()` sobre el mapa actualizado.
5. Si encuentra una ruta, almacena `(pin_origen, pin_destino, camino)` y marca con `"X"` sus posiciones interiores, impidiendo reutilizarlas.
6. Si no encuentra una ruta, añade la pareja a `pendientes`.
7. Devuelve `mapa_trazado`, `rutas` y `pendientes`.

No se cambian los extremos de las conexiones cuando aparece un bloqueo. En el diseño actual se ha establecido previamente un orden con pistas interiores, corredores exteriores y alimentación. La estrategia **no incorpora retroceso ni búsqueda exhaustiva de órdenes alternativos**.

## 6. Resultado del tablero actual

Datos del problema: soporte de 30 × 30, cuatro circuitos de 6 × 6, 64 pines y dos terminales de alimentación; **33 parejas predefinidas**.

La ejecución de `main.py` en PyCharm ha producido las siguientes longitudes:

| Grupo de rutas | Cantidad | Longitudes (movimientos) | Subtotal |
| --- | ---: | --- | ---: |
| Horizontales interiores | 8 | 9 cada una | 72 |
| Verticales interiores | 8 | 9 cada una | 72 |
| Corredor superior | 4 | 13, 17, 21, 25 | 76 |
| Corredor inferior | 4 | 13, 17, 21, 25 | 76 |
| Corredor izquierdo | 3 | 13, 17, 21 | 51 |
| Corredor derecho | 4 | 13, 17, 21, 25 | 76 |
| Alimentación | 2 | 17, 17 | 34 |
| **Total** | **33** | | **457** |

**Resultado comunicado:** `Conexiones realizadas: 33`, `Conexiones pendientes: 0`, `Longitud total: 457`.

### Alcance de la optimalidad

La suma de las **distancias Manhattan** de estas 33 parejas es **381 movimientos**, un límite inferior matemático para el total. El trazado obtenido mide 457 movimientos, es decir, 76 por encima de ese límite. Eso **no demuestra ni descarta** que 457 sea el mínimo global alcanzable con las restricciones; solo confirma una solución válida de longitud 457.

Cada búsqueda individual obtiene el menor camino disponible con las pistas anteriores bloqueadas. El orden establecido es parte de la estrategia, no una garantía de optimalidad global.

## 7. Pruebas y evidencias observadas

El script local `comprobar_diseno.py`, ejecutado en PyCharm, ha comunicado los siguientes resultados:

| Verificación | Salida |
| --- | --- |
| Dimensiones | `30 x 30` |
| Terminales presentes | `66` |
| Terminales usados | `66` |
| Cada terminal se utiliza una vez | `True` |
| Conexiones realizadas | `33` |
| Conexiones pendientes | `[]` |
| Extremos correctos | `True` |
| Movimientos adyacentes | `True` |
| Sin atravesar obstáculos | `True` |
| Sin cruces / casillas interiores repetidas | `True` |
| Longitud total | `457` |
| Resultado global de la comprobación | `DISENO VALIDO: True` |

Estas verificaciones comprueban las rutas calculadas: cada camino une los pines indicados, los movimientos son ortogonales y adyacentes, las casillas interiores estaban libres en el mapa original y ninguna se repite entre las pistas. Dado que los 66 extremos son distintos y los movimientos van de una casilla a otra, el control de posiciones permite detectar intersecciones en el modelo discreto utilizado.

Las pruebas se han ejecutado en el entorno de PyCharm. Sus scripts locales no forman parte del código que se pretende versionar; el informe de pruebas y las evidencias gráficas podrán incorporarse a la documentación final.

## 8. Limitaciones y posibles extensiones

- Las 33 parejas se definen de antemano. **El algoritmo no elige automáticamente qué pines emparejar**.
- La estrategia secuencial encuentra una solución para este tablero, pero podría dejar conexiones pendientes en otras configuraciones.
- No se implementa una búsqueda global que pruebe exhaustivamente órdenes y rutas alternativas. Por tanto, no se afirma que el total de 457 sea óptimo.
- El código se ha validado con el fichero actual; podrían incorporarse comprobaciones adicionales de coordenadas fuera de rango y de ficheros mal formados.
- **Zona reservada para disipación térmica:** sigue pendiente como ampliación opcional. Si se incorpora, se marcará en el tablero inicial y se repetirán el cálculo y la validación de las rutas.

Este documento explica el funcionamiento actual de A* y se actualizará si cambia la estrategia o se añade alguna restricción al trazado.
