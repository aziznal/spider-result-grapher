


class DataCleaner:
    def __init__(self, data: pd.DataFrame, intervals=None, bankname="", save_graph=False, graph_filename=""):

        self.bankname = bankname

        self._save_graph = save_graph
        self.graph_filename = graph_filename

        self.data = self._preprocess_data(data)

        self._set_intervals(intervals)

    def _check_duplicates(self, data):

        prev_val = None
        duplicate_counter = 0

        for index, row in data.iterrows():

            # Skip 1st iteration to set prev_val
            if index == 0:
                prev_val = row
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

    def _find_first_that_matches(self, value):
        """
        return index of first row with 'date' and 'hour_minute' columns
        matching given value. Raise Exception otherwise.
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
            print("Bad Interval was given")

        else:
            self.data = self.data[first_index:last_index]

    def _set_intervals(self, intervals):
        if intervals is None:
            # All data will be graphed
            return

        else:
            self._apply_intervals(intervals)
