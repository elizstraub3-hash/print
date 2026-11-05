import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, '.')
from shimmer_style import caps_font, script_font, gold_text, white_text, paste, ink_size
S = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/'
SRC, OUT = sys.argv[1], sys.argv[2]
TEXT = sys.argv[3].split('|')
NAME = sys.argv[4]
W, H, FPS = 720, 1280, 30
T_OUT, T_IN = 10.2, 10.6   # hook leaves, product card enters

def hook():
    F = ImageFont.truetype(S + 'fonts/Montserrat.ttf', 48); F.set_variation_by_axes([900])
    lay = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(lay)
    for k, ln in enumerate(TEXT):
        d.text(((W - F.getlength(ln)) / 2, 250 + k*64), ln, font=F, fill=(255,255,255,255), stroke_width=5, stroke_fill=(15,15,15,255))
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    sh.putalpha(lay.split()[3].filter(ImageFilter.GaussianBlur(7)).point(lambda v: int(v*0.55)))
    o = Image.new('RGBA', (W, H), (0,0,0,0)); o.alpha_composite(sh, (0,5)); o.alpha_composite(lay); return o

def card():
    o = Image.new('RGBA', (W, H), (0,0,0,0))
    # soft shade only behind the text block (top), never over the piece
    y = np.arange(H, dtype=np.float32)[:, None]
    a = np.clip(1 - y / 520, 0, 1) ** 1.6 * 0.62
    sh = Image.new('RGBA', (W, H), (20,16,12,0)); sh.putalpha(Image.fromarray((np.broadcast_to(a,(H,W))*255).astype(np.uint8)))
    o.alpha_composite(sh)
    cx = W / 2
    cap = white_text('ANEL', caps_font(40, 600), 3)
    nm = gold_text(NAME, script_font(150))
    cw, ch = ink_size(cap); sw, shh = ink_size(nm)
    left = cx - sw / 2
    paste(o, cap, left + sw * 0.06, 70)
    paste(o, nm, left, 70 + ch + 6)
    yy = 70 + ch + 6 + shh + 34
    for ln in ['OURO AMARELO 18K MACIÇO', 'SAFIRA OVAL 6X8 MM', '17 MOISSANITES DE 1,25 MM AO REDOR']:
        lay = white_text(ln, caps_font(25, 600), 2)
        paste(o, lay, cx, yy, anchor='center'); yy += ink_size(lay)[1] + 16
    print('card bottom', yy)
    return o

HK, CD = [np.asarray(x, np.float32) for x in (hook(), card())]
def ease(x): x = min(max(x,0),1); return x*x*(3-2*x)
def comp(f, L, k):
    al = L[..., 3:4] / 255 * k
    return f*(1-al) + L[..., :3]*al

if len(sys.argv) > 5:  # preview frames
    for t in map(float, sys.argv[5:]):
        subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',SRC,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24',S+'_f.raw'])
        f = np.fromfile(S+'_f.raw', np.uint8).reshape(H,W,3).astype(np.float32)
        f = comp(f, HK, 1-ease((t-T_OUT)/0.35)); f = comp(f, CD, ease((t-T_IN)/0.6))
        Image.fromarray(f.astype(np.uint8)).save(S+f'pd_{t}.jpg', quality=90)
    sys.exit()
dec = subprocess.Popen(['ffmpeg','-loglevel','error','-i',SRC,'-vf','fps=30','-f','rawvideo','-pix_fmt','rgb24','-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-',
    '-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-shortest','-c:v','libx264','-preset','slow','-crf','12','-pix_fmt','yuv420p',
    '-profile:v','high','-movflags','+faststart','-c:a','aac','-b:a','128k',OUT], stdin=subprocess.PIPE)
n = 0
while True:
    b = dec.stdout.read(W*H*3)
    if len(b) < W*H*3: break
    t = n / FPS
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
    k1 = 1 - ease((t - T_OUT) / 0.35); k2 = ease((t - T_IN) / 0.6)
    if k1 > 0: f = comp(f, HK, k1)
    if k2 > 0: f = comp(f, CD, k2)
    enc.stdin.write(f.astype(np.uint8).tobytes()); n += 1
enc.stdin.close(); enc.wait(); print('frames', n)
