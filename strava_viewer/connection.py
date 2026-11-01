from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from json import dump, load, loads, dumps
import operator as op


class NotValidConnection(Exception):
    pass


class Connection(ABC):
    """Abstract class for connecting to database containing activities.
    Redis support was dropped and now only .json file could be used"""

    @abstractmethod
    def get_activities(self):
        """Get DataFrame of activities from database"""
        pass

    @abstractmethod
    def save_data(self, acts):
        """Save all data to database (overwrite)"""
        pass

    @abstractmethod
    def is_data_present(self):
        """Check if database is present"""
        pass


class JsonFile(Connection):
    ACT_FILE = Path(__file__).parent / 'local/activities.json'

    # def save_data(self, acts, mode):
    #     _acts = []
    #     if mode == 'append':
    #         if self.is_data_present():
    #             with open(self.ACT_FILE, 'r') as json_file:
    #                 _acts = load(json_file)
    #     _acts.extend(acts)
    #     _acts.sort(key=op.itemgetter('timestamp'), reverse=True)  # descending order by timestamp
    #     with open(self.ACT_FILE, 'w') as json_file:
    #         dump(_acts, json_file)

    def save_data(self, acts):
        """No append mode (acts loaded from gpx files)
        Load data from database (file) - checked against duplicates
        append new acts - save  - file (activities.json) is overwritten"""
        if acts:
            _acts = []
            if self.is_data_present():
                with open(self.ACT_FILE, 'r') as json_file:
                            _acts = load(json_file)
            _acts.extend(acts)
            # print(f'present {_acts}')
            # print(f'new {acts}')
            _acts.sort(key=op.itemgetter('timestamp'), reverse=True)  # descending order by timestamp
            with open(self.ACT_FILE, 'w') as json_file:
                dump(_acts, json_file)

    def get_activities(self):
        _df = pd.read_json(self.ACT_FILE, orient='columns', convert_dates=False)
        return _df

    def is_data_present(self):
        return self.ACT_FILE.exists()


