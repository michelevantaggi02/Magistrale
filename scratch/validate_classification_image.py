import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys

# Load make_classification_approaches_schema
import make_classification_approaches_schema as mcas

# Execute generator to populate figure
fig_w, fig_h = 16, 8.4
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')
ax.set_xlim(0, 16)
ax.set_ylim(0, 8.4)
ax.axis('off')

# Call the drawing code
import inspect
lines = inspect.getsource(mcas.generate_figure).splitlines()
# extract body
body_lines = [l[4:] for l in lines if l.startswith('    ') and not l.strip().startswith('plt.savefig') and not l.strip().startswith('plt.close') and not l.strip().startswith('plt.tight_layout') and not l.strip().startswith('print(')]
exec('\n'.join(body_lines), globals(), locals())

canvas = FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()

cards = [
    ("Card 1 (Generativi)", xs[0], xs[0] + card_w, y_card, y_card + card_h),
    ("Card 2 (Discriminativi Prob)", xs[1], xs[1] + card_w, y_card, y_card + card_h),
    ("Card 3 (Funzioni Discrim)", xs[2], xs[2] + card_w, y_card, y_card + card_h),
]

banner_box = ("Bottom Banner", 0.8, 15.2, bot_y, bot_y + bot_h)

print("=== CHECKING CANVAS BOUNDS ===")
texts = ax.texts
canvas_errors = 0
for t in texts:
    s = t.get_text()
    b = t.get_window_extent(renderer).transformed(ax.transData.inverted())
    if b.x0 < 0 or b.x1 > 16.0 or b.y0 < 0 or b.y1 > 8.4:
        print(f"CANVAS OVERFLOW: '{s[:35]}' at x=[{b.x0:.2f}, {b.x1:.2f}], y=[{b.y0:.2f}, {b.y1:.2f}]")
        canvas_errors += 1

print(f"Canvas overflow errors: {canvas_errors}")

print("\n=== CHECKING CARD & BANNER BOUNDS ===")
box_errors = 0
for t in texts:
    s = t.get_text()
    b = t.get_window_extent(renderer).transformed(ax.transData.inverted())
    cx = (b.x0 + b.x1) / 2
    cy = (b.y0 + b.y1) / 2
    
    # check if belongs to a card
    for cname, x0, x1, y0, y1 in cards:
        if x0 - 0.1 <= cx <= x1 + 0.1 and y0 - 0.1 <= cy <= y1 + 0.1:
            margin_l = b.x0 - x0
            margin_r = x1 - b.x1
            margin_b = b.y0 - y0
            margin_t = y1 - b.y1
            if margin_l < 0.05 or margin_r < 0.05 or margin_b < 0.05 or margin_t < 0.05:
                print(f"BOX OVERFLOW in {cname}: '{s[:35]}'")
                print(f"  Margins: left={margin_l:.2f}, right={margin_r:.2f}, bottom={margin_b:.2f}, top={margin_t:.2f}")
                box_errors += 1

    # check if belongs to banner
    bname, bx0, bx1, by0, by1 = banner_box
    if bx0 - 0.1 <= cx <= bx1 + 0.1 and by0 - 0.1 <= cy <= by1 + 0.1:
        margin_l = b.x0 - bx0
        margin_r = bx1 - b.x1
        margin_b = b.y0 - by0
        margin_t = by1 - b.y1
        if margin_l < 0.05 or margin_r < 0.05 or margin_b < 0.05 or margin_t < 0.05:
            print(f"BANNER OVERFLOW: '{s[:35]}'")
            print(f"  Margins: left={margin_l:.2f}, right={margin_r:.2f}, bottom={margin_b:.2f}, top={margin_t:.2f}")
            box_errors += 1

print(f"Box overflow errors: {box_errors}")

print("\n=== CHECKING PAIRWISE TEXT OVERLAPS ===")
overlap_errors = 0
for i in range(len(texts)):
    t1 = texts[i]
    s1 = t1.get_text()
    b1 = t1.get_window_extent(renderer).transformed(ax.transData.inverted())
    for j in range(i + 1, len(texts)):
        t2 = texts[j]
        s2 = t2.get_text()
        b2 = t2.get_window_extent(renderer).transformed(ax.transData.inverted())
        x_overlap = min(b1.x1, b2.x1) - max(b1.x0, b2.x0)
        y_overlap = min(b1.y1, b2.y1) - max(b1.y0, b2.y0)
        if x_overlap > 0.01 and y_overlap > 0.01:
            print(f"OVERLAP ({x_overlap:.2f} x {y_overlap:.2f}):")
            print(f"  T1: '{s1[:35]}'")
            print(f"  T2: '{s2[:35]}'")
            overlap_errors += 1

print(f"Pairwise overlap errors: {overlap_errors}")

if canvas_errors == 0 and box_errors == 0 and overlap_errors == 0:
    print("\n>>> ALL CHECKS PASSED PERFECTLY! ZERO OVERFLOWS, ZERO OVERLAPS! <<<")
else:
    print("\n>>> CRITICAL: ERRORS FOUND! <<<")
    sys.exit(1)
