import os
import pathlib
import subprocess

# git config --global user.name "Your Name"
# git config --global user.email "youremail@yourdomain.com"

# sudo lsof -i -P -n | grep LISTEN

def main():
    # bl api board

    same_comment = True
    comment = None

    comment = "fix config"
    comment = "wip: refactor role validation"
    comment = "upd: rewrite select all api call"
    comment = "init: screens"
    comment = "impl: create / update portfolio"
    comment = 'ref: rewrite db scheme'

    comment = "fix: wip"

    if same_comment:
        if not comment:
            comment = input("comment for all commits will be same:")

    base_dir = pathlib.Path(os.getcwd()).parent.parent

    result = subprocess.run(
        ["git", "-C", base_dir, "status"],
        capture_output=True, text=True
    )

    print(result.stdout)
    print(80 * "-")

    to_c = set()

    for line in result.stdout.split("\n"):
        if line.startswith("	"):
            line = line.strip()

            if line.startswith("renamed:"):
                line = line.split("-> ")[1]
                to_c.add(line)
                continue

            try:
                line = line.split(":")[1].strip()
            except IndexError:
                pass

            to_c.add(line)

    sh_script_content = []

    print("enter messages")

    for file in set(to_c):
        if not same_comment:
            desc = input(f"{file}\n")
        else:
            desc = comment

        message = "git commit -m " + f'\"{" ".join(file.split("/"))} - {desc}\"'

        file_full_path = base_dir / file
        sh_script_content.append(f"git add {file_full_path}")
        sh_script_content.append(message)

    with open('git.sh', 'w+') as f:
        [f.write(f"{i}\n") for i in sh_script_content]


if __name__ == '__main__':
    main()