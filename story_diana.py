import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '.')
from shimmer_style import caps_font, script_font, gold_text, white_text, paste, ink_size, sans
from story_nativo_lib import emoji
SRC, OUT = sys.argv[1], sys.argv[2]
W, H, FPS = 720, 1280, 30
o = Image.new('RGBA', (W, H), (0,0,0,0))

def pill(text, emo, cy, size, fg, bg, pad=(20, 11), r=15):
    f = sans(size, 700); tw = f.getlength(text)
    e = emoji(emo, int(size*1.05)) if emo else None
    tot = tw + (e.width + 9 if e else 0)
    asc, desc = f.getmetrics(); h = asc + desc
    x0 = W/2 - tot/2
    d = ImageDraw.Draw(o)
    d.rounded_rectangle([x0-pad[0], cy-h/2-pad[1], x0+tot+pad[0], cy+h/2+pad[1]], radius=r, fill=bg)
    d.text((x0, cy-h/2), text, font=f, fill=fg)
    if e: o.alpha_composite(e, (int(x0+tw+9), int(cy-e.height/2)))

BK, WH = (20,20,20,255), (255,255,255,255)
pill('por que ela se chama Diana?', '💙', 82, 34, BK, WH)
lines = ['o anel de noivado da princesa Diana', 'era justamente uma safira oval', 'rodeada de pedras.',
         'é a referência mais famosa', 'desse modelo no mundo']
y = 150
for k, ln in enumerate(lines):
    pill(ln, '👑' if k == 4 else None, y + (12 if k >= 3 else 0), 25, WH, (0,0,0,165), pad=(15, 7), r=12)
    y += 45

# photo sticker: the reference, downscaled only, white border, slight tilt
ref = Image.open('/root/.claude/uploads/081c4020-c9a3-5394-8b04-d630e012eb6b/99a61ffd-image.jpg').convert('RGB')
ref = ref.crop((40, 40, 560, 430)).resize((228, 171), Image.LANCZOS)
b = 8
st = Image.new('RGBA', (ref.width + 2*b, ref.height + 2*b), (0,0,0,0))
m = Image.new('L', st.size, 0); ImageDraw.Draw(m).rounded_rectangle([0,0,st.width-1,st.height-1], radius=14, fill=255)
wb = Image.new('RGBA', st.size, (255,255,255,255)); wb.putalpha(m); st.alpha_composite(wb)
pm = Image.new('L', ref.size, 0); ImageDraw.Draw(pm).rounded_rectangle([0,0,ref.width-1,ref.height-1], radius=9, fill=255)
r2 = ref.convert('RGBA'); r2.putalpha(pm); st.alpha_composite(r2, (b, b))
st = st.rotate(4, resample=Image.BICUBIC, expand=True)
shd = Image.new('RGBA', st.size, (0,0,0,0)); shd.putalpha(st.split()[3].filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v*0.35)))
SX, SY = 466, 368
o.alpha_composite(shd, (SX+2, SY+5)); o.alpha_composite(st, (SX, SY))
def tagp(text, emo, x, y):
    f = sans(22, 700); tw = f.getlength(text); e = emoji(emo, 24)
    w = tw + e.width + 7 + 28; x = x - w; asc, desc = f.getmetrics(); h = asc + desc + 14
    d = ImageDraw.Draw(o); d.rounded_rectangle([x, y, x+w, y+h], radius=12, fill=WH)
    d.text((x+14, y+7), text, font=f, fill=BK); o.alpha_composite(e, (int(x+14+tw+7), int(y+h/2-e.height/2)))
tagp('o anel original', '👑', SX - 4, SY + st.height - 78)

# brand card at the bottom, soft shade only behind it
yy = np.arange(H, dtype=np.float32)[:, None]
a = np.clip((yy - 985) / 130, 0, 1) ** 1.2 * 0.80
sh = Image.new('RGBA', (W, H), (20,16,12,0)); sh.putalpha(Image.fromarray((np.broadcast_to(a,(H,W))*255).astype(np.uint8)))
card = Image.new('RGBA', (W, H), (0,0,0,0)); card.alpha_composite(sh)
cap = white_text('ANEL', caps_font(28, 600), 3); nm = gold_text('Diana', script_font(100))
cw, ch = ink_size(cap); sw, shh = ink_size(nm); left = W/2 - sw/2
top = 1040
paste(card, cap, left + sw*0.06, top); paste(card, nm, left, top + ch + 5)
y2 = top + ch + 5 + shh + 24
for ln in ['OURO AMARELO 18K MACIÇO', 'SAFIRA OVAL 6X8 MM', '17 MOISSANITES DE 1,25 MM AO REDOR']:
    L = white_text(ln, caps_font(20, 600), 2); paste(card, L, W/2, y2, anchor='center'); y2 += ink_size(L)[1] + 11
print('card bottom', y2)
card.alpha_composite(o); o = card
OV = np.asarray(o, np.float32); AL = OV[..., 3:4]/255; RGB = OV[..., :3]
def comp(f): return f*(1-AL) + RGB*AL

if len(sys.argv) > 3:
    for t in map(float, sys.argv[3:]):
        subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',SRC,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','_f.raw'])
        f = np.fromfile('_f.raw', np.uint8).reshape(H,W,3).astype(np.float32)
        Image.fromarray(comp(f).astype(np.uint8)).save(f'sd_{t}.jpg', quality=90)
    sys.exit()
enc = subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-',
    '-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-shortest','-c:v','libx264','-preset','slow','-crf','12','-pix_fmt','yuv420p',
    '-profile:v','high','-movflags','+faststart','-c:a','aac','-b:a','128k',OUT], stdin=subprocess.PIPE)
n = 0
for rep in range(2):  # plays twice so there is time to read
    dec = subprocess.Popen(['ffmpeg','-loglevel','error','-i',SRC,'-vf','fps=30','-f','rawvideo','-pix_fmt','rgb24','-'], stdout=subprocess.PIPE)
    while True:
        b = dec.stdout.read(W*H*3)
        if len(b) < W*H*3: break
        enc.stdin.write(comp(np.frombuffer(b, np.uint8).reshape(H,W,3).astype(np.float32)).astype(np.uint8).tobytes()); n += 1
    dec.wait()
enc.stdin.close(); enc.wait(); print('frames', n)
