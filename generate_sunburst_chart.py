import pandas as pd
from read_gedcom import get_generations, get_ancestors_structure
import plotly.express as px
from collections import defaultdict
from gedcom.parser import Parser

file_path = 'gedcom.ged'
gedcom_parser = Parser()
gedcom_parser.parse_file(file_path)

ancestors = get_ancestors_structure(gedcom_parser)
generations = get_generations(gedcom_parser)

NB = 30  # The number of individuals to display
INDEX_START = 35  # The "weight" to give to generation n°2.

parents = []
children = [""]
values = []

for generation_number, generation_individuals in generations.items():
    for individuals in generation_individuals:
        if isinstance(individuals, str):
            individuals = [individuals]
        for individual in individuals:
            individual_parents = list(ancestors.keys())[list(ancestors.values()).index(individual)]

            if generation_number == 1:
                parents.append(individual)
            if individual_parents:
                parents.extend(individual_parents.split(","))
                children.extend([individual, individual])
            else:
                ...
            
            if generation_number == 1:
                values.append(100)  # root of the sunburst chart
            else:
                value = INDEX_START / (2 ** (generation_number - 2))
                values.append(value)


data_dict = {
        "individuals": parents[:NB],
        "parents": children[:NB],
        "values": values[:NB]
    }
data = pd.DataFrame(
    data=data_dict
)

fig = px.sunburst(
    data,
    names='individuals',
    parents='parents',
    values='values',
    branchvalues="total",
)
fig.show()