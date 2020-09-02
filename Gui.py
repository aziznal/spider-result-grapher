from PyQt5 import uic
from PyQt5.QtWidgets import *

from functions import *

from time import sleep


# Bank names
ISBANK = 0
KUVEYTTURK = 1
VAKIFBANK = 2
YAPIKREDI = 3
ZIRAAT = 4

env_vars = get_env_vars()


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
        self.combobox: QComboBox = self.find_combobox()

        self.current_bank = ISBANK

        self.step2_created = False
        self.step2_window = None

        self.add_all_listeners()

    def find_next_button(self):
        return self.widget_objects['nextButton']

    def find_combobox(self):
        return self.widget_objects['bankDropDownMenu']

    def add_all_listeners(self):
        self.next_button.clicked.connect(self.next_button_onclick)
        self.combobox.activated.connect(self.combobox_onclick)

    def next_button_onclick(self):
        self.goto_step2()

    def combobox_onclick(self):
        self.current_bank = self.combobox.currentIndex()

    def create_step2_window(self):
        gui_path = env_vars['gui']['step2']
        widgets = load_json(env_vars['widgets']['step2'])

        self.step2_window = Step2(
            self, self.current_bank, widget_ids=widgets, gui_file_path=gui_path)
        self.step2_window.show()

        self.step2_created = True

    def show_step2_window(self):
        self.step2_window.current_bank = self.current_bank
        self.step2_window.show()

    def goto_step2(self):
        self.hide()

        sleep(0.05)  # for better transition

        if not self.step2_created:
            self.create_step2_window()

        self.show_step2_window()


class Step2(Gui):
    def __init__(self, step1, current_bank, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # REFACTOR: choose better names for variables

        self.step1 = step1
        self.current_bank = current_bank

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

    def goto_create_graph(self, all_=False):
        if all_:
            create_graph(bank=self.current_bank,
                         intervals=None,
                         graph_all_results=True,
                         save_graph=self.save_graph.isChecked(),
                         graph_filename=self.filename_edit.text()
                         )

        else:
            create_graph(bank=self.current_bank,
                         intervals=self.get_selected_interval(),
                         save_graph=self.save_graph.isChecked(),
                         graph_filename=self.filename_edit.text()
                         )


class App(Gui):
    def __init__(self, widget_ids, gui_file_path):
        super().__init__(widget_ids, gui_file_path)

        self.current_bank = 0

        self.bank_list, self.start_date, self.end_date = self.find_comboboxes()
        self.bank_label = self.find_bank_label()
        self.use_all, self.save_graph = self.find_checkboxes()
        self.start_time, self.end_time = self.find_time_edits()
        self.graph_filename = self.find_graph_filename()
        self.stat_results = self.find_stats_box()

    def add_all_listeners(self):
        self.bank_list.clicked.connect(self.bank_list_listener)

    def find_comboboxes(self):

        comboboxes = [
            self.widget_objects['bankDropDownMenu'],
            self.widget_objects['startDateComboBox'],
            self.widget_objects['endDateComboBox']
        ]

        return comboboxes

    def find_bank_label(self):
        return self.widget_objects['selectedBankLabel']

    def find_checkboxes(self):
        checkboxes = [
            self.widget_objects['useAllDataCheckBox'],
            self.widget_objects['saveGraphCheckBox']
        ]

        return checkboxes

    def find_time_edits(self):
        timeedits = [
            self.widget_objects['startTime'],
            self.widget_objects['endTime']
        ]

        return timeedits

    def find_graph_filename(self):
        return self.widget_objects['graphFilename']

    def find_stats_box(self):
        return self.widget_objects['statResults']

    def bank_list_listener(self):
        self.current_bank = self.bank_list.currentIndex()
        self.bank_label = self.bank_list.currentText()

    def start_date_listener(self):
        pass

    def end_date_listener(self):
        pass
