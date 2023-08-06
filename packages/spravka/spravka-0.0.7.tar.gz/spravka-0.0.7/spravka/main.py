import os
import sys
import yaml
from .make import make
from .html import html
from .coverage import coverage

BASE_DIR = os.getcwd()
CONFIG_PATH = os.path.join(BASE_DIR, "spravka.yml")

with open(CONFIG_PATH, 'r') as stream:
    data_loaded = yaml.safe_load(stream)


def main():
    try:
        command = sys.argv[1]
    except IndexError:
        command = ''
    if command == 'make':
        make()
    elif command == 'html':
        html()
    elif command == 'coverage':
        coverage()
    else:
        print('i will help you')


