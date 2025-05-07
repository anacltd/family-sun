from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from gedcom.parser import Parser


individuals = []
parents = [""]

file_path = 'gedcom.ged'
gedcom_parser = Parser()

gedcom_parser.parse_file(file_path)

family_elements = list(filter(lambda x: isinstance(x, FamilyElement), gedcom_parser.get_root_child_elements()))
individual_elements = list(filter(lambda x: isinstance(x, IndividualElement), gedcom_parser.get_root_child_elements()))

for i, family_element in enumerate(family_elements):
    linked_elements = [element for element in family_element.get_child_elements() if element._Element__tag != "MARR"]
    for l in linked_elements:
        if l._Element__tag == "CHIL":
            child = next((i for i in individual_elements if i._Element__pointer == l._Element__value), None)
            if child:
                child_name = " ".join(child.get_name())
                if i ==0:
                    individuals.insert(i, child_name)
                parents.append(child_name)
                parents.append(child_name)
        else:
            parent = next((i for i in individual_elements if i._Element__pointer == l._Element__value), None)
            if parent:
                parent_name = " ".join(parent.get_name())
                individuals.append(parent_name)

    
