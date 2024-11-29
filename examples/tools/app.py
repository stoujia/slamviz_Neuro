from dash import html, dcc
from dash.dependencies import Input, Output
from pages import page1, page2
from callbacks.page1_callbacks import register_callbacks as register_page1_callbacks
from callbacks.page2_callbacks import register_callbacks as register_page2_callbacks

def configure_layout_and_routes(app):
    # Layout principal avec un menu de navigation
    app.layout = html.Div(
        style={
            "fontFamily": "Arial, sans-serif",
            "backgroundColor": "#f4f4f4",
            "padding": "0",
            "margin": "0",
            "height": "100vh",
            "display": "flex",
            "flexDirection": "column",
        },
        children=[
            # En-tête avec nav bar et logo
            html.Div(
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "backgroundColor": "#3e4c6d",
                    "padding": "10px 20px",
                    "color": "white",
                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                },
                children=[
                    # Logo et titre
                    html.Div(
                        style={"display": "flex", "alignItems": "center", "gap": "10px"},
                        children=[
                            html.Img(
                                src="/assets/logo.svg",  # Utilisation du SVG
                                style={
                                    "width": "40px",
                                    "height": "40px",
                                    "borderRadius": "50%",  # Effet circulaire optionnel
                                },
                            ),
                            html.H1(
                                "Mesh Visualization for Neuroscience",
                                style={"margin": "0", "fontSize": "20px", "fontWeight": "bold"},
                            ),
                        ],
                    ),
                    # Navigation
                    html.Div(
                        style={
                            "display": "flex",
                            "justifyContent": "center",
                            "gap": "30px",
                        },
                        children=[
                            dcc.Link('3D Mesh Visualizer', href='/', className='nav-link'),
                            dcc.Link('Colormap Builder', href='/page2', className='nav-link'),
                        ],
                    ),
                ],
            ),
            # Conteneur pour les pages
            dcc.Location(id='url', refresh=False),
            html.Div(
                id='page-content',
                style={
                    "flex": "1",  # Remplit tout l'espace disponible
                    "padding": "20px",
                },
            ),
        ]
    )

    # Callback pour changer de page
    @app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
    def display_page(pathname):
        if pathname == '/page2':
            return page2.layout
        else:  # Page par défaut
            return page1.layout

    # Enregistrement des callbacks
    register_page1_callbacks(app)
    register_page2_callbacks(app)
