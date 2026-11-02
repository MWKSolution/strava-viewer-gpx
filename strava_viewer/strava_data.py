"""Module for importing data from Strava"""
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
import gpxpy

from strava_viewer.activities_options import get_options
from strava_viewer.layouts import get_chart
from strava_viewer.connection import JsonFile, NotValidConnection
from strava_viewer.gpx_data import is_gpx


class StravaData:

    def __init__(self, data='local'):
        """Database:
            local - local/activities.json
            redis database support was dropped
            no other posibilities"""
        if data == 'local':
            self.conn = JsonFile()
        else:
            self.conn = None
            raise NotValidConnection

    def load_dataGPX(self):
        """Load data present in /gpx directory
        Check for any duplicates against data in activities.json file (id !!!)
        Append new data then save data (overwrite)"""

        _acts = self.get_new_activitiesGPX()
        self.conn.save_data(_acts)

    def load_dataCSV(self):
        """Load data present in /csv directory
        Check for any duplicates against data in activities.json file (id !!!)
        Append new data then save data (overwrite)"""
        _acts = self.get_new_activitiesCSV()
        self.conn.save_data(_acts)

    def get_db_act_ids(self):
        """Getting present activities from database"""
        activities_ids = list()
        if self.acts_data_present():
            # get list of id's of all activities in database to check for duplicates
            activities_ids = self.get_activitiesDATA()['id'].tolist()  # activities in database
        return activities_ids


    def get_new_activitiesCSV(self):
        print()
        print('--- Loading CSV data... ------------------------------------------------------------------------------')
        activities_ids = self.get_db_act_ids()
        new_activities = list()
        file_path = Path(__file__).parent / 'csv' / 'activities.csv'
        columns_to_load = [0, 1, 3, 15, 17, 20, 21, 52]
        # id(0), date(1), type(3), time(15)s, distance(17)m, ascent(20), descent(21), gps(52)

        df = pd.read_csv(file_path, usecols = columns_to_load)  # load only needed columns
        df = df[df[df.columns[7]] == 0.0]  # load only row that in column 7 have 0.0 - manually entered activitie
                                           # rest was/can be laded from gpx files
        df.fillna(0.0, inplace=True)  # get rid of any NaN values

        df.columns = ['id', 'date', 'type', 'time', 'distance', 'ascent', 'descent', 'gps']
        # with pd.option_context("display.max_rows", None, "display.max_columns", None):
        #     print(df)

        acts = df.to_dict(orient='records') # df to list of dicts
        for rec in acts:
            id = int(rec['id'])
            if id not in activities_ids:
                start_time = datetime.strptime(rec['date'], "%d %b %Y, %H:%M:%S")
                year = start_time.year
                month = start_time.month
                day = start_time.day
                type= rec['type'].lower()
                time = rec['time'] / 3600
                distance = rec['distance'] / 1000
                gain = rec['ascent']
                timestamp = int((start_time + timedelta(hours=time)).timestamp())
                print(f'Loading activity {id}  >>>  {year}.{month:02d}.{day:02d} {type}: {time:.1f}h, {distance:.1f}km, {gain:.0f}m')
                new_activities.append(
                    dict(id=id,
                         year=year,
                         month=month,
                         day=day,
                         type=type,
                         time=time,
                         distance=distance,
                         gain=gain,
                         timestamp=timestamp
                         )
                )
                print('OK - loaded')
            else:
                pass
                # already in database
        return new_activities


    def get_new_activitiesGPX(self):
        """Get activities metadata from .gpx files downloaded from strava to /gpx directory"""
        print()
        print('--- Loading GPX data... ------------------------------------------------------------------------------')
        activities_ids = self.get_db_act_ids()
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


    def get_activitiesDATA(self):
        """Get all activities from database and return them as dataframe."""
        _df = self.conn.get_activities()
        ts = _df['timestamp'].max()
        self.LATEST_ACTIVITY = ts
        # latest activity timstamp is not used anymore but left for future use
        return _df

    def acts_data_present(self):
        """Check if activities data is present."""
        return self.conn.is_data_present()

    def get_optionsDATA(self):
        """Update available options for dash"""
        df = self.get_activitiesDATA()
        return get_options(df)

    def get_chartDATA(self, metrics, activity, year):
        """Prepare chart to be displayed by dash.
        Returns dash layout"""
        df = self.get_activitiesDATA()
        if year != 'All':
            df = df[df['year'] == int(year)]
        df = df[df['type'].isin(activity)]
        return get_chart(df, metrics, activity, year)


if __name__ == '__main__':
    # for testing
    data = StravaData()
    activities = data.get_new_activitiesGPX()
    print(activities)
    activities = data.get_new_activitiesCSV()
    print(activities)

