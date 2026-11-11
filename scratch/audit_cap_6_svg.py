import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import numpy as np

import make_cap_6_figures_svg as m6

funcs = [
    ('fig_8_1', m6.generate_fig_8_1),
    ('fig_8_2', m6.generate_fig_8_2),
    ('fig_8_3', m6.generate_fig_8_3),
    ('fig_8_4', m6.generate_fig_8_4),
    ('fig_8_5', m6.generate_fig_8_5),
]

for name, fn in funcs:
    print(f"\n================ AUDITING {name} ================")
    plt.close('all')
    # Run function but don't save or let it save to dummy
    fn(f'/tmp/{name}.svg')
    # Let's inspect the active figure before close or re-create
