from dash import Input, Output


def get_callbacks(app, data):
    """callbacks definition"""
    @app.callback([Output('loading', 'children'),
                   Output('metrics-input', 'options'),
                   Output('metrics-input', 'value'),
                   Output('activity-input', 'options'),
                   Output('activity-input', 'value'),
                   Output('years-input', 'options'),
                   Output('years-input', 'value')],
                  Input('load-data', 'n_clicks'),
                  prevent_initial_call=True)
    def load_data(n_clicks):
        """Callback when clicking 'Reload all data' button."""
        if n_clicks > 0:
            data.load_dataGPX()
            metrics, activities, year = data.get_optionsDATA()
            return '', metrics.options, metrics.value, activities.options, activities.types, year.options, year.value

    # @app.callback([Output('refresh', 'children'),
    #                Output('metrics-input', 'options'),
    #                Output('metrics-input', 'value'),
    #                Output('activity-input', 'options'),
    #                Output('activity-input', 'value'),
    #                Output('years-input', 'options'),
    #                Output('years-input', 'value')],
    #               Input('refresh-data', 'n_clicks'),
    #               prevent_initial_call=True)
    # def refresh_data(n_clicks):
    #     """Callback when clicking 'Reload all data' button."""
    #     if n_clicks > 0:
    #         data.refresh_dataGPX()
    #         metrics, activities, year = data.get_optionsDATA()
    #         return '', metrics.options, metrics.value, activities.options, activities.types, year.options, year.value

    @app.callback(Output('bar-chart', 'figure'),
                  [Input('metrics-input', 'value'),
                   Input('activity-input', 'value'),
                   Input('years-input', 'value')],
                  prevent_initial_call=True)
    def show_bar_chart(metrics, activity, year):
        """Callback updates barchart when changes to metrics or activities or year are made."""
        barchart = data.get_chartDATA(metrics, activity, year)
        return barchart
