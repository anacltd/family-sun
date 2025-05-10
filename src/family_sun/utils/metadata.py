import pandas as pd
import re
import textwrap


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
    if pd.notna(row["cities"]) and pd.notna(row["departments"]):
        lines.append(f"({row['cities']}, {row['departments']})")
    if pd.notna(row["death_years"]):
        lines.append(f"Died in {int(row['death_years'])}")
    return "<br>".join(lines)


def color_by_category(df: pd.DataFrame, category: str, palette: str):
    """Add a color column to a DataFrame based on the unique values of a specified category.

    Args:
        df: The input DataFrame containing the category.
        category: The name of the column within the DataFrame that contains the categories.
        palette: The palette from which colors are drawn.

    Returns:
        The input DataFrame with an additional `color` column.
    """
    unique_keys = df[category].unique()
    color_map = {key: palette[i % len(palette)] for i, key in enumerate(unique_keys)}
    df["color"] = df[category].map(color_map)
    return df


def wrap_text(parents: list[str], children: list[str]) -> tuple[list[str], list[str]]:
    """Wrap text that is too long.
    Both the parents and the children lists are necessary to that the index of the name in both lists remains the same.

    Args:
        parents: The list of parent names.
        children: The list of children names.

    Returns:
        The parent and children lists with updated names.
    """
    names_to_prettify = []
    for p in parents:
        # Add a line break when the name is too long
        pretty_name = "<br>".join(textwrap.wrap(p, 20))
        if p != pretty_name:
            name_index_parents = parents.index(p)
            name_index_children = children.index(p) if p in children else None
            names_to_prettify.append(
                (name_index_parents, name_index_children, pretty_name)
            )
    for i_parent, i_children, name in names_to_prettify:
        parents[i_parent] = name
        if i_children:
            children[i_children] = name
            children[i_children + 1] = name
    return parents, children


def extract_patronyms(parents: list[str]) -> list[str]:
    """Extract the patronym from a name.

    Args:
        parents: The list of parent names.

    Returns:
        The list of patronyms.
    """
    patronyms = []
    for p in parents:
        last_name = re.search(
            r"^((?:[A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸ][a-zàâäçéèêëîïôöùûüÿ\-]+ ?)+(?:\s?\([^)]+\))?) ([A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸ ]+)$",
            p,
        )
        if last_name:
            patronyms.append(last_name.group(2))
        else:
            patronyms.append("")
    return patronyms


def add_dates_to_names(
    ancestors: dict[str, dict[str, str | list[str]]],
    parents: list[str],
    children: list[str],
) -> tuple[list[str], list[str]]:
    """Adds the birth and death years to the name displayed on the tree.
    Both the parents and the children lists are necessary to that the index of the name in both lists remains the same.

    Args:
        ancestors: The dictionary of ancestors to retrieve the dates from.
        parents: The list of parent names.
        children: The list of children names.

    Returns:
        The parent and children lists with updated names.

    """
    indexes = []
    for p in parents:
        # Since this is done after the text wrap, names need to be "unwrapped".
        period = f"{p}<br>{ancestors.get(p.replace('<br>', ' '), {}).get('birth') or ''} - {ancestors.get(p.replace('<br>', ' '), {}).get('death') or ''}"
        name_index_parents = parents.index(p)
        name_index_children = children.index(p) if p in children else None
        indexes.append((name_index_parents, name_index_children, period))
    for i_parent, i_children, period in indexes:
        parents[i_parent] = period
        if i_children:
            children[i_children] = period
            children[i_children + 1] = period
    return parents, children
