from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
from dataclasses import dataclass, fields


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


def get_generations(parser: Parser, root: str = "") -> dict[int, list[list[str]]]:
    """Create a dictionary structure of generations.
    The keys of the dictionary are the generation numbers.
    The values of the dictionary are the list of ancestors, grouped by couples.

    {
        generation_number: [[couple 1], [couple 2]]
    }

    Args:
        parser: The GEDCOM parser.
        root: The name of the root individual.

    Returns:
        The generations in the form of a dictionary.
    """
    individual_elements = list(
        filter(
            lambda x: isinstance(x, IndividualElement), parser.get_root_child_elements()
        )
    )
    if root:
        for i, individual in enumerate(individual_elements):
            if " ".join(individual.get_name()) != root:
                individual_elements.pop(i)
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


def get_ancestors_structure(
    parser: Parser, root: str = ""
) -> dict[str, dict[str, str | list[str]]]:
    """Create a dictionary to keep track of family relationships.
    The keys of the dictionary are the name of each individual.
    The values of the dictionary are dictionaries with the following keys:
        - parents
        - birth (the birth year of the individual)
        - place (the birth place of the individual)
        - death (the death year of the individual)

    Args:
        parser: The GEDCOM parser.
        root: The name of the root individual.

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
        if root and root != individual_name:
            continue
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
