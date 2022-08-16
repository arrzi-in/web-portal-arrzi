from flask import Flask, session
from flask_session import Session
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "andh346isname3467356isj356621ohnce9980na"

    app = Flask(__name__)

    # Set the secret key to some random bytes. Keep this really secret!
    app.secret_key = b'627c3675253e20dc12ac5d3e217a1b6fe8c91f559fd335373fba7deaf6f09d41'

    # SESSION
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    bcrypt = Bcrypt(app)

    @app.context_processor
    def inject_user():
        return dict(session_context=session)

    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    return app
