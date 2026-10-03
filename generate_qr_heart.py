import qrcode
import math
from PIL import Image, ImageDraw

# ============================================================
# НАСТРОЙКИ
# ============================================================
URL = "https://192.168.1.101:5000"

SIZE = 1200
QR_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
HEART_COLOR = (0, 200, 83)

HEART_RATIO = 0.20

OUTPUT = "surprise_qr_heart.png"

# ============================================================
# ШАГ 1. QR-код
# ============================================================
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=20,
    border=3,
)
qr.add_data(URL)
qr.make(fit=True)

qr_img = qr.make_image(
    fill_color=QR_COLOR,
    back_color=BG_COLOR
).convert("RGB")

qr_img = qr_img.resize((SIZE, SIZE), Image.LANCZOS)

# ============================================================
# ШАГ 2. Стираем квадрат в центре
# ============================================================
draw = ImageDraw.Draw(qr_img)

cx = SIZE // 2
cy = SIZE // 2

heart_size = int(SIZE * HEART_RATIO)
pad_square = int(heart_size * 0.75)

draw.rectangle(
    [cx - pad_square, cy - pad_square, cx + pad_square, cy + pad_square],
    fill=BG_COLOR
)

# ============================================================
# ШАГ 3. Красивое сердце (с инверсией Y)
# ============================================================
def heart_points(cx, cy, size, steps=500):
    points = []
    for i in range(steps):
        t = (i / steps) * 2 * math.pi

        x = 16 * math.sin(t) ** 3
        y = (13 * math.cos(t)
             - 5 * math.cos(2 * t)
             - 2 * math.cos(3 * t)
             - math.cos(4 * t))

        # Инверсия Y — чтобы сердце было вверх ногами НЕ перевёрнутым
        y = -y

        points.append((x, y))

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    w = max_x - min_x
    h = max_y - min_y
    scale = size / max(w, h)

    offset_x = cx - (min_x + max_x) / 2 * scale
    offset_y = cy - (min_y + max_y) / 2 * scale

    return [
        (x * scale + offset_x, y * scale + offset_y)
        for x, y in points
    ]


heart_polygon = heart_points(cx, cy, heart_size)
draw.polygon(heart_polygon, fill=HEART_COLOR)

# ============================================================
# ШАГ 4. Сохраняем
# ============================================================
qr_img.save(OUTPUT)
print(f"✅ Готово! Файл: {OUTPUT}")