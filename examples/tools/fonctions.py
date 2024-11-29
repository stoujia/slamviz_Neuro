import numpy as np
import plotly.colors as pc
import nibabel as nib
import trimesh
import plotly.graph_objects as go
import json
import os
from matplotlib.colors import to_rgba

def get_colorscale_names(local_directory='./custom_colormap'):
    sequential_names = [name for name in pc.sequential.__dict__.keys() if '__' not in name and 'swatches' not in name and '_r' not in name]
    diverging_names = [name for name in pc.diverging.__dict__.keys() if '__' not in name and 'swatches' not in name and '_r' not in name]
    cyclical_names = [name for name in pc.cyclical.__dict__.keys() if '__' not in name and 'swatches' not in name and '_r' not in name]
    
    local_colormaps = load_local_colormaps(local_directory)
    local_names = list(local_colormaps.keys())
    print(f"Local colormaps détectées : {local_names}")  # Débogage
    predefined_colormaps = np.hstack([sequential_names[0:10], diverging_names[0:10], cyclical_names[0:10], local_names])    
    return predefined_colormaps


# Fonction pour convertir des couleurs RGB en hexadécimal
def convert_rgb_to_hex_if_needed(colormap):
    hex_colormap = []
    for color in colormap:
        if color.startswith('rgb'):
            rgb_values = [int(c) for c in color[4:-1].split(',')]
            hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb_values)
            hex_colormap.append(hex_color)
        else:
            hex_colormap.append(color)
    return hex_colormap


# Création d'une colormap avec des traits noirs
def create_colormap_with_black_stripes(base_colormap, num_intervals=10, black_line_width=0.01):
    temp_c = pc.get_colorscale(base_colormap)
    temp_c_2 = [ii[1] for ii in temp_c]
    old_colormap = convert_rgb_to_hex_if_needed(temp_c_2)
    custom_colormap = []
    base_intervals = np.linspace(0, 1, len(old_colormap))

    for i in range(len(old_colormap) - 1):
        custom_colormap.append([base_intervals[i], old_colormap[i]])
        if i % (len(old_colormap) // num_intervals) == 0:
            black_start = base_intervals[i]
            black_end = min(black_start + black_line_width, 1)
            custom_colormap.append([black_start, 'rgb(0, 0, 0)'])
            custom_colormap.append([black_end, old_colormap[i]])
    custom_colormap.append([1, old_colormap[-1]])
    return custom_colormap

# Charger les colormaps locales depuis un répertoire
def load_local_colormaps(directory):
    local_colormaps = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r") as file:
                try:
                    data = json.load(file)
                    name = os.path.splitext(filename)[0]
                    local_colormaps[name] = data
                    print(f"Chargé : {name} depuis {filepath}")  # Debug
                except json.JSONDecodeError as e:
                    print(f"Erreur JSON dans {filepath} : {e}")
    return local_colormaps


# Conversion d'une colormap locale en format Plotly
def convert_custom_colormap_to_plotly(colors):
    """
    Convertir une colormap personnalisée en colorscale compatible Plotly.
    
    :param colors: Liste de dicts contenant 'min', 'max', et 'color'.
    :return: Liste de [position_normalisée, couleur] pour Plotly.
    """
    if not colors:
        return []

    total_range = colors[-1]["max"] - colors[0]["min"]
    colorscale = []

    for entry in colors:
        # Positions normalisées pour Plotly
        normalized_min = (entry["min"] - colors[0]["min"]) / total_range
        normalized_max = (entry["max"] - colors[0]["min"]) / total_range

        # Ajouter les couleurs aux positions normalisées
        colorscale.append([normalized_min, entry["color"]])
        colorscale.append([normalized_max, entry["color"]])
        
    return colorscale


#def interpolate_color(color1, color2, t):
    """
    Interpole entre deux couleurs en utilisant un ratio t (0 <= t <= 1).
    :param color1: Couleur de départ en format hex ou nom CSS.
    :param color2: Couleur d'arrivée en format hex ou nom CSS.
    :param t: Ratio d'interpolation (0 = color1, 1 = color2).
    :return: Couleur interpolée en format hex.
    """
    rgba1 = to_rgba(color1)  # Convertir la couleur en format RGBA
    rgba2 = to_rgba(color2)
    rgba_interp = [(1 - t) * c1 + t * c2 for c1, c2 in zip(rgba1, rgba2)]
    return f"rgba({int(rgba_interp[0]*255)}, {int(rgba_interp[1]*255)}, {int(rgba_interp[2]*255)}, {rgba_interp[3]})"


#def convert_custom_colormap_to_plotly(colors, steps=50):
    """
    Convertir une colormap personnalisée en colorscale compatible Plotly
    avec des transitions lisses entre les couleurs, en passant par les centres des plages.
    
    :param colors: Liste de dicts contenant 'min', 'max', et 'color'.
    :param steps: Nombre de pas pour interpoler entre chaque transition.
    :return: Liste de [position_normalisée, couleur] pour Plotly.
    """
    if not colors:
        return []

    # Calculer la plage totale
    total_range = colors[-1]["max"] - colors[0]["min"]
    colorscale = []

    for i in range(len(colors) - 1):
        current = colors[i]
        next_entry = colors[i + 1]

        # Calculer les centres des plages
        current_center = (current["min"] + current["max"]) / 2
        next_center = (next_entry["min"] + next_entry["max"]) / 2

        # Positions normalisées pour les centres
        normalized_current_center = (current_center - colors[0]["min"]) / total_range
        normalized_next_center = (next_center - colors[0]["min"]) / total_range

        # Interpoler entre les couleurs depuis le centre courant vers le centre suivant
        for step in range(steps + 1):
            t = step / steps
            interp_position = (
                normalized_current_center + t * (normalized_next_center - normalized_current_center)
            )
            interp_color = interpolate_color(current["color"], next_entry["color"], t)
            colorscale.append([interp_position, interp_color])

    # Ajouter la couleur de la première plage au début et de la dernière à la fin
    first_entry = colors[0]
    last_entry = colors[-1]
    colorscale.insert(0, [0.0, first_entry["color"]])  # Début avec la couleur initiale
    colorscale.append([1.0, last_entry["color"]])     # Fin avec la couleur finale

    return colorscale



# Fonction pour charger un maillage GIFTI
def load_mesh(gifti_file):
    """
    Charge un fichier GIfTI et retourne un objet Trimesh.
    
    :param gifti_file: Chemin vers le fichier GIfTI.
    :return: Objet trimesh.Trimesh contenant les sommets, les faces et les métadonnées.
    :raises ValueError: Si le fichier GIfTI ne contient pas les intentions requises.
    """
    try:
        # Charger le fichier GIfTI
        g = nib.load(gifti_file)
        
        # Extraire les coordonnées des sommets (POINTSET)
        pointset_code = nib.nifti1.intent_codes['NIFTI_INTENT_POINTSET']
        pointset_array = g.get_arrays_from_intent(pointset_code)
        if not pointset_array:
            raise ValueError("Le fichier GIfTI ne contient pas d'intention POINTSET.")
        coords = pointset_array[0].data

        # Extraire les indices des triangles (TRIANGLE)
        triangle_code = nib.nifti1.intent_codes['NIFTI_INTENT_TRIANGLE']
        triangle_array = g.get_arrays_from_intent(triangle_code)
        if not triangle_array:
            raise ValueError("Le fichier GIfTI ne contient pas d'intention TRIANGLE.")
        faces = triangle_array[0].data

        # Extraire les métadonnées
        metadata = dict(g.meta.metadata)  # Convertir en dictionnaire classique
        metadata['filename'] = gifti_file

        # Créer et retourner l'objet Trimesh
        return trimesh.Trimesh(faces=faces, vertices=coords, metadata=metadata, process=False)

    except Exception as e:
        raise RuntimeError(f"Erreur lors du chargement du fichier GIfTI : {e}")


# Fonction pour lire un fichier GIFTI (scalars.gii)
def read_gii_file(file_path):
    try:
        gifti_img = nib.load(file_path)
        scalars = gifti_img.darrays[0].data
        return scalars
    except Exception as e:
        print(f"Erreur lors du chargement de la texture : {e}")
        return None




def plot_mesh_with_colorbar(vertices, faces, scalars=None, color_min=None, color_max=None, camera=None,
                            show_contours=False, colormap='jet', use_black_intervals=False,
                            center_colormap_on_zero=False, local_colormaps=None, apply_to_faces=False):
    """
    Générer un graphique 3D de maillage avec une barre de couleur et options avancées.

    Args:
        vertices (np.ndarray): Tableau (N, 3) des coordonnées des sommets.
        faces (np.ndarray): Tableau (M, 3) des indices des sommets formant les triangles.
        scalars (np.ndarray, optional): Tableau (N,) ou (M,) des valeurs scalaires à mapper.
        color_min (float, optional): Valeur minimale pour l'échelle des couleurs.
        color_max (float, optional): Valeur maximale pour l'échelle des couleurs.
        camera (dict, optional): Paramètres de la caméra 3D.
        show_contours (bool, optional): Afficher ou non les contours des triangles.
        colormap (str, optional): Nom de la colormap à utiliser.
        use_black_intervals (bool, optional): Ajouter des intervalles noirs dans la colormap.
        center_colormap_on_zero (bool, optional): Centrer la colormap autour de zéro.
        local_colormaps (dict, optional): Colormaps personnalisées au format Plotly.
        apply_to_faces (bool, optional): Si True, les scalars sont convertis pour être appliqués aux faces.

    Returns:
        go.Figure: Figure Plotly contenant le maillage 3D.
    """

    def scalars_vertices_to_faces(scalars, faces):
        """Convertit les scalars définis sur les sommets en scalars définis sur les faces."""
        return np.max(scalars[faces], axis=1)

    def compute_colorscale():
        """Retourne une colormap adaptée selon les paramètres."""
        if local_colormaps and colormap in local_colormaps:
            return convert_custom_colormap_to_plotly(local_colormaps[colormap]["data"])
        elif use_black_intervals:
            return create_colormap_with_black_stripes(colormap)
        else:
            return pc.get_colorscale(colormap)

    fig_data = dict(
        x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2],
        i=faces[:, 0], j=faces[:, 1], k=faces[:, 2],
        flatshading=False,
        hoverinfo='text',
        lighting=dict(
            ambient=0.3,
            diffuse=0.7,
            specular=0.1,
            roughness=0.8,
            fresnel=0.5
        ),
        lightposition=dict(x=100, y=200, z=300)
    )

    if scalars is not None:
        # Convertir les scalars pour les faces si demandé
        if apply_to_faces:
            scalars = scalars_vertices_to_faces(scalars, faces)

        # Gestion des plages de couleurs
        color_min = color_min if color_min is not None else np.min(scalars)
        color_max = color_max if color_max is not None else np.max(scalars)

        if center_colormap_on_zero:
            max_abs_value = max(abs(color_min), abs(color_max))
            color_min, color_max = -max_abs_value, max_abs_value

        # Appliquer la colormap
        colorscale = compute_colorscale()

        fig_data.update(
            intensity=scalars,
            intensitymode='cell' if apply_to_faces else 'vertex',
            cmin=color_min,
            cmax=color_max,
            colorscale=colorscale,
            showscale=True,
            colorbar=dict(
                title="Scalars",
                tickformat=".2f",
                thickness=30,
                len=0.9
            ),
            hovertext=[f'Scalar value: {s:.2f}' for s in scalars]
        )
    else:
        fig_data.update(
            color='lightgray',
            opacity=1
        )

    fig = go.Figure(data=[go.Mesh3d(**fig_data)])

    if show_contours:
        fig.data[0].update(contour=dict(show=True, color='black', width=2))

    fig.update_layout(scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        camera=camera,
        aspectmode='data',
    ),
    height=900,
    width=1000,
    margin=dict(l=10, r=10, b=10, t=10))

    return fig





# Créer des ticks clairs pour le slider
def create_slider_marks(color_min_default, color_max_default):
    return {str(i): f'{i:.2f}' for i in np.linspace(color_min_default, color_max_default, 10)}