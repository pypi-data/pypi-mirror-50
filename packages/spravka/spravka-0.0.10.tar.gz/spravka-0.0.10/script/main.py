from script.change_version import main as change_version
from script.remove_dir import main as remove_dir
from script.git import main as git
from script.pip_upload import main as pip_upload

if __name__ == '__main__':
    change_version()
    pip_upload()
    remove_dir()
    git()
