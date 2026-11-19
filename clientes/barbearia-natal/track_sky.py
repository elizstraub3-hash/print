import cv2, numpy as np, json, subprocess
W,H=1080,1920
p=subprocess.Popen(['ffmpeg','-v','error','-i','original.mp4','-vf','fps=30','-f','rawvideo','-pix_fmt','gray','-'],stdout=subprocess.PIPE)
prev=None; T=np.eye(3); out=[]
while True:
    b=p.stdout.read(W*H)
    if len(b)<W*H: break
    g=np.frombuffer(b,np.uint8).reshape(H,W)
    if prev is not None:
        mask=np.zeros_like(g); mask[:int(H*0.30)]=255   # sky region
        pts=cv2.goodFeaturesToTrack(prev,600,0.01,12,mask=mask)
        nxt,st,_=cv2.calcOpticalFlowPyrLK(prev,g,pts,None,winSize=(31,31),maxLevel=4)
        ok=st.ravel()==1
        M,_=cv2.estimateAffinePartial2D(pts[ok],nxt[ok],method=cv2.RANSAC,ransacReprojThreshold=2)
        A=np.vstack([M,[0,0,1]]); T=A@T
    out.append(T[:2].tolist()); prev=g
json.dump(out,open('track_sky.json','w'))
import math
for i in range(0,len(out),15):
    m=np.array(out[i]); s=math.hypot(m[0,0],m[1,0]); r=math.degrees(math.atan2(m[1,0],m[0,0]))
    print(i, 'tx %.1f ty %.1f scale %.3f rot %.2f'%(m[0,2],m[1,2],s,r))
print(len(out))
