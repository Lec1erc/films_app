from flask import Blueprint, Flask, render_template, redirect, url_for, request, flash

from flask_login import login_required, current_user

from main.parser import Parser
from main.models import Item, User, db


base = Blueprint('base', __name__)


#Main fil is __init__

# app = Flask(__name__)
# # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:admin@host.docker.internal:3300/films"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3300/films"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

@base.route("/", methods=["GET"])

def main():
    items = Item.query.order_by(Item.id).all()

    return render_template("main.html", data=items, name=current_user)


@base.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@base.route("/about/<int:id>", methods=["GET"])
def about(id):
    items = Item.query.get(int(id)) # доставать элемент по имени, а не id, чтоб в адресной строке не id, а name
    return render_template("about.html", data=items, name=current_user)


@base.route("/add", methods=["POST", "GET"])
@login_required
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
    return render_template("add.html", name=current_user)
