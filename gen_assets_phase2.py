"""Phase 2 assets: menu icons (chest, coin, diamond, play/map/upgrade buttons)
and space background with Mars + distant planet, soft grayish star particles."""
from PIL import Image
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)


def build(name, grid, palette, scale=8):
    h = len(grid)
    w = len(grid[0])
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != ".":
                px[x, y] = palette[c]
    img = img.resize((w * scale, h * scale), Image.NEAREST)
    img.save(os.path.join(OUT, f"{name}.png"))
    print(f"saved {name}.png -> {img.size}")


# ---- chest (square canvas so it doesn't stretch in equal square buttons) ----
chest = [
    "................",
    "................",
    "....WWWWWW......",
    "..WWyyyyyyWW....",
    ".WyyyyyyyyyyW...",
    "WyyyyyyyyyyyyW..",
    "BBBBBBBBBBBBBBW.",
    "BBBBBGGGGBBBBBW.",
    "BBBBBGGGGBBBBBW.",
    "BBBBBBBBBBBBBBW.",
    "BBBBBBBBBBBBBBW.",
    ".WWWWWWWWWWWWW..",
    "................",
    "................",
    "................",
    "................",
]
build("chest", chest, {"W": (120, 80, 40, 255), "y": (230, 190, 60, 255),
                        "B": (150, 105, 55, 255), "G": (255, 215, 60, 255)}, scale=8)

# ---- gold coin ----
coin = [
    "..yyyy....", ".yYYYYy...", "yYYyyYYy..", "yYyggyYy..", "yYyggyYy..",
    "yYYyyYYy..", ".yYYYYy...", "..yyyy....", "..........", "..........",
]
build("coin", coin, {"y": (200, 150, 20, 255), "Y": (255, 215, 60, 255), "g": (160, 110, 10, 255)}, scale=10)

# ---- diamond ----
diamond = [
    "..PP......", ".PppP.....", "PppppP....", "PppppP....", ".PppP.....",
    "..Pp......", "..P.......", "..........", "..........", "..........",
]
build("diamond", diamond, {"P": (160, 80, 220, 255), "p": (200, 140, 240, 255)}, scale=10)

# ---- play button (triangle in square) ----
play = [["B" if (x in (0, 19) or y in (0, 19)) else "S" for x in range(20)] for y in range(20)]
for y in range(6, 14):
    width = min(y - 5, 14 - y)
    for x in range(8, 8 + width):
        play[y][x] = "T"
play = ["".join(r) for r in play]
build("play_button", play, {"B": (255, 205, 60, 255), "S": (40, 44, 70, 255), "T": (255, 205, 60, 255)}, scale=8)

# ---- map icon ----
mapicon = [
    "..............", ".WWWWWWWWWWWW.", ".WbbbbbbbbbbW.", ".Wb..S..S...W.",
    ".Wb.....S...W.", ".WbS........W.", ".Wb....S....W.", ".Wb..........W",
    ".WbS...S....W.", ".Wb..........W", ".WbbbbbbbbbbW.", ".WWWWWWWWWWWW.",
    "..............", "..............",
]
build("map_icon", mapicon, {"W": (90, 60, 40, 255), "b": (20, 20, 40, 255), "S": (255, 255, 255, 255)}, scale=8)

# ---- upgrade / rocket icon ----
upgrade = [
    ".....WW.....", "....WWWW....", "...WRRRRW...", "...WRWWRW...", "...WRRRRW...",
    "..WWRRRRWW..", "..WRRRRRRW..", "..WRRRRRRW..", ".YWRRRRRRWY.", ".YYWRRRRWYY.",
    "..YY....YY..", "............",
]
build("upgrade_icon", upgrade, {"W": (220, 220, 225, 255), "R": (214, 61, 61, 255), "Y": (255, 160, 40, 255)}, scale=9)

# ---- Mars planet (24x24, procedural texture) ----
random.seed(7)
mw = 24
mars = Image.new("RGBA", (mw, mw), (0, 0, 0, 0))
mpx = mars.load()
cx = cy = mw / 2
for y in range(mw):
    for x in range(mw):
        d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        if d < mw / 2 - 1:
            shade = random.choice([0, 0, 0, 1, 1, 2])
            base = [(196, 90, 58, 255), (170, 74, 48, 255), (150, 60, 40, 255)][shade]
            if (x - cx) + (y - cy) > mw * 0.25:
                base = tuple(max(0, c - 25) if i < 3 else c for i, c in enumerate(base))
            mpx[x, y] = base
        elif d < mw / 2 + 0.5:
            mpx[x, y] = (120, 45, 30, 140)
mars.resize((mw * 8, mw * 8), Image.NEAREST).save(os.path.join(OUT, "mars.png"))
print("saved mars.png")

# ---- distant small blue-green planet ----
ew = 14
earth = Image.new("RGBA", (ew, ew), (0, 0, 0, 0))
epx = earth.load()
cx = cy = ew / 2
for y in range(ew):
    for x in range(ew):
        d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        if d < ew / 2 - 0.5:
            epx[x, y] = (60, 120, 190, 255) if (x + y) % 3 else (70, 150, 110, 255)
earth.resize((ew * 8, ew * 8), Image.NEAREST).save(os.path.join(OUT, "earth.png"))
print("saved earth.png")

# ---- space background: dark gradient + soft nebula blobs + few grayish soft stars ----
w, h = 64, 96
img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
px = img.load()
for y in range(h):
    t = y / h
    r = int(6 + t * 6)
    g = int(5 + t * 5)
    b = int(14 + t * 16)
    for x in range(w):
        px[x, y] = (r, g, b, 255)


def blob(cx, cy, radius, color):
    for dy in range(-radius, radius):
        for dx in range(-radius, radius):
            x, y = cx + dx, cy + dy
            if 0 <= x < w and 0 <= y < h:
                d = (dx * dx + dy * dy) ** 0.5
                if d < radius:
                    a = int(color[3] * (1 - d / radius))
                    if a > 0:
                        base = px[x, y]
                        nr = min(255, base[0] + color[0] * a // 255)
                        ng = min(255, base[1] + color[1] * a // 255)
                        nb = min(255, base[2] + color[2] * a // 255)
                        px[x, y] = (nr, ng, nb, 255)


blob(15, 20, 18, (40, 10, 50, 90))
blob(45, 60, 22, (10, 30, 45, 70))


def soft_star(x, y, size, alpha):
    for dx in range(size):
        for dy in range(size):
            xx, yy = x + dx, y + dy
            if 0 <= xx < w and 0 <= yy < h:
                base = px[xx, yy]
                g = 190
                nr = base[0] + int((g - base[0]) * alpha)
                ng = base[1] + int((g - base[1]) * alpha)
                nb = base[2] + int((g - base[2]) * alpha)
                px[xx, yy] = (nr, ng, nb, 255)


for _ in range(38):
    x = random.randint(0, w - 2)
    y = random.randint(0, h - 2)
    size = random.choice([1, 1, 1, 2])
    alpha = random.uniform(0.25, 0.5)
    soft_star(x, y, size, alpha)

img.resize((w * 10, h * 10), Image.NEAREST).save(os.path.join(OUT, "space_bg.png"))
print("saved space_bg.png")

print("Phase 2 assets done.")
