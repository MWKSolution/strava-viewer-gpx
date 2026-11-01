from dash import Input, Output


def get_callbacks(app, data):
    """callbacks definition"""
    @app.callback([Output('loading-gpx', 'children'),
                   Output('metrics-input', 'options'),
                   Output('metrics-input', 'value'),
                   Output('activity-input', 'options'),
                   Output('activity-input', 'value'),
                   Output('years-input', 'options'),
                   Output('years-input', 'value')],
                  Input('load-data-gpx', 'n_clicks'),
                  prevent_initial_call=True)
    def load_data_gpx(n_clicks):
        """Callback when clicking 'Reload all data' button."""
        if n_clicks > 0:
            data.load_dataGPX()
            metrics, activities, year = data.get_optionsDATA()
            return '', metrics.options, metrics.value, activities.options, activities.types, year.options, year.value

    @app.callback([Output('loading-csv', 'children'),
                   Output('metrics-input', 'options'),
                   Output('metrics-input', 'value'),
                   Output('activity-input', 'options'),
                   Output('activity-input', 'value'),
                   Output('years-input', 'options'),
                   Output('years-input', 'value')],
                  Input('load-data-csv', 'n_clicks'),
                  prevent_initial_call=True)
    def load_data_csv(n_clicks):
        """Callback when clicking 'Reload all data' button."""
        if n_clicks > 0:
            # TODO # do nothing for now
            # data.refresh_dataGPX()
            metrics, activities, year = data.get_optionsDATA()
            return '', metrics.options, metrics.value, activities.options, activities.types, year.options, year.value

    @app.callback(Output('bar-chart', 'figure'),
                  [Input('metrics-input', 'value'),
                   Input('activity-input', 'value'),
                   Input('years-input', 'value')],
                  prevent_initial_call=True)
    def show_bar_chart(metrics, activity, year):
        """Callback updates barchart when changes to metrics or activities or year are made."""
        barchart = data.get_chartDATA(metrics, activity, year)
        return barchart
