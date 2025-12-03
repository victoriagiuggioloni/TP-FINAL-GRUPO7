# TP-FINAL-GRUPO7
Trabajo Práctico Final PC. Grupo 7: Clara Funes, Felicitas Gramajo, Nicole Hermann y Victoria Giuggioloni


Este proyecto implementa una version del juego Flappy Bird utilizando PyGame, combinado con un algoritmo Genetico que entrena automaticamente a una nueva poblacion de pajaros que va aprendiendo a volar lo mas lejos posible a medida que se va ejecutando el juego. 
En nuestro caso, nostras decidimos crear el juego con tematica Angry Birds, incorporando estetica visual, sprites y sonidos insirados en el mundo de ese videojuego.

El objetivo principal es que, generacion tras generacion, los pajaros vayan evolucionando sus genes hasta que alcancen un rendimiento óptimo. Cuando se llega a las 100 generaciones o mas de 30 pajaros superan los 120 segundos, el juego deja de correr automaticamente. 

Este trabajo practico mezcla visualizacion, simulacion y optimizacion inspirada en evolucion biologica. 

Visualizacion del juego:
Nuestro juego fue desarrollado y diseñado utilizando Pygame, e incluye:
* Animaciones en tiempo real
* Movimiento continuo de tuberias
* Multiples de pajaros generados a medida que se inicia el juego
* Sonidos de voz y musica
* Y un panel lateral con las espicificaciones de las estadisticas de los datos al correr el juego

Etapas del algoritmo:
1) El juego inicia con una poblacion inicial de 100 pajaros donde sus pesos son generados aleatoriamente.
2) Los pajaros juegan hasta morir.
3) Se genera una seleccion de los mejores 15 pajaros de cada partida para luego seleccionar dos aletarioamente de esos 15 y generar mas generaciones.

Requisitos
Python 3.x (probado con 3.11)
Pygame
Instalación rápida: pip install pygame

Archivos:
.
├── main.py
└── Auxiliar/
    ├── Imágenes/
    │   ├── pajaro.png
    │   ├── pajaro_icono.png
    │   ├── fondo.png
    │   ├── tubo arriba.png
    │   └── TUBO ABAJO.png
    └── Musica/
        ├── fondo_musica.mp3
        └── next_round.mp3
    └── _pycache_
    └── vscode
    



