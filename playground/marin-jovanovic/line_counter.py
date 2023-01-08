import os
import pathlib


def sum_lines(path):
    total_lines = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    total_lines += len(lines)
    return total_lines

if __name__ == '__main__':

    current_folder = pathlib.Path(__file__).parent.parent.parent.resolve()
    print(current_folder / "backend")
    t = sum_lines(current_folder / "backend")

    print(f"{t=}")


