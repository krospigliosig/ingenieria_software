from flask import Flask
from Model.extensions import db
from Model.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from .models import Candidato, Elector, eleccion, registro_electoral, administrador_eleccion
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)