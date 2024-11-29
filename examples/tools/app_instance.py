from dash import Dash
import dash_bootstrap_components as dbc
# Initialise une instance unique de l'application Dash
app = Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "Neuro Mesh"
