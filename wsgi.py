from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Pour Render : utilise le port de l'environnement ou 10000 par défaut
    port = int(os.environ.get("PORT", 10000))
    # Debug doit être False en production
    app.run(host="0.0.0.0", port=port, debug=False)