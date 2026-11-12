import cv2, numpy as np, subprocess, pickle, sys
from PIL import Image, ImageFilter
W, H, FPS = 1080, 1920, 30
TR = pickle.load(open('hd/track.pkl', 'rb')); CORN = TR['corners']
logo = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA')   # official logo, design untouched
LW, LH = 1000, 256
logo = logo.resize((LW, LH), Image.LANCZOS)
M = 60; CW, CH = LW + 2 * M, LH + 2 * M
la = np.asarray(logo, np.float32) / 255
# --- 3D sign: face + extruded sides (same logo, darker, stepped toward bottom-right) + soft cast shadow on the wall
canvas = np.zeros((CH, CW, 4), np.float32)
def put(arr, dx, dy, mul=1.0, a_mul=1.0):
    sub = canvas[M + dy:M + dy + LH, M + dx:M + dx + LW]
    rgb = arr[..., :3] * mul; a = arr[..., 3:4] * a_mul
    sub[..., :3] = rgb * a + sub[..., :3] * (1 - a); sub[..., 3:4] = a + sub[..., 3:4] * (1 - a)
sh = Image.fromarray((la[..., 3] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(7))
sha = np.asarray(sh, np.float32)[..., None] / 255
shadow = np.zeros((CH, CW, 4), np.float32); shadow[M + 22:M + 22 + LH, M + 26:M + 26 + LW, 3:4] = sha * 0.42
DEPTH = 9
for k in range(DEPTH, 0, -1):
    put(la, k, k, mul=0.38 + 0.25 * (DEPTH - k) / DEPTH)
put(la, 0, 0)
# plane -> reference frame (perspective of the wall, toward the corner on the left)
src = np.float32([[M, M], [M + LW, M], [M + LW, M + LH], [M, M + LH]])
dst = np.float32([[330, 268], [600, 203], [600, 292], [330, 338]])
P = cv2.getPerspectiveTransform(src, dst)
SHAPE = np.float32([[-202, -47], [202, -75], [202, 51], [-202, 65]])
_q0 = np.float32(CORN[126]).reshape(4, 2); REFD = np.linalg.norm(_q0[2] - _q0[0]) + np.linalg.norm(_q0[3] - _q0[1])
START = 45   # drop the first 1.5 s (the consultant looks at the camera)
def warp(layer, Hm):
    return cv2.warpPerspective(layer, Hm, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
def ease(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
src_v, out = sys.argv[1], sys.argv[2]; prev = sys.argv[3:]
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', src_v, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = None if prev else subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-an', '-c:v', 'libx264', '-crf', '10', '-preset', 'medium', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
n = 0
while True:
    b = dec.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    t = n / FPS; f = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
    if n < START:
        n += 1; continue
    t = (n - START) / FPS
    k = ease((t - 0.2) / 0.8)
    if k > 0 and n < len(CORN):
        q = np.float32(CORN[n]).reshape(4, 2); c = q.mean(0)
        sc = (np.linalg.norm(q[2] - q[0]) + np.linalg.norm(q[3] - q[1])) / REFD
        # upright sign: position and size follow the wall, the shape keeps a mild, constant perspective (no roll, no skew)
        Hm = cv2.getPerspectiveTransform(src, np.float32(c + SHAPE * sc))
        s_ = warp(shadow, Hm); f = f * (1 - s_[..., 3:4] * k)
        l_ = warp(canvas, Hm); a = l_[..., 3:4] * k
        f = f * (1 - a) + l_[..., :3] * a
    o = (np.clip(f, 0, 1) * 255).astype(np.uint8)
    if prev and any(abs(t - float(p)) < 0.017 for p in prev): Image.fromarray(o).save(f'hd/lg_{t:.1f}.jpg', quality=90)
    elif enc: enc.stdin.write(o.tobytes())
    n += 1
if enc: enc.stdin.close(); enc.wait()
print('frames', n)
