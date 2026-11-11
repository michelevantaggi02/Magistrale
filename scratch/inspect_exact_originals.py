import cv2
import numpy as np
import subprocess

files = [
    ('Fig 7.2 (3D Sigmoid)', 'scratch/p_ch7-002.png'),
    ('Fig 8.2 (Gradient & Inverse)', 'scratch/p_ch8-002.png'),
    ('Fig 8.3 (Parallel at Extrema)', 'scratch/p_ch8-004.png'),
    ('Fig 8.4 (Level Curves Min)', 'scratch/p_ch8-005.png'),
    ('Fig 8.5 (Inequality KKT)', 'scratch/p130_fig-000.png'),
]

for label, p in files:
    im = cv2.imread(p)
    print(f"\n==================================================")
    print(f"{label}: {p} (shape: {im.shape})")
    print(f"==================================================")
    
    # Run tesseract with various PSMs to catch all text
    for psm in [3, 6, 11]:
        res = subprocess.run(['tesseract', p, 'stdout', '--psm', str(psm)], capture_output=True, text=True)
        txt = res.stdout.strip().replace('\n', ' | ')
        if txt:
            print(f"  [PSM {psm}]: {txt}")
