import json
import pathlib
import csv


def join_with_curr_path(p):
    curr_path = pathlib.Path(__file__).parent.resolve()
    return curr_path / p


def _get_config(config_name, curr_dir=True, json_or_csv=True):
    p = join_with_curr_path(config_name) if curr_dir else config_name

    if json_or_csv:
        with open(p) as f:
            return json.loads(f.read())

    else:
        with open(p, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',',
                       quotechar='|')

            return [i for i in csv_reader]


vue_interface_path = pathlib.Path(__file__).parent.parent.parent.parent / "public" / "api_scheme" / "params.json"
vue_interface_cfg = _get_config(vue_interface_path, curr_dir=False)
