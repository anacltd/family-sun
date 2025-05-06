from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser


individuals = []
parents = [""]
values = [
    50,
    25, 25,
    12.5, 12.5, 12.5, 12.5,
    7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5,
    2, 2, 2, 2, 2
]

# Path to your `.ged` file
file_path = 'gedcom.ged'

# Initialize the parser
gedcom_parser = Parser()

# Parse your file
gedcom_parser.parse_file(file_path)
elements = list(filter(lambda x: isinstance(x, IndividualElement), gedcom_parser.get_root_child_elements()))

# Iterate through all root child elements
for i, element in enumerate(elements):
    name = " ".join(element.get_name())
    individuals.append(name)
    parents.append(name)
    parents.append(name)
