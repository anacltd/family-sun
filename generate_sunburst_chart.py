import pandas as pd
from read_gedcom import individuals, parents, values
import plotly.express as px

NB = 20

data = pd.DataFrame(
    data={
        "individuals": individuals[:NB],
        "parents": parents[:NB],
        "values": values
    }
)

fig = px.sunburst(
    data,
    names='individuals',
    parents='parents',
    values='values',
    # branchvalues="total",
)
fig.show()