import pandas as pd
from family_sun.process_gedcom import get_generations, get_ancestors_structure
import plotly.express as px
from gedcom.parser import Parser
import click
import re


@click.command()
@click.option("--gedcom-path", default="gedcom.ged", help="Path to the GEDCOM file.")
@click.option(
    "--color-scale",
    default="gray",
    help="The name of the Plotly color scale.",
)
@click.option(
    "--nb-of-generations",
    default=6,
    help="The number of generations to display.",
)
@click.option(
    "--color-by",
    default="generations",
    type=click.Choice(["generations", "patronyms"]),
    help="The category used to color the chart.",
)
@click.option(
    "--save",
    default=False,
    help="Whether to save the file as a PNG.",
)
def generate_sunburst_from_gedcom(
    gedcom_path: str,
    color_scale: str,
    nb_of_generations: int,
    color_by: str,
    save: bool,
):
    """Generate a Plotly sunburst graph from a GEDCOM file.

    Args:
        gedcom_path: The path to the GEDCOM file.
        color_scale: Name of the Plotly color scale.
        When using `generations` to color the chart, refer to [continuous color scales](https://plotly.com/python/builtin-colorscales/)).
        When using `patronyms` to color the chart, refer to [discrete color scales](https://plotly.com/python/discrete-color/).
        nb_of_generations: The number of generations to display.
        color_by: The category used to color the chart.
        save: Whether to save the file as a PNG.
    """
    gedcom_parser = Parser()
    gedcom_parser.parse_file(gedcom_path)

    ancestors = get_ancestors_structure(gedcom_parser)
    generations_dict = get_generations(gedcom_parser)

    parents, children, values = [], [""], []  # The base data for the sunburst chart
    generations, patronyms = (
        [1],
        [],
    )  # To color the chart based on the generations or the patronyms

    for generation_number, generation_individuals in generations_dict.items():
        if generation_number > nb_of_generations:
            break
        for individuals in generation_individuals:
            if isinstance(individuals, str):
                individuals = [individuals]
            for individual in individuals:
                individual_parents = ancestors.get(individual)

                if generation_number == 1:  # root of the sunburst chart
                    parents.append(individual)
                if individual_parents:
                    parents.extend(individual_parents)
                    children.extend([individual, individual])

                # Compute the value of the individual, which should be the sum of their parents.
                if generation_number == 1:
                    values.append(100)  # root of the sunburst chart
                else:
                    value = 34 / (
                        2 ** (generation_number - 2)
                    )  # 34 so that it makes a "split" at the bottom
                    values.append(value)
                    generations.append(generation_number)

    # Retrieves the patronym of the individual
    names_to_prettify = []
    for p in parents:
        last_name = re.search(
            r"^((?:[A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸ][a-zàâäçéèêëîïôöùûüÿ\-]+ ?)+(?:\s?\([^)]+\))?) ([A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸ ]+)$",
            p,
        )
        if last_name:
            patronyms.append(last_name.group(2))
            # Add a line break when the name is too long
            if len(p) > 20:
                pretty_name = "<br>".join(last_name.groups())
                name_index_parents = parents.index(p)
                name_index_children = children.index(p) if p in children else None
                names_to_prettify.append(
                    (name_index_parents, name_index_children, pretty_name)
                )
        else:
            patronyms.append("")
    for i_parent, i_children, name in names_to_prettify:
        parents[i_parent] = name
        if i_children:
            children[i_children] = name
            children[i_children + 1] = name

    data = pd.DataFrame(
        {
            "individuals": parents,
            "parents": children,
            "values": values,
            "generations": generations,
            "patronyms": patronyms,
        }
    )

    kwargs = {
        "data_frame": data,
        "names": "individuals",
        "parents": "parents",
        "values": "values",
        "color": color_by,
        "branchvalues": "total",
    }
    if color_by == "patronyms":
        kwargs["color_discrete_sequence"] = getattr(
            px.colors.qualitative, color_scale.title(), px.colors.qualitative.Pastel1
        )
    else:
        kwargs["color_continuous_scale"] = color_scale

    fig = px.sunburst(**kwargs)
    fig.update_traces(
        rotation=-30
    )  # So that the bottom split is not tilted to the left
    fig.update_traces(insidetextorientation="radial")
    fig.update_coloraxes(showscale=False)
    fig.show()

    if save:
        fig.write_image("family_tree.png", width=3000, height=2500)
