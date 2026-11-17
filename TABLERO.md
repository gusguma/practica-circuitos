# Práctica 1 — Diseño y representación del tablero

## 1. Objetivo

Representar el soporte sobre el que se sitúan los circuitos integrados y definir qué pines deben conectarse antes de calcular las rutas. El proyecto utiliza una matriz bidimensional y un fichero de texto con dos secciones diferenciadas: la geometría del soporte y la lista de conexiones, siguiendo el enfoque de construcción de tableros visto en las clases.

En la implementación actual intervienen los siguientes archivos:

- `generar_tablero.py`: construye los circuitos, sus pines, la zona térmica y las conexiones definidas, y escribe el fichero de entrada.
- `tablero.py`: lee el fichero, busca las posiciones de los pines y muestra las matrices en consola.
- `conexiones.py`: calcula y marca las rutas sobre una copia del mapa.
- `main.py`: coordina la ejecución y presenta las rutas, el tablero resultante y la leyenda.

## 2. Dimensiones y distribución de los circuitos

| Elemento | Características |
| --- | --- |
| Soporte o placa | 30 × 30 casillas (900 posiciones) |
| Circuitos integrados | A, B, C y D |
| Tamaño de cada circuito | 6 × 6 casillas |
| Pines de cada circuito | 16: cuatro por lado, sin utilizar las esquinas |
| Total de pines de circuitos | 64 |
| Terminales de alimentación | S1 y S2 |
| Zona de disipación térmica | 3 × 4 casillas (12 posiciones bloqueadas) |

El requisito del soporte cinco veces mayor que el circuito se interpreta como cinco veces la dimensión lineal: en este caso `6 × 5 = 30`. Esta interpretación es una decisión documentada del diseño.

Las coordenadas se expresan como `(fila, columna)`, comenzando desde cero:

| Componente | Posición inicial | Región o posición ocupada |
| --- | --- | --- |
| Circuito A | `(5, 5)` | Filas 5–10, columnas 5–10 |
| Circuito B | `(5, 19)` | Filas 5–10, columnas 19–24 |
| Circuito C | `(19, 5)` | Filas 19–24, columnas 5–10 |
| Circuito D | `(19, 19)` | Filas 19–24, columnas 19–24 |
| Alimentación S1 | — | `(0, 14)` |
| Alimentación S2 | — | `(29, 14)` |
| Zona térmica | `(13, 13)` | Filas 13–15, columnas 13–16 |

La disposición deja cinco casillas libres entre los circuitos exteriores y el borde de la placa, y ocho casillas libres entre circuitos enfrentados. Los laterales se utilizan para las pistas de conexión.

Esquema orientativo de la distribución de los circuitos, alimentación y zona de disipación 
que no es el de las rutas:

```text
                  S1
       ┌───────────────────────┐
       │      A         B      │
       │                       │
       │        [XXXX]         │
       │      C         D      │
       └───────────────────────┘
                  S2
```

## 3. Identificación y colocación de pines

La función `colocar_circuito(letra, fila_inicial, columna_inicial)` coloca primero las 36 casillas del circuito con `XX` y después los pines en las cuatro posiciones de cada lado.

| Lado | Pines de A | Equivalentes en B, C y D |
| --- | --- | --- |
| Superior | A1, A2, A3, A4 | B1–B4, C1–C4, D1–D4 |
| Derecho | A5, A6, A7, A8 | B5–B8, C5–C8, D5–D8 |
| Inferior | A9, Aa, Ab, Ac | B9–Bc, C9–Cc, D9–Dc |
| Izquierdo | Ad, Ae, Af, Ag | Bd–Bg, Cd–Cg, Dd–Dg |

Se utiliza la secuencia `123456789abcdefg` para mantener los identificadores de pin de dos caracteres (`A1`, `Aa`, `Bg`, etc.). Las esquinas y el interior de cada circuito permanecen bloqueados y no podrán ser ocupados. Las pistas no pueden atravesar pines distintos de sus extremos.

## 4. Fichero de entrada

`datos/DefinicionConexionesCircuito.txt` contiene:

1. Treinta líneas que describen el soporte, con 60 caracteres por línea: dos por casilla.
2. El separador `CONEXIONES:`.
3. Treinta y tres líneas con parejas de pines, utilizando el formato `ORIGEN-DESTINO`.

La lectura transforma los códigos del fichero de la siguiente forma:

| Fichero | Matriz `mapa` | Significado |
| --- | --- | --- |
| `00` | `"0"` | Casilla libre |
| `XX` | `"X"` | Casilla bloqueada (interior de circuitos o zona térmica) |
| `A1`, `Bd`, etc. | Mismo código | Pin de circuito |
| `S1`, `S2` | Mismo código | Terminal de alimentación |

Las dos estructuras resultantes son:

- `mapa`: lista de listas de 30 × 30 posiciones.
- `conexiones`: lista de 33 tuplas `(pin_origen, pin_destino)`.

El fichero de texto es generado por `generar_tablero.py`. Siempre que se cambie la distribución de los circuitos o la lista de parejas de conexiones, debe regenerarse antes de ejecutar `main.py`.

## 5. Conexiones definidas

Las parejas se establecen previamente: El algoritmo A Star no decide qué pines emparejar, sino por dónde debe pasar cada pista.

| Zona | Cantidad | Conexiones |
| --- | ---: | --- |
| Horizontales interiores | 8 | A5–Bd, A6–Be, A7–Bf, A8–Bg, C5–Dd, C6–De, C7–Df, C8–Dg |
| Verticales interiores | 8 | A9–C1, Aa–C2, Ab–C3, Ac–C4, B9–D1, Ba–D2, Bb–D3, Bc–D4 |
| Superior | 4 | A4–B1, A3–B2, A2–B3, A1–B4 |
| Inferior | 4 | Cc–D9, Cb–Da, Ca–Db, C9–Dc |
| Izquierdo | 3 | Ag–Cd, Af–Ce, Ae–Cf |
| Derecho | 4 | B8–D5, B7–D6, B6–D7, B5–D8 |
| Alimentación | 2 | S1–Ad, S2–Cg |
| **Total** | **33** | **66 extremos** |

En este modelo se ha decidido utilizar cada uno de los 64 pines y los dos terminales de alimentación exactamente una vez. Es un modelo de interconexión para la práctica, no es un esquema real.

## 6. Generación y lectura del tablero

### `generar_tablero.py`

1. Construye una matriz de 30 filas, cada una con 30 cadenas `"00"`.
2. Coloca los circuitos A, B, C y D en las posiciones definidas.
3. Coloca los terminales S1 y S2.
4. Reserva la zona térmica central (filas 13–15 y columnas 13–16) y la marca con `XX`.
5. Define las parejas de pines mediante una lista de tuplas.
6. Escribe la placa y las conexiones en `DefinicionConexionesCircuito.txt`.

### `tablero.py`

| Función | Utilidad |
| --- | --- |
| `get_codigo_tablero()` | Convierte `00` en `"0"`, `XX` en `"X"` y conserva los pines. |
| `cargar_tablero()` | Separa tablero y conexiones al leer el fichero. |
| `buscar_pin()` | Devuelve la posición `(fila, columna)` de un pin, o `None` si no existe. |
| `mostrar_matriz()` | Imprime las filas de la matriz con las casillas alineadas. |

Se utilizan las estructuras de datos y recursos del curso. Los nombres de las funciones se han adaptado a la convención `snake_case` de Python.

## 7. Zona de disipación térmica

La placa incorpora una región de 3 filas y 4 columnas, situada en el centro de la base:

| Parámetro | Valor |
| --- | --- |
| Fila inicial | 13 |
| Columna inicial | 13 |
| Alto | 3 casillas |
| Ancho | 4 casillas |
| Casillas bloqueadas | 12 |
| Filas ocupadas | 13, 14 y 15 |
| Columnas ocupadas | 13, 14, 15 y 16 |

En `generar_tablero.py` se definen `FILA_ZONA_TERMICA`, `COLUMNA_ZONA_TERMICA`, `ALTO_ZONA_TERMICA` y `ANCHO_ZONA_TERMICA`. Dos bucles `for` recorren la región. Antes de marcar cada posición, se comprueba que contiene `00`; si una casilla ya está ocupada, se genera un error para evitar sobrescribir circuitos o terminales. Después se escribe `XX`.

Al cargar el fichero, `tablero.py` convierte cada `XX` en `"X"`. Por tanto, la región térmica se comporta como un obstáculo más para A Star sin requerir cambios en el algoritmo. Las casillas reservadas se mantienen visibles como un bloque de 3 × 4 letras `X` en la matriz de salida.

En el tablero original, estas doce casillas estaban libres y no pertenecían a ninguna pista calculada. Tras introducir la región, se han vuelto a ejecutar las 33 conexiones y se ha obtenido la misma longitud total de **457 movimientos**.

Esta zona es una reserva de espacio únicamente

## 8. Representación de las conexiones sobre el soporte

Se mantienen dos matrices diferentes:

- **`mapa`**: representa el soporte original, sin pistas trazadas.
- **`mapa_trazado`**: es una copia de `mapa` en la que `conectar_pines()` marca las rutas encontradas.

El código copia cada fila mediante `fila[:]` para no modificar el tablero original y asi evitar errores inesperados debido a la mutación del original, tal y como muestra el video del Curso de Python. A continuación, calcula cada ruta mediante `find_path()` y marca solo sus casillas interiores, manteniendo visibles los pines inicial y final.

A cada ruta se le asigna un identificador numérico de dos caracteres.

La codificación del tablero mostrado en consola es:

| Código visible | Significado |
| --- | --- |
| `0` | Casilla libre |
| `X` | Casilla prohibida: interior de un circuito o zona térmica |
| `A1`, `Bd`, `Cg`, etc. | Pines de circuitos |
| `S1`, `S2` | Terminales de alimentación |
| `01` a `33` | Casillas interiores ocupadas por una pista identificada |

La numeración corresponde al orden de la lista de conexiones, no al tipo de circuito. Por ejemplo, `01` representa A5–Bd, `17` representa A4–B1, `32` representa S1–Ad y `33` representa S2–Cg. Un número es igual a una conexión.

Las pistas numeradas siguen siendo obstáculos para las búsquedas posteriores: `es_valida()` únicamente permite pasar por `"0"` y por los dos extremos de la conexión actual. Una casilla que contiene `"01"`, `"02"` u otro identificador no es transitable.

La matriz se muestra desde `main.py` con:

```python
print("\nTABLERO CON LAS CONEXIONES")
mostrar_matriz(mapa_trazado)
```

El programa imprime además una leyenda que asocia cada identificador con su pareja de pines. Así se puede interpretar el trazado sin perder la relación entre el número de pista y la conexión correspondiente.

### Leyenda completa

| Pista | Conexión | Pista | Conexión | Pista | Conexión |
| --- | --- | --- | --- | --- | --- |
| 01 | A5–Bd | 12 | Ac–C4 | 23 | Ca–Db |
| 02 | A6–Be | 13 | B9–D1 | 24 | C9–Dc |
| 03 | A7–Bf | 14 | Ba–D2 | 25 | Ag–Cd |
| 04 | A8–Bg | 15 | Bb–D3 | 26 | Af–Ce |
| 05 | C5–Dd | 16 | Bc–D4 | 27 | Ae–Cf |
| 06 | C6–De | 17 | A4–B1 | 28 | B8–D5 |
| 07 | C7–Df | 18 | A3–B2 | 29 | B7–D6 |
| 08 | C8–Dg | 19 | A2–B3 | 30 | B6–D7 |
| 09 | A9–C1 | 20 | A1–B4 | 31 | B5–D8 |
| 10 | Aa–C2 | 21 | Cc–D9 | 32 | S1–Ad |
| 11 | Ab–C3 | 22 | Cb–Da | 33 | S2–Cg |

La impresión de la matriz es una representación discreta en consola que permite comprobar las casillas utilizadas por cada pista, pero no sustituye a un esquema gráfico con líneas y colores. Un diagrama final puede generarse posteriormente a partir de las rutas reales.

## 9. Ejecución y resultados observados

Con el directorio de trabajo de PyCharm situado en la raíz del proyecto:

```bash
python generar_tablero.py
python main.py
```

`generar_tablero.py` ha mostrado un soporte de 30 × 30, cuatro circuitos de 6 × 6, 64 pines, S1 y S2, 33 conexiones definidas y una zona térmica de 3 × 4 con 12 casillas reservadas.

`main.py` ha mostrado **33 conexiones realizadas, 0 pendientes y 457 movimientos**. También ha impreso el `TABLERO CON LAS CONEXIONES`, con pistas numeradas del `01` al `33`, y su leyenda.

Estas comprobaciones se refieren al modelo discreto actual. La explicación de A* y de la longitud total aparece en `ASTAR.md`.

## 10. Limitaciones y posibles ampliaciones

- Las conexiones se definen previamente; el programa no elige los emparejamientos.
- La proporción de tamaño 5:1 se ha aplicado a cada dimensión lineal.
- El formato de entrada no realiza una validación de todos los errores posibles.
- La visualización actual es textual y utiliza códigos numéricos por pista.
- La zona térmica está modelada solo como un obstáculo. Si se cambia su posición o tamaño, habrá que regenerar el tablero y repetir todas las pruebas.
