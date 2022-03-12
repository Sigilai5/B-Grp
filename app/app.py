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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

    def __init__ (self, username, phone_no, email, password, sex):
        self.username = username
        self.phone_no = phone_no
        self.email = email
        self.password = password
        self.sex = sex


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

    def __init__ (self, id, age, weight, allergies,user_id):
        self.id = id
        self.age = age
        self.weight = weight
        self.allergies = allergies
        self.user_id = user_id


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
class userRegistration(FlaskForm):
    username = StringField("username" , validators=[InputRequired()])
    phone_number = IntegerField("phone_number", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired()])
    sex = SelectField("Sex?", choices=[('Male', 'Male'), ('Female', 'Female')])
    password = PasswordField("password", validators=[InputRequired(), EqualTo("confirm_pass", message= "Passwords Don't Match")])
    confirm_pass = PasswordField("confirm_pass")

class userSignin(FlaskForm):
    username = StringField("username" , validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])



class donatebloood(FlaskForm):
    age = IntegerField("age", validators=[InputRequired()])
    weight = IntegerField("weight", validators=[InputRequired()])
    blood_group = StringField("blood_group", validators=[InputRequired()])

class plasmaform(FlaskForm):
    age = IntegerField("age", validators=[InputRequired()])
    weight = IntegerField("weight", validators=[InputRequired()])
    allergies = StringField("allergies", validators=[InputRequired()])


class lungForm(FlaskForm):
    age = IntegerField("age", validators=[InputRequired()])
    weight = IntegerField("weight", validators=[InputRequired()])
    trauma = SelectField("trauma", choices=[('Yes', 'TRUE'), ('no', 'FALSE')])
    smoking = SelectField("Smoking", choices=[('Yes', 'TRUE'), ('no', 'FALSE')])


class kidneyForm(FlaskForm):
    age = IntegerField("age", validators=[InputRequired()])
    weight = IntegerField("weight", validators=[InputRequired()])
    blood_group = StringField("blood_group", validators=[InputRequired()])
    drinking = SelectField("Drinking", choices=[('Yes', 'TRUE'), ('no', 'FALSE')])
    disease_history = StringField("disease_history", validators=[InputRequired()])

######################

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/userRegister/", methods=["GET" , "POST"])
def userReg():
    form = userRegistration()

    if request.method == "POST" and form.validate():
        per = User.query.filter_by(username = form.username.data).first()
        if per:
            flash("Username Already Exist Please Choose Another One")
            return redirect(url_for('userReg'))
        else:
            pass_hash = generate_password_hash(form.password.data, method="sha256")
            new_User = User(username = form.username.data, phone_no = form.phone_number.data, sex =form.sex.data,
                    email = form.email.data, password = pass_hash)
            db.session.add(new_User)
            db.session.commit()

            return redirect(url_for('Signin'))
    return render_template("sigup.html", form =form)



@app.route("/SignIn/", methods=["GET" , "POST"])
def Signin():
    form = userSignin()
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("incorrect credentials")

    return render_template("SignIn.html", form=form)

'''
@app.route("/donate_Blood")
def blood_donation():
    form = donatebloood()
       if request.method == "POST" and form.validate():
        new_Blood = User(username = form.username.data, phone_no = form.phone_number.data, sex =form.sex.data,
                    email = form.email.data, password = pass_hash)            
        db.session.add(new_User)
        db.session.commit()
        return redirect(url_for('Signin'))
        
'''




@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/donations")
def donation():
    return render_template("donations.html")

@app.route("/plasma")
def plasma():
    plasmas = Plasma.query.all()
    users = User.query.all()

    return render_template("plasma.html",plasmas=plasmas,users=users)

@app.route("/blood")
def blood():
    users = User.query.all()
    bloods = Blood.query.all()
    return render_template("blood.html",bloods=bloods,users=users)

@app.route("/kidney")
def kidney():
    users = User.query.all()
    kidneys = Kidney.query.all()
    return render_template("kidney.html",kidneys=kidneys,users=users)

@app.route("/lung")
def lung():
    users = User.query.all()
    lungs = Lung.query.all()
    return render_template("lung.html",lungs=lungs,users=users)

@app.route("/mydonations/")
def mydon():
    user = User.query.get(current_user.id)
    blood = Blood.query.filter_by(user_id = current_user.id).first()
    plasma = Plasma.query.filter_by(user_id = current_user.id).first()
    lung = Lung.query.filter_by(user_id = current_user.id).first()
    kidney = Kidney.query.filter_by(user_id = current_user.id).first()

    return render_template("mydonations.html", user =user, blood =blood, plasma =plasma, lung=lung, kidney=kidney)



@app.route("/logout/")
def Signout():
    logout_user()
    flash('Signed OUT')
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True, port = 5000)