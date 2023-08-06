def make():
    if prebuild():
        WORK_DIR = work_dir()
        for item_dir in data_loaded.get('dir'):
            dir_name = f'{WORK_DIR}/{item_dir}'
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            for item_module in data_loaded.get('dir').get(item_dir):
                file_name = f'{dir_name}/{item_module}.rst'
                with open(file_name, "w+") as f:
                    line = '=' * (len(item_dir) + 1 + len(item_module))
                    f.write(
                        f'{item_dir} {item_module}\n{line}\n\n.. automodule:: {item_dir}.{item_module} \n    :members:\n')

        line = '=' * len("Module")
        file_name = f'{WORK_DIR}/modules.rst'
        content = f'Module\n{line}\n\n.. toctree::\n    :maxdepth: 2\n    :caption: Module:\n    :glob:\n\n'
        for item_dir in data_loaded.get('dir'):
            content += f'    {item_dir}/*\n'
        with open(file_name, "w+") as f:
            f.write(content)
        rewrite_config()


def rewrite_config():
    path, back = get_config_path()
    with open(path, 'a+') as f:
        f.write("import os\n")
        f.write("import sys\n")
        f.write("import django\n")
        f.write(f"sys.path.insert(0, os.path.abspath('{back}'))\n")
        f.write(f"os.environ['DJANGO_SETTINGS_MODULE'] = '{data_loaded.get('DJANGO_SETTINGS_MODULE')}'\n")
        f.write("django.setup()\n")
        f.write("extensions += ['sphinx.ext.autodoc']\n")


def prebuild():
    if os.path.exists('docs'):
        os.chdir('docs')
        if os.path.exists('index.rst'):
            os.chdir('..')
            return True
        elif os.path.exists('index.rst'):
            os.chdir('..')
            return True
    else:
        os.mkdir('docs')
        os.chdir('docs')
    os.system('sphinx-quickstart')
    os.chdir('..')
    return True


def work_dir():
    if os.path.exists('docs/source/index.rst'):
        return 'docs/source'
    elif os.path.exists('docs/index.rst'):
        return 'docs'
    else:
        raise Exception


def get_config_path():
    if os.path.exists('docs/conf.py'):
        return 'docs/conf.py', '..'
    elif os.path.exists('docs/source/conf.py'):
        return 'docs/source/conf.py', '../..'
    else:
        raise Exception