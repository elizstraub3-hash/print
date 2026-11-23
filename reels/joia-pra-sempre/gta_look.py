"""Teste: visual 'ilustrado de game' (inspirado na arte de capa estilo GTA, sem logo/fonte/arte do jogo).
Bordas em traço escuro + cores chapadas (posterização suave) + grade quente/rosada de pôr do sol."""
import sys, cv2, numpy as np
def gta(bgr):
    s = cv2.edgePreservingFilter(bgr, flags=1, sigma_s=60, sigma_r=0.45)
    s = cv2.stylization(s, sigma_s=40, sigma_r=0.35)
    # flatter colours
    z = (s.astype(np.float32) / 255)
    z = np.round(z * 10) / 10
    s = (z * 255).astype(np.uint8)
    # ink outlines
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY); g = cv2.medianBlur(g, 7)
    e = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)
    e = cv2.erode(e, np.ones((2, 2), np.uint8))
    s = cv2.bitwise_and(s, s, mask=e)
    # warm sunset grade (more saturation, orange highlights, magenta shadows)
    hsv = cv2.cvtColor(s, cv2.COLOR_BGR2HSV).astype(np.float32); hsv[..., 1] = np.clip(hsv[..., 1] * 1.45, 0, 255)
    s = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    l = s.mean(2, keepdims=True) / 255
    s = s + (1 - l) * np.array([40, 0, 35]) + l * np.array([-20, 15, 35])
    return np.clip(s, 0, 255).astype(np.uint8)
if __name__ == '__main__':
    outs = []
    for f, t in [('IMG_0068.MP4', 0.8), ('IMG_0100.MP4', 0.8), ('IMG_2303.MP4', 1.0)]:
        cap = cv2.VideoCapture('/home/user/print/videos-drive/' + f); cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, fr = cap.read()
        fr = fr[:, 180:1260]
        outs.append(np.hstack([cv2.resize(fr, (405, 720)), cv2.resize(gta(fr), (405, 720))]))
    cv2.imwrite(sys.argv[1], np.hstack(outs), [cv2.IMWRITE_JPEG_QUALITY, 90])
