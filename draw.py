from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 675

ROOT = Path(__file__).resolve().parent
GHOST_PATH = ROOT / "assets" / "ghost.png"
FONT_PATH = ROOT / "assets" / "Anton-Regular.ttf"
OUT_PATH = ROOT / "meme.png"


def lerp_color(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (
        round(c1[0] + (c2[0] - c1[0]) * t),
        round(c1[1] + (c2[1] - c1[1]) * t),
        round(c1[2] + (c2[2] - c1[2]) * t),
    )


def build_sky_gradient() -> Image.Image:
    stops = [
        (0.00, (34, 10, 74)),
        (0.48, (232, 42, 134)),
        (0.80, (255, 146, 54)),
        (1.00, (255, 118, 44)),
    ]
    strip = Image.new("RGB", (1, HEIGHT))
    pixels = strip.load()
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        for idx in range(len(stops) - 1):
            t0, c0 = stops[idx]
            t1, c1 = stops[idx + 1]
            if t0 <= t <= t1:
                local_t = (t - t0) / (t1 - t0)
                pixels[0, y] = lerp_color(c0, c1, local_t)
                break
    return strip.resize((WIDTH, HEIGHT), Image.Resampling.NEAREST)


def draw_sun(draw: ImageDraw.ImageDraw) -> None:
    cx, cy, r = 445, 428, 152
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 238, 188))


def draw_skyline(draw: ImageDraw.ImageDraw) -> None:
    silhouette = (18, 8, 36)
    buildings = [
        (-5, 65, 515),
        (55, 118, 470),
        (110, 175, 525),
        (168, 225, 448),
        (218, 288, 492),
        (280, 345, 456),
        (338, 395, 512),
        (388, 455, 466),
        (448, 515, 434),
        (508, 575, 484),
        (568, 632, 516),
        (624, 695, 462),
        (688, 748, 504),
        (740, 810, 474),
        (802, 870, 518),
        (862, 930, 468),
        (922, 988, 498),
        (980, 1050, 452),
        (1042, 1118, 506),
        (1110, 1205, 482),
    ]
    for x1, x2, top in buildings:
        draw.rectangle((x1, top, x2, HEIGHT), fill=silhouette)

    draw.rectangle((193, 418, 200, 448), fill=silhouette)
    draw.rectangle((468, 418, 496, 434), fill=silhouette)
    draw.rectangle((654, 442, 666, 462), fill=silhouette)
    draw.rectangle((0, 558, WIDTH, HEIGHT), fill=silhouette)

    windows = [
        (72, 486, 8, 12, (255, 222, 118)),
        (90, 486, 8, 12, (255, 222, 118)),
        (72, 510, 8, 12, (110, 238, 255)),
        (182, 468, 9, 13, (255, 222, 118)),
        (201, 468, 9, 13, (255, 110, 185)),
        (182, 492, 9, 13, (255, 222, 118)),
        (294, 474, 8, 12, (110, 238, 255)),
        (314, 474, 8, 12, (255, 222, 118)),
        (314, 498, 8, 12, (255, 222, 118)),
        (404, 484, 9, 13, (255, 110, 185)),
        (424, 484, 9, 13, (255, 222, 118)),
        (462, 454, 9, 14, (255, 222, 118)),
        (482, 454, 9, 14, (110, 238, 255)),
        (462, 480, 9, 14, (255, 222, 118)),
        (482, 506, 9, 14, (255, 110, 185)),
        (528, 502, 8, 12, (255, 222, 118)),
        (548, 524, 8, 12, (110, 238, 255)),
        (642, 482, 9, 13, (255, 222, 118)),
        (664, 482, 9, 13, (255, 110, 185)),
        (642, 508, 9, 13, (110, 238, 255)),
        (760, 494, 9, 13, (255, 222, 118)),
        (780, 518, 9, 13, (255, 222, 118)),
        (882, 488, 9, 13, (255, 110, 185)),
        (902, 512, 9, 13, (255, 222, 118)),
        (1000, 474, 9, 14, (110, 238, 255)),
        (1020, 474, 9, 14, (255, 222, 118)),
        (1000, 502, 9, 14, (255, 222, 118)),
        (1134, 504, 9, 13, (255, 110, 185)),
        (1156, 526, 9, 13, (255, 222, 118)),
    ]
    for wx, wy, ww, wh, color in windows:
        draw.rectangle((wx, wy, wx + ww, wy + wh), fill=color)


def quad_bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    steps: int,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        inv = 1.0 - t
        x = inv * inv * p0[0] + 2.0 * inv * t * p1[0] + t * t * p2[0]
        y = inv * inv * p0[1] + 2.0 * inv * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


def draw_palm_tree(
    draw: ImageDraw.ImageDraw,
    base: tuple[float, float],
    ctrl: tuple[float, float],
    crown: tuple[float, float],
    fronds: list[tuple[tuple[float, float], tuple[float, float], float]],
) -> None:
    color = (14, 5, 28)
    spine = quad_bezier(base, ctrl, crown, 14)
    left_edge: list[tuple[float, float]] = []
    right_edge: list[tuple[float, float]] = []
    n = len(spine) - 1
    for i, (px, py) in enumerate(spine):
        half_w = 13.0 * (1.0 - i / n) + 4.0 * (i / n)
        left_edge.append((px - half_w, py))
        right_edge.append((px + half_w, py))
    draw.polygon(left_edge + list(reversed(right_edge)), fill=color)

    for mid, tip, thickness in fronds:
        upper_pts = quad_bezier(crown, mid, tip, 10)
        lower_mid = (mid[0], mid[1] + thickness)
        lower_pts = quad_bezier(crown, lower_mid, tip, 10)
        draw.polygon(upper_pts + list(reversed(lower_pts)), fill=color)


def draw_palms(draw: ImageDraw.ImageDraw) -> None:
    left_crown = (92.0, 336.0)
    left_fronds = [
        ((38.0, 294.0), (-8.0, 338.0), 22.0),
        ((52.0, 266.0), (14.0, 274.0), 20.0),
        ((94.0, 252.0), (110.0, 232.0), 18.0),
        ((146.0, 262.0), (196.0, 288.0), 22.0),
        ((162.0, 296.0), (218.0, 348.0), 24.0),
        ((144.0, 338.0), (176.0, 404.0), 20.0),
        ((46.0, 346.0), (14.0, 408.0), 20.0),
    ]
    draw_palm_tree(draw, (26.0, 675.0), (48.0, 495.0), left_crown, left_fronds)

    right_crown = (1102.0, 316.0)
    right_fronds = [
        ((1046.0, 278.0), (990.0, 326.0), 24.0),
        ((1054.0, 248.0), (1008.0, 262.0), 20.0),
        ((1098.0, 236.0), (1086.0, 214.0), 18.0),
        ((1154.0, 246.0), (1206.0, 272.0), 22.0),
        ((1166.0, 284.0), (1216.0, 336.0), 22.0),
        ((1052.0, 324.0), (1024.0, 388.0), 20.0),
        ((1148.0, 324.0), (1182.0, 386.0), 20.0),
    ]
    draw_palm_tree(draw, (1174.0, 675.0), (1152.0, 485.0), right_crown, right_fronds)


def composite_ghost(canvas: Image.Image) -> None:
    ghost = Image.open(GHOST_PATH).convert("RGBA")
    bbox = ghost.getbbox()
    if bbox is not None:
        ghost = ghost.crop(bbox)
    scale = min(355.0 / ghost.width, 365.0 / ghost.height)
    new_w = round(ghost.width * scale)
    new_h = round(ghost.height * scale)
    ghost = ghost.resize((new_w, new_h), Image.Resampling.LANCZOS)
    gx = 1146 - new_w
    gy = 636 - new_h
    canvas.paste(ghost, (gx, gy), ghost)


def fit_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    start_size: int,
    max_width: int,
    stroke_width: int,
) -> ImageFont.FreeTypeFont:
    size = start_size
    while size > 16:
        font = ImageFont.truetype(str(FONT_PATH), size)
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
        if bbox[2] - bbox[0] <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(str(FONT_PATH), 16)


def draw_crisp_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    x_anchor: int,
    y_top: int,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    stroke_fill: tuple[int, int, int],
    stroke_width: int,
    align: str = "center",
) -> None:
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    if align == "center":
        x = x_anchor - (bbox[0] + bbox[2]) // 2
    else:
        x = x_anchor - bbox[0]
    y = y_top - bbox[1]
    draw.text(
        (x + 4, y + 4),
        text,
        font=font,
        fill=(14, 4, 30),
        stroke_width=stroke_width,
        stroke_fill=(14, 4, 30),
    )
    draw.text(
        (x, y),
        text,
        font=font,
        fill=fill,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )


def main() -> None:
    canvas = build_sky_gradient()
    draw = ImageDraw.Draw(canvas)

    draw_sun(draw)
    draw_skyline(draw)
    draw_palms(draw)
    composite_ghost(canvas)

    headline = "WAITED 13 YEARS FOR GTA 6"
    headline_font = fit_font(draw, headline, start_size=82, max_width=1092, stroke_width=4)
    draw_crisp_text(
        draw,
        headline,
        x_anchor=600,
        y_top=30,
        font=headline_font,
        fill=(255, 255, 255),
        stroke_fill=(18, 6, 38),
        stroke_width=4,
        align="center",
    )

    punchline = "MY AGENT GOT PAID FIRST"
    punchline_font = fit_font(draw, punchline, start_size=70, max_width=1092, stroke_width=4)
    draw_crisp_text(
        draw,
        punchline,
        x_anchor=600,
        y_top=128,
        font=punchline_font,
        fill=(255, 224, 92),
        stroke_fill=(18, 6, 38),
        stroke_width=4,
        align="center",
    )

    footer = "on make.fun, where agents win real money"
    footer_font = fit_font(draw, footer, start_size=34, max_width=690, stroke_width=3)
    draw_crisp_text(
        draw,
        footer,
        x_anchor=60,
        y_top=608,
        font=footer_font,
        fill=(246, 244, 255),
        stroke_fill=(14, 5, 28),
        stroke_width=3,
        align="left",
    )

    canvas.save(OUT_PATH, format="PNG")


if __name__ == "__main__":
    main()
