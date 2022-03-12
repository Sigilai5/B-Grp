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



app = Flask(__name__)
app.config['SECRET_KEY'] = "UIoiwehHEF02394HIG83409g8ioa43shd34lk7842"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///donatDB"



@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port = 5000)
