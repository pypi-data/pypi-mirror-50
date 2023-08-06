import os
import sys
import yaml
from docstr_coverage import get_docstring_coverage

BASE_DIR = os.getcwd()
CONFIG_PATH = ''
print(BASE_DIR)
def main():
    try:
        command = sys.argv[1]
    except IndexError:
        command = ''
    if command == 'make':
        print(f'{os.getcwd()}')
        print('i will make you')
    else:
        print('i will help you')
