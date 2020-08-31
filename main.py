from PyQt5.QtWidgets import QApplication
import sys

from Gui import Step1
from functions import *

env_vars = get_env_vars()


def run_program():
    app = QApplication(sys.argv)

    gui_path = env_vars['gui']['step1']
    widgets = load_json(env_vars['widgets']['step1'])

    program = Step1(widget_ids=widgets, gui_file_path=gui_path)

    program.show()

    app.exec_()


if __name__ == '__main__':
    run_program()