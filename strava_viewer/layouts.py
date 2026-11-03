"""Layouts definition for strava-viewer dash app"""
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from strava_viewer.activities_options import Metric, Activity, Year


def get_chart(df, metrics, activity, year):
    """Get plotly bar chart for given parameters"""
    if year == 'All':
        x = 'year'
    else:
        x = 'month'
    # start from empty Figure
    barchart = go.Figure()
    # stacked activities - one colour for one activity
    for i in activity:
        dfa = df[df['type'] == i]
        barchart.add_trace(go.Bar(
            x=dfa[x],
            y=dfa[metrics],
            customdata=dfa['day'],
            name=i,
            hovertemplate="%{y:.3s} : %{customdata}",
            showlegend=True))
    barchart.update_layout(barmode='stack',
                           plot_bgcolor='rgba(200,200,200,1)',  # Transparent plot area
                           paper_bgcolor='rgba(150,150,150,1)',  # Transparent paper area
                           margin=dict(
                               l=40,  # left   (default 80)
                               r=10,  # right  (default 80)
                               t=40,  # top    (default 100)
                               b=40,  # bottom (default 80)
                               pad=0  # extra padding between axis lines and plot area (default 0)
                           ),
                           xaxis=dict(title=x.capitalize(),
                                      dtick=1),
                           yaxis=dict(title=metrics.capitalize(),
                                      rangemode='tozero'))
    # add total sum for given metrics
    dfs = df.groupby([x], as_index=False).sum()
    barchart.add_trace(
        go.Scatter(
            x=dfs[x],
            y=dfs[metrics],
            text=dfs[metrics],
            mode='text',
            textposition='top center',
            texttemplate='%{text:.3s}',
            showlegend=False,
            hoverinfo='skip',
            textfont=dict(size=16)))
    return barchart


class Layout:

    def __init__(self, data):
        self.data = data
        if self.data.acts_data_present():
            self.metrics, self.activities, self.year = self.data.get_optionsDATA()
            self.barchart = self.data.get_chartDATA(self.metrics.value, self.activities.types, self.year.value)
        else:
            self.barchart = {'data': [], 'layout': {}, 'frames': [], }
            self.metrics = Metric(types=[], options=[], value='')
            self.activities = Activity(types=[], options=[], value='')
            self.year = Year(types=[], options=[], value='')

    def __call__(self):
        """Makes instance callable.
        Returns layout for dash.
        Layout depends on data."""
        return self.app_layout()

    def fig(self):
        _fig = dcc.Graph(figure=self.barchart,
                         config={'displaylogo'           : False,
                                 'displayModeBar'        : True,
                                 'scrollZoom'            : True,
                                 'showAxisDragHandles'   : True,
                                 'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'resetScale2d'],
                                 'toImageButtonOptions'  : {'format': 'jpeg', 'scale': 2}},
                         style={'height': '80vh', 'width': '66vw'},
                         id='bar-chart')
        return _fig

    def interval(self):
        _interval = html.Div([
            dbc.Alert('Choose year', color='info', className='m-2'),
            dbc.RadioItems(
                options=self.year.options,
                value=self.year.value,
                id='years-input',
                className='m-3')])
        return _interval

    def metricsl(self):
        _metrics = html.Div([
            dbc.Alert('Choose metrics', color='info', className='m-2'),
            dbc.RadioItems(
                options=self.metrics.options,
                value=self.metrics.value,
                id='metrics-input',
                className='m-3')])
        return _metrics

    def activityl(self):
        _activity = html.Div([
            dbc.Alert('Choose activity', color='info', className='m-2'),
            dbc.Checklist(
                options=self.activities.options,
                value=self.activities.types,
                id='activity-input',
                className='m-3')])
        return _activity

    load_indicator_gpx = dbc.Spinner(html.Div(id='loading-gpx'),
                                        spinner_style={'width': '5rem', 'height': '5rem'},
                                        fullscreen=False,
                                        color='success')

    load_button_gpx = dbc.Button(
        children=['Load data GPX', load_indicator_gpx],
        n_clicks=0,
        color='success',
        id='load-data-gpx',
        type='submit',
        className='m-4')

    load_indicator_csv = dbc.Spinner(html.Div(id='loading-csv'),
                                         spinner_style={'width': '5rem', 'height': '5rem'},
                                         fullscreen=False,
                                         color='success')

    load_button_csv = dbc.Button(
        children=['Load data CSV', load_indicator_csv],
        n_clicks=0,
        color='success',
        id='load-data-csv',
        type='submit',
        className='m-4')

    def main_layout(self):
        _main = html.Div([
            dbc.Row([
                dbc.Col([self.metricsl(), self.activityl(), self.load_button_gpx, self.load_button_csv],
                        width=2),
                dbc.Col([self.fig()], width=8),
                dbc.Col([self.interval()],
                        width=2)])])
        return _main

    nav_bar = dbc.NavbarSimple(
        brand='Strava Viewer by MWK Solution',
        color='primary',
        dark=True)

    def app_layout(self):
        _appl = html.Div([self.nav_bar,
                          self.main_layout()])
        return _appl
