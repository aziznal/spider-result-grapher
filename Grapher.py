import pandas as pd
import matplotlib.pyplot as plt


class Grapher:
    def __init__(self, data: pd.DataFrame, intervals=None):

        self.data = self.prepare_data(data)

        self.set_intervals(intervals)

    def prepare_data(self, data):
        """
        This will divide the time column into 'date' and 'time' columns
        """

        return data

    def filter_data(self, intervals):
        """
        sets data to only the rows that are within the given intervals
        """
        pass

    def set_intervals(self, intervals):
        if intervals is None:
            return

        else:
            self.filter_data(intervals)

    def create_graph(self):
        print("Creating Graph..")
        
        figure = plt.figure()

        plt.plot('time', 'selling', data=self.data)
        plt.plot('time', 'buying', data=self.data)

        plt.xticks([])

        plt.show()
