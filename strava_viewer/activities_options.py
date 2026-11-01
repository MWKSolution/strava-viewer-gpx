"""Module for preparing lists for dash app based on data."""
from collections import namedtuple

METRIC_TYPES = ['distance', 'time', 'gain']
METRIC_OPTIONS = [
        {'label': 'Distance [km]', 'value': 'distance'},
        {'label': 'Time [h]', 'value': 'time'},
        {'label': 'Elevation gain [m]', 'value': 'gain'}]
# {'label': 'Quantity', 'value': 'quan'}] ... for further development
METRIC_VALUE = 'distance'

Metric = namedtuple('Metric', ['types', 'options', 'value'])
Activity = namedtuple('Activity', ['types', 'options', 'value'])
Year = namedtuple('Year', ['types', 'options', 'value'])


def get_options_for_types(_types):
    """Prepare options list as a parameter for dash dbc.Checklist options.Returns list of dictionaries."""
    _opts = []
    for _t in _types:
        _ts = str(_t)
        _opts.append({'label': _ts.capitalize(), 'value': _ts})
    return _opts


def get_options(_df):
    # metrics
    _metric = Metric(types=METRIC_TYPES, options=METRIC_OPTIONS, value=METRIC_VALUE)
    # activities
    _activity_types = list(_df['type'].unique())
    _activity_options = get_options_for_types(_activity_types)
    _activity = Activity(types=_activity_types, options=_activity_options, value=None)
    # years
    _ALL = ['All']
    _years = _df['year'].unique()
    _ALL.extend(_years)
    _years_options = get_options_for_types(_ALL)
    _year = Year(types=_ALL, options=_years_options, value='All')
    return _metric, _activity, _year


if __name__ == '__main__':
    # for testing
    from strava_data import StravaData
    data = StravaData()
    if data.acts_data_present():
        df = data.get_activitiesDATA()
        print(df.head())
        print(*get_options(df), sep='\n')
    else:
        print(f'No data!')

