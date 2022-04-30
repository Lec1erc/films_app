from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:admin@localhost:3300/films"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#id film_name, film_description, film_link
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
        name = request.form["name"]
        description = request.form["description"]
        link = request.form["link"]
        item = Item(name=name, description=description, link=link)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect("/")
        except:
            return "False"
    return render_template("add.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
