import cv2, numpy as np, subprocess, pickle
from scipy.signal import savgol_filter
W, H = 540, 960
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', 'hd/s7.mp4', '-vf', 'scale=540:960:flags=area', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE)
G = []
while True:
    b = dec.stdout.read(W * H)
    if len(b) < W * H: break
    G.append(np.frombuffer(b, np.uint8).reshape(H, W).copy())
n = len(G); R = 126
mask = np.zeros((H, W), np.uint8); mask[:int(H * 0.36), :] = 255
def step(a, b):
    p0 = cv2.goodFeaturesToTrack(G[a], 800, 0.004, 7, mask=mask, blockSize=9)
    p1, st, _ = cv2.calcOpticalFlowPyrLK(G[a], G[b], p0, None, winSize=(31, 31), maxLevel=4)
    p2, st2, _ = cv2.calcOpticalFlowPyrLK(G[b], G[a], p1, None, winSize=(31, 31), maxLevel=4)
    fb = np.linalg.norm(p0 - p2, axis=2).ravel()
    ok = (st.ravel() == 1) & (st2.ravel() == 1) & (fb < 0.7)
    A, _ = cv2.estimateAffinePartial2D(p0[ok], p1[ok], method=cv2.RANSAC, ransacReprojThreshold=1.5)
    return np.vstack([A, [0, 0, 1]])
Hs = [None] * n; Hs[R] = np.eye(3)
for t in range(R + 1, n): Hs[t] = step(t - 1, t) @ Hs[t - 1]
for t in range(R - 1, -1, -1): Hs[t] = step(t + 1, t) @ Hs[t + 1]
Q = (np.float32([[495, 402], [900, 305], [900, 438], [495, 507]]) / 2).reshape(-1, 1, 2)
C = np.array([cv2.perspectiveTransform(Q, h).reshape(-1) for h in Hs]) * 2      # back to 1080x1920
Cs = savgol_filter(C, 15, 2, axis=0)
pickle.dump({'corners': Cs}, open('hd/track.pkl', 'wb'))
print('jitter removed (px rms):', np.sqrt(((C - Cs) ** 2).mean()).round(2))
