import pandas as pd
from family_sun.process_gedcom import get_generations, get_ancestors_structure
import plotly.express as px
from gedcom.parser import Parser
import click
import re


def add_place_and_date_data(row: pd.Series) -> str:
    """Add additional place and date data to an individual so it can be displayed
    on the chart by hivering.

    Args:
        row : The pandas dataframe row to process.

    Returns:
        Additional birth date and place data.
    """
    lines = [f"<b>{row['individuals']}</b>"]
    if pd.notna(row["birth_years"]):
        lines.append(f"Born in {int(row['birth_years'])}")
    if pd.notna(row["birth_places"]):
        lines.append(f"({row['birth_places']})")
    if pd.notna(row["death_years"]):
        lines.append(f"Died in {int(row['death_years'])}")
    if pd.notna(row["death_places"]):
        lines.append(f"({row['death_places']})")
    return "<br>".join(lines)


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
    type=click.Choice(
        [
            "generations",
            "patronyms",
            "birth_places",
            "birth_years",
            "death_places",
            "death_years",
        ]
    ),
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
    generations, patronyms, birth_places, birth_years, death_places, death_years = (
        [1],
        [],
        [],
        [],
        [],
        [],
    )  # To color the chart based on the generations or the patronyms

    for generation_number, generation_individuals in generations_dict.items():
        if generation_number > nb_of_generations:
            break
        for individuals in generation_individuals:
            if isinstance(individuals, str):
                individuals = [individuals]
            for individual in individuals:
                individual_data = ancestors.get(individual, {})
                individual_parents = individual_data.get("parents")
                birth_years.append(individual_data.get("birth", None))
                birth_places.append(individual_data.get("birth_place", None))
                death_years.append(individual_data.get("death", None))
                death_places.append(individual_data.get("death_year", None))

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
            "birth_places": birth_places,
            "birth_years": birth_years,
            "death_places": death_places,
            "death_years": death_years,
        }
    )
    data["hover_text"] = data.apply(add_place_and_date_data, axis=1)

    kwargs = {
        "data_frame": data,
        "names": "individuals",
        "parents": "parents",
        "values": "values",
        "color": color_by,
        "branchvalues": "total",
    }

    if pd.api.types.is_numeric_dtype(data[color_by]):
        kwargs["color_continuous_scale"] = color_scale
    else:
        palette = getattr(
            px.colors.qualitative, color_scale.title(), px.colors.qualitative.Pastel1
        )
        kwargs["color_discrete_sequence"] = palette

    fig = px.sunburst(**kwargs)
    fig.update_traces(
        rotation=-30
    )  # So that the bottom split is not tilted to the left
    fig.update_traces(insidetextorientation="radial")
    fig.update_traces(
        hovertemplate="%{customdata[0]}<extra></extra>",
        customdata=data[["hover_text"]].values,
    )
    fig.update_coloraxes(showscale=False)
    fig.show()

    if save:
        fig.write_image("family_tree.png", width=3000, height=2500)


if __name__ == "__main__":
    generate_sunburst_from_gedcom()
