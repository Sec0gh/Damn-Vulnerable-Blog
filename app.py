from flask import Flask
import os
from database import init_db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

init_db()

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.posts import post_bp
from routes.users import user_bp
from routes.misc import misc_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(post_bp)
app.register_blueprint(user_bp)
app.register_blueprint(misc_bp)

if __name__ == '__main__':
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=True)
