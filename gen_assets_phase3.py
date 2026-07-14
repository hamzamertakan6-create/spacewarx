"""Phase 3 assets: enemies (fighter + drone), UFO boss, bullets, explosion,
and gameplay HUD icons (flame, heart, shield, laser)."""
from PIL import Image
import os

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


# ---- Enemy type 1: red fighter, nose pointing DOWN (toward player) ----
enemy_palette = {
    "R": (200, 40, 40, 255),
    "r": (140, 25, 25, 255),
    "K": (20, 20, 20, 255),
    "D": (230, 30, 30, 255),
}
enemy_grid = [
    "................",
    "................",
    "....RR....RR....",
    "....RR....RR....",
    "..rrRRRRRRRRrr..",
    "..rrRRRRRRRRrr..",
    "...KRRRRRRRRK...",
    "...KRRRRRRRRK...",
    "....RRRRRRRR....",
    ".....RRRRRR.....",
    ".....RRRRRR.....",
    "......RRRR......",
    "......RRRR......",
    ".......RR.......",
    "................",
    "................",
]
build("enemy_red", enemy_grid, enemy_palette, scale=8)

# ---- Enemy type 2: fast grey/cyan interceptor drone ----
drone_palette = {
    "G": (110, 120, 130, 255),
    "g": (70, 78, 88, 255),
    "C": (80, 220, 220, 255),
    "K": (20, 20, 24, 255),
}
drone_grid = [
    "................",
    "................",
    "......GG.......",
    ".....GggG......",
    "....GGggGG.....",
    "...GGGCCGGG....",
    "..GG..CC..GG...",
    ".GG...CC...GG..",
    "GG....KK....GG.",
    "GG..........GG.",
    "..GG......GG...",
    "....GG..GG.....",
    "................",
    "................",
    "................",
    "................",
]
build("enemy_drone", drone_grid, drone_palette, scale=8)

# ---- UFO BOSS: classic flying saucer ----
ufo_palette = {
    "M": (140, 150, 165, 255),
    "m": (95, 105, 120, 255),
    "D": (150, 220, 150, 255),
    "d": (90, 170, 110, 255),
    "L": (255, 235, 90, 255),
    "K": (30, 30, 36, 255),
}
ufo_grid = [
    "......................",
    "........DDDDDD........",
    ".......DddddddD.......",
    "......DddddddddD......",
    ".....DdddddddddD......",
    "....MMMMMMMMMMMMMM.....",
    "..MMMMMMMMMMMMMMMMMM...",
    ".MMMLMmMMMMMMMmMLMMM...",
    "MMMMMmmmmmmmmmmmmMMMM..",
    "MMMLMmmmmmmmmmmmmMLMM..",
    ".MMMMMmmmmmmmmmmMMMM...",
    "..MMMMMMMMMMMMMMMM.....",
    "...MM....KK....MM......",
    "....M.....K.....M......",
    "........................",
    "........................",
]
build("ufo_boss", ufo_grid, ufo_palette, scale=9)

# ---- Bullets ----
build("bullet_player", ["..YY..", ".YYYY.", ".YWWY.", ".YWWY.", ".YYYY.", "..YY.."],
      {"Y": (255, 220, 80, 255), "W": (255, 255, 255, 255)}, scale=6)

build("bullet_enemy", ["..RR..", ".RRRR.", ".RRRR.", "..RR.."],
      {"R": (255, 60, 60, 255)}, scale=6)

build("bullet_ufo", ["..DD..", ".DDDD.", ".DDDD.", "..DD.."],
      {"D": (120, 230, 140, 255)}, scale=7)

# ---- Explosion burst ----
boom = [
    "....WY......",
    "...WYYO.....",
    "..WYYYYO....",
    ".YYYYYYYO...",
    "WYYYYYYYYO..",
    "WYYYRRRYYO..",
    ".OYYRRRYYO..",
    "..OYYYYYO...",
    "...OYYYO....",
    "....OYO.....",
    "............",
    "............",
]
build("explosion", boom, {"W": (255, 255, 255, 255), "Y": (255, 220, 90, 255),
                           "O": (255, 140, 30, 255), "R": (220, 50, 30, 255)}, scale=8)

# ---- Engine flame (follows player) ----
build("flame", ["..OO..", ".OYYO.", ".OYYO.", "..OO..", "..YY..", "..Y..."],
      {"O": (255, 140, 30, 220), "Y": (255, 220, 90, 230)}, scale=8)

# ---- HUD ability icons ----
build("heart_icon", [".WW.WW.", "WWWWWWW", "WWWWWWW", ".WWWWW.", "..WWW..", "...W..."],
      {"W": (230, 60, 70, 255)}, scale=8)

build("shield_icon", [".WWWWWW.", "WWccccWW", "WccccccW", "WccccccW",
                       ".WccccW.", "..WccW..", "...WW..."],
      {"W": (80, 180, 255, 255), "c": (150, 220, 255, 255)}, scale=8)

build("laser_icon", ["...RR...", "...RR...", "...RR...", "...RR...", "...RR...", "...RR..."],
      {"R": (255, 40, 40, 255)}, scale=8)

print("Phase 3 assets done.")
