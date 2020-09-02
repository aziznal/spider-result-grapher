import os
import stat
import platform
import sys


current_os = platform.system()

windows_ext = '.bat'
linux_ext = '.sh'

install_filename = 'install'
run_filename = 'run'


def create_install_file():
    if current_os == "Windows":
        with open(f'{install_filename}{windows_ext}', 'w') as file:
            file.write('python -m venv venv\n')
            file.write('call venv/Scripts/activate\n')
            file.write('python -m pip install --upgrade pip\n')
            file.write('pip install -r requirements.txt\n')

            file.write('\n\nPAUSE\n')


    elif current_os == "Linux":
        pass


def create_run_file():
    if current_os == 'Windows':
        with open(f'{run_filename}{windows_ext}', 'w') as file:
            file.write('call venv/Scripts/activate\n')
            file.write('python main.py\n')

    elif current_os == "Linux":
        pass


if __name__ == "__main__":
    create_install_file()
    create_run_file()
