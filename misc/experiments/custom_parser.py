from lab.parser import Parser
import re


def add_default_value_axiom_count(content, props):
    matches = re.findall(
        r"Default Value Axioms created: (\d+)\n", content
    )
    match len(matches):
        case 0:
            props["default_value_axioms"] = 0
        case 1: 
            props["default_value_axioms"] = int(matches[0])
        case _:
            props.add_unexplained_error(
                f"multiple default value axiom counts found"
            )

def add_default_value_axioms_percentage(content, props):
    matches = re.findall(
        r"Percentage of default value axioms: (.+)\n", content
    )
    match len(matches):
        case 0:
            props["default_value_axioms_percentage"] = 0
        case 1: 
            props["default_value_axioms_percentage"] = float(matches[0])
        case _:
            props.add_unexplained_error(
                f"multiple default value axiom percentages counts found"
            )

def add_unrolling_axiom_count(content, props):
    matches = re.findall(
        r"Axioms created with unrolling: (\d+)\n", content
    )
    match len(matches):
        case 0:
            props["unrolling_axioms"] = 0
        case 1: 
            props["unrolling_axioms"] = int(matches[0])
        case _:
            props.add_unexplained_error(
                f"multiple unrolling axiom counts found"
            )

def add_unrolling_axioms_percentage(content, props):
    matches = re.findall(
        r"Percentage of unrolling axioms: (.+)\n", content
    )
    match len(matches):
        case 0:
            props["unrolling_axioms_percentage"] = 0
        case 1: 
            props["unrolling_axioms_percentage"] = float(matches[0])
        case _:
            props.add_unexplained_error(
                f"multiple unrolling axiom percentages counts found"
            )

def add_unrolling_variables_count(content, props):
    matches = re.findall(
        r"Variables created with unrolling: (\d+)\n", content
    )
    match len(matches):
        case 0:
            props["unrolling_variables"] = 0
        case 1: 
            props["unrolling_variables"] = int(matches[0])
        case _:
            props.add_unexplained_error(
                f"multiple unrolling variable counts found"
            )


def unrolling_parser():
    unrolling_parser = Parser()
    unrolling_parser.add_function(add_default_value_axiom_count)
    unrolling_parser.add_function(add_default_value_axioms_percentage)
    unrolling_parser.add_function(add_unrolling_axiom_count)
    unrolling_parser.add_function(add_unrolling_axioms_percentage)
    unrolling_parser.add_function(add_unrolling_variables_count)
    return unrolling_parser