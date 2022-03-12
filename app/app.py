from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, LoginManager, UserMixin, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, IntegerField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, EqualTo, Length
from wtforms.fields import IntegerRangeField
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate



app = Flask(__name__)
app.config['SECRET_KEY'] = "UIoiwehHEF02394HIG83409g8ioa43shd34lk7842"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///donatDB"


###################
##   FARHAZ
####################
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
migrate = Migrate(app, db)
db.init_app(app)
migrate.init_app(app, db)



#THE DATABASE
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text)
    phone_no = db.Column(db.Integer)
    sex = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    blood = db.relationship("Blood", backref="blood", lazy=True)
    plasma = db.relationship("Plasma", backref="plasma", lazy=True)
    lung = db.relationship("Lung", backref="lung", lazy=True)
    kidney = db.relationship("Kidney", backref="kidney", lazy=True)

    def __init__ (self, username, phone_no, email, password):
        self.username = username
        self.phone_no = phone_no
        self.email = email
        self.password = password



class Blood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    blood_group = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable =False)

    def __init__ (self, id, age, weight, blood_group):
        self.id = id
        self.age = age
        self.weight = weight
        self.blood_group = blood_group


class Plasma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    allergies = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable =False)

    def __init__ (self, id, age, weight, allergies):
        self.id = id
        self.age = age
        self.weight = weight
        self.allergies = allergies


class Lung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    trauma =db.Column(db.Boolean)
    smoking = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable =False)

    def __init__ (self, id, age, weight, smoking, trauma):
        self.id = id
        self.age = age
        self.weight = weight
        self.smoking = smoking
        self.trauma = trauma

class Kidney(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    blood_group = db.Column(db.Text)
    drinking = db.Column(db.Boolean)
    disease_history = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable =False)

    def __init__ (self, id, age, weight, blood_group, drinking, disease_history):
        self.id = id
        self.age = age
        self.weight = weight
        self.blood_group = blood_group
        self.drinking = drinking
        self.disease_history = disease_history



########################

#####################

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port = 5000)