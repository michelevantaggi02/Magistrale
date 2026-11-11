import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import numpy as np

# We can import and modify the savefig to intercept the fig
import make_cap_6_figures_svg as m6

def audit_figure(name, fn):
    print(f"\n================ AUDITING {name} ================")
    # Patch plt.savefig and plt.close to inspect fig before closing
    orig_savefig = plt.savefig
    orig_close = plt.close

    captured_fig = []

    def mock_savefig(*args, **kwargs):
        captured_fig.append(plt.gcf())

    def mock_close(*args, **kwargs):
        pass

    plt.savefig = mock_savefig
    plt.close = mock_close

    try:
        fn('/tmp/dummy.svg')
    finally:
        plt.savefig = orig_savefig
        plt.close = orig_close

    fig = captured_fig[0]
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()

    total_overlaps = 0
    total_overflows = 0

    for ax_idx, ax in enumerate(fig.axes):
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        # Titles are positioned outside the axes area (by design), so check them separately or skip axes bbox check for title
        texts = [t for t in ax.texts if t != ax.title]
        valid_texts = []
        for t in texts:
            s = t.get_text()
            if not s or not s.strip():
                continue
            bbox = t.get_window_extent(renderer).transformed(ax.transData.inverted())
            valid_texts.append((s, bbox, t))

            # Overflow check against data limits
            if bbox.x0 < xlim[0] - 0.1:
                print(f"  [OVERFLOW LEFT] in Ax {ax_idx}: '{s[:30]}' x0={bbox.x0:.2f} < xlim0={xlim[0]:.2f}")
                total_overflows += 1
            if bbox.x1 > xlim[1] + 0.1:
                print(f"  [OVERFLOW RIGHT] in Ax {ax_idx}: '{s[:30]}' x1={bbox.x1:.2f} > xlim1={xlim[1]:.2f}")
                total_overflows += 1
            if bbox.y0 < ylim[0] - 0.1:
                print(f"  [OVERFLOW BOTTOM] in Ax {ax_idx}: '{s[:30]}' y0={bbox.y0:.2f} < ylim0={ylim[0]:.2f}")
                total_overflows += 1
            if bbox.y1 > ylim[1] + 0.1:
                print(f"  [OVERFLOW TOP] in Ax {ax_idx}: '{s[:30]}' y1={bbox.y1:.2f} > ylim1={ylim[1]:.2f}")
                total_overflows += 1

        # Overlap check
        for i in range(len(valid_texts)):
            s1, b1, t1 = valid_texts[i]
            for j in range(i + 1, len(valid_texts)):
                s2, b2, t2 = valid_texts[j]
                x_ov = max(0, min(b1.x1, b2.x1) - max(b1.x0, b2.x0))
                y_ov = max(0, min(b1.y1, b2.y1) - max(b1.y0, b2.y0))
                if x_ov > 0.15 and y_ov > 0.15:
                    print(f"  [OVERLAP {x_ov:.2f}x{y_ov:.2f}] between:")
                    print(f"    Text 1: '{s1.replace(chr(10), ' ')[:35]}'")
                    print(f"    Text 2: '{s2.replace(chr(10), ' ')[:35]}'")
                    total_overlaps += 1

    print(f"Results for {name}: {len(valid_texts)} texts inspected across {len(fig.axes)} axes.")
    print(f"Overlaps: {total_overlaps}, Overflows: {total_overflows}")
    plt.close(fig)
    return total_overlaps == 0 and total_overflows == 0

funcs = [
    ('fig_8_1', m6.generate_fig_8_1),
    ('fig_8_2', m6.generate_fig_8_2),
    ('fig_8_3', m6.generate_fig_8_3),
    ('fig_8_4', m6.generate_fig_8_4),
    ('fig_8_5', m6.generate_fig_8_5),
]

all_ok = True
for name, fn in funcs:
    ok = audit_figure(name, fn)
    if not ok:
        all_ok = False

print(f"\nALL FIGURES PASSED AUDIT: {all_ok}")
