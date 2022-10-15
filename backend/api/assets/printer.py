import pathlib


def print_logo():
    current_folder = pathlib.Path(__file__).parent.resolve()

    with open(current_folder / "ascii_logo.txt", "r") as f:
        print(f.read())


def main():
    print_logo()


if __name__ == '__main__':
    main()
