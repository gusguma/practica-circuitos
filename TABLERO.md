# Práctica 1 — Soporte, circuitos y lectura del tablero

## 1. Objetivo

Representar una placa cuadriculada que contiene cuatro circuitos integrados, identificar sus pines y definir por separado las conexiones que se solicitará realizar. El programa genera un fichero de definición y posteriormente lo lee para obtener dos estructuras: `mapa` y `conexiones`.

La representación y lectura siguen el planteamiento de construcción del tablero de los cuadernos de la asignatura. El trazado de rutas mediante A* todavía no está implementado.

## 2. Dimensiones y distribución

- **Soporte o placa:** 30 × 30 casillas.
- **Circuitos integrados:** A, B, C y D.
- **Tamaño de cada circuito:** 6 × 6 casillas.
- **Pines:** cuatro por lado y dieciséis por circuito, con esquinas libres de pines.
- **Criterio dimensional:** se interpreta que cada dimensión del soporte debe multiplicar por cinco la dimensión correspondiente de un circuito: 6 × 5 = 30.

Las coordenadas tienen el formato `(fila, columna)` y comienzan en cero.

| Circuito | Fila inicial | Columna inicial | Dimensiones |
| --- | ---: | ---: | --- |
| A | 3 | 3 | 6 × 6 |
| B | 3 | 21 | 6 × 6 |
| C | 21 | 3 | 6 × 6 |
| D | 21 | 21 | 6 × 6 |

Los terminales de alimentación se encuentran en `S1 = (0, 14)` y `S2 = (29, 14)`.

## 3. Codificación de las casillas

En el fichero, cada casilla ocupa exactamente dos caracteres. En memoria, la lectura convierte las casillas libres y bloqueadas a códigos simplificados.

| Fichero | En `mapa` | Significado |
| --- | --- | --- |
| `00` | `0` | Casilla libre |
| `XX` | `X` | Casilla no transitable |
| `A1`, `B5`, `Cg`, etc. | Igual | Pines de los circuitos |
| `S1`, `S2` | Igual | Terminales de alimentación |

Los 16 pines de cada circuito se denominan usando la letra del circuito y un símbolo de `123456789abcdefg`:

- Superior: `1`, `2`, `3`, `4`.
- Derecho: `5`, `6`, `7`, `8`.
- Inferior: `9`, `a`, `b`, `c`.
- Izquierdo: `d`, `e`, `f`, `g`.

El interior y las esquinas de cada circuito se representan como `XX` en el fichero original.

## 4. Fichero de definición

El archivo `datos/DefinicionConexionesCircuito.txt` contiene una primera sección de 30 líneas (matriz del soporte). Después aparece el delimitador `CONEXIONES:` y, a continuación, una conexión por línea, escrita como `ORIGEN-DESTINO`.

Actualmente existen **16 conexiones provisionales**, entre los circuitos A–B, C–D, A–C y B–D. No están conectados todos los pines ni se han incluido todavía las conexiones a la alimentación. Por tanto, esta lista aún no constituye la definición definitiva del problema.

## 5. Generación del tablero

`generar_tablero.py` crea la matriz de 30 × 30 con `00`, ocupa las casillas de los circuitos con `XX`, coloca los pines, incorpora `S1` y `S2`, define las conexiones iniciales y escribe el fichero de texto.

Desde la raíz del proyecto:

```bash
python generar_tablero.py
```

## 6. Lectura y representación en Python

El módulo `tablero.py` contiene cuatro funciones. Se utilizan los nombres en *snake_case* adoptados en nuestro proyecto, aunque algunos ejemplos del profesor están escritos en *camelCase*.

### `get_codigo_tablero(caracteres)`

Interpreta el código de una casilla: devuelve `"0"` para `"00"`, `"X"` para `"XX"` y conserva los identificadores de pines y terminales. No comprueba por sí sola si un identificador es válido.

### `cargar_tablero(nombre_fichero)`

Abre el fichero, recorre sus líneas y separa las dos secciones utilizando la marca `CONEXIONES:`. Mientras lee el tablero, avanza de dos en dos caracteres para convertir cada línea en una lista de casillas. En la sección de conexiones, separa cada línea por `-` y guarda una tupla `(origen, destino)`.

Devuelve `mapa, conexiones`, donde:

- `mapa` es una lista de 30 filas; cada fila contiene 30 casillas.
- `conexiones` es una lista de 16 tuplas con nombres de pines.

Esta función presupone el formato del fichero generado; todavía no incorpora una validación exhaustiva de archivos mal formados.

### `buscar_pin(mapa, pin)`

Recorre la matriz mediante dos bucles `for`. Si encuentra el identificador solicitado devuelve una tupla `(fila, columna)`; si no existe, devuelve `None`.

Por ejemplo, según el diseño del generador, `buscar_pin(mapa, "A1")` debe devolver `(3, 4)`.

### `mostrar_matriz(mapa)`

Recorre filas y casillas e imprime cada código alineado en la consola. Esta función permite inspeccionar visualmente la disposición de los circuitos y sus pines, pero no representa todavía las pistas calculadas por A*.

## 7. Ejecución en PyCharm

Con la raíz del proyecto como directorio de trabajo:

```bash
python generar_tablero.py
python main.py
```

`main.py` utiliza las funciones del módulo `tablero.py` para cargar el fichero, consultar posiciones y mostrar la matriz.

**Comprobación comunicada durante el desarrollo:** se han obtenido correctamente 30 filas, 30 columnas y 16 conexiones; también se resolvió una inconsistencia entre `getCodigoTablero` y `get_codigo_tablero` y se consiguió mostrar la matriz. Las comprobaciones automatizadas de todos los pines se incorporarán por separado al informe.

## 8. Estado actual y limitaciones

Están implementadas la generación del soporte, la lectura del fichero, la búsqueda de pines y la visualización textual. Queda pendiente implementar A*, reservar casillas de rutas, completar la lista definitiva de conexiones y verificar los requisitos de ausencia de cruces y longitud mínima de las pistas.

La posible zona reservada para disipación térmica se estudiará tras obtener rutas, pero, si se incorpora, deberá añadirse al tablero de entrada y volver a ejecutarse la búsqueda antes de validar la solución final.

Este documento se actualizará cuando evolucione el funcionamiento del programa; no incluye información del historial de Git.
