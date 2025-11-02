## **Manual Técnico**

Este documento describe la arquitectura interna, los sistemas clave y las decisiones de diseño del juego.

### **1\. Arquitectura del Juego**

El juego está construido alrededor de una clase principal `Game`, que gestiona el estado general, el bucle principal (`run`), y las listas de entidades. La arquitectura está compuesta en varias clases clave:

* **`Game`**: Es la clase orquestadora. Contiene el bucle principal, maneja los eventos, y almacena las listas de `bots`, `food`, y al `player`. Llama a los métodos `update()` y `draw()` de los demás sistemas.  
* **`Blob`**: Es la clase base para todas las entidades "vivas" (el jugador y los bots). Contiene la lógica de movimiento (`move_towards`), física (cálculo de `r` a partir de `mass`), y estado (`alive`).  
* **`Food`**: Una clase ligera (usando `__slots__` para optimizar memoria) que solo almacena su posición, radio y color. No tiene método `update()`.  
* **Mundo y Cámara**: El juego opera en un `WORLD_W` y `WORLD_H` (3000x2000) que es más grande que la `WINDOW` (960x540). Las coordenadas de todos los objetos son absolutas (posición en el mundo). La cámara (`camx`, `camy`) es un par de coordenadas que define la esquina superior izquierda de la "vista" del jugador.

### **2\. Sistema de Cámara**

La cámara no está vinculada directamente al jugador; utiliza una interpolación lineal (lerp) para seguirlo suavemente.

* **Función:** `update_camera(self, dt)`  
* **Lógica:** En lugar de igualar la posición de la cámara a la del jugador, el código calcula la posición objetivo (`target_x`, `target_y`). Luego, en cada *frame*, mueve la cámara un pequeño porcentaje (8%) de la distancia restante hacia ese objetivo: `self.camx += (target_x - self.camx) * 0.08`  
* **Beneficio:** Esto crea un movimiento fluido y profesional que evita saltos bruscos.  
* **Límites:** La cámara está limitada (`clamp`) a los bordes del mundo (`WORLD_W`, `WORLD_H`), asegurando que nunca muestre espacio "vacío" fuera de los límites del juego.

### **3\. Detección de Colisiones**

El sistema de colisiones (`eat_collisions`) está optimizado para manejar una gran cantidad de objetos (cientos de comidas y docenas de *blobs*) de forma eficiente.

Utiliza una **estrategia de dos fases**:

1. **Fase Amplia (Broad Phase):** Se realiza una comprobación de colisión AABB (caja delimitadora) rápida y de bajo coste. Descarta la gran mayoría de los objetos que están demasiado lejos del jugador.  
   * *Código:* `if abs(f.x - px) < pr+12 and abs(f.y - py) < pr+12:`  
2. **Fase Estrecha (Narrow Phase):** Solo para los objetos que pasan la primera fase, se ejecuta una comprobación de colisión por radio (círculo-círculo) precisa.  
   * **Optimización:** Para evitar la costosa operación de raíz cuadrada (`math.sqrt`), el código compara el *cuadrado* de las distancias con el *cuadrado* del radio:  
     * *Código:* `(f.x - px)**2 + (f.y - py)**2 < (pr + f.r)**2`

### **4\. Inteligencia Artificial (IA)**

La IA de los `bots` es un autómata finito (máquina de estados) simple pero efectivo, definido en `update_bots`.

* **Estados:** Perseguir, Huir, Vagar.  
* **Lógica de Decisión:**  
  1. **Amenaza (Huir):** Si un *blob* cercano es **1.35x** más grande (`other.mass > b.mass*1.35`), el bot huirá de él (se mueve en dirección opuesta).  
  2. **Presa (Perseguir):** Si no hay amenaza, y un *blob* cercano es **1.35x** más pequeño (`other.mass*1.35 < b.mass`), el bot lo perseguirá.  
  3. **Vagar:** Si no hay amenazas ni presas, el bot elegirá un punto aleatorio en el mapa (`b.target`) y se moverá hacia él.  
* **Umbrales:** La IA tiene un "campo de visión" limitado (`480` píxeles para amenazas, `420` para presas) para optimizar el rendimiento y hacer el comportamiento más realista.

### **5\. Parámetros y Balance del Juego**

El balance se controla mediante propiedades (`@property`) en la clase `Blob` y constantes en la clase `Game`.

* **Crecimiento (Radio):** `r = math.sqrt(self.mass / math.pi)`. El radio crece con la raíz cuadrada de la masa, lo que significa que un jugador necesita cada vez más masa para crecer visualmente, creando una curva de dificultad creciente.  
* **Velocidad:** `speed = max(60.0, base / (1.0 + 0.04*self.r))`. La velocidad es **inversamente proporcional al radio**. Cuanto más grande eres, más lento te mueves. Esto es fundamental para el balance, permitiendo a los jugadores pequeños escapar de los grandes.  
* **Mecánica de *Dash*:**  
  * **Coste:** `self.player.mass * 0.05` (un coste porcentual del 5% de la masa).  
  * **Beneficio:** Un gran impulso de velocidad (`* 900`).  
  * **Balance:** El coste porcentual y un límite mínimo (`mass < 200`) evitan el *spam* del *dash*, convirtiéndolo en una decisión estratégica (alto riesgo, alta recompensa).  
* **Balance de Comida:**  
  * **Reposición:** El mapa se repuebla con comida (`range(50)`) si el conteo total baja de 1000\.  
  * **Recompensa por Muerte:** Al morir, un bot suelta un anillo de comida (`spawn_food_ring`), incentivando el combate.

