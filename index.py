from flask import Blueprint, Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from flask_login import login_user
from flask_login import login_required, current_user

from main.parser import Parser
from main.models import Item, User, db
import auth

base = Blueprint('base', __name__)
#
# app = Flask(__name__)
# # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:admin@host.docker.internal:3300/films"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3300/films"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


@base.route("/", methods=["GET"])
def main():
    items = Item.query.order_by(Item.id).all()
    return render_template("main.html", data=items)


@base.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@base.route("/about/<int:id>", methods=["GET"])
def about(id):
    items = Item.query.get(int(id))
    return render_template("about.html", data=items)


@base.route("/add", methods=["POST", "GET"])
def add_film():
    if request.method == "POST":
        link = request.form["link"]
        data = Parser(link)
        item = Item(name=data.response()[0],
                    description=data.response()[1],
                    link=link,
                    photo=data.response()[2]
                    )
        try:
            db.session.add(item)
            db.session.commit()
            return redirect("/")
        except:
            return "False"
    return render_template("add.html")

#
# @app.route("/login", methods=["GET"])
# def min():
#     items = Item.query.order_by(Item.id).all()
#     return render_template("login.html")


#
# @app.route('/login', methods=["GET",'POST'])
# def login_post():
#     if request.method =="POST":
#
#         email = request.form.get('email')
#         password = request.form.get('password')
#         remember = True if request.form.get('remember') else False
#
#         user = User.query.filter_by(email=email).first()
#
#         # check if user actually exists
#         # take the user supplied password, hash it, and compare it to the hashed password in database
#         if not user or not check_password_hash(user.password, password):
#             flash('Please check your login details and try again.')
#             return redirect(url_for('/login')) # if user doesn't exist or password is wrong, reload the page
#
#         # if the above check passes, then we know the user has the right credentials
#         login_user(user, remember=remember)
#         return redirect(url_for('/'))
#     else:
#         return render_template('login.html')

#
# if __name__ == "__main__":
#     main.run(host="127.0.0.1", port=8080, debug=True)
