from PyQt5 import uic
from PyQt5.QtWidgets import *

from functions import *

from time import sleep

env_vars = get_env_vars()
banknames = env_vars['banknames']


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

        self.next_button: QPushButton = self.find_next_button()
        self.bank_checkboxes = self.find_bank_checkboxes()
        self.select_all = self.find_select_all_checkbox()

        self.chosen_banks = {name: False for name in banknames}

        self.step2_created = False
        self.step2_window = None

        self.add_all_listeners()

    def find_next_button(self):
        return self.widget_objects['nextButton']

    def find_bank_checkboxes(self):
        return [
            self.widget_objects['isbankCheckBox'],
            self.widget_objects["kuveytturkCheckBox"],
            self.widget_objects["vakifCheckBox"],
            self.widget_objects["yapikrediCheckBox"],
            self.widget_objects["ziraatCheckBox"],
        ]

    def find_select_all_checkbox(self):
        return self.widget_objects['selectAllCheckBox']

    def add_all_listeners(self):
        self.next_button.clicked.connect(self.next_button_onclick)
        [checkbox.clicked.connect(self.bank_checkbox_onclick)
         for checkbox in self.bank_checkboxes]
        self.select_all.clicked.connect(self.select_all_onclick)

    def next_button_onclick(self):
        self.goto_step2()

    def bank_checkbox_onclick(self):
        for checkbox in self.bank_checkboxes:
            self.chosen_banks[checkbox.text().upper()] = checkbox.isChecked()

    def select_all_onclick(self):
        [checkbox.setDisabled(self.select_all.isChecked())
         for checkbox in self.bank_checkboxes]

        for bank in self.chosen_banks.keys():
            self.chosen_banks[bank] = self.select_all.isChecked()

        if not self.select_all.isChecked():
            self.bank_checkbox_onclick()

    def create_step2_window(self):
        gui_path = env_vars['gui']['step2']
        widgets = load_json(env_vars['widgets']['step2'])

        self.step2_window = Step2(self,
                                  chosen_banks=self.chosen_banks,
                                  widget_ids=widgets,
                                  gui_file_path=gui_path
                                  )

        self.step2_window.show()
        self.step2_created = True

    def show_step2_window(self):
        self.step2_window.chosen_banks = self.chosen_banks
        self.step2_window.show()

    def goto_step2(self):
        self.hide()

        sleep(0.05)  # for better transition

        if not self.step2_created:
            self.create_step2_window()

        self.show_step2_window()


class Step2(Gui):
    def __init__(self, step1, chosen_banks, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # REFACTOR: choose better names for variables

        self.step1 = step1
        self.chosen_banks = chosen_banks

        self.back_button = self.find_back_button()
        self.graph_button = self.find_graph_button()

        self.checkbox: QCheckBox = self.find_graph_all_checkbox()

        self.start_datetime: QDateTimeEdit = self.find_start_datetime()
        self.end_datetime: QDateTimeEdit = self.find_end_datetime()

        self.save_graph: QCheckBox = self.find_save_graph_checkbox()
        self.filename_edit: QLineEdit = self.find_filename_input()

        self.add_all_listeners()

    def add_all_listeners(self):
        self.back_button.clicked.connect(self.back_button_onclick)
        self.graph_button.clicked.connect(self.graph_button_onclick)
        self.checkbox.clicked.connect(self.checkbox_onclick)
        self.save_graph.clicked.connect(self.save_graph_onclick)

    def find_back_button(self):
        return self.widget_objects['backButton']

    def find_graph_button(self):
        return self.widget_objects['createGraphButton']

    def find_graph_all_checkbox(self):
        return self.widget_objects['graphAllCheckBox']

    def find_start_datetime(self):
        return self.widget_objects['startDate']

    def find_end_datetime(self):
        return self.widget_objects['endDate']

    def find_save_graph_checkbox(self):
        return self.widget_objects['saveGraphCheckBox']

    def find_filename_input(self):
        return self.widget_objects['filenameLineEdit']

    def back_button_onclick(self):
        self.goto_step1()

    def checkbox_onclick(self):
        checked = self.checkbox.isChecked()

        if checked:
            self.start_datetime.setDisabled(True)
            self.end_datetime.setDisabled(True)

        else:
            self.start_datetime.setDisabled(False)
            self.end_datetime.setDisabled(False)

    def save_graph_onclick(self):
        if self.save_graph.isChecked():
            self.filename_edit.setEnabled(True)
            self.filename_edit.setPlaceholderText('filename.png')

        else:
            self.filename_edit.setEnabled(False)
            self.filename_edit.setPlaceholderText('')

    def graph_button_onclick(self):
        self.goto_create_graph(all_=self.checkbox.isChecked())

    def get_selected_interval(self):
        interval_1 = self.start_datetime.text()
        interval_2 = self.end_datetime.text()

        return interval_1, interval_2

    def goto_step1(self):
        self.hide()

        sleep(0.05)  # for better transition

        self.step1.show()

    def multiple_banks_chosen(self):
        print(self.chosen_banks)
        return len([val for val in self.chosen_banks.values() if val == True]) > 1

    def goto_create_graph(self, all_=False):
        
        if self.multiple_banks_chosen():
            create_overlayed_graph(intervals=self.get_selected_interval(),
                                   chosen_banks=self.chosen_banks,
                                   save_graph=self.save_graph.isChecked(),
                                   graph_filename=self.filename_edit.text(),
                                   graph_all_results=self.checkbox.isChecked()
                                   )

        else:
            create_graph(intervals=self.get_selected_interval(),
                         chosen_banks=self.chosen_banks,
                         save_graph=self.save_graph.isChecked(),
                         graph_filename=self.filename_edit.text(),
                         graph_all_results=self.checkbox.isChecked()
                         )
