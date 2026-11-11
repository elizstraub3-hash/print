import subprocess, json
U = '/root/.claude/uploads/081c4020-c9a3-5394-8b04-d630e012eb6b/'
BASE = "hqdn3d=2:1.5:6:5,scale=720:1280:flags=lanczos,unsharp=5:5:0.55:5:5:0"
IN = BASE + ",eq=contrast=1.05:saturation=1.04:gamma=1.05,colortemperature=temperature=6000:mix=0.35,setsar=1,format=yuv420p"
OUTD = BASE + ",eq=contrast=1.07:saturation=1.08:gamma=1.14:brightness=0.015,colortemperature=temperature=5200:mix=0.45,setsar=1,format=yuv420p"
SEG = [  # (file, start, end, grade)
 ('f123ab8c-IMG_0272.MOV', 0.2, 2.3, OUTD),    # street
 ('e9f1daef-IMG_0275.MOV', 1.2, 4.6, OUTD),    # building: Maria points at the sign
 ('a0c4358d-IMG_0271.MOV', 5.8, 7.6, IN),      # 8th floor corridor
 ('f6f10521-IMG_2554.MOV', 0.0, 4.8, IN),      # hallway, intercom
 ('34bbe71e-IMG_0245.MOV', 0.0, 3.8, IN),      # gate opens
 ('0393284d-IMG_0246.MOV', 1.5, 6.0, IN),      # led inside
 ('5eb18a2f-IMG_0247.MOV', 0.3, 4.9, IN),      # office door opens
 ('LOCAL:office_logo.mp4', 0.0, 7.7, None),   # office with the 3D logo
 ('4888063c-IMG_0250.MOV', 2.0, 8.5, IN),      # rings
 ('7042035d-IMG_0255.MOV', 0.3, 5.0, IN),      # tray
 ('a2530030-IMG_0259.MOV', 3.5, 10.0, IN),     # ring on her hand
]
T = 0.4; END = 3.5; TE = 0.6
inputs, fl, labels, starts = [], [], [], []
for i, (f, a, b, g) in enumerate(SEG):
    path = f[6:] if f.startswith('LOCAL:') else U + f
    inputs += ['-i', path]
    chain = f"[{i}:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30," + (g if g else "setsar=1,format=yuv420p") + f"[s{i}]"
    fl.append(chain); labels.append(f"s{i}")
inputs += ['-loop', '1', '-t', str(END), '-i', 'end2.png']
fl.append(f"[{len(SEG)}:v]fps=30,scale=720:1280,setsar=1,format=yuv420p[e]")
cur, t0 = labels[0], SEG[0][2] - SEG[0][1]; starts.append(0.0)
for i in range(1, len(SEG)):
    off = round(t0 - T, 3); starts.append(off)
    fl.append(f"[{cur}][{labels[i]}]xfade=transition=fade:duration={T}:offset={off}[x{i}]"); cur = f"x{i}"
    t0 = off + (SEG[i][2] - SEG[i][1])
off = round(t0 - TE, 3); starts.append(off)
fl.append(f"[{cur}][e]xfade=transition=fade:duration={TE}:offset={off}[v]")
total = off + END
cmd = ['ffmpeg', '-loglevel', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(fl), '-map', '[v]', '-c:v', 'libx264', '-crf', '12', '-preset', 'slow', '-pix_fmt', 'yuv420p', 'inst_full.mp4']
subprocess.run(cmd, check=True)
json.dump({'starts': starts, 'total': total}, open('timeline.json', 'w'))
print('starts', [round(s, 2) for s in starts], 'total', round(total, 2))
