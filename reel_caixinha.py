import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/'
SRC, OUT = sys.argv[1], sys.argv[2]
TEXT = sys.argv[3].split('|')
W, H = 720, 1280
F = ImageFont.truetype(S + 'fonts/Montserrat.ttf', 48); F.set_variation_by_axes([900])
lay = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(lay)
lh, y0 = 64, 250
for k, ln in enumerate(TEXT):
    d.text(((W - F.getlength(ln)) / 2, y0 + k*lh), ln, font=F, fill=(255,255,255,255), stroke_width=5, stroke_fill=(15,15,15,255))
sh = Image.new('RGBA', (W, H), (0,0,0,0))
sh.putalpha(lay.split()[3].filter(ImageFilter.GaussianBlur(7)).point(lambda v: int(v*0.55)))
CAP = Image.new('RGBA', (W, H), (0,0,0,0)); CAP.alpha_composite(sh, (0,5)); CAP.alpha_composite(lay)
capa = np.asarray(CAP, np.float32); al = capa[..., 3:4] / 255; rgb = capa[..., :3]
dec = subprocess.Popen(['ffmpeg','-loglevel','error','-i',SRC,'-vf','fps=30','-f','rawvideo','-pix_fmt','rgb24','-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-',
    '-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-shortest','-c:v','libx264','-preset','slow','-crf','12','-pix_fmt','yuv420p',
    '-profile:v','high','-movflags','+faststart','-c:a','aac','-b:a','128k',OUT], stdin=subprocess.PIPE)
n = 0
while True:
    b = dec.stdout.read(W*H*3)
    if len(b) < W*H*3: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
    enc.stdin.write((f*(1-al) + rgb*al).astype(np.uint8).tobytes()); n += 1
enc.stdin.close(); enc.wait(); print('frames', n)
