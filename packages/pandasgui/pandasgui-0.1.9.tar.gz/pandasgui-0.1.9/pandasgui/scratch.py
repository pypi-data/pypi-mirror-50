import numpy as np
import plotly.graph_objs as go
import plotly.offline
from pandasgui.widgets import PlotlyViewer

fig = go.Figure()
fig.add_scatter(x=np.random.rand(100), y=np.random.rand(100), mode='markers',
                marker={'size': 30, 'color': np.random.rand(100), 'opacity': 0.6,
                        'colorscale': 'Viridis'});

win = PlotlyViewer(fig, exec=True)
