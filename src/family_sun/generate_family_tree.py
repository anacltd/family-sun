import pandas as pd
from family_sun.process_gedcom import get_generations, get_ancestors_structure
import plotly.express as px
from gedcom.parser import Parser
import click


@click.command()
@click.option("--gedcom_path", default="gedcom.ged", help="Path to the GEDCOM file.")
@click.option(
    "--color_scale",
    default="Brwnyl",
    help="The name of the Plotly color scale. Default to Brwnyl.",
)
@click.option(
    "--save",
    default=False,
    help="The name of the Plotly color scale. Default to Brwnyl.",
)
def generate_sunburst_from_gedcom(gedcom_path: str, color_scale: str, save: bool):
    """Generate a Plotly sunburst graph from a GEDCOM file.

    Args:
        gedcom_path: The path to the GEDCOM file.
        color_scale: Name of the Plotly color scale (see [here](https://plotly.com/python/builtin-colorscales/)).
    """
    gedcom_parser = Parser()
    gedcom_parser.parse_file(gedcom_path)

    ancestors = get_ancestors_structure(gedcom_parser)
    generations_dict = get_generations(gedcom_parser)

    parents, children, generations = [], [""], [1]
    values = []

    for generation_number, generation_individuals in generations_dict.items():
        for individuals in generation_individuals:
            if isinstance(individuals, str):
                individuals = [individuals]
            for individual in individuals:
                individual_parents = list(ancestors.keys())[
                    list(ancestors.values()).index(individual)
                ]

                if generation_number == 1:
                    parents.append(individual)
                if individual_parents:
                    parents.extend(individual_parents.split(","))
                    children.extend([individual, individual])

                if generation_number == 1:
                    values.append(100)  # root of the sunburst chart
                else:
                    value = 34 / (
                        2 ** (generation_number - 2)
                    )  # 34 so that it makes a "split" at the bottom
                    values.append(value)
                    generations.append(generation_number)

    data = pd.DataFrame(
        {
            "individuals": parents[: len(values)],
            "parents": children[: len(values)],
            "values": values,
            "generation": generations,
        }
    )

    fig = px.sunburst(
        data,
        names="individuals",
        parents="parents",
        values="values",
        color="generation",
        color_continuous_scale=color_scale,
        branchvalues="total",
    )
    fig.update_traces(
        rotation=-30
    )  # So that the bottom split is not tilted to the left
    fig.update_coloraxes(showscale=False)
    fig.show()
    if save:
        fig.write_image("family_tree.png", width=1000, height=1000)


if __name__ == "__main__":
    generate_sunburst_from_gedcom()
