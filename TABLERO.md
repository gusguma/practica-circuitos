# Práctica 1 — Diseño del soporte y los circuitos integrados

## 1. Objetivo

Representar sobre una cuadrícula los circuitos integrados y sus pines, así como definir las conexiones que deberán trazarse posteriormente. La geometría del soporte y la lista de conexiones se mantienen separadas, siguiendo el planteamiento de los cuadernos de clase.

## 2. Dimensiones y distribución

- **Soporte (placa):** 30 × 30 casillas.
- **Circuitos integrados:** cuatro, identificados como A, B, C y D.
- **Dimensiones de cada circuito:** 6 × 6 casillas.
- **Pines:** cuatro en cada lado; 16 por circuito, sin ocupar las esquinas.
- **Relación de tamaños:** se interpreta que cada lado del soporte mide cinco veces el lado de un circuito (30 = 5 × 6).

Las posiciones se expresan mediante pares `(fila, columna)`, comenzando por `(0, 0)` en la esquina superior izquierda.

| Circuito | Fila inicial | Columna inicial | Dimensiones |
| --- | ---: | ---: | --- |
| A | 3 | 3 | 6 × 6 |
| B | 3 | 21 | 6 × 6 |
| C | 21 | 3 | 6 × 6 |
| D | 21 | 21 | 6 × 6 |

## 3. Representación del tablero

Se utiliza una **lista de listas** de Python, donde cada elemento representa una casilla de la placa. En el fichero de texto, cada casilla se codifica mediante **dos caracteres**.

| Código | Significado |
| --- | --- |
| `00` | Casilla libre |
| `XX` | Casilla ocupada o no transitable (interior y esquinas de los circuitos) |
| `A1`, `B5`, etc. | Pin de un circuito integrado |
| `S1`, `S2` | Terminales de alimentación |

Los terminales de alimentación se sitúan en `S1 = (0, 14)` y `S2 = (29, 14)`.

## 4. Identificación de los pines

Para mantener una anchura de dos caracteres por casilla, los 16 pines se identifican mediante la letra del circuito y uno de los símbolos `123456789abcdefg`.

La distribución de identificadores es:

- **Lado superior:** `1`, `2`, `3`, `4`.
- **Lado derecho:** `5`, `6`, `7`, `8`.
- **Lado inferior:** `9`, `a`, `b`, `c`.
- **Lado izquierdo:** `d`, `e`, `f`, `g`.

Por ejemplo, `Aa` es un pin del circuito A y `Dg` es un pin del circuito D.

## 5. Definición de las conexiones

El fichero `datos/DefinicionConexionesCircuito.txt` contiene dos partes:

1. La matriz que describe la placa y los circuitos.
2. La lista de parejas de pines, después de la línea `CONEXIONES:`.

Actualmente se generan **16 conexiones iniciales**: cuatro entre A y B, cuatro entre C y D, cuatro entre A y C, y cuatro entre B y D.

Estas conexiones son provisionales: **no cubren todos los pines ni incluyen aún los terminales de alimentación**. La definición deberá revisarse para cumplir el enunciado completo.

## 6. Generación del soporte

El archivo `generar_tablero.py`:

1. Crea una matriz de 30 × 30 casillas libres (`00`).
2. Sitúa los cuatro circuitos, marcando su interior como `XX`.
3. Identifica cuatro pines por cada lado de cada circuito.
4. Añade los terminales de alimentación.
5. Define la lista inicial de conexiones.
6. Guarda la matriz y las conexiones en `datos/DefinicionConexionesCircuito.txt`.

El soporte puede generarse desde la raíz del proyecto con:

```bash
python generar_tablero.py
```

## 7. Estado actual del diseño y limitaciones

La generación del soporte y de las 16 conexiones iniciales está implementada. La lectura independiente del fichero, el cálculo de rutas con A* y la comprobación de que todas las conexiones pueden trazarse sin cruces **no forman parte todavía del funcionamiento implementado**.

La búsqueda de la ruta mínima entre dos pines no garantiza por sí sola una solución global que conecte todos los pines sin cruces. Esta restricción deberá abordarse y comprobarse al desarrollar el trazado de las conexiones.

Este documento se actualizará cuando cambien la geometría, los identificadores, las conexiones o las reglas de representación del soporte.