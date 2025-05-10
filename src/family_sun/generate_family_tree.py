import pandas as pd
from family_sun.utils.process_gedcom import get_generations, get_ancestors_structure
from family_sun.utils.metadata import (
    add_place_and_date_data,
    color_by_category,
    extract_patronyms,
    wrap_text,
    add_dates_to_names,
)
from family_sun.utils import color_palettes
import plotly.express as px
from gedcom.parser import Parser
import click


@click.command()
@click.option("--root", default="", help="The name of the root individual.")
@click.option("--gedcom-path", default="gedcom.ged", help="Path to the GEDCOM file.")
@click.option(
    "--color-scale",
    default="earth",
    help="The name of the color scale.",
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
            "regions",
            "departments",
            "citiesbirth_years",
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
    root: str,
    gedcom_path: str,
    color_scale: str,
    nb_of_generations: int,
    color_by: str,
    save: bool,
):
    """Generate a Plotly sunburst graph from a GEDCOM file.

    Args:
        gedcom_path: The path to the GEDCOM file.
        color_scale: Name of the color scale to use (see `utils/color_palettes.py`).
        nb_of_generations: The number of generations to display.
        color_by: The category used to color the chart.
        save: Whether to save the file as a PNG.
    """
    gedcom_parser = Parser()
    gedcom_parser.parse_file(gedcom_path)

    ancestors = get_ancestors_structure(gedcom_parser, root)
    generations_dict = get_generations(gedcom_parser, root)

    parents, children, values = [], [""], []  # The base data for the sunburst chart
    generations, patronyms, places, birth_years, death_years = (
        [1],
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
                places.append(individual_data.get("place", None))
                death_years.append(individual_data.get("death", None))

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

    # Process metadata
    patronyms = extract_patronyms(parents)
    parents, children = wrap_text(parents, children)
    parents, children = add_dates_to_names(ancestors, parents, children)

    data = pd.DataFrame(
        {
            "individuals": parents,
            "parents": children,
            "values": values,
            "generations": generations,
            "patronyms": patronyms,
            "regions": [p.region for p in places],
            "departments": [p.department for p in places],
            "cities": [p.city for p in places],
            "birth_years": birth_years,
            "death_years": death_years,
        }
    )
    data["hover_text"] = data.apply(add_place_and_date_data, axis=1)
    palette = getattr(color_palettes, color_scale.upper(), px.colors.qualitative.Pastel)
    data = color_by_category(data, color_by, palette)

    kwargs = {
        "data_frame": data,
        "names": "individuals",
        "parents": "parents",
        "values": "values",
        "color": color_by,
        "branchvalues": "total",
    }

    if pd.api.types.is_numeric_dtype(data[color_by]):
        kwargs["color_continuous_scale"] = palette
    else:
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
