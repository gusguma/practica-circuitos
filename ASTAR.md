# Práctica 1 — Algoritmo A* y trazado de conexiones

## 1. Objetivo y referencias de clase

Calcular rutas para parejas de pines **previamente definidas**, utilizando el algoritmo A* y respetando los obstáculos de la placa, la zona de disipación térmica y las pistas ya trazadas. El cálculo se realiza sobre el soporte de 30 × 30 descrito en `TABLERO.md`.

La implementación sigue el enfoque de los cuadernos de la asignatura:

- **Clase 5 — `AStar-2Oct2026.ipynb`:** representación de estados, nodos, abiertos y cerrados, función de evaluación y heurística Manhattan.
- **Clase 7 — `InterconexionCircuitos-Clase7-VEstudiantes.ipynb`:** aplicación a interconexión de circuitos, nodos representados mediante diccionarios, `heapq` y funciones auxiliares.

Hemos utilizado nombres `snake_case` y listas de listas para el mapa. El módulo `conexiones.py` es una **ampliación propia** que coordina varias búsquedas A* consecutivas, sin sustituir el algoritmo principal.

## 2. Formulación del problema de búsqueda

| Concepto | Representación |
| --- | --- |
| Estado | `(fila, columna)` de una casilla |
| Estado inicial | Coordenadas del pin de origen |
| Meta | Coordenadas del pin de destino |
| Acciones | Arriba, abajo, derecha e izquierda |
| Coste de acción | 1 movimiento |
| Posiciones transitables | Casillas `"0"` y extremos de la conexión actual |
| Posiciones bloqueadas | `"X"` (circuitos y zona térmica), otros pines y pistas ya ocupadas |
| Solución individual | Lista de posiciones ordenadas desde origen hasta destino |
| Sin solución | Lista vacía `[]` |

Solo se permiten movimientos ortogonales; no se contemplan diagonales ni saltos entre posiciones. La longitud de una ruta se calcula con `len(camino) - 1`.

## 3. Función de evaluación y heurística

A* utiliza:

```text
f(n) = g(n) + h(n)
```

- `g(n)` es el número de movimientos realizados desde el origen hasta el nodo `n`.
- `h(n)` estima los movimientos restantes hasta la meta.
- `f(n)` estima el coste total de la ruta que pasa por `n`.

Para calcular `h(n)` usamos **distancia Manhattan**, como en el ejemplo de tablero bidimensional de la Clase 5:

```text
h(n) = abs(fila_actual - fila_destino)
     + abs(columna_actual - columna_destino)
```

Con cuatro movimientos ortogonales de coste 1, Manhattan es admisible y consistente: nunca sobreestima la distancia mínima real, aunque ignore los obstáculos.

En las condiciones de esta implementación, A* encuentra el camino más corto **para una conexión individual considerando las casillas bloqueadas en ese momento**. Esto no equivale a optimizar simultáneamente todas las pistas.

## 4. Funciones de `astar.py`

| Función | Descripción |
| --- | --- |
| `crear_nodo()` | Crea un diccionario con `posicion`, `padre`, `g`, `h`, `f`. |
| `calcular_heuristica()` | Calcula Manhattan entre dos posiciones. |
| `reconstruir_camino()` | Recorre los enlaces `padre` desde la meta y devuelve las posiciones en orden origen → destino. |
| `es_valida()` | Comprueba los límites y que la casilla sea libre o un extremo permitido. |
| `sucesores()` | Genera movimientos ortogonales válidos. |
| `find_path()` | Ejecuta A* utilizando una cola de prioridad, costes conocidos y posiciones exploradas. |

Los nodos se representan mediante **diccionarios**, de acuerdo con la plantilla de la Clase 7, en lugar de reproducir la clase `Nodo` genérica de la Clase 5.

### Funcionamiento de `find_path()`

1. Comprueba que se han localizado el origen y el destino.
2. Crea el nodo inicial con `g=0` y `h` igual a Manhattan.
3. Lo introduce en `abiertos`, gestionado mediante `heapq`.
4. Extrae el nodo con menor `f`.
5. Si es el destino, devuelve `reconstruir_camino(nodo_actual)`.
6. En otro caso, lo añade a `cerrados` y estudia sus sucesores.
7. Para cada sucesor, calcula el nuevo coste `g`; si mejora el coste conocido, crea un nodo y lo añade a `abiertos`.
8. Si se agotan los nodos pendientes sin encontrar la meta, devuelve `[]`.

Las estructuras empleadas son:

| Estructura | Utilidad |
| --- | --- |
| `abiertos` | Cola de prioridad de nodos pendientes. |
| `cerrados` | Conjunto de posiciones exploradas. |
| `mejores_costes` | Diccionario con el mejor coste `g` conocido para cada posición. |
| `contador` | Desempata prioridades iguales sin comparar diccionarios de nodos. |

La función `es_valida()` evita cruzar el interior de los circuitos, la zona térmica y otros pines. Más adelante, la misma comprobación impide usar las casillas que ocupan rutas ya calculadas.

## 5. Gestión de varias conexiones

El módulo `conexiones.py` contiene `conectar_pines(mapa, conexiones)`. Esta función **no determina los emparejamientos**; recibe las parejas en el orden definido en el fichero de entrada.

Su procedimiento es:

1. Crear `mapa_trazado` como copia de `mapa`, copiando cada fila mediante `fila[:]`.
2. Inicializar las listas `rutas` y `pendientes`.
3. Para cada pareja, localizar sus pines con `buscar_pin()`.
4. Llamar a `find_path(mapa_trazado, origen, destino)`.
5. Si hay camino, guardar `(pin_origen, pin_destino, camino)` y reservar sus casillas interiores.
6. Si no hay camino, almacenar la pareja en `pendientes`.
7. Devolver `mapa_trazado, rutas, pendientes`.

### Identificación de pistas en la matriz

En la versión actual las posiciones interiores de una ruta no se marcan con el carácter genérico `"X"`, sino con **un identificador numérico de dos caracteres**:

```python
identificador = str(numero_conexion).rjust(2, "0")

for fila, columna in camino[1:-1]:
    mapa_trazado[fila][columna] = identificador
```

Así la pista `01` corresponde a A5–Bd, la `02` a A6–Be, y sucesivamente hasta `33`, que corresponde a S2–Cg. Los pines de origen y destino permanecen visibles.

**Este cambio de representación no modifica el criterio de búsqueda.** La función `es_valida()` solo admite casillas `"0"` o los extremos de la conexión actual; por ello, las casillas que contienen `"01"` a `"33"` siguen bloqueadas para las conexiones posteriores.

La distinción entre matrices es importante:

- `mapa` contiene el soporte original, sin pistas.
- `mapa_trazado` conserva ese soporte e incorpora las rutas numeradas.

En `main.py` se muestra la matriz calculada con `mostrar_matriz(mapa_trazado)` y después una leyenda `01 : A5 - Bd`, ..., `33 : S2 - Cg`. La correspondencia completa de las 33 pistas aparece en `TABLERO.md`.

### Zona de disipación térmica como obstáculo

Antes de ejecutar A*, `generar_tablero.py` marca como `XX` un rectángulo de **3 × 4 casillas** en las filas **13–15** y columnas **13–16**. Al leer el fichero, `tablero.py` convierte `XX` en `"X"`. Por eso, `es_valida()` rechaza estas casillas exactamente igual que el interior bloqueado de los circuitos; **no se ha modificado `astar.py` ni `conexiones.py`** para incorporar la restricción.

Las doce casillas reservadas no pertenecían a las rutas calculadas antes de esta modificación, de modo que las 33 conexiones siguen completándose con **457 movimientos**. Si la zona se trasladara a una pista existente, sería necesario recalcular y validar de nuevo todo el trazado.

### Orden de trazado

Se procesan primero las 16 pistas interiores, después las de los corredores superior, inferior, izquierdo y derecho, y finalmente las dos de alimentación. Ese orden forma parte de la definición de entrada. La estrategia actual es **secuencial**: no incorpora retroceso ni un planificador global que reconsidere caminos anteriores.

## 6. Resultados de ejecución

El tablero tiene cuatro circuitos con 64 pines, los terminales S1 y S2 y una zona térmica de **12 casillas bloqueadas**; hay **33 conexiones previamente definidas**. La ejecución realizada en PyCharm obtuvo:

| Grupo | Rutas | Longitudes (movimientos) | Subtotal |
| --- | ---: | --- | ---: |
| Horizontales interiores | 8 | 9 cada una | 72 |
| Verticales interiores | 8 | 9 cada una | 72 |
| Corredor superior | 4 | 13, 17, 21, 25 | 76 |
| Corredor inferior | 4 | 13, 17, 21, 25 | 76 |
| Corredor izquierdo | 3 | 13, 17, 21 | 51 |
| Corredor derecho | 4 | 13, 17, 21, 25 | 76 |
| Alimentación | 2 | 17, 17 | 34 |
| **Total** | **33** | | **457** |

Resultados observados:

```text
Conexiones realizadas: 33
Conexiones pendientes: 0
Longitud total: 457
```

Además, `main.py` ha mostrado el **tablero de 30 × 30 con las pistas numeradas del `01` al `33`** y la leyenda correspondiente. Se ha comprobado que añadir esos números no altera las longitudes ni impide completar ninguna de las rutas.

## 7. Validación de las rutas

El script local `comprobar_diseno.py`, ejecutado después de incorporar la zona térmica y las pistas numeradas, ha devuelto:

```text
Dimensiones: 30 x 30
Terminales del tablero: 66
Terminales utilizados: 66
Todos conectados una vez: True
Conexiones realizadas: 33
Conexiones pendientes: []
Extremos correctos: True
Movimientos validos: True
Sin obstaculos: True
Sin cruces: True
Longitud total: 457
DISENO VALIDO: True
```

Estas pruebas verifican que:

- Todos los terminales definidos aparecen como extremos de una conexión, exactamente una vez.
- Cada recorrido empieza y termina en los pines adecuados.
- Los movimientos son adyacentes y ortogonales.
- Ninguna casilla interior de una ruta contiene un obstáculo en el tablero original.
- No se repite ninguna casilla interior entre rutas distintas.
- No quedan conexiones pendientes y la longitud total es 457.

La comprobación local específica `comprobar_zona_termica.py` ha devuelto:

```text
PRUEBA DE LA ZONA TERMICA
Dimensiones de la zona: 3 x 4
Casillas reservadas: 12
Todas las casillas bloqueadas: True
Conexiones definidas: 33
Conexiones realizadas: 33
Conexiones pendientes: []
Ninguna ruta atraviesa la zona: True
Longitud total: 457
ZONA TERMICA VALIDA: True
```

Esta segunda prueba comprueba explícitamente las coordenadas bloqueadas y que ningún camino utiliza una de esas posiciones. Como los extremos son distintos y las rutas solo pasan por casillas interiores libres, el control de ocupación es apropiado para detectar solapamientos y cruces **en la cuadrícula discreta utilizada**. Las pruebas locales quedan fuera del repositorio, mientras que sus resultados se recogen en la documentación del proyecto.

## 8. Análisis de la optimalidad

La suma de las distancias Manhattan entre las 33 parejas es de **381 movimientos**, lo que representa un límite inferior para cualquier trazado con movimientos ortogonales de coste 1.

El trazado obtenido utiliza **457 movimientos**, es decir, 76 más que ese límite inferior. Estas diferencias proceden de los rodeos necesarios para evitar componentes y pistas ocupadas.

Por tanto:

- Cada ejecución individual de A* busca el camino más corto disponible con los obstáculos establecidos en ese instante.
- Las 33 rutas obtenidas constituyen una **solución válida** para el tablero y el orden actuales.
- **No se ha demostrado que 457 sea el mínimo global** para todas las conexiones simultáneamente: otra planificación podría producir una longitud total menor.

## 9. Limitaciones y posibles ampliaciones

- Las parejas de pines están fijadas en el fichero; no se generan automáticamente.
- El planificador secuencial puede bloquear conexiones en otros tableros, aunque en el actual complete las 33.
- No se implementan búsqueda exhaustiva de órdenes alternativos ni retroceso global.
- La representación gráfica actual es la matriz textual con identificadores; un esquema visual puede construirse a partir de las coordenadas reales de las rutas.
- La zona de disipación térmica ya está incorporada como obstáculo fijo de 12 casillas y ha superado su validación. No se modela el comportamiento físico del calor; si cambia la zona habrá que repetir la búsqueda y las comprobaciones.

Este documento describe el algoritmo y su aplicación en el estado actual del proyecto. Se actualizará si se modifica la estrategia de planificación o se añaden restricciones.
