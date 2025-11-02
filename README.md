Mini Agar.io en Pygame

Este es un "Mini Agar.io", un proyecto didáctico creado en Python y Pygame. Demuestra una variedad de técnicas avanzadas de desarrollo de juegos, incluyendo una cámara 2D con zoom, un mundo, mecánicas de juego basadas en la física (masa) y una IA de bots reactiva.



🚀 Características Principales

Mundo (Cámara 2D): El mundo del juego (3000x2000) es mucho más grande que la ventana (960x540). Una cámara sigue al jugador.

Movimiento Suave de Cámara: La cámara utiliza interpolación lineal (lerp) para seguir suavemente al jugador, en lugar de "saltar" bruscamente.

Zoom Dinámico: La cámara se aleja (zoom out) a medida que la masa total del jugador aumenta, permitiéndole ver más del campo de juego.

Mecánica de Dividir (Split): Presiona W para dividir tus blobs por la mitad y lanzarlos hacia el cursor, permitiéndote atrapar presas.

Mecánica de Dash: Presiona SPACE para perder un 5% de tu masa y ganar un impulso de velocidad.

Fusión de Blobs: Después de dividirte, tus blobs tienen un temporizador y no pueden fusionarse de nuevo hasta que este se acabe.

IA de Bots: El juego incluye bots de IA que siguen reglas simples: huir de amenazas más grandes, perseguir presas más pequeñas y vagar si están a salvo.

Física Basada en Masa:

Radio: El radio se calcula con la raíz cuadrada de la masa (r = \sqrt{Masa/pi }), para un crecimiento de área realista.

Velocidad: La velocidad es inversamente proporcional al radio. ¡Mientras más grande eres, más lento te mueves!

Colisiones Eficientes: Utiliza un sistema de colisión de dos fases (AABB broad-phase y círculo narrow-phase) para optimizar el rendimiento.

🔧 Instalación y Ejecución

Para correr este proyecto, necesitas Python y Pygame.

1. Instalar Pygame:
Abre tu terminal o consola y escribe:

pip install pygame


2. Ejecutar el Juego:
Guarda el código como agar_game.py (o cualquier nombre) y ejecútalo desde tu terminal


🎮 Controles

Moverse: Mueve el Mouse para dirigir tu(s) blob(s).

Dividir (Split): Presiona la tecla W.

Dash (Impulso): Presiona la Barra Espaciadora.

Reiniciar: Presiona R (después de perder o ganar).

Salir: Presiona ESC.

🧬 Resumen Técnico

Game: Clase principal que gestiona el estado del juego, el bucle, las listas de entidades y la cámara.

Blob: Clase para todas las entidades "vivas" (jugador y bots). Maneja la masa, el radio, la velocidad y la lógica de movimiento.

Food: Clase ligera (__slots__) para las partículas de comida.

update_camera(): Implementa el seguimiento lerp y el zoom dinámico basado en la masa total del jugador.

eat_collisions(): Maneja todas las interacciones de "comer" (jugador-comida, jugador-bot, bot-jugador) usando colisiones optimizadas.

update_bots(): Contiene la IA (máquina de estados simple) que decide si huir, perseguir o vagar.
