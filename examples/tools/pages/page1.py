from dash import html, dcc
import dash_uploader as du
import fonctions as fct
import numpy as np

# Chemins par défaut
DEFAULT_MESH_PATH = './data/mesh.gii'
colorscale_names = fct.get_colorscale_names('./custom_colormap')

# Charger les données par défaut
mesh = fct.load_mesh(DEFAULT_MESH_PATH)
vertices = mesh.vertices
faces = mesh.faces

# Définir les plages par défaut
default_min, default_max = 0, 1
default_marks = {i: f"{i:.2f}" for i in np.linspace(default_min, default_max, 5)}

# Layout pour la page 1
layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "backgroundColor": "#ffffff",
        "padding": "20px",
        "height": "calc(100vh - 60px)",
        "boxSizing": "border-box",
    },
    children=[
        # Contenu principal
        html.Div(
            style={
                "display": "flex",
                "flexGrow": 1,
                "width": "100%",
                "gap": "20px",
            },
            children=[
                # Panneau gauche : Options
                html.Div(
                    style={
                        "flex": "1",
                        "backgroundColor": "#f9f9f9",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "20px",
                    },
                    children=[
                        html.Label("Importer un nouveau maillage :", style={"fontWeight": "bold", "fontSize": "16px"}),
                        du.Upload(id='upload-mesh', text="Importer un maillage", default_style={"padding": "10px"}),

                        html.Label("Importer une texture :", style={"fontWeight": "bold", "fontSize": "16px"}),
                        du.Upload(id='upload-texture', text="Importer une texture", default_style={"padding": "10px"}),

                        html.Label("Sélectionner une colormap", style={"fontWeight": "bold", "fontSize": "16px"}),
                        dcc.Dropdown( id='colormap-dropdown', options=[{'label': cmap, 'value': cmap} for cmap in colorscale_names],
                                     value='Viridis',clearable=False),    
                        html.Label("Appliquer valeur max sommet aux faces", style={"fontWeight": "bold", "fontSize": "16px"}),
                        dcc.Checklist(id='toggle-triangle', options=[{'label': 'Oui', 'value': 'on'}], value=[]),
                        html.Label("Afficher les isolignes", style={"fontWeight": "bold", "fontSize": "16px"}),
                        dcc.Checklist(id='toggle-contours', options=[{'label': 'Oui', 'value': 'on'}], value=[]),
                        html.Label("Activer traits noirs", style={"fontWeight": "bold", "fontSize": "16px"}),
                        dcc.Checklist(id='toggle-black-intervals', options=[{'label': 'Oui', 'value': 'on'}], value=[]),
                        html.Label("Centrer la colormap sur 0", style={"fontWeight": "bold", "fontSize": "16px"}),
                        dcc.Checklist(id='toggle-center-colormap', options=[{'label': 'Oui', 'value': 'on'}], value=[]),
                    ],
                ),
                # Zone centrale : Visualisation
                html.Div(
                    style={
                        "flex": "2",
                        "backgroundColor": "#ffffff",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                        "display": "flex",
                        "justifyContent": "center",
                        "alignItems": "center",
                    },
                    children=[
                        dcc.Graph(id='3d-mesh', style={"width": "100%", "height": "100%"}),
                    ],
                ),
                # Panneau droit : Slider
                html.Div(
                    style={
                        "flex": "1",
                        "backgroundColor": "#f9f9f9",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "alignItems": "center",
                    },
                    children=[
                        html.Label("Ajuster la plage de valeurs", style={"fontWeight": "bold", "fontSize": "16px"}),
                        dcc.RangeSlider(
                            id='range-slider',
                            min=default_min,
                            max=default_max,
                            step=0.01,
                            value=[default_min, default_max],
                            marks=default_marks,
                            vertical=True,
                            verticalHeight=500,
                            tooltip={"placement": "right", "always_visible": True},
                        ),
                        html.Div(id='upload-status', style={"color": "green", "marginTop": "10px"}),
                    ],
                ),
            ],
        ),
    ],
)