import os
from ruamel.yaml import YAML

def replace(target: dict) -> dict:
    result = dict()
    for key, val in target.items():
        if isinstance(val, dict):
            rval = replace(val)
            result[key] = rval
        else:
            result[key] = os.getenv(str(val), val)
    return result

if __name__ == '__main__':
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(curr_dir)

    yaml = YAML()
    yaml.preserve_quotes = True
    with open('./config.template.yaml', 'r', encoding='utf-8') as file:
        template_dict: dict = yaml.load(file)

    result_dict = replace(template_dict)

    with open('/configs/config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(result_dict, file)
