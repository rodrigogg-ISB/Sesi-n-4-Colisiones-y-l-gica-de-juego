## **Manual de Usuario**

Bienvenido a "Mini Agar.io". Esta guía te explica cómo instalar y jugar el juego.

### **1\. Instalación**

Para jugar, solo necesitas dos cosas instaladas en tu computadora:

1. **Python 3:** (probado con 3.10+, pero cualquier versión reciente debería funcionar).

**Biblioteca Pygame:** Puedes instalarla abriendo una terminal o consola y escribiendo:  
pip install pygame

2. 

### **2\. Ejecución**

1. Guarda el código del juego en un archivo con extensión `.py` (ejemplo: `agar_game.py`).  
2. Abre una terminal o consola.  
3. Navega hasta la carpeta donde guardaste el archivo.  
4. Ejecuta el juego escribiendo  
     
   **3\. Objetivo y Controles**

**Objetivo:** Eres el *blob* celeste. Muévete por el mundo para comer la comida (círculos pequeños) y a otros *blobs* (IA) que sean más pequeños que tú. Evita que los *blobs* más grandes te coman.

**Controles:**

* **Moverse:** Mueve el Mouse. Tu *blob* seguirá automáticamente el cursor.  
* **Dash (Impulso):** Presiona la Barra Espaciadora. Perderás un 5% de tu masa actual para ganar un impulso de velocidad.  
* **Reiniciar:** Si te comen (GAME OVER) o si ganas, presiona la tecla R para comenzar una nueva partida.  
* **Salir:** Presiona la tecla ESC o cierra la ventana del juego.

### **4\. Solución de Problemas**

* **Error: `ModuleNotFoundError: No module named 'pygame'`**  
  * **Solución:** No tienes Pygame instalado. Sigue el paso 2 de la **Instalación** para instalarlo (`pip install pygame`).  
* **El juego se cierra inmediatamente:**  
  * **Solución:** Revisa la consola o terminal. Es probable que haya un error en el código (por ejemplo, un error de tipeo o indentación) que se mostrará allí.  
* **El juego va muy lento:**  
  * **Solución:** Este juego genera muchas entidades. Si tu computadora es más antigua, el rendimiento puede verse afectado. No hay una solución simple aparte de reducir la cantidad de comida o de bots en el código.

