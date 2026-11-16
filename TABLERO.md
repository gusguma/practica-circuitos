# Práctica 1 — Diseño y representación del tablero

## 1. Objetivo

Representar el soporte sobre el que se colocan los circuitos integrados y definir, **antes de buscar las rutas**, qué pines deben conectarse. El proyecto emplea una matriz bidimensional y un fichero de texto que separa el plano de la placa de la lista de conexiones, siguiendo el planteamiento de construcción del tablero estudiado en clase.

`generar_tablero.py` construye la definición y `tablero.py` la interpreta. `main.py` utiliza posteriormente estos datos para el trazado con A*.

## 2. Dimensiones y posición de los componentes

- **Soporte (placa):** 30 × 30 casillas (900 posiciones).
- **Circuitos integrados:** A, B, C y D.
- **Dimensiones de cada circuito:** 6 × 6 casillas.
- **Pines por circuito:** 16, distribuidos en cuatro por lado, sin pines en las esquinas.
- **Total de pines de circuitos:** 64.
- **Terminales de alimentación adicionales:** S1 y S2.

Se interpreta el requisito de que el soporte sea cinco veces el tamaño del circuito como un factor **cinco en cada dimensión lineal**: 6 × 5 = 30.

Las coordenadas están expresadas como `(fila, columna)` y comienzan en cero:

| Elemento | Coordenada inicial | Región ocupada / posición |
| --- | --- | --- |
| Circuito A | `(5, 5)` | Filas 5–10, columnas 5–10 |
| Circuito B | `(5, 19)` | Filas 5–10, columnas 19–24 |
| Circuito C | `(19, 5)` | Filas 19–24, columnas 5–10 |
| Circuito D | `(19, 19)` | Filas 19–24, columnas 19–24 |
| Alimentación S1 | — | `(0, 14)` |
| Alimentación S2 | — | `(29, 14)` |

Esta distribución deja cinco casillas libres entre los circuitos exteriores y el borde más próximo de la placa, y ocho casillas libres en los corredores entre circuitos enfrentados. El desplazamiento hacia el centro permite disponer de más espacio para las pistas de los lados exteriores.

## 3. Distribución e identificación de los pines

Cada circuito ocupa una superficie 6 × 6. La función `colocar_circuito(letra, fila_inicial, columna_inicial)` marca inicialmente todas sus casillas como `XX` y luego sustituye las posiciones del perímetro que corresponden a pines.

| Lado | Identificadores del circuito A | Equivalentes en los demás circuitos |
| --- | --- | --- |
| Superior | A1, A2, A3, A4 | B1–B4, C1–C4, D1–D4 |
| Derecho | A5, A6, A7, A8 | B5–B8, C5–C8, D5–D8 |
| Inferior | A9, Aa, Ab, Ac | B9–Bc, C9–Cc, D9–Dc |
| Izquierdo | Ad, Ae, Af, Ag | Bd–Bg, Cd–Cg, Dd–Dg |

Se usan los caracteres `123456789abcdefg` para que cada identificador ocupe **exactamente dos caracteres**. Las cuatro esquinas y el interior de cada circuito permanecen bloqueados. Los códigos de pines representan posiciones de conexión, no casillas libres por las que puedan atravesar pistas ajenas.

## 4. Formato de la definición

El fichero `datos/DefinicionConexionesCircuito.txt` contiene:

1. **Treinta líneas de tablero:** 60 caracteres por línea, con dos caracteres por casilla.
2. El separador literal `CONEXIONES:`.
3. **Treinta y tres líneas de conexiones:** una pareja `ORIGEN-DESTINO` por línea.

Codificación de las casillas:

| En fichero | En `mapa` tras la lectura | Interpretación |
| --- | --- | --- |
| `00` | `"0"` | Casilla libre |
| `XX` | `"X"` | Obstáculo, interior o esquina no transitable |
| `A1`, `Bd`, `Cg`, etc. | Mismo identificador | Pin de un circuito |
| `S1`, `S2` | Mismo identificador | Terminal de alimentación |

El fichero es generado por `generar_tablero.py`. Si se cambian posiciones o parejas en el generador, hay que volver a ejecutarlo para mantener el fichero sincronizado.

## 5. Definición de las conexiones

**Las parejas de pines se establecen antes de ejecutar A*.** El programa de búsqueda calcula las rutas, pero no decide con qué otro pin debe conectarse cada extremo.

| Grupo | Número | Parejas |
| --- | ---: | --- |
| Horizontales interiores | 8 | A5–Bd, A6–Be, A7–Bf, A8–Bg, C5–Dd, C6–De, C7–Df, C8–Dg |
| Verticales interiores | 8 | A9–C1, Aa–C2, Ab–C3, Ac–C4, B9–D1, Ba–D2, Bb–D3, Bc–D4 |
| Corredor superior | 4 | A4–B1, A3–B2, A2–B3, A1–B4 |
| Corredor inferior | 4 | Cc–D9, Cb–Da, Ca–Db, C9–Dc |
| Corredor izquierdo | 3 | Ag–Cd, Af–Ce, Ae–Cf |
| Corredor derecho | 4 | B8–D5, B7–D6, B6–D7, B5–D8 |
| Alimentación | 2 | S1–Ad, S2–Cg |
| **Total** | **33** | **66 extremos** |

Este modelo utiliza los 64 pines de los circuitos y los dos terminales de alimentación exactamente una vez, como **decisión de diseño** de esta práctica. No pretende representar las necesidades eléctricas reales de cuatro circuitos integrados.

## 6. Generación y lectura con Python

### `generar_tablero.py`

- Crea `mapa` como lista de 30 filas de 30 códigos `00`.
- Coloca los circuitos llamando a `colocar_circuito()`.
- Añade `S1` y `S2`.
- Construye una lista de tuplas `conexiones`, con las parejas ya definidas.
- Escribe el fichero con la matriz y la sección de conexiones.

### `tablero.py`

- `get_codigo_tablero(caracteres)`: transforma `00` en `"0"`, `XX` en `"X"` y conserva los identificadores de pines.
- `cargar_tablero(nombre_fichero)`: lee las dos secciones del fichero y devuelve `mapa, conexiones`.
- `buscar_pin(mapa, pin)`: recorre las casillas y devuelve `(fila, columna)` o `None` si no lo encuentra.
- `mostrar_matriz(mapa)`: muestra el tablero en consola, alineando sus casillas.

Los nombres del proyecto están escritos en `snake_case`. El enfoque de lectura y representación procede de los ejemplos de construcción de tablero de la asignatura.

## 7. Ejecución y verificaciones

Con PyCharm configurado para trabajar desde la raíz del proyecto:

```bash
python generar_tablero.py
python main.py
```

Salida comunicada de `generar_tablero.py`:

```text
Soporte: 30 x 30
Circuitos: A, B, C, D
Dimensiones de cada circuito: 6 x 6
Pines por circuito: 16
Total de pines de circuitos: 64
Terminales de alimentacion: S1 y S2
Conexiones definidas: 33
Fichero generado: datos/DefinicionConexionesCircuito.txt
```

La comprobación local del diseño ha informado de 66 terminales en el tablero, 66 terminales utilizados y `Todos conectados una vez: True`. Además, el trazado ha obtenido las 33 rutas sin pendientes. La validación de trayectorias se explica en `ASTAR.md`.

## 8. Limitaciones y evolución del diseño

- Las parejas se definen de forma fija en el generador; el proyecto **no empareja automáticamente** los pines.
- La proporción 5:1 se aplica a las dimensiones lineales del soporte, como interpretación documentada del enunciado.
- El fichero generado utiliza un formato sencillo de texto; su lector no valida exhaustivamente todos los posibles errores de formato.
- **La zona opcional para disipación térmica todavía no está incorporada.** Si se decide añadirla, se deberá introducir como obstáculo en el tablero de entrada y repetir el trazado y sus pruebas. No basta con marcar una zona libre una vez calculadas las pistas.

Este documento describe el estado actual del diseño y se actualizará si cambian las dimensiones, los circuitos, los pines o las conexiones.
