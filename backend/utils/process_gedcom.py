from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
from dataclasses import dataclass, fields
from utils.metadata import (
    add_dates_to_names,
    extract_patronyms,
    wrap_text,
    color_by_category,
    add_strauss_howe_classification,
)
import tempfile


@dataclass
class Place:
    city: str
    postal_code: str
    department: str
    region: str
    country: str

    @classmethod
    def from_string(cls, input_str: str, delimiter: str = ", "):
        """Parse a string into a Place object.
        The string must be a French address.

        Args:
            input_str: The string containing the address.
            delimiter: The delimiter for the different element.

        Returns:
            A Place object.
        """
        if not input_str or delimiter not in input_str:
            return Place("Unknown", "Unknown", "Unknown", "Unknown", "Unknown")
        parts = input_str.split(delimiter)
        if (
            len(parts) > 5
        ):  # There can be hamlet or other stuff at the beginning of the address
            parts = parts[len(parts) - 5 :]
        field_types = [f.type for f in fields(cls)]
        typed_parts = [t(p) for t, p in zip(field_types, parts)]
        return cls(*typed_parts)


def get_generations(parser: Parser) -> dict[int, list[list[str]]]:
    """Create a dictionary structure of generations.
    The keys of the dictionary are the generation numbers.
    The values of the dictionary are the list of ancestors, grouped by couples.

    {
        generation_number: [[couple 1], [couple 2]]
    }

    Args:
        parser: The GEDCOM parser.

    Returns:
        The generations in the form of a dictionary.
    """
    individual_elements = list(
        filter(
            lambda x: isinstance(x, IndividualElement), parser.get_root_child_elements()
        )
    )
    root_individual = individual_elements[0]

    n = 1
    individuals = {n: [" ".join(root_individual.get_name())]}

    next_individuals = [root_individual]
    keep_looping = True

    while keep_looping:
        generation, ancestors = [], []
        for i in next_individuals:
            parents = parser.get_parents(individual=i)
            ancestors.extend(parents)
            parents_name = [" ".join(p.get_name()) for p in parents]
            generation.append(parents_name)
        n += 1
        individuals[n] = generation
        next_individuals = ancestors
        if not next_individuals:
            keep_looping = False

    return individuals


def get_ancestors_structure(parser: Parser) -> dict[str, dict[str, str | list[str]]]:
    """Create a dictionary to keep track of family relationships.
    The keys of the dictionary are the name of each individual.
    The values of the dictionary are dictionaries with the following keys:
        - parents
        - birth (the birth year of the individual)
        - place (the birth place of the individual)
        - death (the death year of the individual)

    Args:
        parser: The GEDCOM parser.

    Returns:
        A dictionary with the name of each individuals and their parents.
    """
    ancestors = {}
    individual_elements = list(
        filter(
            lambda x: isinstance(x, IndividualElement), parser.get_root_child_elements()
        )
    )

    for individual in individual_elements:
        individual_name = " ".join(individual.get_name())
        parents = parser.get_parents(individual=individual)
        birth_year, death_year = (
            individual.get_birth_year(),
            individual.get_death_year(),
        )
        _, place, _ = individual.get_birth_data()
        ancestors[individual_name] = {
            "parents": [" ".join(p.get_name()) for p in parents],
            "birth": birth_year if birth_year > -1 else None,
            "place": Place.from_string(place),
            "death": death_year if death_year > -1 else None,
        }
    return ancestors


def parse_gedcom_to_sunburst(file_bytes, nb_of_generations, color_by, palette):
    # Create a temporary file from the uploaded bytes
    with tempfile.NamedTemporaryFile(delete=True, suffix=".ged") as tmp_file:
        tmp_file.write(file_bytes)
        tmp_file.flush()  # Make sure data is written to disk
        gedcom_parser = Parser()
        gedcom_parser.parse_file(tmp_file.name)

    ancestors = get_ancestors_structure(gedcom_parser)
    generations_dict = get_generations(gedcom_parser)

    parents, children, values = [], [""], []  # The base data for the sunburst chart
    generations, patronyms, places, years = (
        [1],
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
                years.append(individual_data.get("birth", None))
                places.append(individual_data.get("place", None))

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
    parents, children = parents[: len(values)], children[: len(values)]
    patronyms = extract_patronyms(parents)
    parents, children = wrap_text(parents, children)
    parents, children = add_dates_to_names(ancestors, parents, children)
    periods = add_strauss_howe_classification(years)

    colors = color_by_category(
        {
            "patronym": patronyms,
            "generation": generations,
            "region": [p.region for p in places],
            "department": [p.department for p in places],
            "city": [p.city for p in places],
            "year": periods,
        },
        category=color_by,
        palette=palette,
    )
    return [
        {
            "labels": parents,
            "parents": children,
            "values": values,
            "type": "sunburst",
            "marker": {"colors": colors},
            "branchvalues": "total",
            "rotation": -30,
        }
    ]
