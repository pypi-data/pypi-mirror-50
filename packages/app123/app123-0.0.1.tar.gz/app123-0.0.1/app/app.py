__version__ = "0.0.1"

import sys


def main():
    print(f"version={__version__}")
    print(f"called '{sys.argv[0]}' with args {sys.argv[1:]}")
