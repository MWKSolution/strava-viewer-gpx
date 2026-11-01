"""Module for importing data from Strava"""
from pathlib import Path
from urllib3 import disable_warnings, exceptions
from datetime import datetime
from strava_viewer.activities_options import get_options
from strava_viewer.layouts import get_chart
from strava_viewer.connection import JsonFile, NotValidConnection

from strava_viewer.formats import is_gpx
import gpxpy

disable_warnings(exceptions.InsecureRequestWarning)


class StravaData:

    def __init__(self, data='local'):
        """local - local/activities.json"""
        if data == 'local':
            self.conn = JsonFile()
        else:
            self.conn = None
            raise NotValidConnection

    def load_dataGPX(self):
        """Load data present in /gpx directory
        Check for any duplicates against data in activities.json file (id !!!)
        Then save data (overwrite)"""
        _acts = self.get_new_activitiesGPX()
        self.conn.save_data(_acts)

    # def refresh_dataGPX(self): # TODO # fix this
    #     """???"""
    #     _acts = self.get_activitiesGPX(after=self.LATEST_ACTIVITY + 900)
    #     # +900 - 'after' should be +15 min than latest activity ??????????????????????????????????????????????
    #     self.conn.save_data(_acts, mode='append')


    def get_new_activitiesGPX(self):
        """Get activities metadata from .gpx files downloaded from strava to /gpx directory"""
        print()
        print('Loading data...')
        activities_ids = list()
        if self.acts_data_present():
            # get list of id's of all actvities in database to check for duplicates
            activities_ids = self.get_activitiesDATA()['id'].tolist()  # activities in database
        new_activities = list()  # list of all unique activities extracted from gpx files
        directory = Path(__file__).parent / 'gpx'
        for file_path in directory.iterdir():
            if file_path.suffix == ".gpx" and file_path.is_file():
                # activity id is in the name of file
                # fast check to not open and process file
                try:
                    # convert to int value - pd.read_json in connection.py reads it as int anyway
                    aid = int(file_path.stem.removeprefix('strava_'))
                except ValueError:
                    print(f'Loading file: {file_path.name}', end='  >>>  ')
                    print('GPX file ID error')
                    print('ERROR - skipped')
                else:
                    if aid not in activities_ids: # dont process duplicates
                        print(f'Loading file: {file_path.name}', end='  >>>  ')
                        if is_gpx(file_path):
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                gpx = gpxpy.parse(f)
                            track = gpx.tracks[0]
                            bounds = track.get_time_bounds()
                            uphill, downhill = track.get_uphill_downhill()
                            # add list entry as a
                            new_activities.append(
                                dict(id=aid,
                                     year=bounds.start_time.year,
                                     month=bounds.start_time.month,
                                     day=bounds.start_time.day,
                                     type=track.type,
                                     time=track.get_duration() / 3600,  # hours
                                     distance=track.length_3d() / 1000, # kilometers
                                     gain=uphill,
                                     timestamp=int(bounds.end_time.timestamp())
                                     )
                            )
                            print('OK - loaded')
                        else:
                            print('ERROR - skipped')
        return new_activities

# TODO # check all below this!!!
#         dt_obj = datetime.strptime(act_date, '%Y-%m-%dT%H:%M:%SZ')


    def get_activitiesDATA(self):
        """Get all activities from file or redis and return them as dataframe."""
        _df = self.conn.get_activities()
        ts = _df['timestamp'].max()
        self.LATEST_ACTIVITY = ts
        return _df

    def acts_data_present(self):
        """Check if activities data is present."""
        return self.conn.is_data_present()

    def get_optionsDATA(self):
        df = self.get_activitiesDATA()
        return get_options(df)

    def get_chartDATA(self, metrics, activity, year):
        df = self.get_activitiesDATA()
        if year != 'All':
            df = df[df['year'] == int(year)]
        df = df[df['type'].isin(activity)]
        return get_chart(df, metrics, activity, year)


if __name__ == '__main__':

    data = StravaData()

    activities = data.get_new_activitiesGPX()

    print(activities)

