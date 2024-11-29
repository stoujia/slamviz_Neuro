from app_instance import app
from app import configure_layout_and_routes

# Configure les layouts et les routes
configure_layout_and_routes(app)

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
