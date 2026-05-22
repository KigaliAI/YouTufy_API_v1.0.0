import pandas as pd
import dash
from dash import dcc, html, dash_table
import plotly.express as px

CSV_PATH = "all_youtube_channels.csv"

df = pd.read_csv(CSV_PATH)

# Convert numeric fields
for col in ["subscriber_count", "video_count", "view_count"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["latest_video_date"] = pd.to_datetime(df["latest_video_date"], errors="coerce")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("YouTube Channels Dashboard", style={"textAlign": "center"}),

    # Filters
    html.Div([
        html.Label("Filter by Country"),
        dcc.Dropdown(
            id="country_filter",
            options=[{"label": c, "value": c} for c in sorted(df["country"].dropna().unique())],
            multi=True
        ),

        html.Label("Filter by User Email"),
        dcc.Dropdown(
            id="user_filter",
            options=[{"label": u, "value": u} for u in sorted(df["user_email"].unique())],
            multi=True
        ),
    ], style={"width": "40%", "margin": "auto"}),

    html.Br(),

    # Graphs
    dcc.Graph(id="top_subscribers"),
    dcc.Graph(id="top_views"),
    dcc.Graph(id="country_distribution"),

    html.H2("All Channels Table"),
    dash_table.DataTable(
        id="channels_table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        page_size=20,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
    )
])

@app.callback(
    [
        dash.dependencies.Output("top_subscribers", "figure"),
        dash.dependencies.Output("top_views", "figure"),
        dash.dependencies.Output("country_distribution", "figure"),
        dash.dependencies.Output("channels_table", "data"),
    ],
    [
        dash.dependencies.Input("country_filter", "value"),
        dash.dependencies.Input("user_filter", "value"),
    ]
)
def update_dashboard(selected_countries, selected_users):
    filtered = df.copy()

    if selected_countries:
        filtered = filtered[filtered["country"].isin(selected_countries)]

    if selected_users:
        filtered = filtered[filtered["user_email"].isin(selected_users)]

    # Top subscribers
    fig_subs = px.bar(
        filtered.nlargest(20, "subscriber_count"),
        x="title",
        y="subscriber_count",
        title="Top 20 Channels by Subscribers"
    )

    # Top views
    fig_views = px.bar(
        filtered.nlargest(20, "view_count"),
        x="title",
        y="view_count",
        title="Top 20 Channels by Views"
    )

    # Country distribution
    fig_country = px.histogram(
        filtered,
        x="country",
        title="Channel Distribution by Country"
    )

    return fig_subs, fig_views, fig_country, filtered.to_dict("records")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)

