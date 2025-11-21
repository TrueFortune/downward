from lab.parser import Parser
import re

def add_unrolling_axiom_count(content, props):
    matches = re.findall(
        r"Axioms created with unrolling: (\d+)\n", content
    )
    print(matches)
    exit()
    match len(matches):
        case 0:
            props["unrolling_axioms"] = 0
        case 1: 
            props["unrolling_axioms"] = int(matches[0])
        case _:
            props.add_unexplained_error(
                f"multiple unrolling axiom counts found"
            )


def unrolling_parser():
    unrolling_parser = Parser()
    unrolling_parser.add_function(add_unrolling_axiom_count)
    return unrolling_parser