#!/usr/bin/env python3
"""ストーリーズ用の画像（縦1080×1920・JPEG）を自宅写真から1枚作る。
使い方: python3 kit/story.py <写真名(kit/h/の拡張子なし)> <小見出し> <大見出し(｜で改行)> <本文(｜で改行。空でも可)> <出力.jpg> [dark]
例: python3 kit/story.py kitchen_pro "家づくりメモ" "キッチンは｜高さで決まる" "毎日立つ場所だから｜ショールームで必ず立ってみる" stories/2026-11-18_08.jpg
大見出しは1行9文字まで、本文は1行18文字まで。dark を付けると写真全体を暗くする（明るい写真で文字が読みにくいとき）。
"""
import sys
from PIL import Image, ImageDraw, ImageFont
FP = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
W, H = 1080, 1920
GOLD = (243, 223, 160); CREAM = (241, 232, 208); NAVY = (16, 28, 45)
def F(s): return ImageFont.truetype(FP, s, index=0)
def main():
    photo, label, head, body, out = sys.argv[1:6]
    dark = len(sys.argv) > 6 and sys.argv[6] == "dark"
    im = Image.open(f"kit/h/{photo}.jpg").convert("RGB")
    w = round(im.width * H / im.height)
    if w < W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS); im = im.crop((0, (im.height - H) // 2, W, (im.height - H) // 2 + H))
    else:
        im = im.resize((w, H), Image.LANCZOS); im = im.crop(((w - W) // 2, 0, (w - W) // 2 + W, H))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    if dark: d.rectangle([0, 0, W, H], fill=NAVY + (140,))
    for i in range(1100):
        d.line([(0, H - 1100 + i), (W, H - 1100 + i)], fill=NAVY + (int(235 * (i / 1100) ** 1.1),))
    im = Image.alpha_composite(im.convert("RGBA"), ov); d = ImageDraw.Draw(im)
    def c(y, t, f, fill):
        tw = d.textlength(t, font=f)
        if tw > 1000: raise SystemExit(f"文字が長すぎます（{t}）")
        d.text(((W - tw) / 2 + 3, y + 3), t, font=f, fill=(0, 0, 0, 170)); d.text(((W - tw) / 2, y), t, font=f, fill=fill)
    heads = head.split("｜"); bodies = [b for b in body.split("｜") if b]
    y = 1500 - len(heads) * 130 - len(bodies) * 66 - 110
    c(y, label, F(40), GOLD); y += 70
    d.line([(W / 2 - 50, y), (W / 2 + 50, y)], fill=GOLD, width=3); y += 30
    for i, t in enumerate(heads):
        c(y, t, F(104), GOLD if i == len(heads) - 1 and len(heads) > 1 else CREAM); y += 130
    y += 20
    for t in bodies:
        c(y, t, F(48), CREAM); y += 66
    c(1530, "DMに「相談」で無料相談", F(40), CREAM)
    c(1590, "@maechan_0616", F(40), GOLD)
    im.convert("RGB").save(out, quality=90)
    print(out)
main()
