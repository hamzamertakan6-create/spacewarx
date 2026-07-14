"""Phase 1 assets: language flags + tutorial arrow + loading icon."""
from PIL import Image
import os

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)


def build(name, grid, palette, scale=10):
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


# ---- flags: 1px dark frame so tiles read as separate even edge-to-edge ----
FRAME = "F"
frame_color = {"F": (20, 18, 26, 255)}


def framed(inner_rows):
    w = len(inner_rows[0]) + 2
    top = FRAME * w
    rows = [top]
    for r in inner_rows:
        rows.append(FRAME + r + FRAME)
    rows.append(top)
    return rows


flag_tr = framed([
    "RRRRRRRRRRRR",
    "RRRWWRRRRRRR",
    "RRWRRWWWRRRR",
    "RRWRRWWWRRRR",
    "RRRWWRRRRRRR",
    "RRRRRRRRRRRR",
])
build("flag_tr", flag_tr, {**frame_color, "R": (227, 10, 23, 255), "W": (255, 255, 255, 255)}, scale=7)

flag_en = framed([
    "BBBBWBBBBWBB",
    "WWWWWWWWWWWW",
    "BBBBRRRRBBBB",
    "BBBBRRRRBBBB",
    "WWWWWWWWWWWW",
    "BBBBWBBBBWBB",
])
build("flag_en", flag_en, {**frame_color, "B": (12, 33, 105, 255), "W": (255, 255, 255, 255), "R": (200, 16, 46, 255)}, scale=7)

flag_fr = framed([
    "BBBBWWWWRRRR",
    "BBBBWWWWRRRR",
    "BBBBWWWWRRRR",
    "BBBBWWWWRRRR",
    "BBBBWWWWRRRR",
    "BBBBWWWWRRRR",
])
build("flag_fr", flag_fr, {**frame_color, "B": (0, 85, 164, 255), "W": (255, 255, 255, 255), "R": (239, 65, 53, 255)}, scale=7)

flag_pt = framed([
    "GGGGRRRRRRRR",
    "GGGGRRWRRRRR",
    "GGGGRWWWRRRR",
    "GGGGRWWWRRRR",
    "GGGGRRWRRRRR",
    "GGGGRRRRRRRR",
])
build("flag_pt", flag_pt, {**frame_color, "G": (0, 102, 51, 255), "R": (255, 0, 0, 255), "W": (255, 206, 0, 255)}, scale=7)

flag_ru = framed([
    "WWWWWWWWWWWW",
    "WWWWWWWWWWWW",
    "BBBBBBBBBBBB",
    "BBBBBBBBBBBB",
    "RRRRRRRRRRRR",
    "RRRRRRRRRRRR",
])
build("flag_ru", flag_ru, {**frame_color, "W": (255, 255, 255, 255), "B": (0, 57, 166, 255), "R": (213, 43, 30, 255)}, scale=7)

flag_jp = framed([
    "WWWWWWWWWWWW",
    "WWWWRRRRWWWW",
    "WWWRRRRRRWWW",
    "WWWRRRRRRWWW",
    "WWWWRRRRWWWW",
    "WWWWWWWWWWWW",
])
build("flag_jp", flag_jp, {**frame_color, "W": (255, 255, 255, 255), "R": (188, 0, 45, 255)}, scale=7)

flag_cn = framed([
    "RRRRRRRRRRRR",
    "RRYRRRRRRRRR",
    "RRRRRRRYRRRR",
    "RRRRRRRRRRRR",
    "RRRRRRRYRRRR",
    "RRYRRRRRRRRR",
])
build("flag_cn", flag_cn, {**frame_color, "R": (222, 41, 16, 255), "Y": (255, 222, 0, 255)}, scale=7)

# ---- tutorial arrow: white transparent pixel arrow (points up by default) ----
arrow_grid = [
    "....WW....",
    "...WWWW...",
    "..WWWWWW..",
    ".WWWWWWWW.",
    "....WW....",
    "....WW....",
    "....WW....",
    "....WW....",
]
build("arrow", arrow_grid, {"W": (255, 255, 255, 230)}, scale=12)

print("Phase 1 assets done.")
