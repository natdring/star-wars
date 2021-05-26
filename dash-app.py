from prepData import prepData
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

node_df, link_df, mentions_df = prepData()



external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Star Wars Analytics"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🪐", className="header-emoji"),
                html.H1(
                    children="Star Wars Analytics", className="header-title"
                ),
                html.P(
                    children="Visualize the interactive relationships"
                    " between characters from a long time ago"
                    " in a galaxy far away",
                    className="header-description"
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Episode", className="menu-title"),
                        dcc.Dropdown(
                            id="episode-select",
                            options=[
                                {"label": episode, "value": episode}
                                for episode in range(1,8)
                            ],
                            value=3,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                # html.Div(
                #     children=[
                #         html.Div(children="Type", className="menu-title"),
                #         dcc.Dropdown(
                #             id="type-filter",
                #             options=[
                #                 {"label": avocado_type, "value": avocado_type}
                #                 for avocado_type in data.type.unique()
                #             ],
                #             value="organic",
                #             clearable=False,
                #             searchable=False,
                #             className="dropdown",
                #         ),
                #     ],
                # ),
                # html.Div(
                #     children=[
                #         html.Div(
                #             children="Date Range",
                #             className="menu-title"
                #             ),
                #         dcc.DatePickerRange(
                #             id="date-range",
                #             min_date_allowed=data.Date.min().date(),
                #             max_date_allowed=data.Date.max().date(),
                #             start_date=data.Date.min().date(),
                #             end_date=data.Date.max().date(),
                #         ),
                #     ]
                # ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="mentions-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                # html.Div(
                #     children=dcc.Graph(
                #         id="volume-chart", config={"displayModeBar": False},
                #     ),
                #     className="card",
                # ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [Output("mentions-chart", "figure")],
    [
        Input("episode-select", "value"),
        # Input("type-filter", "value"),
        # Input("date-range", "start_date"),
        # Input("date-range", "end_date"),
    ],
)
def update_charts(episode):
    mask = (
        (mentions_df['episode']==episode)
    )
    filtered_data = mentions_df.loc[mask, :]
    mentions_chart_figure = {
        "data": [
            {
                "x": filtered_data["name"],
                "y": filtered_data["value"],
                "type": "bar",
            },
        ],
        "layout": {
            "title": {
                "text": "Number of Times Character was Mentioned in Episode " + str(episode),
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True, "tickangle" : -45},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    # volume_chart_figure = {
    #     "data": [
    #         {
    #             "x": filtered_data["Date"],
    #             "y": filtered_data["Total Volume"],
    #             "type": "lines",
    #         },
    #     ],
    #     "layout": {
    #         "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
    #         "xaxis": {"fixedrange": True},
    #         "yaxis": {"fixedrange": True},
    #         "colorway": ["#E12D39"],
    #     },
    # }
    return mentions_chart_figure,


if __name__ == "__main__":
    app.run_server(debug=True)