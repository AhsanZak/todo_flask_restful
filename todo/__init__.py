from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow 
import os
from authlib.integrations.flask_client import OAuth
# Importing Blueprints
from admin.admin import dashboard
from flask_login import LoginManager

# Init app
app = Flask(__name__)
app.secret_key = 'FlaskTodOaPp'

app.register_blueprint(dashboard, url_prefix="/admin")



basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='586195531913-rb7bj2p60tgiba0940p6pi3sqm2ctebu.apps.googleusercontent.com',
    client_secret='j1Sj4ILJ96GwwUgzJ4huIiT2',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)

from todo import routes
from todo import error_handlers