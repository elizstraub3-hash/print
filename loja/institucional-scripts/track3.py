import cv2, numpy as np, subprocess, pickle
W, H = 720, 1280
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', 'office_seg.mp4', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE)
G = []
while True:
    b = dec.stdout.read(W * H)
    if len(b) < W * H: break
    G.append(np.frombuffer(b, np.uint8).reshape(H, W).copy())
n = len(G); R = 126
mask = np.zeros((H, W), np.uint8); mask[:int(H * 0.36), :] = 255
def step(a, b):
    p0 = cv2.goodFeaturesToTrack(G[a], 600, 0.005, 8, mask=mask, blockSize=9)
    p1, st, _ = cv2.calcOpticalFlowPyrLK(G[a], G[b], p0, None, winSize=(31, 31), maxLevel=4)
    p2, st2, _ = cv2.calcOpticalFlowPyrLK(G[b], G[a], p1, None, winSize=(31, 31), maxLevel=4)   # forward-backward check
    fb = np.linalg.norm(p0 - p2, axis=2).ravel()
    ok = (st.ravel() == 1) & (st2.ravel() == 1) & (fb < 1.0)
    A, inl = cv2.estimateAffinePartial2D(p0[ok], p1[ok], method=cv2.RANSAC, ransacReprojThreshold=2.0)
    return np.vstack([A, [0, 0, 1]]), int(ok.sum())
Hs = [None] * n; Hs[R] = np.eye(3); cnt = []
for t in range(R + 1, n): A, c = step(t - 1, t); Hs[t] = A @ Hs[t - 1]; cnt.append(c)
for t in range(R - 1, -1, -1): A, c = step(t + 1, t); Hs[t] = A @ Hs[t + 1]; cnt.append(c)
Q = np.float32([[330, 268], [600, 203], [600, 292], [330, 338]]).reshape(-1, 1, 2)
C = np.array([cv2.perspectiveTransform(Q, h).reshape(-1) for h in Hs])
Cs = C.copy()
for t in range(n):
    a, b = max(0, t - 2), min(n, t + 3); Cs[t] = C[a:b].mean(0)
pickle.dump({'corners': Cs, 'quad': Q.reshape(-1, 2)}, open('track2.pkl', 'wb'))
print('min feats', min(cnt), 'median', int(np.median(cnt)))
for t in (45, 75, 126, 165, 222): print(t, Cs[t][:2].round(0))
