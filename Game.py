import pygame
import sys
import random
import math

pygame.init()

W, H = 800, 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("LEGO Memory Quest")
clock = pygame.time.Clock()
FPS = 60

# ── Colors ───────────────────────────────────────────────────────────────────
WHITE    = (255, 255, 255)
BLACK    = (0,   0,   0)
RED      = (227, 0,   11)
YELLOW   = (255, 213, 0)
BLUE     = (0,   153, 204)
DKBLUE   = (0,   60,  100)
GREEN    = (34,  139, 34)
DKGREEN  = (20,  80,  20)
BROWN    = (101, 67,  33)
ORANGE   = (255, 140, 0)
SKYBLUE  = (135, 206, 235)
GRAY     = (80,  80,  80)
DKGRAY   = (40,  40,  40)
LTGRAY   = (160, 160, 160)
SAND     = (194, 154, 84)
PURPLE   = (80,  40,  120)
GOLD     = (255, 200, 0)
OFFWHITE = (245, 245, 220)
CYAN     = (0,   200, 220)
PINK     = (255, 100, 180)

font_big = pygame.font.SysFont("impact", 56)
font_med = pygame.font.SysFont("impact", 32)
font_sm  = pygame.font.SysFont("arial",  20)
font_xs  = pygame.font.SysFont("arial",  16)

# ── Helpers ──────────────────────────────────────────────────────────────────

def draw_text(surf, text, font, color, cx, cy, shadow=False):
    if shadow:
        s = font.render(text, True, BLACK)
        surf.blit(s, s.get_rect(center=(cx+2, cy+2)))
    img = font.render(text, True, color)
    surf.blit(img, img.get_rect(center=(cx, cy)))


def draw_lego_brick(surf, x, y, w, h, color):
    darker  = tuple(max(0, c - 50) for c in color)
    lighter = tuple(min(255, c + 60) for c in color)
    pygame.draw.rect(surf, color,   (x, y, w, h), border_radius=3)
    pygame.draw.rect(surf, darker,  (x, y, w, h), 2, border_radius=3)
    pygame.draw.rect(surf, lighter, (x+2, y+2, w-4, h//3), border_radius=2)
    studs = max(1, w // 16)
    for i in range(studs):
        sx = x + 8 + i * ((w-16) // max(1, studs-1)) if studs > 1 else x + w//2
        pygame.draw.ellipse(surf, color,   (sx-7, y-6, 14, 8))
        pygame.draw.ellipse(surf, darker,  (sx-7, y-6, 14, 8), 1)
        pygame.draw.ellipse(surf, lighter, (sx-5, y-5, 6,  4))


def draw_lego_figure(surf, x, y, color=RED):
    pygame.draw.ellipse(surf, YELLOW,      (x-10, y-38, 20, 20))
    pygame.draw.ellipse(surf, (180,150,0), (x-10, y-38, 20, 20), 1)
    pygame.draw.circle(surf, BLACK, (x-4, y-30), 2)
    pygame.draw.circle(surf, BLACK, (x+4, y-30), 2)
    pygame.draw.arc(surf, BLACK, (x-5, y-26, 10, 6), math.pi, 0, 2)
    draw_lego_brick(surf, x-12, y-18, 24, 20, color)
    pygame.draw.rect(surf, DKBLUE, (x-12, y+2,  10, 16), border_radius=2)
    pygame.draw.rect(surf, DKBLUE, (x+2,  y+2,  10, 16), border_radius=2)
    pygame.draw.rect(surf, color,  (x-18, y-16, 6,  14), border_radius=2)
    pygame.draw.rect(surf, color,  (x+12, y-16, 6,  14), border_radius=2)
    pygame.draw.circle(surf, YELLOW, (x-15, y-2), 4)
    pygame.draw.circle(surf, YELLOW, (x+15, y-2), 4)
    pygame.draw.ellipse(surf, YELLOW, (x-4, y-42, 8, 5))


def draw_plane(surf, x, y):
    pygame.draw.ellipse(surf, BLUE,   (x-30, y-12, 80, 24))
    pygame.draw.ellipse(surf, DKBLUE, (x-30, y-12, 80, 24), 2)
    pts = [(x+50, y), (x+70, y-5), (x+70, y+5)]
    pygame.draw.polygon(surf, BLUE, pts)
    pts2 = [(x-30, y-4), (x-50, y-24), (x-38, y-4)]
    pygame.draw.polygon(surf, BLUE, pts2)
    pygame.draw.polygon(surf, DKBLUE, pts2, 1)
    pts3 = [(x-10, y+2), (x+20, y+2), (x+10, y+26), (x-20, y+26)]
    pygame.draw.polygon(surf, (0, 100, 180), pts3)
    pygame.draw.polygon(surf, DKBLUE, pts3, 2)
    for i in range(3):
        pygame.draw.ellipse(surf, SKYBLUE, (x-10+i*18, y-8, 12, 12))
        pygame.draw.ellipse(surf, WHITE,   (x-10+i*18, y-8, 12, 12), 1)
    angle = pygame.time.get_ticks() / 80
    for a in [angle, angle + math.pi]:
        px2 = x + 70 + int(math.cos(a)*18)
        py2 = y      + int(math.sin(a)*18)
        pygame.draw.line(surf, DKGRAY, (x+70, y), (px2, py2), 4)


def _draw_car_base(surf, x, y):
    pygame.draw.rect(surf, RED,     (x, y+12, 80, 26), border_radius=4)
    pygame.draw.rect(surf, BLACK,   (x, y+12, 80, 26), 2, border_radius=4)
    pygame.draw.rect(surf, RED,     (x+14, y, 52, 18), border_radius=4)
    pygame.draw.rect(surf, BLACK,   (x+14, y, 52, 18), 2, border_radius=4)
    pygame.draw.rect(surf, SKYBLUE, (x+18, y+3,  20, 12), border_radius=2)
    pygame.draw.rect(surf, SKYBLUE, (x+42, y+3,  20, 12), border_radius=2)
    for wx in [x+14, x+60]:
        pygame.draw.circle(surf, DKGRAY, (wx, y+40), 14)
        pygame.draw.circle(surf, GRAY,   (wx, y+40), 10)
        pygame.draw.circle(surf, LTGRAY, (wx, y+40), 4)
    pygame.draw.rect(surf, YELLOW, (x+74, y+16, 6, 8), border_radius=2)
    for i in range(3):
        sx = x + 22 + i*16
        pygame.draw.ellipse(surf, (200,0,0), (sx-5, y-5, 10, 6))
        pygame.draw.ellipse(surf, BLACK,     (sx-5, y-5, 10, 6), 1)


# ── Terrain ───────────────────────────────────────────────────────────────────

def generate_terrain(length=3000):
    pts = []
    y = 340
    x = 0
    while x < length:
        pts.append((x, y))
        x += random.randint(20, 40)
        y += random.randint(-20, 22)
        y = max(280, min(410, y))
    return pts


def get_ground_y(terrain, x):
    for i in range(len(terrain)-1):
        x0, y0 = terrain[i]
        x1, y1 = terrain[i+1]
        if x0 <= x <= x1:
            t = (x-x0)/(x1-x0)
            return y0 + t*(y1-y0)
    return 360


def draw_terrain(surf, terrain, offset):
    pts = [(pt[0]-offset, pt[1]) for pt in terrain]
    visible = [(px, py) for px, py in pts if -60 < px < W+60]
    if len(visible) < 2:
        return
    poly = visible + [(visible[-1][0], H), (visible[0][0], H)]
    pygame.draw.polygon(surf, DKGREEN, poly)
    for i in range(len(visible)-1):
        pygame.draw.line(surf, GREEN, visible[i], visible[i+1], 3)


# ── Particle ─────────────────────────────────────────────────────────────────

class Particle:
    def __init__(self, x, y, color):
        self.x = x; self.y = y; self.color = color
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, 0)
        self.life = 1.0

    def update(self):
        self.x += self.vx; self.y += self.vy
        self.vy += 0.2; self.life -= 0.03

    def draw(self, surf):
        alpha = max(0, int(self.life * 255))
        s = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (4, 4), 4)
        surf.blit(s, (int(self.x)-4, int(self.y)-4))


# ── Cloud ─────────────────────────────────────────────────────────────────────

class Cloud:
    def __init__(self, x=None):
        self.x = x if x is not None else W + random.randint(0, 200)
        self.y = random.randint(30, 160)
        self.w = random.randint(60, 110)
        self.speed = random.uniform(0.4, 0.9)

    def update(self):
        self.x -= self.speed
        if self.x < -self.w - 20:
            self.x = W + 20
            self.y = random.randint(30, 160)

    def draw(self, surf):
        s = pygame.Surface((self.w+20, 60), pygame.SRCALPHA)
        c = (255, 255, 255, 200)
        pygame.draw.ellipse(s, c, (0, 20, self.w, 32))
        pygame.draw.ellipse(s, c, (self.w//4, 4, self.w//2, 30))
        pygame.draw.ellipse(s, c, (self.w//8, 12, self.w//3, 26))
        surf.blit(s, (int(self.x), int(self.y)))


# ── Stage definitions ─────────────────────────────────────────────────────────

STAGES = [
    {"name": "Legoland Run",     "desc": "SPACE/UP=jump to top route  |  SHIFT=drop to bottom route",  "type": "run",   "souvenir": "Lego Minifig"},
    {"name": "Memory Waters",    "desc": "Avoid trash, fish & jellyfish! [SPACE/UP=boost up]",          "type": "water", "souvenir": "Pearl Shell"},
    {"name": "Road of Memories", "desc": "Hold SPACE to accelerate — don't flip or fall!",             "type": "car",   "souvenir": "Photo Frame"},
    {"name": "Sky of Souvenirs", "desc": "Flap the plane through 15 pipes! [SPACE/UP=flap]",           "type": "fly",   "souvenir": "Golden Wings"},
]

# Stage 1 coin quotas — must collect this many from EACH route
TOP_COIN_QUOTA    = 10
BOTTOM_COIN_QUOTA = 10
COIN_GOAL         = TOP_COIN_QUOTA + BOTTOM_COIN_QUOTA   # 20 total

PIPE_GOAL  = 15
WATER_GOAL = 100
CAR_GOAL   = 2200

# Platform Y positions (feet of player land here)
PLATFORM_TOP_Y    = 290   # upper platform surface
PLATFORM_BOTTOM_Y = 370   # lower platform / ground surface


# ── Main Game ─────────────────────────────────────────────────────────────────

class Game:
    def __init__(self):
        self.state     = "title"
        self.stage_idx = 0
        self.collected = []
        self.particles = []
        self.clouds    = [Cloud(random.randint(0, W)) for _ in range(6)]
        self.frame     = 0

        # Load custom plane image (pre-flipped, background removed, sized at 100px wide)
        import os
        plane_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plane.png")
        raw = pygame.image.load(plane_path).convert_alpha()
        plane_width = 50
        pw, ph = raw.get_size()
        self.plane_img = pygame.transform.smoothscale(raw, (plane_width, int(ph * plane_width / pw)))

        self.reset_stage()

    def reset_stage(self):
        t = STAGES[self.stage_idx]["type"]
        self.obstacles       = []
        self.particles       = []
        self.coins           = []
        self.frame           = 0
        self.score           = 0.0
        self.coins_collected = 0
        self.pipes_passed    = 0

        if t == "run":
            self.px, self.py = 100, PLATFORM_BOTTOM_Y - 44
            self.pvy = 0
            self.on_ground  = True
            self.on_top     = False   # True when standing on upper platform
            self.drop_timer = 0       # frames remaining where top platform is ignored
            # Per-route coin quotas
            self.top_coins_collected    = 0
            self.bottom_coins_collected = 0
            self._spawn_run_section(0)

        elif t == "water":
            self.px, self.py = 100, 220
            self.pvy = 0

        elif t == "car":
            self.terrain        = generate_terrain()
            self.terrain_offset = 0.0
            self.car_speed      = 0.0
            self.px, self.py    = 80, 280
            self.pvy            = 0.0
            self.car_angle      = 0.0
            self.flip_timer     = 0

        elif t == "fly":
            self.px, self.py = 120, 220
            self.pvy = 0

    # ── Stage 1 coin/route spawning ────────────────────────────────────────
    def _spawn_run_section(self, start_x):
        """
        Spawn coins alternating on top and bottom routes so both quotas
        can be filled.  Each section adds coins to whichever route needs
        more to keep the world balanced.
        """
        x = start_x + W
        for _ in range(8):
            x += random.randint(90, 130)

            # Decide route: bias toward whichever quota is less filled
            top_pct    = self.top_coins_collected    / TOP_COIN_QUOTA
            bottom_pct = self.bottom_coins_collected / BOTTOM_COIN_QUOTA

            # Count pending (already spawned but uncollected) coins per route
            pending_top    = sum(1 for c in self.coins if not c["collected"] and c["route"] == "top")
            pending_bottom = sum(1 for c in self.coins if not c["collected"] and c["route"] == "bottom")

            # Effective fill = collected + pending
            eff_top    = (self.top_coins_collected    + pending_top)    / TOP_COIN_QUOTA
            eff_bottom = (self.bottom_coins_collected + pending_bottom) / BOTTOM_COIN_QUOTA

            if eff_top <= eff_bottom:
                route = "top"
            else:
                route = "bottom"

            cy = PLATFORM_TOP_Y - 20 if route == "top" else PLATFORM_BOTTOM_Y - 20

            self.coins.append({
                "x":         x,
                "y":         cy,
                "route":     route,
                "collected": False
            })

            # Obstacles only on the same route, slightly offset
            if random.random() < 0.35:
                oy = (PLATFORM_TOP_Y - random.randint(28, 46)) if route == "top" else (PLATFORM_BOTTOM_Y - random.randint(28, 46))
                self.obstacles.append({
                    "x":     x + 55,
                    "y":     oy,
                    "w":     28,
                    "h":     random.randint(28, 46),
                    "color": BROWN
                })

    # ── Events ─────────────────────────────────────────────────────────────
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "title":
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.state = "playing"; self.reset_stage()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

            elif self.state == "playing":
                t = STAGES[self.stage_idx]["type"]
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if t == "run" and self.on_ground:
                        self.pvy = -13; self.on_ground = False
                    elif t == "water":
                        self.pvy = -8
                    elif t == "fly":
                        self.pvy = -8

                # SHIFT = drop to lower route
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    if t == "run" and self.on_top:
                        # Burst downward; suppress upper-platform landing for 25 frames
                        self.pvy        = 10
                        self.on_ground  = False
                        self.on_top     = False
                        self.drop_timer = 25

            elif self.state in ("souvenir", "gameover", "win"):
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.proceed()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == "title":
                mx, my = event.pos
                if 300 <= mx <= 500 and 200 <= my <= 260:
                    self.state = "playing"; self.reset_stage()
                elif 300 <= mx <= 500 and 280 <= my <= 340:
                    pygame.quit(); sys.exit()
            elif self.state in ("souvenir", "gameover", "win"):
                self.proceed()

    def proceed(self):
        if self.state == "gameover":
            self.reset_stage(); self.state = "playing"
        elif self.state == "souvenir":
            self.stage_idx += 1
            if self.stage_idx >= len(STAGES):
                self.state = "win"
            else:
                self.reset_stage(); self.state = "playing"
        elif self.state == "win":
            self.stage_idx = 0; self.collected = []
            self.reset_stage(); self.state = "title"

    # ── Update ─────────────────────────────────────────────────────────────
    def update(self):
        for c in self.clouds: c.update()
        for p in self.particles: p.update()
        self.particles = [p for p in self.particles if p.life > 0]
        if self.state != "playing":
            return
        self.frame += 1
        t = STAGES[self.stage_idx]["type"]
        keys = pygame.key.get_pressed()
        if   t == "run":   self.update_run(keys)
        elif t == "water": self.update_water(keys)
        elif t == "car":   self.update_car(keys)
        elif t == "fly":   self.update_fly(keys)

    # ── Stage 1: Two-route runner with per-route coin quotas ──────────────
    def update_run(self, keys):
        SPEED = 5

        # Tick drop cooldown
        if self.drop_timer > 0:
            self.drop_timer -= 1

        self.pvy += 0.6
        self.py  += self.pvy

        player_feet = self.py + 44
        player_rect = pygame.Rect(self.px + 4, self.py + 4, 28, 36)

        # ── Platform collision ────────────────────────────────────────────
        landed_top    = False
        landed_bottom = False

        if self.pvy > 0:
            # Upper platform: land only when drop_timer has expired
            if (self.drop_timer == 0 and
                    player_feet >= PLATFORM_TOP_Y and
                    player_feet <= PLATFORM_TOP_Y + 18):
                self.py  = PLATFORM_TOP_Y - 44
                self.pvy = 0
                self.on_ground = True
                self.on_top    = True
                landed_top     = True

            # Bottom platform
            if (not landed_top and
                    player_feet >= PLATFORM_BOTTOM_Y):
                self.py  = PLATFORM_BOTTOM_Y - 44
                self.pvy = 0
                self.on_ground = True
                self.on_top    = False
                landed_bottom  = True

        # If standing on top platform and walking off the edge: start falling
        if self.on_top and not landed_top and self.pvy > 0.5:
            self.on_ground = False
            self.on_top    = False

        # Fell off screen
        if self.py > H + 60:
            self.trigger_gameover(); return

        # ── Scroll obstacles & coins ──────────────────────────────────────
        for o in self.obstacles: o["x"] -= SPEED
        for coin in self.coins:  coin["x"] -= SPEED
        self.obstacles = [o for o in self.obstacles if o["x"] > -60]
        self.coins     = [c for c in self.coins if c["x"] > -30]

        # Spawn more when world runs thin
        rightmost = max((c["x"] for c in self.coins), default=0)
        if rightmost < W + 200:
            self._spawn_run_section(rightmost - W)

        # ── Coin collection ───────────────────────────────────────────────
        for coin in self.coins:
            if not coin["collected"]:
                cr = pygame.Rect(coin["x"] - 10, coin["y"] - 10, 20, 20)
                if player_rect.colliderect(cr):
                    coin["collected"] = True
                    self.coins_collected += 1
                    if coin["route"] == "top":
                        self.top_coins_collected    = min(self.top_coins_collected + 1,    TOP_COIN_QUOTA)
                    else:
                        self.bottom_coins_collected = min(self.bottom_coins_collected + 1, BOTTOM_COIN_QUOTA)
                    for _ in range(8):
                        self.particles.append(Particle(coin["x"], coin["y"], GOLD))

        # ── Obstacle collision ────────────────────────────────────────────
        for o in self.obstacles:
            if player_rect.colliderect(pygame.Rect(o["x"] + 3, o["y"] + 3, o["w"] - 6, o["h"] - 6)):
                self.trigger_gameover(); return

        # ── Completion: both quotas must be full ──────────────────────────
        if (self.top_coins_collected    >= TOP_COIN_QUOTA and
                self.bottom_coins_collected >= BOTTOM_COIN_QUOTA):
            self._stage_complete()

    # ── Stage 2: Jetpack joyride underwater — avoid obstacles ─────────────
    def update_water(self, keys):
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.pvy -= 0.55
        self.pvy += 0.22
        self.pvy *= 0.97
        self.py  += self.pvy

        WATER_TOP    = 80
        WATER_BOTTOM = H - 60

        if self.frame % 80 == 0:
            kind = random.choice(["trash", "fish", "jelly"])
            self.obstacles.append({
                "x":    W + 20,
                "y":    random.randint(WATER_TOP + 30, WATER_BOTTOM - 30),
                "kind": kind,
                "r":    22 if kind == "jelly" else 18,
                "vy":   random.uniform(-0.8, 0.8)
            })

        for o in self.obstacles:
            o["x"] -= 4
            o["y"] += o.get("vy", 0)
            if o["y"] < WATER_TOP + 15 or o["y"] > WATER_BOTTOM - 15:
                o["vy"] = -o.get("vy", 0)
        self.obstacles = [o for o in self.obstacles if o["x"] > -50]

        self.score += 0.5

        for o in self.obstacles:
            dx = self.px - o["x"]
            dy = self.py - o["y"]
            if math.sqrt(dx*dx + dy*dy) < o["r"] + 16:
                self.trigger_gameover(); return

        if self.py > WATER_BOTTOM - 10 or self.py < WATER_TOP + 10:
            self.trigger_gameover(); return

        if self.score >= WATER_GOAL:
            self._stage_complete()

    # ── Stage 3: Hill Climb — hold SPACE to accelerate ────────────────────
    def update_car(self, keys):
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.car_speed = min(self.car_speed + 0.15, 7.0)
        else:
            self.car_speed = max(self.car_speed - 0.06, 0.0)

        self.terrain_offset += self.car_speed
        self.pvy += 0.55
        self.py  += self.pvy

        mid_x    = self.px + 40 + self.terrain_offset
        ground_y = get_ground_y(self.terrain, mid_x)

        if self.py + 54 >= ground_y:
            self.py = ground_y - 54; self.pvy = 0

        g1 = get_ground_y(self.terrain, self.px +  0 + self.terrain_offset)
        g2 = get_ground_y(self.terrain, self.px + 80 + self.terrain_offset)
        self.car_angle = math.atan2(g2 - g1, 80)

        if abs(self.car_angle) > 1.1:
            self.flip_timer += 1
        else:
            self.flip_timer = max(0, self.flip_timer - 1)

        if self.flip_timer > 30:
            self.trigger_gameover(); return

        if self.py > H + 80:
            self.trigger_gameover(); return

        if self.terrain_offset >= CAR_GOAL:
            self._stage_complete()

    # ── Stage 4: Flappy Bird plane through pipes ──────────────────────────
    def update_fly(self, keys):
        self.pvy += 0.38
        self.py  += self.pvy

        if self.frame % 120 == 0:
            gap   = 170
            gap_y = random.randint(130, 340)
            self.obstacles.append({
                "x":       W + 10,
                "gap_top": gap_y - gap//2,
                "gap_bot": gap_y + gap//2,
                "passed":  False
            })

        for o in self.obstacles:
            o["x"] -= 4
            if not o["passed"] and o["x"] < self.px - 20:
                o["passed"] = True
                self.pipes_passed += 1
                for _ in range(6):
                    self.particles.append(Particle(self.px, self.py, GOLD))
        self.obstacles = [o for o in self.obstacles if o["x"] > -80]

        pr = pygame.Rect(self.px-28, self.py-10, 56, 20)
        for o in self.obstacles:
            cx = int(o["x"])
            if pr.colliderect(pygame.Rect(cx-30, 0, 60, o["gap_top"])):
                self.trigger_gameover(); return
            if pr.colliderect(pygame.Rect(cx-30, o["gap_bot"], 60, H - o["gap_bot"])):
                self.trigger_gameover(); return

        if self.py > H - 60 or self.py < 10:
            self.trigger_gameover(); return

        if self.pipes_passed >= PIPE_GOAL:
            self._stage_complete()

    def _stage_complete(self):
        self.collected.append(STAGES[self.stage_idx]["souvenir"])
        for _ in range(25):
            self.particles.append(Particle(self.px, self.py, GOLD))
        self.state = "souvenir"

    def trigger_gameover(self):
        for _ in range(15):
            self.particles.append(Particle(self.px, self.py, RED))
        self.state = "gameover"

    # ── Draw ───────────────────────────────────────────────────────────────
    def draw(self):
        screen.fill(DKGRAY)
        if   self.state == "title":    self.draw_title()
        elif self.state == "playing":  self.draw_stage()
        elif self.state == "souvenir": self.draw_souvenir()
        elif self.state == "gameover":
            self.draw_stage(); self.draw_gameover_overlay()
        elif self.state == "win":      self.draw_win()
        pygame.display.flip()

    # ── Title ──────────────────────────────────────────────────────────────
    def draw_title(self):
        screen.fill((13, 13, 31))
        random.seed(42)
        for _ in range(60):
            rx, ry = random.randint(0, W), random.randint(0, H)
            pygame.draw.circle(screen, (255,255,200), (rx,ry), 1)
        random.seed()
        for c in self.clouds: c.draw(screen)
        draw_text(screen, "LEGO MEMORY QUEST", font_big, RED, W//2, 100, shadow=True)
        draw_text(screen, "A journey through art, bricks & souvenirs", font_xs, OFFWHITE, W//2, 155)
        for label, cy, hcol in [("▶  START GAME", 240, GREEN), ("✕  EXIT", 320, RED)]:
            mx, my = pygame.mouse.get_pos()
            rect   = pygame.Rect(W//2-120, cy-30, 240, 52)
            hover  = rect.collidepoint(mx, my)
            pygame.draw.rect(screen, hcol if hover else (60,60,80), rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
            draw_text(screen, label, font_med, WHITE, W//2, cy)
        draw_text(screen, "Stage 1: SPACE/UP=jump  |  SHIFT=drop to lower route", font_xs, LTGRAY, W//2, 390)
        draw_text(screen, "Collect coins on BOTH routes to complete Stage 1!", font_xs, GOLD, W//2, 412)
        draw_text(screen, "SPACE / UP to boost, accelerate or flap in later stages", font_xs, LTGRAY, W//2, 434)
        if self.collected:
            draw_text(screen, "Souvenirs: " + "  ★  ".join(self.collected), font_xs, GOLD, W//2, 458)

    # ── Stage router ───────────────────────────────────────────────────────
    def draw_stage(self):
        t = STAGES[self.stage_idx]["type"]
        if   t == "run":   self.draw_run()
        elif t == "water": self.draw_water()
        elif t == "car":   self.draw_car_stage()
        elif t == "fly":   self.draw_fly()
        for p in self.particles: p.draw(screen)
        self.draw_hud()

    # ── Stage 1 draw ───────────────────────────────────────────────────────
    def draw_run(self):
        screen.fill(SKYBLUE)
        pygame.draw.circle(screen, YELLOW, (700, 70), 38)
        for c in self.clouds: c.draw(screen)

        # ── Upper platform ────────────────────────────────────────────────
        # Tinted blue to distinguish it as the "top route"
        pygame.draw.rect(screen, (60, 160, 60),  (0, PLATFORM_TOP_Y,    W, 20))
        pygame.draw.rect(screen, DKGREEN,         (0, PLATFORM_TOP_Y,    W, 4))

        # ── Lower platform / ground ───────────────────────────────────────
        pygame.draw.rect(screen, GREEN,   (0, PLATFORM_BOTTOM_Y, W, H - PLATFORM_BOTTOM_Y))
        pygame.draw.rect(screen, DKGREEN, (0, PLATFORM_BOTTOM_Y, W, 4))

        # ── Route labels (faint, on the platforms) ────────────────────────
        lbl_top = font_xs.render("▲ TOP ROUTE  (SPACE to jump up)", True, (180, 255, 180))
        screen.blit(lbl_top, (8, PLATFORM_TOP_Y + 5))
        lbl_bot = font_xs.render("▼ BOTTOM ROUTE  (SHIFT to drop down)", True, (180, 255, 180))
        screen.blit(lbl_bot, (8, PLATFORM_BOTTOM_Y + 5))

        # ── Coins ─────────────────────────────────────────────────────────
        for coin in self.coins:
            if not coin["collected"]:
                cx, cy = int(coin["x"]), int(coin["y"])
                # Top-route coins: gold.  Bottom-route coins: pink-gold tint
                inner = YELLOW if coin["route"] == "top" else PINK
                pygame.draw.circle(screen, GOLD,  (cx, cy), 10)
                pygame.draw.circle(screen, inner, (cx, cy), 7)
                pygame.draw.circle(screen, WHITE, (cx-3, cy-3), 3)
                pygame.draw.circle(screen, BLACK, (cx, cy), 10, 2)

        # ── Obstacles ─────────────────────────────────────────────────────
        for o in self.obstacles:
            draw_lego_brick(screen, o["x"], o["y"], o["w"], o["h"], o["color"])

        # ── Player ────────────────────────────────────────────────────────
        draw_lego_figure(screen, int(self.px) + 18, int(self.py) + 44)

    # ── Stage 2 draw ───────────────────────────────────────────────────────
    def draw_water(self):
        pygame.draw.rect(screen, SKYBLUE,      (0, 0,  W, 80))
        pygame.draw.rect(screen, (0, 60, 120), (0, 80, W, H-60-80))
        for i in range(5):
            s = pygame.Surface((W, 30), pygame.SRCALPHA)
            s.fill((0, 120, 200, 25))
            screen.blit(s, (0, 80 + i*70 + (self.frame*2 + i*30) % 70 - 35))
        pygame.draw.rect(screen, (90,60,30),   (0, H-60, W, 60))
        pygame.draw.rect(screen, (110,80,40),  (0, H-60, W, 8))
        for i in range(0, W, 50):
            bx = (i + self.frame*2) % (W+50) - 50
            pygame.draw.ellipse(screen, SAND, (bx, H-64, 35, 10))
        pygame.draw.rect(screen, CYAN, (0, 78, W, 6))

        for o in self.obstacles:
            ox, oy = int(o["x"]), int(o["y"])
            if o["kind"] == "trash":
                pygame.draw.rect(screen, (50,50,50),    (ox-14, oy-20, 28, 40), border_radius=4)
                pygame.draw.rect(screen, (80,80,80),    (ox-14, oy-20, 28, 40), 2, border_radius=4)
                pygame.draw.rect(screen, (30,30,30),    (ox-16, oy-22, 32, 8),  border_radius=3)
                pygame.draw.line(screen, (100,100,100), (ox-6, oy-20), (ox-6, oy+18), 2)
                pygame.draw.line(screen, (100,100,100), (ox+6, oy-20), (ox+6, oy+18), 2)
            elif o["kind"] == "fish":
                pygame.draw.ellipse(screen, ORANGE, (ox-20, oy-10, 40, 20))
                pts = [(ox-20, oy), (ox-34, oy-10), (ox-34, oy+10)]
                pygame.draw.polygon(screen, ORANGE, pts)
                pygame.draw.circle(screen, BLACK, (ox+10, oy-3), 4)
                pygame.draw.circle(screen, WHITE, (ox+11, oy-4), 1)
            elif o["kind"] == "jelly":
                pygame.draw.ellipse(screen, (180,100,220), (ox-18, oy-18, 36, 28))
                for j in range(4):
                    tx  = ox - 12 + j*8
                    wave = int(math.sin(self.frame*0.1 + j) * 5)
                    pygame.draw.line(screen, (200,140,255), (tx, oy+10), (tx, oy+28+wave), 2)

        px, py = int(self.px), int(self.py)
        pygame.draw.ellipse(screen, YELLOW, (px-10, py-18, 20, 20))
        pygame.draw.rect(screen,   BLUE,    (px-12, py+2,  24, 18), border_radius=3)
        pygame.draw.ellipse(screen, GREEN,  (px-20, py+16, 18, 8))
        pygame.draw.ellipse(screen, GREEN,  (px+2,  py+16, 18, 8))
        if self.frame % 15 == 0:
            self.particles.append(Particle(px+8, py-18, (180,220,255)))

    # ── Stage 3 draw ───────────────────────────────────────────────────────
    def draw_car_stage(self):
        screen.fill(SKYBLUE)
        for c in self.clouds: c.draw(screen)
        pygame.draw.circle(screen, YELLOW, (100, 70), 44)

        draw_terrain(screen, self.terrain, int(self.terrain_offset))

        water_surf = pygame.Surface((W, 60), pygame.SRCALPHA)
        water_surf.fill((0, 80, 180, 160))
        screen.blit(water_surf, (0, H-60))
        pygame.draw.rect(screen, CYAN, (0, H-62, W, 4))

        spd  = font_xs.render(f"Speed: {self.car_speed:.1f}", True, WHITE)
        screen.blit(spd, (W-130, H-30))
        if self.car_speed < 0.5:
            tip, tc = "Hold SPACE to go!", GREEN
        elif self.car_speed > 5.5:
            tip, tc = "Too fast — ease off!", RED
        else:
            tip, tc = "Good speed!", GREEN
        screen.blit(font_xs.render(tip, True, tc), (W-180, H-50))

        if self.flip_timer > 10:
            draw_text(screen, "Too steep! SLOW DOWN!", font_med, RED, W//2, 60, shadow=True)

        cx, cy = int(self.px), int(self.py)
        tmp = pygame.Surface((90, 60), pygame.SRCALPHA)
        _draw_car_base(tmp, 0, 0)
        rotated = pygame.transform.rotate(tmp, -math.degrees(self.car_angle))
        rr = rotated.get_rect(center=(cx+40, cy+27))
        screen.blit(rotated, rr.topleft)

    # ── Stage 4 draw ───────────────────────────────────────────────────────
    def draw_fly(self):
        screen.fill((100, 180, 240))
        pygame.draw.rect(screen, (80,160,220), (0, 0, W, H//2))
        pygame.draw.circle(screen, YELLOW, (680, 60), 44)
        for c in self.clouds: c.draw(screen)

        pygame.draw.rect(screen, DKGREEN, (0, H-55, W, 55))
        pygame.draw.rect(screen, GREEN,   (0, H-55, W, 10))
        for i in range(0, W+80, 80):
            tx = (i - self.frame*3) % (W+80)
            pygame.draw.rect(screen, BROWN,   (tx-5,  H-55, 10, 20))
            pygame.draw.circle(screen, GREEN, (tx, H-65), 18)

        for o in self.obstacles:
            cx = int(o["x"])
            bot_h = H - 55 - o["gap_bot"]
            pygame.draw.rect(screen, (34,139,34), (cx-30, o["gap_bot"], 60, bot_h))
            pygame.draw.rect(screen, DKGREEN,     (cx-30, o["gap_bot"], 60, bot_h), 2)
            pygame.draw.rect(screen, GREEN,       (cx-36, o["gap_bot"]-16, 72, 16), border_radius=4)
            pygame.draw.rect(screen, (34,139,34), (cx-30, 0, 60, o["gap_top"]))
            pygame.draw.rect(screen, DKGREEN,     (cx-30, 0, 60, o["gap_top"]), 2)
            pygame.draw.rect(screen, GREEN,       (cx-36, o["gap_top"], 72, 16), border_radius=4)

        # Draw custom plane image centred on player position
        img = self.plane_img
        iw, ih = img.get_size()
        screen.blit(img, (int(self.px) - iw // 2, int(self.py) - ih // 2))
        draw_text(screen, f"Pipes: {self.pipes_passed}/{PIPE_GOAL}", font_sm, WHITE, W-90, 22, shadow=True)

    # ── HUD ────────────────────────────────────────────────────────────────
    def draw_hud(self):
        t = STAGES[self.stage_idx]["type"]

        if t == "run":
            # Wider HUD panel for two-route quota display
            bar = pygame.Surface((300, 80), pygame.SRCALPHA)
            bar.fill((0, 0, 0, 150))
            screen.blit(bar, (8, 8))

            # Top-route quota
            top_done = self.top_coins_collected >= TOP_COIN_QUOTA
            top_col  = GREEN if top_done else GOLD
            draw_text(screen, f"▲ Top:    {self.top_coins_collected}/{TOP_COIN_QUOTA}", font_sm, top_col, 110, 24)

            # Bottom-route quota
            bot_done = self.bottom_coins_collected >= BOTTOM_COIN_QUOTA
            bot_col  = GREEN if bot_done else PINK
            draw_text(screen, f"▼ Bottom: {self.bottom_coins_collected}/{BOTTOM_COIN_QUOTA}", font_sm, bot_col, 110, 46)

            # Progress bar = overall fraction
            prog = min(1.0, (self.top_coins_collected + self.bottom_coins_collected) / COIN_GOAL)
            pygame.draw.rect(screen, DKGRAY, (8, 64, 300, 10), border_radius=5)
            pygame.draw.rect(screen, GOLD,   (8, 64, int(300*prog), 10), border_radius=5)

        else:
            bar = pygame.Surface((240, 44), pygame.SRCALPHA)
            bar.fill((0, 0, 0, 140))
            screen.blit(bar, (8, 8))

            if t == "water":
                prog = min(1.0, self.score / WATER_GOAL)
                draw_text(screen, f"Score: {int(self.score)}/{WATER_GOAL}", font_sm, WHITE, 130, 22)
            elif t == "car":
                prog = min(1.0, self.terrain_offset / CAR_GOAL)
                draw_text(screen, f"Dist: {int(self.terrain_offset)}/{CAR_GOAL}", font_sm, WHITE, 130, 22)
            elif t == "fly":
                prog = min(1.0, self.pipes_passed / PIPE_GOAL)

            pygame.draw.rect(screen, DKGRAY, (8, 54, 240, 10), border_radius=5)
            pygame.draw.rect(screen, GOLD,   (8, 54, int(240*prog), 10), border_radius=5)

        draw_text(screen, f"Stage {self.stage_idx+1}/4", font_xs, YELLOW, 26, 76 if t == "run" else 68)
        draw_text(screen, STAGES[self.stage_idx]["name"], font_xs, WHITE,    W//2, 14, shadow=True)
        draw_text(screen, STAGES[self.stage_idx]["desc"], font_xs, OFFWHITE, W//2, 30)

        for i, _ in enumerate(self.collected):
            draw_text(screen, "★", font_sm, GOLD, W-30-i*28, 22)

    # ── Souvenir screen ────────────────────────────────────────────────────
    def draw_souvenir(self):
        screen.fill((13, 13, 40))
        random.seed(99)
        for _ in range(80):
            rx, ry = random.randint(0, W), random.randint(0, H)
            col = random.choice([GOLD, YELLOW, ORANGE, WHITE])
            pygame.draw.circle(screen, col, (rx, ry), 2)
        random.seed()
        for p in self.particles: p.draw(screen)
        glow = pygame.Surface((300, 300), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 220, 0, 30), (150, 150), 150)
        screen.blit(glow, (W//2-150, H//2-150))
        s = STAGES[self.stage_idx-1] if self.stage_idx > 0 else STAGES[-1]
        draw_text(screen, "Memory Collected!", font_big, GOLD,  W//2, 140, shadow=True)
        draw_text(screen, f"You found:  {s['souvenir']}", font_med, WHITE, W//2, 210)
        pygame.draw.rect(screen, (40,40,80), (W//2-80, 250, 160, 70), border_radius=12)
        pygame.draw.rect(screen, GOLD,       (W//2-80, 250, 160, 70), 2,  border_radius=12)
        draw_text(screen, "★", font_big, GOLD, W//2, 282)
        if self.stage_idx < len(STAGES):
            draw_text(screen, f"Stage {self.stage_idx+1} awaits...", font_sm, LTGRAY, W//2, 360)
        draw_text(screen, "[ SPACE or Click to continue ]", font_xs, OFFWHITE, W//2, 420)

    def draw_gameover_overlay(self):
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))
        draw_text(screen, "OOPS!", font_big, RED, W//2, 180, shadow=True)
        draw_text(screen, "You didn't make it this time.", font_med, WHITE, W//2, 260)
        draw_text(screen, "[ SPACE or Click to retry ]", font_sm, GOLD, W//2, 330)

    def draw_win(self):
        screen.fill((10, 10, 30))
        random.seed(77)
        for _ in range(100):
            rx, ry = random.randint(0, W), random.randint(0, H)
            col = random.choice([GOLD, YELLOW, RED, BLUE, GREEN, ORANGE])
            pygame.draw.circle(screen, col, (rx, ry), random.randint(2, 4))
        random.seed()
        for p in self.particles: p.draw(screen)
        draw_text(screen, "QUEST COMPLETE!", font_big, GOLD,    W//2, 110, shadow=True)
        draw_text(screen, "All memories have been collected!", font_sm, WHITE, W//2, 175)
        draw_text(screen, "Your Souvenirs:", font_med, OFFWHITE, W//2, 230)
        for i, name in enumerate(self.collected):
            draw_text(screen, f"  ★  {name}", font_sm, YELLOW, W//2, 270+i*32)
        draw_text(screen, "[ SPACE or Click to return to title ]", font_xs, LTGRAY, W//2, 450)


# ── Run ───────────────────────────────────────────────────────────────────────

def main():
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            game.handle_event(event)
        game.update()
        game.draw()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
