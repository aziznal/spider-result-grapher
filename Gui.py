from PyQt5 import uic
from PyQt5.QtWidgets import *


class Gui(QMainWindow):

    def __init__(self, widget_ids: dict, gui_file_path: str):
        super().__init__()
        
        # Stores all loaded widgets for easy access
        self.widget_objects = {}

        uic.loadUi(gui_file_path, self)

        self.gui_file_path = gui_file_path

        self.widget_ids: dict = widget_ids

        self._load_all_qt_objects()

    def _load_all_qt_objects(self):
        for object_type, id_list in self.widget_ids.items():
            for object_id in id_list:
                exec(
                    "self.widget_objects[object_id] = self.findChild(" + object_type + ", object_id)")


class Step1(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.next_button = self.find_next_button()
        self.combobox = self.find_combobox()

        self.add_all_listeners()

    def find_next_button(self):
        return self.widget_objects['nextButton']

    def find_combobox(self):
        return self.widget_objects['bankDropDownMenu']

    def add_all_listeners(self):
        self.next_button.clicked.connect(self.next_button_onclick)
        self.combobox.activated.connect(self.combobox_onclick)

    def next_button_onclick(self):
        print("next")

    def combobox_onclick(self):
        print(self.combobox.currentText())


class Step2(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_all_listeners()

    def add_all_listeners(self):
        pass


class Step3(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_all_listeners()

    def add_all_listeners(self):
        pass
