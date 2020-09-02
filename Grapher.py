import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Grapher:
    def __init__(self, data: pd.DataFrame, intervals=None):

        self.data = self._preprocess_data(data)

        self._set_intervals(intervals)

    def _check_duplicates(self, data):

        prev_val = None
        duplicate_counter = 0

        for index, row in data.iterrows():

            # Skip 1st iteration to set prev_val
            if index == 0:
                prev_val = row
                print(prev_val)
                continue
            
            # Actual Loop
            if prev_val[0] == row[0]:
                duplicate_counter += 1

            # df.set_value(index,'ifor',ifor_val)
            prev_val = row

        return duplicate_counter > 0

    def _create_new_time_val(self, datetime_, flag=False):

        date, hour = datetime_.split('_')

        if not flag:
            hour += ":30"
        else:
            hour += ":00"
        
        fixed_datetime = "_".join([date, hour])

        return fixed_datetime

    def _fix_duplicates(self, data):
        
        prev_val = None

        for index, row in data.iterrows():

            # Skip 1st iteration to set prev_val
            if index == 0:
                prev_val = row
                new_val = self._create_new_time_val(row[0], True)
                data.at[index, 'time'] = new_val
                continue
            
            # Actual Loop
            if prev_val[0] == row[0]:
                new_val = self._create_new_time_val(row[0])
                data.at[index, 'time'] = new_val

            else:
                new_val = self._create_new_time_val(row[0], True)
                data.at[index, 'time'] = new_val

            prev_val = row

    def _repair_time_column(self, data):
        """
        Time column has rows that refer to different rates but have the
        same value. This method fixes that by appending a ':00' or ':30' to the
        hour:minute section of the date
        """
        has_duplicates = self._check_duplicates(data)

        if has_duplicates:
            self._fix_duplicates(data)

        else:
            return

    def _create_date_column(self, data):
        date_column = []

        for val in data['time']:
            date_val = val.split('_')[0]
            date_column.append(date_val)

        data['date'] = np.array(date_column)

    def _create_hour_column(self, data):
        hourminute_column = []

        for val in data['time']:
            hourminute_val = val.split('_')[1]
            hourminute_column.append(hourminute_val)

        data['hour_minute'] = np.array(hourminute_column)

    def _preprocess_data(self, data):
        """
        Fixes non-unique entries in the time column and
        Divides the time column into 'date' and 'hour' columns
        """

        self._repair_time_column(data)

        self._create_date_column(data)
        
        self._create_hour_column(data)

        return data

    def _apply_intervals(self, intervals):
        """
        sets data to only the rows that are within the given intervals

        example of intervals: ('31/08/2020 09:00', '31/08/2020 18:00')
        """
        pass

    def _set_intervals(self, intervals):
        if intervals is None:
            # All data will be graphed
            return

        else:
            self._apply_intervals(intervals)

    def create_graph(self):

        print(self.data)

        figure = plt.figure()

        plt.plot('time', 'selling', data=self.data[:10])
        plt.plot('time', 'buying', data=self.data[:10])

        # Clear xtick labels
        plt.xticks([])

        plt.show()
