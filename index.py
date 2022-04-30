from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from main.parser import Parser


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:admin@localhost:3300/films"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    link = db.Column(db.String(200))
    photo = db.Column(db.String(200))

    def __repr__(self):
        return self.name


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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
