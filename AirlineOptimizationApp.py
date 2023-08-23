import pandas as pd
import dash
from dash import dcc , html
from dash.dependencies import Input, Output

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv("airline_routes.csv")

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the web application
app.layout = html.Div([
    html.H1("Airline Route Optimization"),
    dcc.Dropdown(
        id="origin-dropdown",
        options=[{'label': airport, 'value': airport} for airport in df['origin_airport'].unique()],
        value=df['origin_airport'].iloc[0]
    ),
    dcc.Graph(id="route-graph")
])

# Callback to update the graph based on the selected origin airport
@app.callback(
    Output("route-graph", "figure"),
    [Input("origin-dropdown", "value")]
)
def update_graph(selected_origin):
    filtered_df = df[df['origin_airport'] == selected_origin]
    figure = {
        'data': [
            {'x': filtered_df['destination_airport'], 'y': filtered_df['ticket_price'], 'type': 'bar', 'name': 'Ticket Price'},
            {'x': filtered_df['destination_airport'], 'y': filtered_df['demand'], 'type': 'line', 'name': 'Demand'},
            {'x': filtered_df['destination_airport'], 'y': filtered_df['fuel_cost'], 'type': 'line', 'name': 'Fuel Cost'}
        ],
        'layout': {
            'title': f"Flight Routes from {selected_origin}",
            'xaxis': {'title': 'Destination Airport'},
            'yaxis': {'title': 'Value'},
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
