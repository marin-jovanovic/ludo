import pathlib


def print_logo():
    current_folder = pathlib.Path(__file__).parent.parent.parent.parent.resolve()

    print(current_folder)
    with open(current_folder / "resources" / "ascii_art" / "ascii_logo.txt", "r") as f:
        print(f.read())

def main():
    print_logo()


if __name__ == '__main__':
    main()
