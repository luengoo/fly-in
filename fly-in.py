from sys import argv
from parser import Parser
from pydantic import ValidationError
from simulation import Simulation


def main() -> None:

    if len(argv) != 2 or not argv[1].endswith(".txt"):
        print("Usage: python3 fly-in.py input.txt")
        return
    else:
        try:
            simulation = Simulation()
            graph = Parser(argv[1]).parse()
            simulation.simulate(graph)

        except (ValueError, ValidationError) as e:
            if isinstance(e, ValidationError):
                print(f"Error during parsing: {e}")
                return
            else:
                print(f"Error during parsing {e}")
                return


if __name__ == "__main__":
    main()
