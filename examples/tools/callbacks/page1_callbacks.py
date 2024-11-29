from dash.dependencies import Input, Output, State
import dash_uploader as du
import fonctions as fct
import numpy as np
import os
from dash import callback_context


# Charger les colormaps locales
local_colormaps = fct.load_local_colormaps('./custom_colormap')

UPLOAD_DIRECTORY = "./uploaded_files/"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def register_callbacks(app):
    global current_mesh, current_vertices, current_faces, current_scalars, default_min, default_max
    current_mesh = fct.load_mesh('./data/mesh.gii')
    current_vertices, current_faces = current_mesh.vertices, current_mesh.faces
    current_scalars = None  # Pas de texture par défaut
    default_min, default_max = 0, 1

    du.configure_upload(app, UPLOAD_DIRECTORY, use_upload_id=False)

    @app.callback(
        [
            Output('3d-mesh', 'figure'),
            Output('upload-status', 'children'),
            Output('range-slider', 'min'),
            Output('range-slider', 'max'),
            Output('range-slider', 'value'),
            Output('range-slider', 'marks'),
        ],
        [
            Input('upload-mesh', 'isCompleted'),
            Input('upload-texture', 'isCompleted'),
            Input('range-slider', 'value'),
            Input('toggle-triangle', 'value'),
            Input('toggle-contours', 'value'),
            Input('toggle-black-intervals', 'value'),
            Input('colormap-dropdown', 'value'),
            Input('toggle-center-colormap', 'value'),
        ],
        [
            State('upload-mesh', 'fileNames'),
            State('upload-texture', 'fileNames'),
        ],
    )
    def update_figure(
        mesh_uploaded, texture_uploaded, value_range, toggle_triangle, toggle_contours,
        toggle_black_intervals, selected_colormap, center_colormap,
        mesh_files, texture_files
    ):
        global current_mesh, current_vertices, current_faces, current_scalars, default_min, default_max

        triggered = callback_context.triggered
        feedback = None

        # Handle new mesh upload
        if any("upload-mesh" in t["prop_id"] for t in triggered):
            if mesh_uploaded and mesh_files:
                uploaded_file = os.path.join(UPLOAD_DIRECTORY, mesh_files[0])
                current_mesh = fct.load_mesh(uploaded_file)
                current_vertices, current_faces = current_mesh.vertices, current_mesh.faces
                current_scalars = None  # Reset texture
                default_min, default_max = 0, 1  # Reset slider range
                feedback = f"Maillage {mesh_files[0]} chargé avec succès."
                return (
                    fct.plot_mesh_with_colorbar(current_vertices, current_faces, None),
                    feedback,
                    default_min,
                    default_max,
                    [default_min, default_max],
                    {i: f"{i:.2f}" for i in np.linspace(default_min, default_max, 5)},
                )

        # Handle new texture upload
        if any("upload-texture" in t["prop_id"] for t in triggered):
            if texture_uploaded and texture_files:
                uploaded_file = os.path.join(UPLOAD_DIRECTORY, texture_files[0])
                current_scalars = fct.read_gii_file(uploaded_file)
                feedback = f"Texture {texture_files[0]} chargée avec succès."

                # Update slider and colorbar range based on new texture
                default_min, default_max = np.min(current_scalars), np.max(current_scalars)
                slider_marks = {i: f"{i:.2f}" for i in np.linspace(default_min, default_max, 5)}
                return (
                    fct.plot_mesh_with_colorbar(
                        current_vertices,
                        current_faces,
                        current_scalars,
                        color_min=default_min,
                        color_max=default_max,
                        colormap=selected_colormap,
                        local_colormaps=local_colormaps,  # Passer les colormaps locales ici
                        show_contours='on' in toggle_contours,
                        center_colormap_on_zero='on' in center_colormap,
                        use_black_intervals='on' in toggle_black_intervals,
                    ),
                    feedback,
                    default_min,
                    default_max,
                    [default_min, default_max],
                    slider_marks,
                )

        # Generate figure with current data
        feedback = None
        if selected_colormap in local_colormaps:
            feedback = f"Application de la colormap personnalisée : {selected_colormap}"
        else:
            feedback = f"Application de la colormap : {selected_colormap}"

        fig = fct.plot_mesh_with_colorbar(
            current_vertices,
            current_faces,
            current_scalars,
            color_min=value_range[0],
            color_max=value_range[1],
            colormap=selected_colormap,
            local_colormaps=local_colormaps,  # Passer les colormaps locales ici
            show_contours='on' in toggle_contours,
            center_colormap_on_zero='on' in center_colormap,
            use_black_intervals='on' in toggle_black_intervals,
            apply_to_faces='on' in toggle_triangle
        )
        return (
            fig,
            feedback,
            default_min,
            default_max,
            value_range,
            {i: f"{i:.2f}" for i in np.linspace(default_min, default_max, 5)},
        )
