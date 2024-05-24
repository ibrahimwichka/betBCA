from flask import Flask, render_template
import flask_material
from config import Config
from db.models import db, User, Bet, Topic

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)
    
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)