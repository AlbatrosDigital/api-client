import sys
import json
import importlib.util
from pathlib import Path


def jsonify(path: Path):
    module_name = path.stem

    spec = importlib.util.spec_from_file_location(module_name, str(path))
    input_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(input_module)

    input_dict = input_module.INPUT
    role = input_module.ROLE

    input = json.dumps(input_dict)
    output = {
        "name": module_name,
        "role": role,
        "value": input
    }
    return output
