from flask import Flask, render_template, redirect, url_for, flash
import forms
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db_path = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = "ThisIsMySecretKey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" +\
                                        os.path.join(db_path, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Migrate(app=app, db=db)


class Pups(db.Model):
    __tablename__ = "pups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    owner = db.relationship("Owner", backref="pups", uselist=False)

    def __init__(self, name):
        self.name = str(name)

    def __repr__(self):
        if self.owner:
            return f"ID: {self.id} - {self.name}. Owner: {self.owner.name}"
        else:
            return f"ID: {self.id} - {self.name}."


class Owner(db.Model):
    __tablename__ = "owners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    puppy_id = db.Column(db.Integer, db.ForeignKey("pups.id"))

    def __init__(self, name, puppy):
        self.name = name
        self.puppy_id = puppy

    def __repr__(self):
        return f"ID: {self.id} - {self.name}"


db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_pup", methods=["POST", "GET"])
def add_pup():
    form = forms.AddPup()
    if form.validate_on_submit():
        pup_name = form.pup_name.data
        puppy = Pups(pup_name)
        db.session.add(puppy)
        db.session.commit()
        flash(f"Puppy {pup_name} added to the list")
        return redirect(url_for("list_pups"))
    return render_template("add_pup.html", form=form)


@app.route("/list_pups", methods=["POST", "GET"])
def list_pups():
    puppies = Pups.query.all()
    return render_template("list_pups.html", puppies=puppies)


@app.route("/del_pup", methods=["POST", "GET"])
def del_pup():
    form = forms.DeletePup()
    if form.validate_on_submit():
        pup_id = form.pup_id.data
        pup_to_delete = Pups.query.get(pup_id)
        db.session.delete(pup_to_delete)
        db.session.commit()
        flash(f"Pup {pup_to_delete.name} succesfully deleted")
        return redirect(url_for("list_pups"))
    return render_template("del_pup.html", form=form)


@app.route("/add_owner", methods=["POST", "GET"])
def add_owner():
    form = forms.AddOwner()
    if form.validate_on_submit():
        owner = Owner(form.owner_name.data, form.pup_id.data)
        pup = Pups.query.filter_by(id=form.pup_id.data).first()
        db.session.add(owner)
        db.session.commit()
        flash(f"Pup {pup.name} has a new owner: {owner.name}")
        return redirect(url_for("list_pups"))
    return render_template("add_owner.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
