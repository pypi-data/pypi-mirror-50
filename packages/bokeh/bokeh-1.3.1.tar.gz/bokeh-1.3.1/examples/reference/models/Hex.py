import numpy as np

from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid
from bokeh.models.markers import Hex
from bokeh.io import curdoc, show

N = 9
x = np.linspace(-2, 2, N)
y = x**2
sizes = np.linspace(10, 20, N)

source = ColumnDataSource(dict(x=x, y=y, sizes=sizes))

plot = Plot(
    title=None, plot_width=300, plot_height=300,
    min_border=0, toolbar_location=None)

glyph = Hex(x="x", y="y", size="sizes", fill_color="#f0027f")
plot.add_glyph(source, glyph)

xaxis = LinearAxis()
plot.add_layout(xaxis, 'below')

yaxis = LinearAxis()
plot.add_layout(yaxis, 'left')

plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

curdoc().add_root(plot)

show(plot)
