import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def save_figs_as_pdf(figs, fn):
    if isinstance(figs, list):
        pdf = PdfPages(fn)
        for f in figs:
            pdf.savefig(f)
        pdf.close()
    else:
        figs.savefig(fn, format='pdf')
    print('File %s created' % fn)

# En latex despues se usa
# \includegraphics[width=0.5\columnwidth,page=3]{senos}}
