import os
import sys


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
