import qrcode

URL = "https://hibiscusy.github.io/EazinOC/"
OUT = "qrcode-oc-universe.png"

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,  # 中等容错，图片被压缩仍能扫
    box_size=20,
    border=6,  # 较大静区，避免被笔记裁切干扰
)
qr.add_data(URL)
qr.make(fit=True)

img = qr.make_image(fill_color="#0b0f1a", back_color="#ffffff")
img.save(OUT)
print(f"saved {OUT} size={img.size}")
