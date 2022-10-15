import pathlib
import subprocess


def main():
    current_dir = pathlib.Path(__file__).parent.resolve()
    src = current_dir.parent.resolve()

    build_env_scheme(src)
    build_pip_req(src)


def build_pip_req(src):

    destination_file_name = "requirements.pip.txt"

    with open(src / destination_file_name, "w+") as f:

        result = subprocess.run(
            ["pip3", "freeze"], text=True, stdout=f
        )

    if result.stderr:
        print("stderr:", result.stderr)

    return not result.stderr


def build_env_scheme(src):
    destination_file_name = "env-scheme.txt"

    with open(src / ".env", "r") as f:
        l = f.read()
        l = [i.split("=", 1)[0] + "=" for i in l.split("\n") if i]

        for i in l:
            if i.islower():
                print(
                    f"possible leak detected, check {destination_file_name} file")

        with open(src / destination_file_name, "w+") as f_2:
            for i in l:
                f_2.write(i + "\n")



if __name__ == '__main__':
    main()