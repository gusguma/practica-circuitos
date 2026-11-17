# Práctica 1 - Conexión de circuitos

**Autor** Gustavo Gutierrez  
**Asignatura:** Sistemas Inteligentes   
**Curso:** 2026-2027  
**Opción 1:** Conexión de circuitos

## Descripción

Esta práctica consiste en conectar los pines de varios circuitos integrados colocados sobre una placa. Para buscar las rutas se utiliza el algoritmo A Star con la heurística de distancia Manhattan.

El programa debe encontrar caminos entre parejas de pines que previamente han sido definidas, evitando pasar por los circuitos, cruzar otras conexiones o atravesar zonas reservadas para disipación térmica.

## Diseño del tablero

- Placa de **30 × 30** casillas.
- **4 circuitos** (A, B, C y D) de **6 × 6** casillas.
- **16 pines por circuito**, cuatro en cada lado: 64 pines en total.
- **2 terminales de alimentación:** S1 y S2.
- **33 conexiones** definidas previamente en el fichero de entrada.
- **Zona térmica de 3 × 4** casillas, situada en las filas 13-15 y columnas 13-16.

La placa se representa mediante una matriz. En ella, `0` identifica una casilla libre, `X` una casilla bloqueada que no puede tener uso y los códigos como `A1` o `S1` identifican los diferentes terminales. Una vez calculadas las rutas, las pistas que ocuparan las conexiones aparecen numeradas de `01` a `33`.

## Archivos principales

| Archivo | Función |
| --- | --- |
| `generar_tablero.py` | Crea la placa, coloca los circuitos, reserva la zona térmica y genera el fichero de datos. |
| `tablero.py` | Lee el fichero de datos, busca pines y muestra la matriz. |
| `astar.py` | Implementa el algoritmo A* con distancia Manhattan. |
| `conexiones.py` | Calcula las conexiones una a una y marca las pistas en el tablero. |
| `main.py` | Ejecuta la práctica y muestra los resultados, el tablero y la leyenda. |
| `datos/DefinicionConexionesCircuito.txt` | Contiene la placa y las parejas de pines que deben conectarse. |
| `TABLERO.md` | Explica el diseño y la representación de la placa. |
| `ASTAR.md` | Explica el algoritmo y el trazado de las conexiones. |

## Requisitos

- Python 3. La versión usada en el desarrollo es la 3.14
- No se necesitan bibliotecas externas: el proyecto usa la biblioteca estándar de Python.

## Ejecución

Abrir una terminal en la **carpeta raíz del proyecto** y ejecutar los siguientes comandos en este orden.

**1. Generar la placa y el fichero de conexiones:**

```bash
python generar_tablero.py
```

Este comando crea o actualiza `datos/DefinicionConexionesCircuito.txt`.

**2. Calcular y mostrar las rutas:**

```bash
python main.py
```

Se muestran los pesos (longitudes) de cada conexión, el tablero completo con las pistas numeradas y la leyenda que relaciona cada número con cada pin.

## Resultados obtenidos

En la configuración incluida en el proyecto, las ejecuciones realizadas han obtenido:

```text
Conexiones realizadas: 33
Conexiones pendientes: 0
Longitud total: 457
```

También se ha verificado en las pruebas locales que los **66 terminales** se utilizan una vez y que las rutas no atraviesan obstáculos ni se cruzan.

## Sobre el algoritmo

A Star busca un camino corto entre cada pareja de pines utilizando movimientos horizontales y verticales cuyo coste individual es 1. La distancia sirve para estimar cuánto falta para llegar al destino.

Las conexiones se calculan **secuencialmente**: una vez dibujada una pista, sus casillas quedan ocupadas para las siguientes. Por ello, aunque cada búsqueda encuentra el camino más corto disponible en ese momento, **no se garantiza que los 457 movimientos constituyan el mínimo global** para las 33 conexiones.

Para una explicación más detallada se pueden consultar [TABLERO.md](TABLERO.md) y [ASTAR.md](ASTAR.md).
