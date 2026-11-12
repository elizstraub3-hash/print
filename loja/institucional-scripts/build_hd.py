import subprocess, json
U = '/root/.claude/uploads/081c4020-c9a3-5394-8b04-d630e012eb6b/'
BASE = "hqdn3d=2:1.5:6:5,scale=1080:1920:flags=lanczos,unsharp=5:5:0.55:5:5:0"
IN = BASE + ",eq=contrast=1.05:saturation=1.04:gamma=1.05,colortemperature=temperature=6000:mix=0.35,setsar=1,format=yuv420p"
OUTD = BASE + ",eq=contrast=1.07:saturation=1.08:gamma=1.14:brightness=0.015,colortemperature=temperature=5200:mix=0.45,setsar=1,format=yuv420p"
D = [2.1, 3.4, 1.8, 4.8, 3.8, 4.5, 4.6, 6.2, 6.5, 4.7, 6.5]
SEG = [(f'LOCAL:hd/s{i}.mp4' if i != 7 else 'LOCAL:hd/s7_logo.mp4', 0.0, d, None) for i, d in enumerate(D)]
T = 0.4; END = 3.5; TE = 0.6
inputs, fl, labels, starts = [], [], [], []
for i, (f, a, b, g) in enumerate(SEG):
    path = f[6:] if f.startswith('LOCAL:') else U + f
    inputs += ['-i', path]
    chain = f"[{i}:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30," + (g if g else "setsar=1,format=yuv420p") + f"[s{i}]"
    fl.append(chain); labels.append(f"s{i}")
inputs += ['-loop', '1', '-t', str(END), '-i', 'hd/end.png']
fl.append(f"[{len(SEG)}:v]fps=30,scale=1080:1920,setsar=1,format=yuv420p[e]")
cur, t0 = labels[0], SEG[0][2] - SEG[0][1]; starts.append(0.0)
for i in range(1, len(SEG)):
    off = round(t0 - T, 3); starts.append(off)
    fl.append(f"[{cur}][{labels[i]}]xfade=transition=fade:duration={T}:offset={off}[x{i}]"); cur = f"x{i}"
    t0 = off + (SEG[i][2] - SEG[i][1])
off = round(t0 - TE, 3); starts.append(off)
fl.append(f"[{cur}][e]xfade=transition=fade:duration={TE}:offset={off}[v]")
total = off + END
cmd = ['ffmpeg', '-loglevel', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(fl), '-map', '[v]', '-c:v', 'libx264', '-crf', '11', '-preset', 'medium', '-pix_fmt', 'yuv420p', 'hd/full.mp4']
subprocess.run(cmd, check=True)
json.dump({'starts': starts, 'total': total}, open('timeline.json', 'w'))
print('starts', [round(s, 2) for s in starts], 'total', round(total, 2))
