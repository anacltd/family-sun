from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser


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
        - birth_place
        - death (the death year of the individual)
        - death_place

    Args:
        parser: The GEDCOM parser.

    Returns:
        A dictionary with the name of each individuals and their parents.
    """
    # ancestors = {
    #     " ".join(individual.get_name()): [
    #         " ".join(p.get_name()) for p in parser.get_parents(individual)
    #     ]
    #     for individual in filter(
    #         lambda x: isinstance(x, IndividualElement),
    #         parser.get_root_child_elements(),
    #     )
    # }
    # return ancestors
    ancestors = {}
    individual_elements = list(
        filter(
            lambda x: isinstance(x, IndividualElement), parser.get_root_child_elements()
        )
    )

    for individual in individual_elements:
        individual_name = " ".join(individual.get_name())
        parents = parser.get_parents(individual=individual)
        birth_year, birth_place, _ = individual.get_birth_data()
        death_year, death_place, _ = individual.get_death_data()
        ancestors[individual_name] = {
            "parents": [" ".join(p.get_name()) for p in parents],
            "birth": birth_year.rsplit(" ")[-1] or None,
            "birth_place": birth_place.split(", ")[2]
            if len(birth_place.split(", ")) > 2
            else None,  # département
            "death": death_year.rsplit(" ")[-1] or None,
            "death_place": death_place.split(", ")[2]
            if len(death_place.split(", ")) > 2
            else None,  # département
        }
    return ancestors
