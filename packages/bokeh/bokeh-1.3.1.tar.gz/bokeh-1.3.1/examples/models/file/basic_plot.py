from __future__ import print_function

from numpy import pi, arange, sin

from bokeh.util.browser import view
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.models.glyphs import Circle
from bokeh.models import Plot, LinearAxis, ColumnDataSource, PanTool, WheelZoomTool
from bokeh.resources import INLINE

x = arange(-2*pi, 2*pi, 0.1)
y = sin(x)

source = ColumnDataSource(
    data=dict(x=x, y=y)
)

plot = Plot(min_border=80)

circle = Circle(x="x", y="y", fill_color="red", size=5, line_color="black")
plot.add_glyph(source, circle)

plot.add_layout(LinearAxis(), 'below')
plot.add_layout(LinearAxis(), 'left')

plot.add_tools(PanTool(), WheelZoomTool())

doc = Document()
doc.add_root(plot)

if __name__ == "__main__":
    doc.validate()
    filename = "basic_plot.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "Basic Glyph Plot"))
    print("Wrote %s" % filename)
    view(filename)
