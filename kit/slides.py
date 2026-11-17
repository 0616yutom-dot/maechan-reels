#!/usr/bin/env python3
"""写真スライド投稿（縦4:5＝1080×1350・JPEG）を自宅写真からまとめて作る。
使い方: python3 kit/slides.py <設定.json> <出力フォルダ>   → 01.jpg, 02.jpg … と確認用の _sheet.jpg ができる
設定.json は場面のリスト。例:
[
 {"type":"cover","photo":"ldk_pro","label":"ROOM TOUR","title":["吹き抜けのある","わが家を公開"],"sub":"スワイプして見てください →"},
 {"type":"photo","photo":"kitchen_pro","label":"01","title":["キッチン"],"sub":"木目の天井と間接照明","yoff":0.35},
 {"type":"text","photo":"fan","label":"POINT","title":["対策は3つ"],"lines":["① 断熱性能を上げる","② 天井にファンをつける","③ 寝室を離す"]},
 {"type":"cta","photo":"fukinuke_day","title":["家づくりの相談、","無料で受けています"],"word":"相談"}
]
- cover=表紙（大きな見出し。最後の行が金色）／photo=写真が主役で下に短い名前／text=写真を暗くして箇条書き／cta=最後の案内（DMの合言葉）
- yoff=写真の上下の切り取り位置（0=上、1=下。既定0.45）。"dark":0.2 などで写真を暗くできる。
- 見出しは1行10文字まで、sub と lines は1行20文字まで（長いとエラーで止まる）。枚数は2〜10枚。
"""
import sys, json, os
from PIL import Image, ImageDraw, ImageFont
FP = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
W, H = 1080, 1350
GOLD = (243, 223, 160); CREAM = (241, 232, 208); NAVY = (16, 28, 45)
def F(s): return ImageFont.truetype(FP, s, index=0)
def base(name, yoff=0.45, dark=0.0):
    im = Image.open(f"kit/h/{name}.jpg").convert("RGB")
    h = round(im.height * W / im.width)
    if h >= H:
        im = im.resize((W, h), Image.LANCZOS); y = round((h - H) * yoff); im = im.crop((0, y, W, y + H))
    else:
        w = round(im.width * H / im.height); im = im.resize((w, H), Image.LANCZOS); x = (w - W) // 2; im = im.crop((x, 0, x + W, H))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for i in range(560):
        d.line([(0, H - 560 + i), (W, H - 560 + i)], fill=NAVY + (int(230 * (i / 560) ** 1.3),))
    if dark: d.rectangle([0, 0, W, H], fill=NAVY + (int(255 * dark),))
    return Image.alpha_composite(im.convert("RGBA"), ov)
def c(d, y, t, f, fill):
    w = d.textlength(t, font=f)
    if w > 1000: raise SystemExit(f"文字が長すぎます（{t}）")
    d.text(((W - w) / 2 + 3, y + 3), t, font=f, fill=(0, 0, 0, 160)); d.text(((W - w) / 2, y), t, font=f, fill=fill)
def make(s):
    t = s["type"]; title = s.get("title", [])
    if t == "cover":
        im = base(s["photo"], s.get("yoff", 0.45), s.get("dark", 0.18)); d = ImageDraw.Draw(im)
        y = 1230 - len(title) * 120 - 70
        c(d, y, s.get("label", ""), F(36), GOLD); y += 62
        for i, x in enumerate(title):
            c(d, y, x, F(96), GOLD if i == len(title) - 1 and len(title) > 1 else CREAM); y += 120
        if s.get("sub"): c(d, 1250, s["sub"], F(36), CREAM)
    elif t == "photo":
        im = base(s["photo"], s.get("yoff", 0.45), s.get("dark", 0)); d = ImageDraw.Draw(im)
        c(d, 1075, s.get("label", ""), F(34), GOLD); d.line([(W / 2 - 40, 1128), (W / 2 + 40, 1128)], fill=GOLD, width=2)
        c(d, 1145, title[0], F(68), CREAM)
        if s.get("sub"): c(d, 1245, s["sub"], F(34), CREAM)
    elif t == "text":
        im = base(s["photo"], s.get("yoff", 0.45), s.get("dark", 0.72)); d = ImageDraw.Draw(im)
        lines = s.get("lines", []); y = (H - (70 + len(title) * 105 + 50 + len(lines) * 84)) // 2
        c(d, y, s.get("label", ""), F(36), GOLD); y += 70
        for x in title: c(d, y, x, F(84), GOLD); y += 105
        y += 50
        for x in lines: c(d, y, x, F(50), CREAM); y += 84
    elif t == "cta":
        im = base(s["photo"], s.get("yoff", 0.4), s.get("dark", 0.72)); d = ImageDraw.Draw(im)
        y = 380
        for i, x in enumerate(title):
            c(d, y, x, F(84), GOLD if i == len(title) - 1 else CREAM); y += 110
        word = s.get("word", "相談")
        c(d, 680, f"DMにこの{len(word)}文字を送るだけ", F(40), CREAM)
        ww = d.textlength(word, font=F(64)); bw = max(400, ww + 160)
        d.rounded_rectangle([(W - bw) / 2, 760, (W + bw) / 2, 880], radius=60, fill=CREAM)
        d.text(((W - ww) / 2, 775), word, font=F(64), fill=NAVY)
        c(d, 960, "@maechan_0616", F(40), GOLD)
        c(d, 1020, "宅建士が「家づくりで損しない知識」を発信中", F(32), CREAM)
    else: raise SystemExit("type は cover / photo / text / cta")
    return im.convert("RGB")
def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8")); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    if not 2 <= len(spec) <= 10: raise SystemExit("枚数は2〜10枚")
    ims = [make(s) for s in spec]
    for i, im in enumerate(ims): im.save(f"{out}/{i+1:02d}.jpg", quality=92)
    sh = Image.new("RGB", (len(ims) * 324, 405))
    for i, im in enumerate(ims): sh.paste(im.resize((324, 405)), (i * 324, 0))
    sh.save(f"{out}/_sheet.jpg", quality=80); print(out, len(ims), "枚")
main()
