import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
matplotlib.rcParams['font.sans-serif'] = 'DejaVu Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'

import matplotlib.pyplot as plt
import matplotlib.patches as patches

with open('scratch/make_classification_approaches_schema.py') as f:
    text = f.read()

# remove everything from plt.tight_layout to end
idx = text.find('plt.tight_layout()')
if idx != -1:
    code = text[:idx]
else:
    code = text

loc = {}
exec(code, globals(), loc)

fig = loc['fig']
ax = loc['ax']

canvas = FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()

cards = [
    ("Card 1", loc['x1'], loc['x1'] + loc['card_w'], loc['y_bottom'], loc['y_bottom'] + loc['card_h']),
    ("Card 2", loc['x2'], loc['x2'] + loc['card_w'], loc['y_bottom'], loc['y_bottom'] + loc['card_h']),
    ("Card 3", loc['x3'], loc['x3'] + loc['card_w'], loc['y_bottom'], loc['y_bottom'] + loc['card_h']),
]

print("Checking text elements against card bounds:")
texts = ax.texts
overflow_count = 0
for t in texts:
    s = t.get_text()
    if not s or s.startswith("Tassonomia") or s.startswith("Inquadramento") or s.startswith(r"$\mathbf{Regola"):
        continue
    bbox = t.get_window_extent(renderer).transformed(ax.transData.inverted())
    x0, y0, x1, y1 = bbox.x0, bbox.y0, bbox.x1, bbox.y1
    
    center_x = (x0 + x1) / 2
    for cname, cx0, cx1, cy0, cy1 in cards:
        if cx0 - 0.5 <= center_x <= cx1 + 0.5:
            overflow_left = x0 < cx0 + 0.05
            overflow_right = x1 > cx1 - 0.05
            overflow_bottom = y0 < cy0 + 0.05
            overflow_top = y1 > cy1 - 0.05
            if overflow_left or overflow_right or overflow_bottom or overflow_top:
                overflow_count += 1
                print(f"OVERFLOW in {cname} for '{s.replace(chr(10), ' ')[:45]}':")
                print(f"  Text bbox: x=[{x0:.2f}, {x1:.2f}], y=[{y0:.2f}, {y1:.2f}]")
                print(f"  Card bounds: x=[{cx0:.2f}, {cx1:.2f}], y=[{cy0:.2f}, {cy1:.2f}]")
                if overflow_right: print(f"    --> EXCEEDS RIGHT BORDER by {x1 - (cx1 - 0.05):.2f}")
                if overflow_left: print(f"    --> EXCEEDS LEFT BORDER by {(cx0 + 0.05) - x0:.2f}")
                if overflow_bottom: print(f"    --> EXCEEDS BOTTOM BORDER by {(cy0 + 0.05) - y0:.2f}")
                if overflow_top: print(f"    --> EXCEEDS TOP BORDER by {y1 - (cy1 - 0.05):.2f}")

print(f"\nTotal overflows detected: {overflow_count}")

# Check pairwise text overlaps within each card
print("\nChecking pairwise text overlaps:")
overlap_count = 0
for i in range(len(texts)):
    t1 = texts[i]
    s1 = t1.get_text()
    if not s1 or s1.startswith("Tassonomia") or s1.startswith("Inquadramento") or s1.startswith(r"$\mathbf{Regola"):
        continue
    b1 = t1.get_window_extent(renderer).transformed(ax.transData.inverted())
    for j in range(i + 1, len(texts)):
        t2 = texts[j]
        s2 = t2.get_text()
        if not s2 or s2.startswith("Tassonomia") or s2.startswith("Inquadramento") or s2.startswith(r"$\mathbf{Regola"):
            continue
        b2 = t2.get_window_extent(renderer).transformed(ax.transData.inverted())
        x_overlap = max(0, min(b1.x1, b2.x1) - max(b1.x0, b2.x0))
        y_overlap = max(0, min(b1.y1, b2.y1) - max(b1.y0, b2.y0))
        if x_overlap > 0.05 and y_overlap > 0.05:
            overlap_count += 1
            print(f"OVERLAP ({x_overlap:.2f} x {y_overlap:.2f}) between:")
            print(f"  A: '{s1.replace(chr(10), ' ')[:35]}'")
            print(f"  B: '{s2.replace(chr(10), ' ')[:35]}'")

print(f"Total pairwise overlaps detected: {overlap_count}")
