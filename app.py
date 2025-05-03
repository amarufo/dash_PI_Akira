# app.py
import dash
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import registrar_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Monitoreo Educativo"
app.layout = layout

# Registramos aquí todos los callbacks
registrar_callbacks(app)

server = app.server

if __name__ == "__main__":
    app.run(debug=True)
