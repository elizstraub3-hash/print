import subprocess, numpy as np, cv2, sys
U = '/root/.claude/uploads/081c4020-c9a3-5394-8b04-d630e012eb6b/'
DN = "hqdn3d=2:1.5:6:5"
IN = DN + ",eq=contrast=1.05:saturation=1.04:gamma=1.05,colortemperature=temperature=6000:mix=0.35"
OUTD = DN + ",eq=contrast=1.07:saturation=1.08:gamma=1.14:brightness=0.015,colortemperature=temperature=5200:mix=0.45"
SEG = [('9361a9a7-IMG_0248.MOV', 1.0, 3.4, IN), ('9361a9a7-IMG_0248.MOV', 10.6, 13.8, IN)]
sr = cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel('FSRCNN_x2.pb'); sr.setModel('fsrcnn', 2)
W, H = 1080, 1920
only = [int(x) for x in sys.argv[1:]]
for i, (f, a, b, g) in enumerate(SEG):
    if only and i not in only: continue
    vf = f"trim={a}:{b},setpts=PTS-STARTPTS,fps=30,{g}"
    # stabilise every clip (the office one a bit stronger, the 3D sign depends on it)
    sm, zm = (25, 4) if False else (18, 5)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', U + f, '-vf', f"trim={a}:{b},setpts=PTS-STARTPTS,fps=30,vidstabdetect=shakiness=6:accuracy=15:result=hd/jt{i}.trf", '-f', 'null', '-'], check=True)
    vf = f"trim={a}:{b},setpts=PTS-STARTPTS,fps=30,vidstabtransform=input=hd/jt{i}.trf:smoothing={sm}:zoom={zm}:optzoom=0:interpol=bicubic,{g}"
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', U + f, '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                            '-an', '-c:v', 'libx264', '-crf', '10', '-preset', 'medium', '-pix_fmt', 'yuv420p', f'hd/j{i}.mp4'], stdin=subprocess.PIPE)
    n = 0
    while True:
        b_ = dec.stdout.read(320 * 568 * 3)
        if len(b_) < 320 * 568 * 3: break
        im = np.frombuffer(b_, np.uint8).reshape(568, 320, 3)
        up = cv2.resize(sr.upsample(im), (W, H), interpolation=cv2.INTER_LANCZOS4)
        bl = cv2.GaussianBlur(up, (0, 0), 2.0); up = cv2.addWeighted(up, 1.35, bl, -0.35, 0)   # gentle unsharp
        enc.stdin.write(up.tobytes()); n += 1
    enc.stdin.close(); enc.wait(); print(i, n, flush=True)
