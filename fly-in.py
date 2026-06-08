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
            graph = Parser(argv[1]).parse()

        except Exception as e:
            print(f"Error during parsing {e}")
            return
        try:
            simulation = Simulation()
            simulation.simulate(graph)
        except Exception as e:
           print(f"Something went wrong in the simulation: {e}") 


if __name__ == "__main__":
    main()
