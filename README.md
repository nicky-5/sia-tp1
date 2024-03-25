
# TP1 SIA - Métodos de Búsqueda

[Enunciado](docs/SIA_TP1.pdf)

Dentro de src podemos encontrar los distintos archivos que hacen a nuestro proyecto. Primero en functions.py podemos encontrar las
funciones que permiten navegar el tablero de sokoban de manera correcta, aqui podemos encontrar tanto las comparaciones de las distintas
partes del tablero como tambien funciones de lectura o impresion. Es principalmente una libreria estandar de funciones basicas.
Luego en heuristics.py podemos encontrar las implementaciones de las distintas heuristicas, tanto las admisibles como las inadmisibles.
En methods.py se encuentran las implementaciones de los distintos metodos de busqueda, todos implementan dentro las mismas funciones 
para que despues sea simple intercambiar el metodo de busqueda por el deseado en el archivo main.py. Luego en search.py podemos encontrar
la funcion que utiliza los distintos metodos de busqueda para encontrar la solucion del juego, search es nuestra funcion principal que hace 
uso de todas las otras implementaciones. Aqui tambien podemos encontrar una funcion auxiliar para el search utilizando el algoritmo de a*.
En sokoban.py estan las reglas del juego, donde describimos el tablero, jugador y todas las partes necesarias para poder implementar el juego.

Dentro de la carpeta test se encuentran los distintos mapas para el sokoban junto con las soluciones de los dichos mapas.

### Requisitos

- Python3
- pip3
- [pipenv](https://pypi.org/project/pipenv/)

### Instalación

Parado en la carpeta del tp1 ejecutar

```sh
pipenv install
```

para instalar las dependencias necesarias en el ambiente virtual

## Ejecución


Dentro del main se puede seleccionar la heuristica para utilizar y luego el metodo de busqueda que va a utilizar esta heuristica.
Luego podemos tambien seleccionar el mapa a correr al editar la variable file_name y cambiamos el numero del test al que deseamos correr
Finalmente, seleccionamos el metodo de busqueda que vamos a utilizar al cargar la funcion deseada en la variable solution.
Guardamos el archivo con los cambios hechos y luego corremos el archivo main como lo dice abajo.

```
pipenv run python main.py
```

