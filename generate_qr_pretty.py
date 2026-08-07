import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

URL = "https://hibiscusy.github.io/EazinOC/"

# ---------- fonts (Windows CJK fallback) ----------
def load_font(candidates, size):
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()

CN_B = ["C:/Windows/Fonts/msyhbd.ttc", "C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/msyh.ttc"]
CN_R = ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/msyhbd.ttc"]
title_font = load_font(CN_B, 72)
sub_font = load_font(CN_R, 32)
hint_font = load_font(CN_R, 30)

# ---------- QR code (high contrast: dark modules on white) ----------
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=16, border=4)
qr.add_data(URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="#0e1a3a", back_color="white").convert("RGB")
PAD = 24
qr_frame = Image.new("RGB", (qr_img.width + 2 * PAD, qr_img.height + 2 * PAD), "white")
qr_frame.paste(qr_img, (PAD, PAD))

# ---------- canvas ----------
W, H = 1080, 1440
canvas = Image.new("RGB", (W, H))
d = ImageDraw.Draw(canvas)

# vertical gradient background (deep blue -> near black)
top = (10, 20, 48)
bot = (5, 6, 15)
for y in range(H):
    t = y / (H - 1)
    r = int(top[0] + (bot[0] - top[0]) * t)
    g = int(top[1] + (bot[1] - top[1]) * t)
    b = int(top[2] + (bot[2] - top[2]) * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# stars
random.seed(7)
for _ in range(180):
    x = random.randint(0, W)
    y = random.randint(0, H)
    rr = random.choice([1, 1, 1, 2])
    br = random.randint(140, 255)
    d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(int(br * 0.8), int(br * 0.85), 255))
    if random.random() < 0.05:
        d.ellipse([x - rr * 3, y - rr * 3, x + rr * 3, y + rr * 3], fill=(br // 7, br // 7, br // 5))

# ---------- helpers ----------
def hgrad(size, c1, c2):
    w, h = size
    grad = Image.new("RGB", size)
    for x in range(w):
        t = x / (w - 1)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        grad.paste(Image.new("RGB", (1, h), (r, g, b)), (x, 0))
    return grad

def gradient_text(canvas, text, font, y, c1, c2):
    tmp = ImageDraw.Draw(canvas)
    bb = tmp.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    x = (W - tw) // 2 - bb[0]
    ty = y - bb[1]
    mask = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(mask).text((x, ty), text, font=font, fill=255)
    grad = hgrad(canvas.size, c1, c2)
    canvas.paste(grad, (0, 0), mask)

def center_text(draw, text, font, y, color):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    x = (W - tw) // 2 - bb[0]
    draw.text((x, y - bb[1]), text, font=font, fill=color)

# ---------- white rounded card holding the QR ----------
pw = qr_frame.width + 100
ph = qr_frame.height + 100
px = (W - pw) // 2
py = 450

shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle(
    [px + 10, py + 16, px + pw + 10, py + ph + 16], radius=44, fill=(0, 0, 0, 150))
shadow = shadow.filter(ImageFilter.GaussianBlur(22))
canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow).convert("RGB")
d = ImageDraw.Draw(canvas)
d.rounded_rectangle([px, py, px + pw, py + ph], radius=44, fill="#fbfcff", outline="#cdd6f5", width=2)
qx = px + (pw - qr_frame.width) // 2
qy = py + (ph - qr_frame.height) // 2
canvas.paste(qr_frame, (qx, qy))

# ---------- texts ----------
gradient_text(canvas, "蒲熠星 OC 宇宙", title_font, 210, (90, 176, 255), (255, 143, 199))
# decorative gradient line under title
line_w = 440
lx = (W - line_w) // 2
line_img = hgrad((line_w, 4), (90, 176, 255), (255, 143, 199))
canvas.paste(line_img, (lx, 312))
center_text(d, "扫码进入 · 星际猎手的世界", sub_font, 340, (174, 184, 208))
center_text(d, "长按识别二维码 · 探索完整 OC 宇宙", hint_font, H - 150, (138, 147, 168))
center_text(d, "hibiscusy.github.io/EazinOC", hint_font, H - 100, (110, 118, 140))

out = "qrcode-oc-pretty.png"
canvas.save(out)
print("SAVED", out, canvas.size)
