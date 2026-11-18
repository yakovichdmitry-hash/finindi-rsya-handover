# -*- coding: utf-8 -*-
"""
Сборка рекламного креатива VK Ads 600x600 + иконки-логотипа 256x256
для PDF-гида «Инвестиционные показатели без воды» (finindi).

Гипотеза: «Карта вместо лоскутов» — 20+ показателей собраны в одном
практическом руководстве, а не ищутся по разрозненным источникам.

Используются ТОЛЬКО реальные материалы продукта:
  - обложка и реальные страницы PDF (нарезка из direct-campaigns/.../source_crops)
  - реальный логотип finindi (avatar-finindi-512.png)

Запуск:
    set PYTHONPATH=C:\\...\\default-workspace\\_skill_deps
    python build_vk_creative.py

Выход (рядом со скриптом):
    finindi_vk_600x600.png    600x600, RGB, < 1 МБ
    finindi_logo_256x256.png  256x256, RGB
    preview_300.png           300x300 — превью для проверки читаемости
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# --------------------------------------------------------------------------
# Пути
# --------------------------------------------------------------------------
WS = Path(r"C:\Users\User\Documents\deepseek-harness\default-workspace")

SRC_PAGES = WS / "direct-campaigns" / "finindi" / "assets" / "source_crops"
LOGO_SRC = WS / "finindi" / "deliverables" / "avatar-finindi-512.png"
OUT_DIR = WS / "vk-finindi" / "creative"

OUT_CREATIVE = OUT_DIR / "finindi_vk_600x600.png"
OUT_LOGO = OUT_DIR / "finindi_logo_256x256.png"
OUT_PREVIEW = OUT_DIR / "preview_300.png"

# Реальные страницы продукта для «веера»:
#   guide_p01 — обложка (центр, лицо продукта)
#   guide_p03 — содержание: полный список показателей = «карта в одном месте»
#   guide_p23 — чек-лист 8 чисел: формулы и пороги = практика
PAGE_COVER = SRC_PAGES / "guide_p01.png"
PAGE_LEFT = SRC_PAGES / "guide_p03.png"
PAGE_RIGHT = SRC_PAGES / "guide_p23.png"

# --------------------------------------------------------------------------
# Фирменные цвета (взяты с реальной обложки)
# --------------------------------------------------------------------------
NAVY = (27, 34, 51)          # #1B2233
PAPER = (247, 242, 232)      # #F7F2E8
LIME = (201, 241, 88)        # #C9F158
GOLD = (176, 140, 66)        # #B08C42
GOLD_LIGHT = (218, 183, 112)  # осветлённое золото для мелкого текста на тёмном
WHITE = (255, 255, 255)
SUBTEXT = (223, 218, 208)    # бумажный, приглушённый
MUTED = (160, 169, 190)      # служебный текст в шапке
TILE_FILL = (36, 46, 68)     # #242E44 — приподнятая плашка цены

# --------------------------------------------------------------------------
# Шрифты
# --------------------------------------------------------------------------
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_SEMI = r"C:\Windows\Fonts\seguisb.ttf"
FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"

# --------------------------------------------------------------------------
# Геометрия
# --------------------------------------------------------------------------
W = H = 600
MARGIN = 32

# Тексты
TXT_HEADER_BADGE = "PDF-гид · 67 страниц"
TXT_WORDMARK = "finindi"
TXT_KICKER = "ИНВЕСТИЦИОННЫЕ ПОКАЗАТЕЛИ БЕЗ ВОДЫ"
TXT_H1 = "20+ показателей"
TXT_H2 = "в одной карте"
TXT_SUB = "Формулы, примеры и ориентиры — в одном гиде"
TXT_TARIFF_1 = "ГИД"
TXT_PRICE_1 = "490 ₽"
TXT_TARIFF_2 = "КОМПЛЕКТ"
TXT_PRICE_2 = "990 ₽"


# --------------------------------------------------------------------------
# Хелперы
# --------------------------------------------------------------------------
def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def tracked_width(text: str, font, tracking: float) -> float:
    if not text:
        return 0.0
    return sum(font.getlength(ch) for ch in text) + tracking * (len(text) - 1)


def fit_tracking(text, font, max_width: float, max_tracking: float = 2.0) -> float:
    """Подбирает трекинг так, чтобы строка влезла в max_width (не меньше 0)."""
    base = tracked_width(text, font, 0.0)
    if base >= max_width or len(text) < 2:
        return 0.0
    return max(0.0, min(max_tracking, (max_width - base) / (len(text) - 1)))


def draw_tracked(draw, xy, text, font, fill, tracking=0.0, anchor_center=None):
    """Текст с межбуквенным трекингом. xy — (x, middle_y) при anchor_center=None
    либо (center_x, middle_y) при anchor_center='x'."""
    total = tracked_width(text, font, tracking)
    x = (xy[0] - total / 2.0) if anchor_center == "x" else xy[0]
    for ch in text:
        draw.text((x, xy[1]), ch, font=font, fill=fill, anchor="lm")
        x += font.getlength(ch) + tracking
    return total


def soft_glow(canvas_size, center, radius, color, peak_alpha, blur_factor=0.55):
    """Мягкое радиальное свечение (RGBA-слой)."""
    layer = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = center
    d.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=color + (peak_alpha,),
    )
    return layer.filter(ImageFilter.GaussianBlur(radius * blur_factor))


def page_card(path: Path, height: int, border_alpha: int = 46) -> Image.Image:
    """Страница реального PDF, приведённая к нужной высоте, с тонкой рамкой."""
    src = Image.open(path)
    src = src.convert("RGB")
    w = max(1, round(height * src.width / src.height))
    src = src.resize((w, height), Image.LANCZOS)

    card = Image.new("RGBA", (w, height), (0, 0, 0, 0))
    card.paste(src, (0, 0))
    d = ImageDraw.Draw(card)
    d.rectangle([0, 0, w - 1, height - 1], outline=(255, 255, 255, border_alpha), width=1)
    return card


def rotate_card(card: Image.Image, angle: float) -> Image.Image:
    """Поворот вокруг центра на квадратном холсте с запасом — без обрезки."""
    w, h = card.size
    side = int((w * w + h * h) ** 0.5) + 4
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(card, ((side - w) // 2, (side - h) // 2))
    return square.rotate(angle, resample=Image.BICUBIC, expand=False)


def drop_shadow(rotated: Image.Image, blur: int = 11, opacity: int = 120) -> Image.Image:
    alpha = rotated.getchannel("A")
    shadow = Image.new("RGBA", rotated.size, (0, 0, 0, 0))
    shadow.paste(Image.new("RGBA", rotated.size, (0, 0, 0, opacity)), (0, 0), alpha)
    return shadow.filter(ImageFilter.GaussianBlur(blur))


def overlay(base: Image.Image, layer: Image.Image) -> Image.Image:
    return Image.alpha_composite(base.convert("RGBA"), layer)


# --------------------------------------------------------------------------
# 1. Креатив 600x600
# --------------------------------------------------------------------------
def build_creative() -> Image.Image:
    canvas = Image.new("RGB", (W, H), NAVY)

    # --- фон: глубина, без стоковых картинок -------------------------------
    # мягкое свечение за веером страниц + затемнение к низу
    canvas = overlay(canvas, soft_glow((W, H), (300, 368), 262, (64, 80, 120), 150, 0.6))
    canvas = overlay(canvas, soft_glow((W, H), (300, 545), 330, (8, 11, 18), 100, 0.65))

    # --- веер реальных страниц --------------------------------------------
    # центр — обложка, слева содержание, справа чек-лист
    card_side_h = 198
    card_center_h = 210

    left = rotate_card(page_card(PAGE_LEFT, card_side_h), -10.0)
    right = rotate_card(page_card(PAGE_RIGHT, card_side_h), 10.0)
    center = rotate_card(page_card(PAGE_COVER, card_center_h, border_alpha=95), 0.0)

    placements = [
        (left, (204, 360), 7, 10),    # (слой, центр, dy, blur)
        (right, (396, 360), 7, 10),
        (center, (300, 352), 9, 14),
    ]
    for layer, (cx, cy), dy, blur in placements:
        shadow = drop_shadow(layer, blur=blur, opacity=130)
        half = layer.width // 2
        canvas_rgba = canvas.convert("RGBA")
        canvas_rgba.paste(shadow, (cx - half, cy - half + dy), shadow)
        canvas_rgba.paste(layer, (cx - half, cy - half), layer)
        canvas = canvas_rgba.convert("RGB")

    draw = ImageDraw.Draw(canvas)

    # --- шапка: логотип + finindi + «PDF-гид · 67 страниц» -----------------
    logo = Image.open(LOGO_SRC).convert("RGBA")
    logo_size = 34
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    logo_y = 27
    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.paste(logo, (MARGIN, logo_y), logo)
    canvas = canvas_rgba.convert("RGB")
    draw = ImageDraw.Draw(canvas)

    head_mid = logo_y + logo_size // 2 + 1
    f_word = load_font(FONT_BOLD, 18)
    word_x = MARGIN + logo_size + 11
    draw.text((word_x, head_mid), TXT_WORDMARK, font=f_word, fill=WHITE, anchor="lm")
    word_end = word_x + f_word.getlength(TXT_WORDMARK)

    sep_x = word_end + 14
    draw.line([(sep_x, head_mid - 9), (sep_x, head_mid + 9)], fill=(255, 255, 255, 60), width=1)

    f_badge = load_font(FONT_SEMI, 15)
    draw.text((sep_x + 14, head_mid), TXT_HEADER_BADGE, font=f_badge, fill=MUTED, anchor="lm")

    # --- кикер: название продукта -----------------------------------------
    f_kicker = load_font(FONT_BOLD, 16)
    kick_tracking = fit_tracking(TXT_KICKER, f_kicker, max_width=W - 2 * MARGIN, max_tracking=1.5)
    draw_tracked(draw, (MARGIN, 78), TXT_KICKER, f_kicker, GOLD_LIGHT, tracking=kick_tracking)

    # --- заголовок ---------------------------------------------------------
    f_h1 = load_font(FONT_BOLD, 56)
    draw.text((MARGIN, 128), TXT_H1, font=f_h1, fill=WHITE, anchor="lm")
    draw.text((MARGIN, 186), TXT_H2, font=f_h1, fill=LIME, anchor="lm")

    # --- подзаголовок ------------------------------------------------------
    f_sub = load_font(FONT_SEMI, 20)
    draw.text((MARGIN, 236), TXT_SUB, font=f_sub, fill=(238, 233, 222), anchor="lm")

    # --- две равные плашки с тарифами -------------------------------------
    gap = 14
    tile_w = (W - 2 * MARGIN - gap) // 2
    tile_h = 88
    tile_y = 486
    f_tariff = load_font(FONT_BOLD, 18)
    f_price = load_font(FONT_BOLD, 31)

    for i, (tariff, price) in enumerate(
        [(TXT_TARIFF_1, TXT_PRICE_1), (TXT_TARIFF_2, TXT_PRICE_2)]
    ):
        x0 = MARGIN + i * (tile_w + gap)
        x1 = x0 + tile_w
        draw.rounded_rectangle(
            [x0, tile_y, x1, tile_y + tile_h],
            radius=11,
            fill=TILE_FILL,
            outline=LIME,
            width=2,
        )
        cx = (x0 + x1) / 2
        draw_tracked(
            draw, (cx, tile_y + 25), tariff, f_tariff, LIME, tracking=1.6, anchor_center="x"
        )
        draw.text((cx, tile_y + 59), price, font=f_price, fill=WHITE, anchor="mm")

    return canvas


# --------------------------------------------------------------------------
# 2. Иконка-логотип 256x256
# --------------------------------------------------------------------------
def build_logo() -> Image.Image:
    """Реальный логотип целиком (без обрезки знака) на брендовом фоне, RGB."""
    src = Image.open(LOGO_SRC).convert("RGBA")
    target = 256
    # вписываем квадрат целиком, сохраняя пропорции
    scale = min(target / src.width, target / src.height)
    new_size = (max(1, round(src.width * scale)), max(1, round(src.height * scale)))
    mark = src.resize(new_size, Image.LANCZOS)

    bg = Image.new("RGB", (target, target), NAVY)
    bg_rgba = bg.convert("RGBA")
    bg_rgba.paste(mark, ((target - new_size[0]) // 2, (target - new_size[1]) // 2), mark)
    return bg_rgba.convert("RGB")


# --------------------------------------------------------------------------
# 3. Сборка + проверка
# --------------------------------------------------------------------------
def verify(path: Path, expect_size: tuple) -> dict:
    img = Image.open(path)
    info = {
        "path": str(path),
        "size": img.size,
        "mode": img.mode,
        "bytes": path.stat().st_size,
    }
    assert img.size == expect_size, f"{path.name}: размер {img.size} != {expect_size}"
    assert img.mode == "RGB", f"{path.name}: режим {img.mode} != RGB"
    assert info["bytes"] < 1024 * 1024, f"{path.name}: {info['bytes']} байт >= 1 МБ"
    return info


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    creative = build_creative()
    creative.save(OUT_CREATIVE, "PNG", optimize=True)

    logo = build_logo()
    logo.save(OUT_LOGO, "PNG", optimize=True)

    preview = creative.copy()
    preview = preview.resize((300, 300), Image.LANCZOS)
    preview.save(OUT_PREVIEW, "PNG", optimize=True)

    rows = [
        verify(OUT_CREATIVE, (600, 600)),
        verify(OUT_LOGO, (256, 256)),
        verify(OUT_PREVIEW, (300, 300)),
    ]
    print("=== ГОТОВО ===")
    for r in rows:
        print(
            f"{Path(r['path']).name:28s} {r['size'][0]}x{r['size'][1]}  "
            f"{r['mode']}  {r['bytes'] / 1024:.1f} КБ"
        )
    print("\nИсходные страницы продукта:")
    for p in (PAGE_COVER, PAGE_LEFT, PAGE_RIGHT):
        print("  -", p)


if __name__ == "__main__":
    main()
