import os
import yaml
from docstr_coverage import get_docstring_coverage

BASE_DIR = os.getcwd()
CONFIG_PATH = os.path.join(BASE_DIR, "spravka.yml")

with open(CONFIG_PATH, 'r') as stream:
    data_loaded = yaml.safe_load(stream)

coverage_list = []
def coverage():
    for item_dir in data_loaded.get('dir'):
        for item_module in data_loaded.get('dir').get(item_dir):
            coverage_list.append(f'{item_dir}/{item_module}.py')
    response = get_docstring_coverage(coverage_list)
    for i in response[0]:
        print("{0:40} {1}%".format(i, response[0][i].get('coverage')), end='\n\n')
