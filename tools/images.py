"""Turn the Instagram originals into web-ready images and build og.jpg."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "originals", ROOT / "img"

# name: (source, crop box as fractions or None)
JOBS = {
    "roof": ("p01.jpg", None),
    "underside": ("p03.jpg", (0, 0, 1, 0.78)),
    "wall": ("p05.jpg", None),
    "inverter": ("p06.jpg", None),
    "fan": ("p08.jpg", None),
    "commercial": ("p11.jpg", (0, 0.12, 1, 0.72)),
}

def prep(src, crop):
    im = Image.open(SRC / src).convert("RGB")
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0]*w), int(crop[1]*h), int(crop[2]*w), int(crop[3]*h)))
    im = ImageEnhance.Contrast(im).enhance(1.04)
    return im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))

for name, (src, crop) in JOBS.items():
    im = prep(src, crop)
    im.save(OUT / f"{name}.webp", quality=80, method=6)
    print(name, im.size, (OUT / f"{name}.webp").stat().st_size // 1024, "KB")

logo = Image.open(SRC / "logo.jpg").convert("RGB")
logo.save(OUT / "logo.webp", quality=90)

# og.jpg 1200x630 for WhatsApp/Facebook previews
W, H = 1200, 630
og = Image.new("RGB", (W, H), "#0E2A47")
d = ImageDraw.Draw(og)
for y in range(H):  # warm glow rising from the bottom left, like sunrise after an outage
    pass
glow = Image.new("RGB", (W, H), "#F59A23")
mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(mask).ellipse((-300, 330, 700, 1130), fill=110)
og = Image.composite(glow, og, mask.filter(ImageFilter.GaussianBlur(120)))
photo = prep("p06.jpg", (0, 0.02, 1, 0.98))
photo.thumbnail((420, 560))
og.paste(photo, (W - photo.width - 60, (H - photo.height) // 2))
d = ImageDraw.Draw(og)
F = "C:/Windows/Fonts/"
big = ImageFont.truetype(F + "seguibl.ttf", 64)
mid = ImageFont.truetype(F + "segoeui.ttf", 30)
small = ImageFont.truetype(F + "seguisb.ttf", 26)
d.text((64, 70), "Waltnet Energy", font=small, fill="#F59A23")
d.multiline_text((64, 120), "When NEPA takes\nlight, your house\nstays on.", font=big, fill="white", spacing=8)
d.text((64, 400), "Solar panels, inverters and batteries,\nsold and installed in Benin City.", font=mid, fill="#DCE6F0", spacing=6)
d.text((64, 520), "WhatsApp 0813 777 3440", font=small, fill="white")
og.save(ROOT / "og.jpg", quality=84, optimize=True)
print("og", (ROOT / "og.jpg").stat().st_size // 1024, "KB")
