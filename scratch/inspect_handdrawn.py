import os, cv2, glob
import numpy as np

imgs = sorted(glob.glob('Anno 1/Machine Learning/immagini/fig_*.png'))
extracted = [f for f in imgs if not os.path.basename(f).startswith('fig_ex_')]

# Let's write an inspection script to check how many unique colors or handwriting appearance they have
for f in extracted:
    bname = os.path.basename(f)
    im = cv2.imread(f)
    if im is None: continue
    
    # Bishop plots are typically very clean antialiased line plots on pure white (#ffffff), with standard font (Helvetica/Times).
    # Handwritten notes have pen strokes with varying thickness, non-standard handwriting text, or iPad stylus drawings.
    # Let's inspect by saving small thumbnails or checking text characteristics.
