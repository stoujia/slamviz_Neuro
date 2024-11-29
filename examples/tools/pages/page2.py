from dash import html, dcc

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
        html.Div(
            style={
                "display": "flex",
                "flexGrow": 1,
                "width": "100%",
                "gap": "20px",
            },
            children=[
                html.Div(
                    style={
                        "flex": "1",
                        "backgroundColor": "#f9f9f9",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "20px",
                    },
                    children=[
                        html.Label("Set Colormap Bounds", style={"fontWeight": "bold", "fontSize": "16px"}),
                        dcc.Input(
                            id="mincolormap",
                            type="number",
                            placeholder="Min value",
                            value=0,
                            style={"width": "100%"},
                        ),
                        dcc.Input(
                            id="maxcolormap",
                            type="number",
                            placeholder="Max value",
                            value=100,
                            style={"width": "100%"},
                        ),
                        html.Button(
                            "Apply Bounds",
                            id="apply-bounds-btn",
                            n_clicks=0,
                            style={
                                "marginTop": "15px",
                                "backgroundColor": "#3e4c6d",
                                "color": "white",
                            },
                        ),
                        html.Label("Background Color", style={"fontWeight": "bold", "fontSize": "16px"}),
                        dcc.Dropdown(
                            id="background-color-dropdown",
                            options=[
                                {"label": "White", "value": "white"},
                                {"label": "Black", "value": "black"},
                                {"label": "Gray", "value": "gray"},
                                {"label": "Light Blue", "value": "lightblue"},
                                {"label": "Light Green", "value": "lightgreen"},
                            ],
                            value="white",
                            style={"marginTop": "10px"},
                        ),
                        html.Label("Add Color", style={"fontWeight": "bold", "fontSize": "16px"}),
                        dcc.Dropdown(
                            id="color-dropdown",
                            options=[
                                {"label": c.title(), "value": c}
                                for c in ["red", "blue", "green", "orange", "purple", "yellow", "cyan", "magenta", "gray", "brown"]
                            ],
                            placeholder="Select a color",
                            style={"marginTop": "10px"},
                        ),
                        dcc.Input(
                            id="min-range",
                            type="number",
                            placeholder="Min range",
                            style={"width": "100%", "marginTop": "10px"},
                        ),
                        dcc.Input(
                            id="max-range",
                            type="number",
                            placeholder="Max range",
                            style={"width": "100%", "marginTop": "10px"},
                        ),
                        html.Button(
                            "Add Color",
                            id="add-color-btn",
                            n_clicks=0,
                            style={
                                "marginTop": "15px",
                                "backgroundColor": "#3e4c6d",
                                "color": "white",
                            },
                        ),
                        html.Button(
                            "Save Colormap",
                            id="save-colormap-btn",
                            n_clicks=0,
                            style={
                                "marginTop": "15px",
                                "backgroundColor": "#3e4c6d",
                                "color": "white",
                            },
                        ),
                        html.Button(
                            "Reset Colormap",
                            id="reset-colormap-btn",
                            n_clicks=0,
                            style={
                                "marginTop": "15px",
                                "backgroundColor": "#d9534f",
                                "color": "white",
                            },
                        ),
                        html.Div(id="save-status", style={"marginTop": "10px", "color": "green"}),
                    ],
                ),
                html.Div(
                    style={
                        "flex": "2",
                        "backgroundColor": "#ffffff",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                    },
                    children=[
                        html.Label(
                            "Colormap Visualization",
                            style={"fontWeight": "bold", "fontSize": "16px"},
                        ),
                        dcc.Graph(id="colormap-visual"),
                        html.Div(id="color-info", style={"marginTop": "20px"}),
                        dcc.Dropdown(
                            id="colormap-dropdown2",
                            options=[],
                            placeholder="Select a colormap to load",
                            style={"marginTop": "15px"},
                        ),
                    ],
                ),
            ],
        ),
    ],
)