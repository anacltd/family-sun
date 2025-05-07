import pandas as pd
from read_gedcom import individuals, parents
import plotly.express as px

NB = 10


data = pd.DataFrame(
    data={
        "individuals": individuals[:NB],
        "parents": parents[:NB],
        "values": [100, 25, 25, 12.5, 12.5, 6.25, 6.25, 3.125, 3.125, 3.125],
    }
)

fig = px.sunburst(
    data,
    names='individuals',
    parents='parents',
    values='values',
    branchvalues="total",
)
fig.show()