# Pygame - Mini Agar.io (Starter didáctico)
# Autor: Prof. Luis (plantilla)
# Mecánica: círculo jugador que come comida y blobs pequeños, crece y se vuelve más lento.
# Mundo > pantalla con cámara centrada. Mouse para mover; SPACE = dash (-5% masa); R = reset; ESC = salir.
 
import pygame, sys, random, math
 
pygame.init()
WIDTH, HEIGHT = 960, 540                 # tamaño de ventana
WORLD_W, WORLD_H = 3000, 2000            # tamaño del mundo
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Agar.io - Starter")
CLOCK = pygame.time.Clock()
FPS = 60
 
def clamp(v, a, b): return max(a, min(v, b))
 
def draw_grid(surf, camx, camy):
    surf.fill((18,20,26))
    color = (28,32,40)  
    step = 64
    w, h = surf.get_size()
    sx = -(camx) % step
    sy = -(camy) % step
    for x in range(int(sx), int(w), step):
      pygame.draw.line(surf, color, (x, 0), (x, h))
    for y in range(int(sy), int(h), step):
      pygame.draw.line(surf, color, (0, y), (w, y))
 
class Food:
    __slots__ = ("x","y","r","col")
    def __init__(self, x, y):
      self.x, self.y = x, y
      self.r = random.randint(3, 6)
      self.col = random.choice([(255,173,72),(170,240,170),(150,200,255),(255,120,160),(255,220,120)])
    def draw(self, surf, camx, camy):
      pygame.draw.circle(surf, self.col, (int(self.x - camx), int(self.y - camy)), self.r)
 
class Blob:
    def __init__(self, x, y, mass, color):
      self.x, self.y = x, y
      self.mass = mass # masa ~ área
      self.color = color
      self.vx = 0.0; self.vy = 0.0
      self.target = None
      self.alive = True
      self.merge_timer = 0 # Tiempo antes de poder fusionarse
 
    @property
    def r(self):
    # radio ~ sqrt(masa) (crecimiento "realista" para área ~ masa)
        return max(6, int(math.sqrt(self.mass / math.pi)))
     
    @property
    def speed(self):
      # más masa -> más lento
      base = 260.0
      return max(60.0, base / (1.0 + 0.04*self.r))
 
    def move_towards(self, tx, ty, dt):
      dx, dy = tx - self.x, ty - self.y
      dist = math.hypot(dx, dy)
      if dist > 1e-3:
          vx = (dx / dist) * self.speed
          vy = (dy / dist) * self.speed
      else:
          vx = vy = 0.0
      # inercia ligera
      self.vx = self.vx*0.85 + vx*0.15
      self.vy = self.vy*0.85 + vy*0.15
      self.x += self.vx * dt
      self.y += self.vy * dt
      self.x = clamp(self.x, 0, WORLD_W)
      self.y = clamp(self.y, 0, WORLD_H) 
    def draw(self, surf, camx, camy, outline=True):
        pygame.draw.circle(surf, self.color, (int(self.x - camx), int(self.y - camy)), self.r)
        if outline:
          pygame.draw.circle(surf, (255,255,255), (int(self.x - camx), int(self.y - camy)), self.r, 2)
 
class Game:
    def __init__(self):
      self.reset()
 
    def reset(self):
                random.seed()
                player_blob = Blob(WORLD_W/2, WORLD_H/2, mass=600, color=(120,200,255))
                self.player_blobs = [player_blob]
                self.bots = []
                for _ in range(18):
                        bx = random.randint(50, WORLD_W-50)
                        by = random.randint(50, WORLD_H-50)
                        mass = random.randint(200, 900)
                        col = random.choice([(255,140,120),(255,200,90),(170,240,170),(160,200,255),(255,120,180)])
                        self.bots.append(Blob(bx, by, mass, col))
                self.food = [Food(random.randint(0,WORLD_W), random.randint(0,WORLD_H)) for _ in range(1200)]
                self.zoom = 1.0
                self.camx, self.camy = self.player_blobs[0].x - WIDTH/2, self.player_blobs[0].y - HEIGHT/2
                self.time = 0.0
                self.merge_time = 6.0 # segundos para poder volver a unir blobs
                self.state = "PLAY" # PLAY / GAMEOVER / WIN
 
    def spawn_food_ring(self, cx, cy, count=40, radius=120):
      for i in range(count):
         ang = (i / count) * math.tau
         fx = cx + math.cos(ang) * radius + random.uniform(-10,10)
         fy = cy + math.sin(ang) * radius + random.uniform(-10,10)
         fx = clamp(fx, 0, WORLD_W); fy = clamp(fy, 0, WORLD_H)
         self.food.append(Food(fx, fy))
 
    def update_player(self, dt):
     # Control con mouse: dirigir hacia el cursor
     mx, my = pygame.mouse.get_pos() # Coordenadas del ratón en la ventana
     tx = self.camx + mx / self.zoom # Convertir a coordenadas del mundo
     ty = self.camy + my / self.zoom
     for p in self.player_blobs:
        p.move_towards(tx, ty, dt)
 
    def update_bots(self, dt):
     # IA muy simple: huye de amenazas, persigue presas cercanas; si no, vaga
     for b in self.bots:
         if not b.alive: continue
         threat = None; prey = None; mindist_threat = 1e9
         for other in self.bots + self.player_blobs:
             if other is b or not other.alive: continue
             d = abs(other.x - b.x) + abs(other.y - b.y) # (distancia manhattan)
             if other.mass > b.mass*1.35 and d < 480:  
                if d < mindist_threat: mindist_threat = d; threat = other
             elif other.mass*1.35 < b.mass and d < 420:
                 prey = other
 
         if threat is not None:
             tx = b.x - (threat.x - b.x) # huir (vector opuesto)
             ty = b.y - (threat.y - b.y)
         elif prey is not None:
             tx, ty = prey.x, prey.y
         else:
             if b.target is None or random.random() < 0.005:
                 b.target = (random.randint(0,WORLD_W), random.randint(0,WORLD_H))
             tx, ty = b.target
         b.move_towards(tx, ty, dt)
 
    def get_player_center(self):
        if not self.player_blobs:
            return self.camx + (WIDTH/2 / self.zoom), self.camy + (HEIGHT/2 / self.zoom)
        sum_x = sum(p.x * p.mass for p in self.player_blobs)
        sum_y = sum(p.y * p.mass for p in self.player_blobs)
        total_mass = self.get_total_player_mass()
        if total_mass == 0:
            return self.player_blobs[0].x, self.player_blobs[0].y
        return sum_x / total_mass, sum_y / total_mass

    def get_total_player_mass(self):
        return sum(p.mass for p in self.player_blobs)

    def eat_collisions(self):
        # player blobs comen food
        remain_food = []
        for f in self.food:
            eaten = False
            for p in self.player_blobs:
                # Comprobación rápida (caja) antes de la precisa (círculo)
                if abs(f.x - p.x) < p.r + 12 and abs(f.y - p.y) < p.r + 12:
                    if (f.x - p.x)**2 + (f.y - p.y)**2 < (p.r + f.r)**2:
                        p.mass += f.r * 0.9
                        eaten = True
                        break # La comida ya fue comida, no chequear otros blobs
            if not eaten:
                remain_food.append(f)
        self.food = remain_food
        # player blobs comen bots pequeños
        for p in self.player_blobs:
            for b in self.bots:
                if not b.alive: continue
                rsum = p.r - b.r * 0.95
                if rsum < 0: continue
                if (b.x - p.x)**2 + (b.y - p.y)**2 < rsum**2 and p.mass > b.mass*1.15:
                    p.mass += b.mass * 0.80
                    b.alive = False
                    self.spawn_food_ring(b.x, b.y, count=50, radius=140)

        # bots comen player blobs
        for b in self.bots:
            if not b.alive: continue
            for p in self.player_blobs:
                if b.mass > p.mass*1.20:
                    if (b.x - p.x)**2 + (b.y - p.y)**2 < (b.r - p.r*0.9)**2:
                        p.alive = False # El bot se come una parte del jugador
        
        self.player_blobs = [p for p in self.player_blobs if p.alive]
        if not self.player_blobs:
            self.state = "GAMEOVER"

        # Player blobs se fusionan entre sí
        if len(self.player_blobs) > 1:
            merged_blobs = []
            for i in range(len(self.player_blobs)):
                p1 = self.player_blobs[i]
                if not p1.alive: continue
                for j in range(i + 1, len(self.player_blobs)):
                    p2 = self.player_blobs[j]
                    if not p2.alive: continue
                    
                    # Solo fusionar si ambos timers han acabado
                    if p1.merge_timer > 0 or p2.merge_timer > 0: continue

                    dist_sq = (p1.x - p2.x)**2 + (p1.y - p2.y)**2
                    if dist_sq < (p1.r + p2.r)**2:
                        # El más grande se come al más pequeño
                        if p1.mass > p2.mass:
                            p1.mass += p2.mass
                            p2.alive = False
                        else:
                            p2.mass += p1.mass
                            p1.alive = False
            self.player_blobs = [p for p in self.player_blobs if p.alive]
 
    def update_camera(self, dt):
        # Zoom basado en la masa total del jugador
        total_mass = self.get_total_player_mass()
        # A mayor masa, menor zoom (más alejado). pow() suaviza el efecto.
        zoom_ratio = 600.0 / (total_mass + 1e-5)
        target_zoom = pow(zoom_ratio, 0.12) # Exponente balanceado para una curva suave
        target_zoom = clamp(target_zoom, 0.4, 2.0) # Rango de zoom reducido para ser menos extremo
        self.zoom += (target_zoom - self.zoom) * 0.04 # Transición ligeramente más lenta y suave

        # Cámara con lerp suave que sigue el centro de masa
        center_x, center_y = self.get_player_center()
        target_x = center_x - (WIDTH / 2 / self.zoom)
        target_y = center_y - (HEIGHT / 2 / self.zoom)
        self.camx += (target_x - self.camx) * 0.08
        self.camy += (target_y - self.camy) * 0.08
        self.camx = clamp(self.camx, 0, WORLD_W - (WIDTH / self.zoom))
        self.camy = clamp(self.camy, 0, WORLD_H - (HEIGHT / self.zoom))
 
    def dash(self):
        if not self.player_blobs: return

        # dash: pierde 5% masa y gana impulso hacia el ratón
        mx, my = pygame.mouse.get_pos()
        tx = self.camx + mx / self.zoom
        ty = self.camy + my / self.zoom

        for p in self.player_blobs:
            loss = p.mass * 0.05
            if p.mass - loss < 30: continue # Masa mínima para hacer dash
            p.mass -= loss
            dx, dy = tx - p.x, ty - p.y
            dist = math.hypot(dx, dy) + 1e-5
            p.vx = (dx/dist) * 900
            p.vy = (dy/dist) * 900
 
    def split(self):
        # Límite de 8 blobs y masa mínima para dividir
        if len(self.player_blobs) >= 8:
            return

        new_blobs = []
        # Usamos una copia de la lista para poder modificarla mientras iteramos
        for p in list(self.player_blobs):
            if p.mass < 200: continue # Masa mínima para dividir

            p.mass /= 2
            new_mass = p.mass

            mx, my = pygame.mouse.get_pos()
            tx = self.camx + mx / self.zoom
            ty = self.camy + my / self.zoom
            dx, dy = tx - p.x, ty - p.y
            dist = math.hypot(dx, dy) + 1e-5

            new_blob = Blob(p.x, p.y, new_mass, p.color)
            # Impulso de eyección
            ejection_speed = 600 + new_blob.r * 2
            new_blob.vx = (dx/dist) * ejection_speed
            new_blob.vy = (dy/dist) * ejection_speed
            
            # Activar temporizador para no poder fusionarse inmediatamente
            p.merge_timer = self.merge_time
            new_blob.merge_timer = self.merge_time
            new_blobs.append(new_blob)
        
        if new_blobs:
            self.player_blobs.extend(new_blobs)

    def update(self, dt):
        if self.state != "PLAY":
            return
        self.time += dt
        # Actualizar temporizadores de fusión
        for p in self.player_blobs:
            if p.merge_timer > 0: p.merge_timer -= dt

        self.update_player(dt)
        self.update_bots(dt) # Los bots ahora ven una lista de blobs de jugador
        self.eat_collisions()
        # respawn de comida
        if len(self.food) < 1000:
            for _ in range(50):
                self.food.append(Food(random.randint(0,WORLD_W), random.randint(0,WORLD_H)))
        # ganar: todos los bots muertos
        if all(not b.alive for b in self.bots):
            self.state = "WIN"
        self.update_camera(dt)
 
    def draw(self):
        # Preparamos una superficie temporal para dibujar el mundo con zoom
        world_surf = pygame.Surface((WIDTH / self.zoom, HEIGHT / self.zoom))
        
        wx, wy = self.camx, self.camy
        draw_grid(world_surf, wx, wy)

        # comida
        for f in self.food:
            f.draw(world_surf, wx, wy)

        # bots
        for b in self.bots:
            if b.alive:
                b.draw(world_surf, wx, wy)
        
        # jugador (todos sus blobs)
        for p in self.player_blobs:
            p.draw(world_surf, wx, wy)

        # Escalamos la superficie del mundo a la ventana principal
        scaled_world = pygame.transform.smoothscale(world_surf, (WIDTH, HEIGHT))
        WINDOW.blit(scaled_world, (0, 0))

        # HUD
        pygame.draw.rect(WINDOW, (25,28,36), (10, 10, 300, 70), border_radius=8)
        font = pygame.font.SysFont(None, 24)
        WINDOW.blit(font.render(f"Masa Total: {int(self.get_total_player_mass())}", True, (235,235,245)), (20, 18))
        WINDOW.blit(font.render("W = dividir | SPACE = dash", True, (200,220,255)), (20, 44))

        if self.state == "GAMEOVER":
            t = pygame.font.SysFont(None, 48).render("GAME OVER", True, (255,120,120))
            r = t.get_rect(center=(WIDTH//2, HEIGHT//2-10))
            WINDOW.blit(t, r)
            s = pygame.font.SysFont(None, 28).render("[R] reiniciar - [ESC] salir", True, (235,235,245))
            WINDOW.blit(s, (WIDTH//2 - s.get_width()//2, HEIGHT//2 + 26))

        if self.state == "WIN":
            t = pygame.font.SysFont(None, 48).render("¡GANASTE!", True, (180,255,180))
            r = t.get_rect(center=(WIDTH//2, HEIGHT//2-10))
            WINDOW.blit(t, r)
            s = pygame.font.SysFont(None, 28).render("Todos los bots derrotados - [R] reiniciar", True, (235,235,245))
            WINDOW.blit(s, (WIDTH//2 - s.get_width()//2, HEIGHT//2 + 26))
 
    def run(self):
        running = True
        while running:
            dt = CLOCK.tick(FPS) / 1000.0
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        running = False
                    elif e.key == pygame.K_r:
                        self.reset()
                    elif e.key == pygame.K_SPACE and self.state == "PLAY":
                        self.dash()
                    elif e.key == pygame.K_w and self.state == "PLAY":
                        self.split()

            # actualizar y dibujar una vez por frame (fuera del bucle de eventos)
            self.update(dt)
            self.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()
    
def main():
    Game().run()
 
if __name__ == "__main__":
    main()
