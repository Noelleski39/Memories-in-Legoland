import pygame
import sys
import random
import math
import json
import os

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

W, H = 800, 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Memories in LEGOLAND!")
plane_img = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "plane.png")).convert_alpha()
pygame.mixer.music.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "whileplaying.mp3"))
pygame.mixer.music.set_volume(0.25)
clock = pygame.time.Clock()
FPS = 60

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

font_big = pygame.font.SysFont("impact", 56)
font_med = pygame.font.SysFont("impact", 32)
font_sm  = pygame.font.SysFont("arial",  20)
font_xs  = pygame.font.SysFont("arial",  16)

# ── Leaderboard file (saved next to main.py) ──────────────────────────────────
LEADERBOARD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.json")

def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_to_leaderboard(name, time_ms):
    data = load_leaderboard()
    # Strip out any old-format entries that don't have time_ms
    data = [e for e in data if "time_ms" in e]
    entry = {"name": name, "time_ms": time_ms}
    data.append(entry)
    data.sort(key=lambda e: e["time_ms"])
    save_leaderboard(data)
    for i, e in enumerate(data):
        if e["name"] == name and e["time_ms"] == time_ms:
            return i + 1, data
    return len(data), data

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

def generate_terrain(length=3000):
    pts = []
    y = 340; x = 0
    while x < length:
        pts.append((x, y))
        x += random.randint(20, 40)
        y += random.randint(-20, 22)
        y = max(280, min(410, y))
    return pts

def get_ground_y(terrain, x):
    for i in range(len(terrain)-1):
        x0, y0 = terrain[i]; x1, y1 = terrain[i+1]
        if x0 <= x <= x1:
            t = (x-x0)/(x1-x0)
            return y0 + t*(y1-y0)
    return 360

def draw_terrain(surf, terrain, offset):
    pts = [(pt[0]-offset, pt[1]) for pt in terrain]
    visible = [(px, py) for px, py in pts if -60 < px < W+60]
    if len(visible) < 2: return
    poly = visible + [(visible[-1][0], H), (visible[0][0], H)]
    pygame.draw.polygon(surf, DKGREEN, poly)
    for i in range(len(visible)-1):
        pygame.draw.line(surf, GREEN, visible[i], visible[i+1], 3)

class Particle:
    def __init__(self, x, y, color):
        self.x = x; self.y = y; self.color = color
        self.vx = random.uniform(-3, 3); self.vy = random.uniform(-5, 0); self.life = 1.0
    def update(self):
        self.x += self.vx; self.y += self.vy; self.vy += 0.2; self.life -= 0.03
    def draw(self, surf):
        alpha = max(0, int(self.life * 255))
        s = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (4, 4), 4)
        surf.blit(s, (int(self.x)-4, int(self.y)-4))

class Cloud:
    def __init__(self, x=None):
        self.x = x if x is not None else W + random.randint(0, 200)
        self.y = random.randint(30, 160); self.w = random.randint(60, 110); self.speed = random.uniform(0.4, 0.9)
    def update(self):
        self.x -= self.speed
        if self.x < -self.w - 20: self.x = W + 20; self.y = random.randint(30, 160)
    def draw(self, surf):
        s = pygame.Surface((self.w+20, 60), pygame.SRCALPHA); c = (255,255,255,200)
        pygame.draw.ellipse(s, c, (0, 20, self.w, 32))
        pygame.draw.ellipse(s, c, (self.w//4, 4, self.w//2, 30))
        pygame.draw.ellipse(s, c, (self.w//8, 12, self.w//3, 26))
        surf.blit(s, (int(self.x), int(self.y)))

STAGES = [
    {"name": "Legoland Run", "desc": "Collect 20 coins! Obstacles everywhere — W=jump  S=drop", "type": "run", "souvenir": "Lego Minifig"},    {"name": "Memory Waters", "desc": "Avoid 12 obstacles — dodge trash, fish & jellyfish!", "type": "water", "souvenir": "Pearl Shell"},
    {"name": "Road of Memories", "desc": "Hold D to accelerate — don't flip or fall!",             "type": "car",   "souvenir": "Photo Frame"},
    {"name": "Sky of Souvenirs", "desc": "Press W to flap through 15 pipes!",                      "type": "fly",   "souvenir": "Golden Wings"},
]

COIN_GOAL  = 20
PIPE_GOAL  = 15
WATER_GOAL = 12   # obstacles avoided to win
CAR_GOAL      = 300   # frames spent in sweet spot to win
CAR_SPEED_MIN = 3.0
CAR_SPEED_MAX = 5.5
GROUND_TOP    = 290
GROUND_BOTTOM = 370


class Game:
    def __init__(self):
        self.state        = "title"
        self.stage_idx    = 0
        self.collected    = []
        self.particles    = []
        self.clouds       = [Cloud(random.randint(0, W)) for _ in range(6)]
        self.frame        = 0
        self.player_name  = ""
        self.name_cursor  = 0
        self.lb_data      = []
        self.lb_my_rank   = None
        self.lb_my_name   = ""
        self.lb_my_stages = 0
        self.reset_stage()
        self.run_start_time = pygame.time.get_ticks()  # never resets, runs whole game
    def reset_stage(self):
        t = STAGES[self.stage_idx]["type"]
        self.obstacles = []; self.particles = []; self.coins = []
        self.frame = 0; self.score = 0.0
        self.coins_collected = 0; self.pipes_passed = 0; self.drop_through = False
        if t == "run":
            self.px, self.py = 100, GROUND_TOP - 44
            self.pvy = 0; self.on_ground = True
            self._spawn_run_section(0)
            self.pvy = 0; self.on_ground = True
            self.jumps_left = 2
        elif t == "water":
            self.px, self.py = 100, 220
            self.pvy = 0
            self.obstacles_avoided = 0
        elif t == "car":
            self.terrain = generate_terrain(); self.terrain_offset = 0.0
            self.car_speed = 0.0; self.px, self.py = 80, 280
            self.pvy = 0.0; self.car_angle = 0.0; self.flip_timer = 0
            self.speed_progress = 0 
        elif t == "fly":
                        self.px, self.py = 120, 220; self.pvy = 0
    def _spawn_run_section(self, start_x):
        x = start_x + W
        for _ in range(8):
            x += random.randint(75, 115)
            route = random.choice(["top", "bottom"])
            cy = GROUND_TOP - 20 if route == "top" else GROUND_BOTTOM - 20

            # Count how many obstacles are within 120px — max 2 allowed nearby
            nearby = sum(1 for o in self.obstacles if abs(o["x"] - x) < 120)

            # Only place coin if no obstacle is within 40px
            too_close = any(abs(o["x"] - x) < 40 for o in self.obstacles)
            if not too_close and random.random() < 0.50:
                self.coins.append({"x": x, "y": cy, "collected": False})

            if nearby < 2 and random.random() < 0.55:
                oh = random.randint(28, 46)
                oy = GROUND_TOP - oh if route == "top" else GROUND_BOTTOM - oh
                self.obstacles.append({"x": x + 50, "y": oy, "w": 28, "h": oh, "color": BROWN})
                        
    # ─────────────────────────────────────────────────────────────────────────
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            # Name entry
            if self.state == "name_entry":
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._submit_name()
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.player_name = ""
                elif len(self.player_name) < 16:
                    ch = event.unicode
                    if ch.isprintable() and (ch != " " or self.player_name):
                        self.player_name += ch
                return

            # Leaderboard screens
            if self.state in ("leaderboard_result", "leaderboard_browse"):
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    self._go_to_title()
                return

            # Title
            if self.state == "title":
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.state = "playing"; self.reset_stage()
                    pygame.mixer.music.play(-1)  # -1 loops
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

            # Playing
            elif self.state == "playing":
                if event.key == pygame.K_w:
                    if STAGES[self.stage_idx]["type"] == "fly":
                        self.pvy = -8
                    elif STAGES[self.stage_idx]["type"] == "run" and self.jumps_left > 0:
                        self.pvy = -13; self.on_ground = False; self.jumps_left -= 1

            # Overlays
            elif self.state in ("souvenir", "gameover", "win"):
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.proceed()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if self.state == "title":
                if 300 <= mx <= 500 and 187 <= my <= 237:
                    self.state = "playing"; self.reset_stage()
                    pygame.mixer.music.play(-1)
                elif 300 <= mx <= 500 and 255 <= my <= 305:
                    self.lb_data = load_leaderboard(); self.lb_my_rank = None
                    self.state = "leaderboard_browse"
                elif 300 <= mx <= 500 and 323 <= my <= 373:
                    pygame.quit(); sys.exit()
            elif self.state in ("souvenir", "gameover", "win"):
                self.proceed()
            elif self.state in ("leaderboard_result", "leaderboard_browse"):
                self._go_to_title()

    def _submit_name(self):
        name = self.player_name.strip() or "Anonymous"
        time_ms = self.finish_time - self.run_start_time
        rank, data = add_to_leaderboard(name, time_ms)
        self.lb_data = data
        self.lb_my_rank = rank
        self.lb_my_name = name
        self.lb_my_time = time_ms
        self.state = "leaderboard_result"

    def _go_to_title(self):
        self.stage_idx = 0; self.collected = []; self.player_name = ""
        self.reset_stage(); self.state = "title"
        self.run_start_time = pygame.time.get_ticks()


    def proceed(self):
        if self.state == "gameover":
            self.reset_stage(); self.state = "playing"
        elif self.state == "souvenir":
            self.stage_idx += 1
            if self.stage_idx >= len(STAGES): self.state = "win"
            else: self.reset_stage(); self.state = "playing"
        elif self.state == "win":
            self.finish_time = pygame.time.get_ticks()  # ← ADD this line
            self.player_name = ""; self.state = "name_entry"

    # ─────────────────────────────────────────────────────────────────────────
    def update(self):
        for c in self.clouds: c.update()
        for p in self.particles: p.update()
        self.particles = [p for p in self.particles if p.life > 0]
        self.name_cursor = (self.name_cursor + 1) % 60
        if self.state != "playing": return
        self.frame += 1
        t = STAGES[self.stage_idx]["type"]
        keys = pygame.key.get_pressed()
        if   t == "run":   self.update_run(keys)
        elif t == "water": self.update_water(keys)
        elif t == "car":   self.update_car(keys)
        elif t == "fly":   self.update_fly(keys)

    def update_run(self, keys):
        SPEED = 5
        if keys[pygame.K_s] and self.on_ground and not self.drop_through:
            if self.py + 44 <= GROUND_TOP + 8:
                self.drop_through = True; self.on_ground = False; self.pvy = 10
        self.pvy += 0.9; self.py += self.pvy
        feet = self.py + 44
        if feet >= GROUND_BOTTOM:
            self.py = GROUND_BOTTOM-44; self.pvy = 0; self.on_ground = True; self.drop_through = False; self.jumps_left = 2
        elif feet >= GROUND_TOP and self.pvy > 0 and not self.drop_through:
            self.py = GROUND_TOP-44; self.pvy = 0; self.on_ground = True; self.jumps_left = 2
        if self.py > H+60: self.trigger_gameover(); return
        for o in self.obstacles: o["x"] -= SPEED
        for coin in self.coins:  coin["x"] -= SPEED
        self.obstacles = [o for o in self.obstacles if o["x"] > -60]
        self.coins     = [c for c in self.coins if c["x"] > -30]
        rightmost = max((c["x"] for c in self.coins), default=0)
        if rightmost < W+200: self._spawn_run_section(rightmost-W)
        pr = pygame.Rect(self.px+4, self.py+4, 28, 36)
        for coin in self.coins:
            if not coin["collected"] and pr.colliderect(pygame.Rect(coin["x"]-10, coin["y"]-10, 20, 20)):
                coin["collected"] = True; self.coins_collected += 1
                for _ in range(8): self.particles.append(Particle(coin["x"], coin["y"], GOLD))
        for o in self.obstacles:
            if pr.colliderect(pygame.Rect(o["x"]+3, o["y"]+3, o["w"]-6, o["h"]-6)):
                self.trigger_gameover(); return
        if self.coins_collected >= COIN_GOAL: self._stage_complete()

    def update_water(self, keys):
        if keys[pygame.K_w]: self.pvy -= 0.55
        self.pvy += 0.22; self.pvy *= 0.97; self.py += self.pvy
        WT = 80; WB = H - 60

        if self.frame % 80 == 0:
            kind = random.choice(["trash", "fish", "jelly"])
            self.obstacles.append({
                "x": W + 20, "y": random.randint(WT + 30, WB - 30),
                "kind": kind, "r": 22 if kind == "jelly" else 18,
                "vy": random.uniform(-0.8, 0.8), "passed": False
            })

        for o in self.obstacles:
            o["x"] -= 4
            o["y"] += o.get("vy", 0)
            if o["y"] < WT + 15 or o["y"] > WB - 15: o["vy"] = -o.get("vy", 0)
            if not o.get("passed") and o["x"] < self.px - 20:
                o["passed"] = True
                self.obstacles_avoided += 1
                for _ in range(6): self.particles.append(Particle(self.px, self.py, CYAN))

        self.obstacles = [o for o in self.obstacles if o["x"] > -50]

        for o in self.obstacles:
            if math.hypot(self.px - o["x"], self.py - o["y"]) < o["r"] + 16:
                self.trigger_gameover(); return
        if self.py > WB - 10 or self.py < WT + 10:
            self.trigger_gameover(); return
        if self.obstacles_avoided >= WATER_GOAL:
            self._stage_complete()

    def update_car(self, keys):
        if keys[pygame.K_d]: self.car_speed = min(self.car_speed + 0.15, 7.0)
        else:
            self.car_speed = max(self.car_speed - 0.06, 0.0)

        self.terrain_offset += self.car_speed
        if self.terrain_offset + W + 200 > self.terrain[-1][0]:
            last_x, last_y = self.terrain[-1]
            ext_x = last_x
            for _ in range(100):
                ext_x += random.randint(20, 40)
                last_y += random.randint(-20, 22)
                last_y = max(280, min(410, last_y))
                self.terrain.append((ext_x, last_y))
        self.pvy += 0.55; self.py += self.pvy
        gY = get_ground_y(self.terrain, self.px + 40 + self.terrain_offset)
        if self.py + 54 >= gY: self.py = gY - 54; self.pvy = 0

        g1 = get_ground_y(self.terrain, self.px + self.terrain_offset)
        g2 = get_ground_y(self.terrain, self.px + 80 + self.terrain_offset)
        self.car_angle = math.atan2(g2 - g1, 80)

        if self.py > H + 80: self.trigger_gameover(); return

        in_zone = CAR_SPEED_MIN <= self.car_speed <= CAR_SPEED_MAX
        if in_zone:
            self.speed_progress += 1

        if self.speed_progress >= CAR_GOAL: self._stage_complete()

    def update_fly(self, keys):
        self.pvy+=0.38; self.py+=self.pvy
        if self.frame%120==0:
            gap=170; gap_y=random.randint(130,340)
            self.obstacles.append({"x":W+10,"gap_top":gap_y-gap//2,"gap_bot":gap_y+gap//2,"passed":False})
        for o in self.obstacles:
            o["x"]-=4
            if not o["passed"] and o["x"]<self.px-20:
                o["passed"]=True; self.pipes_passed+=1
                for _ in range(6): self.particles.append(Particle(self.px,self.py,GOLD))
        self.obstacles=[o for o in self.obstacles if o["x"]>-80]
        pr=pygame.Rect(self.px-28,self.py-10,56,20)
        for o in self.obstacles:
            cx=int(o["x"])
            if pr.colliderect(pygame.Rect(cx-30,0,60,o["gap_top"])): self.trigger_gameover(); return
            if pr.colliderect(pygame.Rect(cx-30,o["gap_bot"],60,H-o["gap_bot"])): self.trigger_gameover(); return
        if self.py>H-60 or self.py<10: self.trigger_gameover(); return
        if self.pipes_passed>=PIPE_GOAL: self._stage_complete()

    def _stage_complete(self):
        self.collected.append(STAGES[self.stage_idx]["souvenir"])
        for _ in range(25): self.particles.append(Particle(self.px,self.py,GOLD))
        self.state="souvenir"

    def trigger_gameover(self):
        for _ in range(15): self.particles.append(Particle(self.px,self.py,RED))
        self.state="gameover"

    # ─────────────────────────────────────────────────────────────────────────
    def draw(self):
        screen.fill(DKGRAY)
        if   self.state=="title":              self.draw_title()
        elif self.state=="playing":            self.draw_stage()
        elif self.state=="souvenir":           self.draw_souvenir()
        elif self.state=="gameover":           self.draw_stage(); self.draw_gameover_overlay()
        elif self.state=="win":                self.draw_win()
        elif self.state=="name_entry":         self.draw_name_entry()
        elif self.state=="leaderboard_result": self.draw_leaderboard(result_mode=True)
        elif self.state=="leaderboard_browse": self.draw_leaderboard(result_mode=False)
        pygame.display.flip()

    def draw_title(self):
        screen.fill((13,13,31))
        random.seed(42)
        for _ in range(60):
            rx,ry=random.randint(0,W),random.randint(0,H)
            pygame.draw.circle(screen,(255,255,200),(rx,ry),1)
        random.seed()
        for c in self.clouds: c.draw(screen)
        draw_text(screen,"Memories in LEGOLAND!",font_big,RED,W//2,90,shadow=True)
        draw_text(screen,"A journey through art, bricks & souvenirs",font_xs,OFFWHITE,W//2,148)
        buttons=[("START GAME",215,GREEN),("LEADERBOARD",283,GOLD),("EXIT",351,RED)]
        mx,my=pygame.mouse.get_pos()
        for label,cy,hcol in buttons:
            rect=pygame.Rect(W//2-120,cy-28,240,50)
            hover=rect.collidepoint(mx,my)
            pygame.draw.rect(screen,hcol if hover else (60,60,80),rect,border_radius=10)
            pygame.draw.rect(screen,WHITE,rect,2,border_radius=10)
            draw_text(screen,label,font_med,WHITE,W//2,cy)
        draw_text(screen,"Stage 1: W to Jump & S to Drop    Stage 2: W to Boost",font_xs,LTGRAY,W//2,400)
        draw_text(screen,"Stage 3: D to Accelerate      Stage 4: W to Fly", font_xs,LTGRAY,W//2,418)
        draw_text(screen,"Press ENTER or SPACE to start",font_xs,GOLD,W//2,445)
        if self.collected:
            draw_text(screen,"Souvenirs: "+"  ★  ".join(self.collected),font_xs,GOLD,W//2,470)

    def draw_stage(self):
        t=STAGES[self.stage_idx]["type"]
        if   t=="run":   self.draw_run()
        elif t=="water": self.draw_water()
        elif t=="car":   self.draw_car_stage()
        elif t=="fly":   self.draw_fly()
        for p in self.particles: p.draw(screen)
        self.draw_hud()

    def draw_run(self):
        screen.fill(SKYBLUE)
        pygame.draw.circle(screen,YELLOW,(700,70),38)
        for c in self.clouds: c.draw(screen)
        pygame.draw.rect(screen,GREEN,(0,GROUND_TOP,W,20))
        pygame.draw.rect(screen,DKGREEN,(0,GROUND_TOP,W,4))
        pygame.draw.rect(screen,GREEN,(0,GROUND_BOTTOM,W,H-GROUND_BOTTOM))
        pygame.draw.rect(screen,DKGREEN,(0,GROUND_BOTTOM,W,4))
        feet=self.py+44
        for coin in self.coins:
            if not coin["collected"]:
                cx,cy=int(coin["x"]),int(coin["y"])
                pygame.draw.circle(screen,GOLD,(cx,cy),10)
                pygame.draw.circle(screen,YELLOW,(cx,cy),7)
                pygame.draw.circle(screen,WHITE,(cx-3,cy-3),3)
                pygame.draw.circle(screen,BLACK,(cx,cy),10,2)
        for o in self.obstacles:
            draw_lego_brick(screen,o["x"],o["y"],o["w"],o["h"],o["color"])
        draw_lego_figure(screen,int(self.px)+18,int(self.py)+44)

    def draw_water(self):
        pygame.draw.rect(screen,SKYBLUE,(0,0,W,80))
        pygame.draw.rect(screen,(0,60,120),(0,80,W,H-60-80))
        for i in range(5):
            s=pygame.Surface((W,30),pygame.SRCALPHA); s.fill((0,120,200,25))
            screen.blit(s,(0,80+i*70+(self.frame*2+i*30)%70-35))
        pygame.draw.rect(screen,(90,60,30),(0,H-60,W,60))
        pygame.draw.rect(screen,(110,80,40),(0,H-60,W,8))
        for i in range(0,W,50):
            bx=(i+self.frame*2)%(W+50)-50
            pygame.draw.ellipse(screen,SAND,(bx,H-64,35,10))
        pygame.draw.rect(screen,CYAN,(0,78,W,6))
        for o in self.obstacles:
            ox,oy=int(o["x"]),int(o["y"])
            if o["kind"]=="trash":
                pygame.draw.rect(screen,(50,50,50),(ox-14,oy-20,28,40),border_radius=4)
                pygame.draw.rect(screen,(80,80,80),(ox-14,oy-20,28,40),2,border_radius=4)
                pygame.draw.rect(screen,(30,30,30),(ox-16,oy-22,32,8),border_radius=3)
                pygame.draw.line(screen,(100,100,100),(ox-6,oy-20),(ox-6,oy+18),2)
                pygame.draw.line(screen,(100,100,100),(ox+6,oy-20),(ox+6,oy+18),2)
            elif o["kind"]=="fish":
                pygame.draw.ellipse(screen,ORANGE,(ox-20,oy-10,40,20))
                pygame.draw.polygon(screen,ORANGE,[(ox-20,oy),(ox-34,oy-10),(ox-34,oy+10)])
                pygame.draw.circle(screen,BLACK,(ox+10,oy-3),4)
                pygame.draw.circle(screen,WHITE,(ox+11,oy-4),1)
            elif o["kind"]=="jelly":
                pygame.draw.ellipse(screen,(180,100,220),(ox-18,oy-18,36,28))
                for j in range(4):
                    tx=ox-12+j*8; wave=int(math.sin(self.frame*0.1+j)*5)
                    pygame.draw.line(screen,(200,140,255),(tx,oy+10),(tx,oy+28+wave),2)
        px,py=int(self.px),int(self.py)
        pygame.draw.ellipse(screen,YELLOW,(px-10,py-18,20,20))
        pygame.draw.rect(screen,BLUE,(px-12,py+2,24,18),border_radius=3)
        pygame.draw.ellipse(screen,GREEN,(px-20,py+16,18,8))
        pygame.draw.ellipse(screen,GREEN,(px+2,py+16,18,8))
        if self.frame%15==0: self.particles.append(Particle(px+8,py-18,(180,220,255)))

    def draw_car_stage(self):
        screen.fill(SKYBLUE)
        for c in self.clouds: c.draw(screen)
        pygame.draw.circle(screen,YELLOW,(100,70),44)
        draw_terrain(screen,self.terrain,int(self.terrain_offset))
        ws=pygame.Surface((W,60),pygame.SRCALPHA); ws.fill((0,80,180,160))
        screen.blit(ws,(0,H-60)); pygame.draw.rect(screen,CYAN,(0,H-62,W,4))
        screen.blit(font_xs.render(f"Speed: {self.car_speed:.1f}",True,WHITE),(W-130,H-30))
        if self.car_speed < CAR_SPEED_MIN:   tip,tc="Hold D to reach the zone!",GREEN
        elif self.car_speed > CAR_SPEED_MAX: tip,tc="Ease off — too fast!",RED
        else:                                tip,tc="✓ Sweet spot!",GOLD
        screen.blit(font_xs.render(tip,True,tc),(W-180,H-50))
        cx,cy=int(self.px),int(self.py)
        tmp=pygame.Surface((90,60),pygame.SRCALPHA); _draw_car_base(tmp,0,0)
        rotated=pygame.transform.rotate(tmp,-math.degrees(self.car_angle))
        screen.blit(rotated,rotated.get_rect(center=(cx+40,cy+27)).topleft)

    def draw_fly(self):
        screen.fill((100,180,240))
        pygame.draw.rect(screen,(80,160,220),(0,0,W,H//2))
        pygame.draw.circle(screen,YELLOW,(680,60),44)
        for c in self.clouds: c.draw(screen)
        pygame.draw.rect(screen,DKGREEN,(0,H-55,W,55))
        pygame.draw.rect(screen,GREEN,(0,H-55,W,10))
        for i in range(0,W+80,80):
            tx=(i-self.frame*3)%(W+80)
            pygame.draw.rect(screen,BROWN,(tx-5,H-55,10,20))
            pygame.draw.circle(screen,GREEN,(tx,H-65),18)
        for o in self.obstacles:
                    cx=int(o["x"]); bh=H-55-o["gap_bot"]
                    pygame.draw.rect(screen,(34,139,34),(cx-30,o["gap_bot"],60,bh))
                    pygame.draw.rect(screen,DKGREEN,(cx-30,o["gap_bot"],60,bh),2)
                    pygame.draw.rect(screen,GREEN,(cx-36,o["gap_bot"]-16,72,16),border_radius=4)
                    pygame.draw.rect(screen,(34,139,34),(cx-30,0,60,o["gap_top"]))
                    pygame.draw.rect(screen,DKGREEN,(cx-30,0,60,o["gap_top"]),2)
                    pygame.draw.rect(screen,GREEN,(cx-36,o["gap_top"],72,16),border_radius=4)
        scaled = pygame.transform.smoothscale(plane_img, (120, 75))
        screen.blit(scaled, scaled.get_rect(center=(int(self.px), int(self.py))))

    def draw_hud(self):
        bar=pygame.Surface((240,44),pygame.SRCALPHA); bar.fill((0,0,0,140)); screen.blit(bar,(8,8))
        t=STAGES[self.stage_idx]["type"]
        if t=="run":
            prog=min(1.0,self.coins_collected/COIN_GOAL)
            draw_text(screen,f"Coins: {self.coins_collected}/{COIN_GOAL}",font_sm,GOLD,130,22)
        elif t == "water":
            prog = min(1.0, self.obstacles_avoided / WATER_GOAL)
            draw_text(screen, f"Avoided: {self.obstacles_avoided}/{WATER_GOAL}", font_sm, CYAN, 130, 22)
        elif t == "car":
            prog = min(1.0, self.speed_progress / CAR_GOAL)
            draw_text(screen, f"Cruise: {self.speed_progress}/{CAR_GOAL}", font_sm, WHITE, 130, 22)
        elif t=="fly":
            prog=min(1.0,self.pipes_passed/PIPE_GOAL)
            draw_text(screen,f"Pipes: {self.pipes_passed}/{PIPE_GOAL}",font_sm,WHITE,130,22)
        pygame.draw.rect(screen,DKGRAY,(8,54,240,10),border_radius=5)
        pygame.draw.rect(screen,GOLD,(8,54,int(240*prog),10),border_radius=5)
        draw_text(screen,STAGES[self.stage_idx]["name"],font_xs,WHITE,W//2,14,shadow=True)
        draw_text(screen,STAGES[self.stage_idx]["desc"],font_xs,OFFWHITE,W//2,30)
        draw_text(screen, f"Stage {self.stage_idx+1}/4", font_sm, WHITE, W-70, 22, shadow=True)


    def draw_souvenir(self):
        screen.fill((13,13,40))
        random.seed(99)
        for _ in range(80):
            rx,ry=random.randint(0,W),random.randint(0,H)
            pygame.draw.circle(screen,random.choice([GOLD,YELLOW,ORANGE,WHITE]),(rx,ry),2)
        random.seed()
        for p in self.particles: p.draw(screen)
        glow=pygame.Surface((300,300),pygame.SRCALPHA)
        pygame.draw.circle(glow,(255,220,0,30),(150,150),150)
        screen.blit(glow,(W//2-150,H//2-150))
        s=STAGES[self.stage_idx-1] if self.stage_idx>0 else STAGES[-1]
        draw_text(screen,"Memory Collected!",font_big,GOLD,W//2,140,shadow=True)
        draw_text(screen,f"You found:  {s['souvenir']}",font_med,WHITE,W//2,210)
        pygame.draw.rect(screen,(40,40,80),(W//2-80,250,160,70),border_radius=12)
        pygame.draw.rect(screen,GOLD,(W//2-80,250,160,70),2,border_radius=12)
        draw_text(screen,"★",font_big,GOLD,W//2,282)
        if self.stage_idx<len(STAGES):
            draw_text(screen,f"Stage {self.stage_idx+1} awaits...",font_sm,LTGRAY,W//2,360)
        draw_text(screen,"[ ENTER / SPACE or Click to continue ]",font_xs,OFFWHITE,W//2,420)

    def draw_gameover_overlay(self):
        ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,170)); screen.blit(ov,(0,0))
        draw_text(screen,"OOPS!",font_big,RED,W//2,180,shadow=True)
        draw_text(screen,"You didn't make it this time.",font_med,WHITE,W//2,260)
        draw_text(screen,"[ ENTER / SPACE or Click to retry ]",font_sm,GOLD,W//2,330)

    def draw_win(self):
        screen.fill((10,10,30))
        random.seed(77)
        for _ in range(100):
            rx,ry=random.randint(0,W),random.randint(0,H)
            pygame.draw.circle(screen,random.choice([GOLD,YELLOW,RED,BLUE,GREEN,ORANGE]),(rx,ry),random.randint(2,4))
        random.seed()
        for p in self.particles: p.draw(screen)
        draw_text(screen,"QUEST COMPLETE!",font_big,GOLD,W//2,100,shadow=True)
        draw_text(screen,"All memories collected!",font_sm,WHITE,W//2,160)
        draw_text(screen,"Your Souvenirs:",font_med,OFFWHITE,W//2,205)
        for i,name in enumerate(self.collected):
            draw_text(screen,f"  ★  {name}",font_sm,YELLOW,W//2,245+i*30)
        draw_text(screen,"[ ENTER / SPACE to submit your score ]",font_xs,GOLD,W//2,450)

    # ── Name entry ────────────────────────────────────────────────────────────
    def draw_name_entry(self):
        screen.fill((13,13,40))
        random.seed(42)
        for _ in range(60):
            rx,ry=random.randint(0,W),random.randint(0,H)
            pygame.draw.circle(screen,(255,255,200),(rx,ry),1)
        random.seed()
        draw_text(screen,"QUEST COMPLETE!",font_big,GOLD,W//2,80,shadow=True)
        elapsed = self.finish_time - self.run_start_time
        mm = elapsed // 60000
        ss = (elapsed // 1000) % 60
        cs = (elapsed // 10) % 100
        draw_text(screen, f"Your time:  {mm:02d}:{ss:02d}.{cs:02d}", font_med, GOLD, W//2, 135)
        draw_text(screen, "Enter your name for the leaderboard:", font_sm, OFFWHITE, W//2, 200)        # Input box
        box=pygame.Rect(W//2-160,308,320,44)
        pygame.draw.rect(screen,(30,30,60),box,border_radius=8)
        pygame.draw.rect(screen,GOLD,box,2,border_radius=8)
        display=self.player_name+("│" if self.name_cursor<30 else " ")
        screen.blit(font_med.render(display,True,WHITE),font_med.render(display,True,WHITE).get_rect(center=(W//2,330)))
        draw_text(screen,"Press ENTER or SPACE to confirm  |  max 16 chars",font_xs,LTGRAY,W//2,372)

    # ── Leaderboard (shared: result after game + browse from title) ───────────
    def draw_leaderboard(self, result_mode=False):
        screen.fill((10,10,30))
        random.seed(55)
        for _ in range(80):
            rx,ry=random.randint(0,W),random.randint(0,H)
            pygame.draw.circle(screen,(255,255,200),(rx,ry),1)
        random.seed()

        draw_text(screen,"LEADERBOARD",font_big,GOLD,W//2,44,shadow=True)

        if result_mode and self.lb_my_rank:
            mm = self.lb_my_time // 60000
            ss = (self.lb_my_time // 1000) % 60
            cs = (self.lb_my_time // 10) % 100
            draw_text(screen, f"You ranked #{self.lb_my_rank}  —  {mm:02d}:{ss:02d}.{cs:02d}", font_sm, CYAN, W//2, 88)

        hy = 112
        pygame.draw.line(screen, GOLD, (50, hy+20), (W-50, hy+20), 1)
        draw_text(screen, "RANK", font_xs, LTGRAY, 90,  hy)
        draw_text(screen, "NAME", font_xs, LTGRAY, 300, hy)
        draw_text(screen, "TIME", font_xs, LTGRAY, 580, hy)

        data = self.lb_data
        if not data:
            draw_text(screen, "No scores yet — be the first!", font_sm, LTGRAY, W//2, 260)
        else:
            medals = {1:"#1", 2:"#2", 3:"#3"}
            rank_colors = {1:GOLD, 2:LTGRAY, 3:ORANGE}
            for i, entry in enumerate(data[:9]):
                ry2 = 142 + i*34
                t_ms = entry.get("time_ms", 0)
                mm = t_ms // 60000
                ss = (t_ms // 1000) % 60
                cs = (t_ms // 10) % 100
                time_str = f"{mm:02d}:{ss:02d}.{cs:02d}"
                is_me = (result_mode
                        and self.lb_my_rank == i+1
                        and entry.get("name") == self.lb_my_name
                        and entry.get("time_ms") == self.lb_my_time)
                if is_me:
                    hi = pygame.Surface((W-100, 28), pygame.SRCALPHA)
                    hi.fill((255,200,0,45))
                    screen.blit(hi, (50, ry2-12))
                    pygame.draw.rect(screen, GOLD, (50, ry2-12, W-100, 28), 1, border_radius=3)
                rank_txt = medals.get(i+1, f"#{i+1}")
                rc = rank_colors.get(i+1, WHITE)
                nc = GOLD if is_me else WHITE
                draw_text(screen, rank_txt,               font_sm, rc,     90,  ry2)
                draw_text(screen, entry.get("name", "?"), font_sm, nc,    300,  ry2)
                draw_text(screen, time_str,               font_sm, YELLOW, 580, ry2)
            if len(data) > 9:
                draw_text(screen, f"... and {len(data)-9} more", font_xs, LTGRAY, W//2, 452)

        draw_text(screen,"[ ENTER / SPACE / ESC  —  back ]",font_xs,OFFWHITE,W//2,478)
def main():
    game=Game()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); sys.exit()
            game.handle_event(event)
        game.update()
        game.draw()
        clock.tick(FPS)

if __name__=="__main__":
    main()