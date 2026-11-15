"""HTMLアニメを1コマずつ撮って動画にする。
使い方: capture.py <html> <出力名> still t1,t2,...     … 確認用の静止画
        capture.py <html> <出力名> video 0,1.3,5.3,...  … シーン境界ごとに mp4 を作り連結
"""
import sys, os, subprocess, asyncio
from playwright.async_api import async_playwright

FPS = 30
html, out, mode, arg = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
only = set(sys.argv[5].split(',')) if len(sys.argv) > 5 else None  # 作り直すシーン番号
here = os.path.dirname(os.path.abspath(html))
ENC = ['-vf', 'scale=in_color_matrix=bt601:in_range=full:out_color_matrix=bt709:out_range=tv,format=yuv420p',
       '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS),
       '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-video_track_timescale', '15360']

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--font-render-hinting=none'])
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
        await pg.goto('file://' + os.path.abspath(html))
        await pg.evaluate('document.fonts.ready')
        if mode == 'still':
            for ts in arg.split(','):
                await pg.evaluate(f'render({ts})')
                await pg.screenshot(path=f'{out}_{ts}.jpg', type='jpeg', quality=80)
            await b.close(); return
        cuts = [float(x) for x in arg.split(',')]
        segs = []
        for i in range(len(cuts) - 1):
            seg = os.path.join(here, f'{out}_seg{i}.mp4'); segs.append(seg)
            if only and str(i) not in only and os.path.exists(seg): continue
            tmp = seg.replace('.mp4', '.tmp.mp4')
            ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', str(FPS), '-i', '-'] + ENC + [tmp], stdin=subprocess.PIPE)
            f0, f1 = round(cuts[i] * FPS), round(cuts[i + 1] * FPS)
            for f in range(f0, f1):
                await pg.evaluate(f'render({f / FPS})')
                ff.stdin.write(await pg.screenshot(type='jpeg', quality=92))
            ff.stdin.close()
            if ff.wait() != 0: raise SystemExit('ffmpeg failed')
            os.rename(tmp, seg); print('seg', i, f1 - f0, 'frames', flush=True)
        await b.close()
        lst = os.path.join(here, f'{out}_list.txt')
        open(lst, 'w').write(''.join(f"file '{s}'\n" for s in segs))
        subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', os.path.join(here, f'{out}_silent.mp4')])
asyncio.run(main())
