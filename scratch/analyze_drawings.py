import cv2
import numpy as np

for name in ['fig_8_2_componente_gradiente_non_nullo.png',
             'fig_8_3_parallelismo_gradienti_punto_estremale.png',
             'fig_8_4_curve_di_livello_minimo_vincolato.png',
             'fig_8_5_vincoli_disuguaglianza_kkt.png',
             'fig_7_2_sigmoide_lda_superficie.png']:
    im = cv2.imread('Anno 1/Machine Learning/immagini/' + name)
    print(f"\n=================== {name} ({im.shape[1]}x{im.shape[0]}) ===================")
    # let's save a downsampled view or describe connected components
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # Check if there are colored strokes
    b, g, r = cv2.split(im)
    diff_rg = np.abs(r.astype(int) - g.astype(int))
    diff_gb = np.abs(g.astype(int) - b.astype(int))
    color_mask = (diff_rg > 20) | (diff_gb > 20)
    print(f"Color pixels: {np.sum(color_mask)}")
    # Find contours
    thresh = (gray < 220).astype(np.uint8)
    contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Total external contours: {len(contours)}")
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:8]
    for i, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        print(f"  Contour {i}: x={x}, y={y}, w={w}, h={h}, area={area:.1f}")
