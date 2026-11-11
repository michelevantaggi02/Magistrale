import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import numpy as np

import generate_all_corrected_figures as gen

funcs = [
    ('fig_8_2', gen.generate_fig_8_2),
    ('fig_8_3', gen.generate_fig_8_3),
    ('fig_8_4', gen.generate_fig_8_4),
    ('fig_8_5', gen.generate_fig_8_5),
]

def audit(name, fn):
    print(f"\n================ AUDITING {name} ================")
    captured = []
    orig_savefig = plt.savefig
    orig_close = plt.close
    plt.savefig = lambda *a, **k: captured.append(plt.gcf())
    plt.close = lambda *a, **k: None

    try:
        fn('/tmp/dummy.svg')
    finally:
        plt.savefig = orig_savefig
        plt.close = orig_close

    fig = captured[0]
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()

    total_overlaps = 0
    total_overflows = 0

    for ax_idx, ax in enumerate(fig.axes):
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        texts = [t for t in ax.texts if t != ax.title]
        valid = []
        for t in texts:
            s = t.get_text()
            if not s or not s.strip():
                continue
            bbox = t.get_window_extent(renderer).transformed(ax.transData.inverted())
            valid.append((s, bbox, t))

            if bbox.x0 < xlim[0] - 0.15:
                print(f"  [OVERFLOW LEFT] '{s[:30]}' x0={bbox.x0:.2f} < {xlim[0]:.2f}")
                total_overflows += 1
            if bbox.x1 > xlim[1] + 0.15:
                print(f"  [OVERFLOW RIGHT] '{s[:30]}' x1={bbox.x1:.2f} > {xlim[1]:.2f}")
                total_overflows += 1
            if bbox.y0 < ylim[0] - 0.15:
                print(f"  [OVERFLOW BOTTOM] '{s[:30]}' y0={bbox.y0:.2f} < {ylim[0]:.2f}")
                total_overflows += 1
            if bbox.y1 > ylim[1] + 0.15:
                print(f"  [OVERFLOW TOP] '{s[:30]}' y1={bbox.y1:.2f} > {ylim[1]:.2f}")
                total_overflows += 1

        for i in range(len(valid)):
            s1, b1, _ = valid[i]
            for j in range(i + 1, len(valid)):
                s2, b2, _ = valid[j]
                x_ov = max(0, min(b1.x1, b2.x1) - max(b1.x0, b2.x0))
                y_ov = max(0, min(b1.y1, b2.y1) - max(b1.y0, b2.y0))
                if x_ov > 0.1 and y_ov > 0.1:
                    print(f"  [OVERLAP {x_ov:.2f}x{y_ov:.2f}] between:")
                    print(f"    A: '{s1.replace(chr(10), ' ')[:35]}'")
                    print(f"    B: '{s2.replace(chr(10), ' ')[:35]}'")
                    total_overlaps += 1

    print(f"Audit {name}: Overlaps={total_overlaps}, Overflows={total_overflows}")
    plt.close(fig)
    return total_overlaps == 0 and total_overflows == 0

all_ok = True
for name, fn in funcs:
    if not audit(name, fn):
        all_ok = False

print(f"\n2D ALL AUDIT RESULT: {all_ok}")
