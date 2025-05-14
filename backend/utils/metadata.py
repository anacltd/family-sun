import re
import textwrap
from utils.constants import STRAUSS_HOWE_CLASSIFICATION, PALLETTES


def color_by_category(data: dict, category: str, palette: str):
    """Add a color column to a dictionary based on the unique values of a specified category.

    Args:
        data: The input dictionary containing the category.
        category: The name of the column within the dictionary that contains the categories.

    Returns:
        The input dictionary with an additional `color` column.
    """
    chosen_palette = PALLETTES.get(palette)
    colors = []
    unique_keys = list(set(data[category]))
    color_map = {
        key: chosen_palette[i % len(chosen_palette)]
        for i, key in enumerate(unique_keys)
    }
    for d in data[category]:
        colors.append(color_map.get(d, "#a6a6a6"))
    return colors


def add_strauss_howe_classification(dates: list) -> list[str]:
    """Regroup generations based on the [Strauss-Howe generational theory](https://en.wikipedia.org/wiki/Strauss%E2%80%93Howe_generational_theory).

    Args:
        dates: The list of birth years.

    Returns:
        The list of generations' names.
    """
    generations = []
    for d in dates:
        try:
            birth_date = int(d["year"])
            for gen, period in STRAUSS_HOWE_CLASSIFICATION.items():
                if period.get("start") <= birth_date <= period.get("end"):
                    generations.append(gen)
                    continue
        except Exception:
            generations.append(0)
    return generations


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
