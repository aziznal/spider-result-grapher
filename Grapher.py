import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from DataCleaner import DataCleaner, DataMerger


# Bank Line Colors
ISBANK = '#0042ff'          # Blue
KUVEYTTURK = '#00ff78'      # Green
VAKIF = '#e48a00'           # Yellow
YAPIKREDI = '#00d8ff'       # Light Blue
ZIRAAT = '#ff2a00'          # Red


def get_color_from_bankname(bankname):

    if bankname == 'ISBANK':
        print(bankname)
        return ISBANK

    if bankname == 'KUVEYTTURK':
        print(bankname)
        return KUVEYTTURK

    if bankname == 'VAKIF':
        print(bankname)
        return VAKIF

    if bankname == 'YAPIKREDI':
        print(bankname)
        return YAPIKREDI

    if bankname == 'ZIRAAT':
        print(bankname)
        return ZIRAAT


class Grapher:
    def __init__(self, data: pd.DataFrame, intervals=None, bankname="", save_graph=False, graph_filename=""):

        self.bankname = bankname

        self._save_graph = save_graph
        self.graph_filename = graph_filename

        self.data = self.clean_data(data)

        self._set_intervals(intervals)

    def clean_data(self, data):
        cleaner = DataCleaner(data)
        cleaner.clean()

        cleaner.save("clean_data/clean_" + self.bankname + ".csv")

        return cleaner.data

    def _find_first_that_matches(self, value):
        """
        return index of first row with 'date' and 'hour_minute' columns
        matching given value.
        """
        date, time = value.split(' ')

        time_val = ":".join(time.split(':')[:2]) + ":00"

        datelist = self.data[self.data['date'] == date]

        for i, row in datelist.iterrows():
            val = row[-1]

            if val == time_val:
                return i

        return -1

    def _apply_intervals(self, intervals):
        """
        sets data to only the rows that are within the given intervals

        example of intervals: ('31-08-2020 09:00', '31-08-2020 18:00')
        """

        first_index = self._find_first_that_matches(intervals[0])
        last_index = self._find_first_that_matches(intervals[1])

        if first_index == -1 or last_index == -1:
            # All data will be graphed in this case
            print("Bad Interval was given")

        else:
            self.data = self.data[first_index:last_index]

    def _set_intervals(self, intervals):
        if intervals is None:
            # All data will be graphed
            return

        else:
            self._apply_intervals(intervals)

    def create_graph(self):

        print(self.data.head())

        figure, ax = plt.subplots()

        color = get_color_from_bankname(self.bankname)

        plt.plot('time', 'buying', data=self.data, c=color, linewidth=1)
        plt.plot('time', 'selling', data=self.data, c=color, linewidth=1)

        plt.title('USD to TL conversion rates - %s' % self.bankname)
        plt.xlabel('Time')
        plt.ylabel('Price (TL)')

        # Some settings for xticklabels
        ax.xaxis.set_major_locator(plt.MaxNLocator(9))
        plt.xticks(rotation=45, ha='right', fontsize=7)

        # self.set_xtick_labels()

        figure.tight_layout()

        if self._save_graph:
            # TODO: automate filename creation
            print("Saving Graph..")

            try:
                plt.savefig(self.graph_filename, dpi=600)

            except FileNotFoundError:
                dirname = self.graph_filename.split('/')[0]
                os.mkdir(dirname)

                plt.savefig(self.graph_filename, dpi=600)


        self.print_std_deviation()
        plt.show()

    def print_std_deviation(self):
        print(f"Standard deviation of {self.bankname}:\n {self.data.std()}")


class SuperGrapher(Grapher):
    def __init__(self, raw_bank_data: dict, intervals=None, save_graph=False, graph_filename=''):
        """
        :param data (dict): a dictionary with the form {bankname: bankdata}
        """

        self._save_graph = save_graph
        self.graph_filename = graph_filename

        self.raw_bank_data = raw_bank_data

        self.clean_bank_data = self.load_all_data(intervals)

        self.merged_data = self.merge_datasets()
    
    def load_all_data(self, intervals):
        """
        pass all data through Grapher.__init__ for cleaning and preprocessing
        """
        data = {}

        for bankname, bankdata in self.raw_bank_data.items():
            clean_data = Grapher(data=bankdata, intervals=intervals, bankname=bankname).data
            data[bankname] = clean_data

        return data

    def merge_datasets(self):

        merger = DataMerger(self.clean_bank_data)
        merger.merge_data()

        merger.save(path="merged_data/")

        return merger.datasets

    def create_overlayed_graph(self):

        figure, ax = plt.subplots()

        for bankname, bankdata in self.merged_data.items():

            color = get_color_from_bankname(bankname)
            plt.plot('time', 'buying', data=bankdata, c=color, linewidth=1)
            plt.plot('time', 'selling', data=bankdata, c=color, linewidth=1)

        plt.title('USD to TL conversion rates - All banks')
        plt.xlabel('Time')
        plt.ylabel('Price (TL)')

        # Some settings for xticklabels
        ax.xaxis.set_major_locator(plt.MaxNLocator(9))
        plt.xticks(rotation=45, ha='right', fontsize=7)

        labels = []
        for name in self.merged_data.keys():
            labels.append(name + "- Buying")
            labels.append(name + "- Selling")

        plt.legend(labels)

        figure.tight_layout()

        if self._save_graph:
            # TODO: automate filename creation
            print("Saving Graph..")

            try:
                plt.savefig(self.graph_filename, dpi=690)

            except FileNotFoundError:
                dirname = self.graph_filename.split('/')[0]
                os.mkdir(dirname)

                plt.savefig(self.graph_filename, dpi=600)

        plt.show()
