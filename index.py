from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from main.parser import Parser
from main.models import Item

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3300/films"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/", methods=["GET"])
def main():
    items = Item.query.order_by(Item.id).all()
    return render_template("main.html", data=items)


@app.route("/about/<int:id>", methods=["GET"])
def about(id):
    items = Item.query.get(int(id))
    return render_template("about.html", data=items)


@app.route("/add", methods=["POST", "GET"])
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


@app.route("/login", methods=["GET"])
def min():
    items = Item.query.order_by(Item.id).all()
    return render_template("login.html")



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
