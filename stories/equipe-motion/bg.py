"""Background plate (60 s): attendance clips from the Drive, slowed 1.3x, upscaled + softly blurred, crossfaded."""
import subprocess
V = '/home/user/print/videos-drive/'
# opens with the door + the store, no repeated clips, ends with both sitting at the desk
SEG = [('IMG_2564.MOV', 0, 10.8), ('IMG_0250.MOV', 0, 10.1), ('IMG_0255.MOV', 0, 5.7), ('IMG_0258.MOV', 0, 4.4),
       ('IMG_0259.MOV', 0, 10.1), ('IMG_2564.MOV', 10.8, 18.5)]
SL, XF = 1.3, 0.6
ins, fl, durs = [], [], []
for i, (f, a, b) in enumerate(SEG):
    ins += ['-i', V + f]
    fl.append(f"[{i}:v]trim={a}:{b},setpts={SL}*(PTS-STARTPTS),fps=30,scale=1080:1920:flags=lanczos,hqdn3d=3:2:6:5,gblur=sigma=1.6,"
              f"eq=contrast=1.03:saturation=0.92:gamma=1.06,colortemperature=temperature=6200:mix=0.3,format=yuv420p[s{i}]")
    durs.append((b - a) * SL)
cur, t = 's0', durs[0]
for i in range(1, len(SEG)):
    off = t - XF
    fl.append(f"[{cur}][s{i}]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}]"); cur = f'x{i}'; t = off + durs[i]
print('total', t)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fl), '-map', f'[{cur}]', '-t', '60',
                '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', 'bg.mp4'], check=True)
