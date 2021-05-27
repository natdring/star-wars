from prepData import prepData, prepNetwork
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import networkx as nx
import plotly.graph_objects as go

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
                html.Div(
                    children=dcc.Graph(
                        id="network", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

def dashNetwork(episode):
    G = prepNetwork()[episode]
    # G = nx.random_geometric_graph(200, 0.125)

    pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    return edge_trace, node_trace

@app.callback(
    [Output("mentions-chart", "figure"), Output("network", "figure")],
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

    network_data = dashNetwork(episode)
    network_figure = go.Figure(
            data=[network_data[0], network_data[1]],
            layout=go.Layout(
            title='<br>Episode ' + str(episode) + ' Social Network',
            titlefont_size=16,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="FOO BAR",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002 ) ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
        )
    return mentions_chart_figure, network_figure


if __name__ == "__main__":
    app.run_server(debug=True)