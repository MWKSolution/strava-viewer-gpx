from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from json import dump, load
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
    """Connecting to database written in json file."""
    ACT_FILE = Path(__file__).parent / 'local/activities.json'

    def save_data(self, new_acts):
        """Append new activities to current database and save (overwrite).
        New acts must be checked against duplicates before sending to this function !!!."""
        if new_acts:
            _acts = []
            if self.is_data_present():  # load current database
                with open(self.ACT_FILE, 'r') as json_file:
                            _acts = load(json_file)
            _acts.extend(new_acts)  # add new activities
            _acts.sort(key=op.itemgetter('timestamp'), reverse=True)  # descending order by timestamp
            with open(self.ACT_FILE, 'w') as json_file: # save as json file
                dump(_acts, json_file)

    def get_activities(self):
        """oad activities from database"""
        _df = pd.read_json(self.ACT_FILE, orient='columns', convert_dates=False)
        return _df

    def is_data_present(self):
        """Check if database exists"""
        return self.ACT_FILE.exists() #


