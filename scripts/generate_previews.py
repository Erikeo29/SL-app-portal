"""
Génère des vignettes PNG stylisées pour chaque app du portail.
Usage : python scripts/generate_previews.py   (depuis 26_SL_AppPortal/)
Sortie : assets/screenshots/<id>.png  (480x280 px)
"""

import math
import pathlib
import textwrap

import yaml
from PIL import Image, ImageDraw, ImageFont

ROOT      = pathlib.Path(__file__).parent.parent
YAML_FILE = ROOT / "data" / "apps.yaml"
OUT_DIR   = ROOT / "assets" / "screenshots"
W, H      = 480, 280

CAT_COLORS = {
    "Electrochimie":     (0,   75,  135),
    "Simulation":        (0,   119, 204),
    "Normes & RAG":      (184, 50,  0),
    "Gestion de projet": (42,  110, 42),
    "Qualité & Vision":  (110, 42,  110),
}


# ── Dégradé diagonal ──────────────────────────────────────────────────────────
def make_gradient(color: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (W, H))
    r0, g0, b0 = color
    r1 = min(255, int(r0 * 1.55))
    g1 = min(255, int(g0 * 1.55))
    b1 = min(255, int(b0 * 1.55))
    for y in range(H):
        for x in range(W):
            t = (x / W * 0.6 + (H - y) / H * 0.4)
            r = int(r0 + (r1 - r0) * t)
            g = int(g0 + (g1 - g0) * t)
            b = int(b0 + (b1 - b0) * t)
            img.putpixel((x, y), (r, g, b))
    return img


# ── Motif graphique par catégorie ─────────────────────────────────────────────
def draw_pattern(draw: ImageDraw.ImageDraw, category: str, color: tuple) -> None:
    w = (min(255, color[0] + 80), min(255, color[1] + 80), min(255, color[2] + 80), 60)
    lw = 2

    if category == "Electrochimie":
        # Voltamogramme cyclique stylisé
        pts = []
        for i in range(120):
            t = i / 119
            x = 60 + int(t * 360)
            angle = t * 2 * math.pi
            y = 120 + int(math.sin(angle) * 55 + math.sin(angle * 2) * 18)
            pts.append((x, y))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i + 1]], fill=w, width=lw)

    elif category == "Simulation":
        # Vecteurs de flux (grille de flèches)
        for gx in range(60, 430, 70):
            for gy in range(60, 210, 55):
                dx = int(20 * math.sin(gx / 60))
                dy = int(12 * math.cos(gy / 40))
                draw.line([(gx, gy), (gx + dx, gy + dy)], fill=w, width=lw)
                # pointe de flèche
                draw.ellipse([(gx + dx - 3, gy + dy - 3), (gx + dx + 3, gy + dy + 3)], fill=w)

    elif category == "Normes & RAG":
        # Barres horizontales style résultats de recherche
        for i, (bar_w, y) in enumerate([(320, 70), (260, 110), (290, 150), (200, 190)]):
            draw.rounded_rectangle([(80, y), (80 + bar_w, y + 18)], radius=4, fill=w)
        # Point bullet
        for y in [79, 119, 159, 199]:
            draw.ellipse([(58, y), (70, y + 12)], fill=w)

    elif category == "Gestion de projet":
        # Gantt simplifié
        tasks = [(80, 200, 70), (130, 320, 70), (200, 280, 70), (250, 380, 70)]
        for i, (x0, x1, y_base) in enumerate(tasks):
            y = 55 + i * 42
            draw.rounded_rectangle([(x0, y), (x1, y + 26)], radius=5, fill=w)
        # Ligne de temps
        draw.line([(60, 230), (430, 230)], fill=w, width=1)
        for x in range(80, 440, 60):
            draw.line([(x, 225), (x, 235)], fill=w, width=1)

    elif category == "Qualité & Vision":
        # Grille image + rectangle de détection
        cell = 28
        for gx in range(60, 380, cell):
            for gy in range(40, 210, cell):
                val = int(40 + 30 * math.sin(gx / 25) * math.cos(gy / 20))
                draw.rectangle([(gx, gy), (gx + cell - 2, gy + cell - 2)],
                                fill=(w[0], w[1], w[2], max(20, val)))
        # Bounding box
        draw.rectangle([(130, 75), (310, 195)], outline=w, width=3)
        # Coin haut-gauche du rectangle
        draw.line([(130, 75), (150, 75)], fill=w, width=4)
        draw.line([(130, 75), (130, 95)], fill=w, width=4)
        draw.line([(290, 75), (310, 75)], fill=w, width=4)
        draw.line([(310, 75), (310, 95)], fill=w, width=4)


# ── Texte centré avec retour à la ligne ───────────────────────────────────────
def draw_centered_text(draw: ImageDraw.ImageDraw, text: str, y_center: int,
                       font: ImageFont.ImageFont, fill: tuple, max_w: int = 380) -> None:
    lines = textwrap.wrap(text, width=22)[:2]
    try:
        line_h = font.getbbox("Ag")[3] + 4
    except Exception:
        line_h = 22
    total_h = len(lines) * line_h
    y = y_center - total_h // 2
    for line in lines:
        try:
            bbox = font.getbbox(line)
            lw = bbox[2] - bbox[0]
        except Exception:
            lw = len(line) * 10
        x = (W - lw) // 2
        draw.text((x + 1, y + 1), line, font=font, fill=(0, 0, 0, 80))
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h


# ── Génération d'une vignette ─────────────────────────────────────────────────
def generate(app: dict) -> None:
    cat    = app.get("category", "")
    color  = CAT_COLORS.get(cat, (74, 144, 217))
    name   = app["name"]
    abbrev = app.get("abbrev", app["id"].upper())

    img  = make_gradient(color).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    draw_pattern(draw, cat, color)

    # Bandeau bas semi-transparent
    band = Image.new("RGBA", (W, 44), (0, 0, 0, 120))
    img.alpha_composite(band, (0, H - 44))
    draw = ImageDraw.Draw(img, "RGBA")

    # Tentative de chargement de font - fallback Pillow default
    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_sm  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        font_cat = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except Exception:
        font_big = ImageFont.load_default()
        font_sm  = font_big
        font_cat = font_big

    # Nom de l'app (centré verticalement dans la partie haute)
    draw_centered_text(draw, name, y_center=118, font=font_big,
                       fill=(255, 255, 255), max_w=380)

    # Abréviation en haut à gauche
    draw.text((14, 12), abbrev, font=font_sm, fill=(255, 255, 255, 160))

    # Catégorie dans le bandeau bas
    try:
        cat_w = font_cat.getbbox(cat)[2]
    except Exception:
        cat_w = len(cat) * 7
    draw.text(((W - cat_w) // 2, H - 30), cat, font=font_cat,
              fill=(255, 255, 255, 200))

    out_path = OUT_DIR / f"{app['id']}.png"
    img.convert("RGB").save(out_path, "PNG", optimize=True)
    print(f"  ✓ {out_path.name}  [{name}]")


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(YAML_FILE, encoding="utf-8") as f:
        apps = yaml.safe_load(f).get("apps", [])

    print(f"Génération de {len(apps)} vignettes → {OUT_DIR}")
    for app in apps:
        generate(app)
    print("Terminé.")


if __name__ == "__main__":
    main()
