from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
#db = SQLAlchemy()



app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost:3300/films"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(app.config)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from main.models import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# blueprint for auth routes in our app
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)#, url_prefix='/auth'

# blueprint for non-auth parts of app
from index import base as base_blueprint
app.register_blueprint(base_blueprint)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

