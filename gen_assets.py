"""
Pixel art sprite generator for SpaceWarx game.
Draws sprites on a small pixel grid then upscales with NEAREST
so edges stay crisp (classic pixel-art look).
"""
from PIL import Image
import os

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)

SCALE = 8  # final size = grid_size * SCALE

def build(name, grid, palette, scale=SCALE):
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


# ---------- PLAYER PLANE (16x16) nose pointing right ----------
plane_palette = {
    "R": (214, 61, 61, 255),    # red body
    "r": (161, 39, 39, 255),    # dark red shade
    "W": (240, 240, 240, 255),  # white highlight / windows
    "Y": (255, 205, 60, 255),   # yellow tail tip
    "G": (90, 90, 100, 255),    # grey engine
}
plane_grid = [
    "................",
    ".......RR.......",
    "......RRRR......",
    "......RRRR......",
    ".....RRRRRR.....",
    ".....RRRRRR.....",
    "....RRRRRRRR....",
    "...GRRRWWRRRG...",
    "...GRRRWWRRRG...",
    "..YrRRRRRRRRrY..",
    "..YrRRRRRRRRrY..",
    "....RR....RR....",
    "....RR....RR....",
    "....Yr....rY....",
    "................",
    "................",
]
build("player", plane_grid, plane_palette)

# ---------- CLOUD OBSTACLE (16x12) ----------
cloud_palette = {
    "W": (255, 255, 255, 235),
    "L": (222, 232, 245, 235),
}
cloud_grid = [
    "................",
    "......WWWW......",
    "....WWWWWWWW....",
    "..WWWWWWWWWWWW..",
    ".WWWWWWWWWWWWWW.",
    "WWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWW",
    "LLLLLLLLLLLLLLLL",
    ".LLLLLLLLLLLLLL.",
    "..LLLLLLLLLLLL..",
    "................",
    "................",
]
build("cloud", cloud_grid, cloud_palette)

# ---------- BIRD OBSTACLE (14x10) ----------
bird_palette = {
    "B": (70, 70, 90, 255),
    "b": (40, 40, 55, 255),
    "O": (240, 160, 40, 255),
}
bird_grid = [
    "..............",
    "....BB....BB..",
    "...BBBB..BBBB.",
    "..BBBBBBBBBBBB",
    ".BBBBBbbBBBBB.",
    "BBBBBbbbbBBBB.",
    "..BBbbObbBB...",
    "....bbbb......",
    "....b..b......",
    "..............",
]
build("bird", bird_grid, bird_palette)

# ---------- STAR COLLECTIBLE (10x10) ----------
star_palette = {
    "Y": (255, 221, 89, 255),
    "y": (255, 190, 40, 255),
}
star_grid = [
    "....yy....",
    "....YY....",
    "....YY....",
    "yYYYYYYYYy",
    ".yYYYYYYy.",
    "..YYYYYY..",
    ".yY....Yy.",
    "yy......yy",
    "..........",
    "..........",
]
build("star", star_grid, star_palette)

# ---------- BACKGROUND (32x18) soft sky gradient with small clouds ----------
bg_palette = {
    "1": (135, 206, 250, 255),
    "2": (160, 216, 250, 255),
    "3": (190, 226, 250, 255),
    "4": (215, 236, 250, 255),
    "W": (255, 255, 255, 180),
}
bg_grid = []
for y in range(18):
    if y < 4:
        row = "1" * 32
    elif y < 8:
        row = "2" * 32
    elif y < 13:
        row = "3" * 32
    else:
        row = "4" * 32
    bg_grid.append(list(row))

def stamp_cloud(gx, gy):
    pattern = [
        "..WWWW..",
        ".WWWWWW.",
        "WWWWWWWW",
    ]
    for dy, r in enumerate(pattern):
        for dx, c in enumerate(r):
            if c == "W" and 0 <= gy+dy < 18 and 0 <= gx+dx < 32:
                bg_grid[gy+dy][gx+dx] = "W"

stamp_cloud(3, 2)
stamp_cloud(20, 5)
stamp_cloud(11, 9)

bg_grid = ["".join(r) for r in bg_grid]
build("background", bg_grid, bg_palette, scale=20)

# ---------- ICON (32x32) for app / play store: transparent dark rounded tile ----------
icon_img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
icon_px = icon_img.load()
for y in range(32):
    for x in range(32):
        corner_cut = (x < 3 and y < 3) or (x > 27) and (y < 3) or (x < 3 and y > 27) or (x > 27 and y > 27)
        if not corner_cut:
            icon_px[x, y] = (14, 12, 24, 255)
for y, row in enumerate(plane_grid):
    for x, c in enumerate(row):
        if c != ".":
            iy, ix = 8 + y, 8 + x
            if 0 <= iy < 32 and 0 <= ix < 32:
                icon_px[ix, iy] = plane_palette[c]
icon_img = icon_img.resize((32 * 16, 32 * 16), Image.NEAREST)
icon_img.save(os.path.join(OUT, "icon.png"))
print(f"saved icon.png -> {icon_img.size}")

print("All assets generated.")
