from pathlib import Path

DATA_DIRECTORY = Path(__file__).parents[1] / "files"
ASSETS_DIRECTORY = Path(__file__).parents[1] / "assets"


if __name__ == "__main__":
    print("\n"*2)
    print(DATA_DIRECTORY)
    print("\n"*2)
    print(ASSETS_DIRECTORY)
    print("\n"*2)