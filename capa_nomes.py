import sys, math
SCR = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/'
src = open(SCR + 'capas_icones.py').read()
src = src[:src.index('ICONS =')] + src[src.index('def ring'):src.index('os.makedirs')]
OUTF = sys.argv[1]
sys.argv = [sys.argv[0], '/tmp']
exec(src)

def i_nomes():
    """Name tag, tilted, with a short string curling out of its hole."""
    m, d = canvas()
    a = math.radians(-35)
    w, h, tip = 1020, 580, 300
    cx, cy = C / 2 + 150, C / 2 + 110
    def rot(x, y):
        return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))
    pts = [(-w/2 + tip, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2 + tip, h/2), (-w/2, 0)]
    poly(d, [rot(*p) for p in pts])
    hx, hy = rot(-w/2 + tip * 0.85, 0)
    circle(d, hx, hy, 70, int(LW * 0.75))
    # cubic bezier string from the hole edge, curling up-left
    p0 = (hx - 50, hy - 50); p1 = (hx - 330, hy - 330); p2 = (hx - 120, hy - 640); p3 = (hx - 470, hy - 600)
    curve = []
    for i in range(121):
        t = i / 120
        x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t*t*p2[0] + t**3*p3[0]
        y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t*t*p2[1] + t**3*p3[1]
        curve.append((x, y))
    d.line(curve, fill=255, width=int(LW * 0.75), joint='curve')
    r = int(LW * 0.375)
    for (x, y) in (curve[0], curve[-1]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    return m

ic = gold_fill(i_nomes().resize((660, 660), Image.LANCZOS))
img = Image.new('RGBA', (W, H), BG + (255,))
ring(img, 460, 22)
img.alpha_composite(ic, (W // 2 - ic.width // 2, H // 2 - ic.height // 2))
save_hq(img, OUTF)
sq = img.crop((0, (H - W) // 2, W, (H - W) // 2 + W)).resize((300, 300), Image.LANCZOS)
sq.convert('RGB').save(SCR + 'capa_nomes_prev.jpg')
