from flask import Flask, render_template, url_for, request, redirect, session, flash, send_file
from flask import make_response, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import os
from email.message import EmailMessage
import datetime

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "You need to Login first"

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Updating-Gen-Z.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile = db.Column(db.LargeBinary)
    name = db.Column(db.String(200))
    about = db.Column(db.String(500))
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    mail_id = db.Column(db.String(200), nullable=False, unique=True)
    expertise = db.Column(db.String(200))
    grammer_points = db.Column(db.Integer)
    history_points = db.Column(db.Integer)
    geography_points = db.Column(db.Integer)
    humanresource_points = db.Column(db.Integer)
    law_points = db.Column(db.Integer)
    psychology_points = db.Column(db.Integer)
    economy_points = db.Column(db.Integer)
    agriculture_points = db.Column(db.Integer)
    science_points = db.Column(db.Integer)
    sociology_points = db.Column(db.Integer)
    politics_points = db.Column(db.Integer)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False, unique=True)
    choice1 = db.Column(db.String(200))
    choice2 = db.Column(db.String(200))
    choice3 = db.Column(db.String(200))
    choice4 = db.Column(db.String(200))
    answer = db.Column(db.String(200))


class Blog(db.Model):
    user_id = db.Column(db.Integer)
    post = db.Column(db.String(1500))
    picture = db.Column(db.LargeBinary)
    like = db.Column(db.Integer, default=0)
    topic = db.Column(db.String(200))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# EMAIL_ADDRESS = 'updatinggenz@gmail.com'
# EMAIL_PASSWORD = 'updatinggenzpassword'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method="sha256")
        cpassword = request.form['cpassword']
        mail_id = request.form['mail_id']

        user = Users.query.filter_by(username=username).first()
        if user:
            flash("User Name Already Exists, Choose another one")
            return redirect("/signup")
        user = Users.query.filter_by(mail_id=mail_id).first()
        if user:
            flash("Email Already Registered, Try logging in")
            return redirect("/login")

        if(password == cpassword):
            new_user = Users(username=username, name=name,
                             password=hashed_password, mail_id=mail_id)
            db.session.add(new_user)
            db.session.commit()

            # msg = EmailMessage()
            # msg['Subject'] = 'Sucessfully Registered to Updating Gen-z!'
            # msg['From'] = EMAIL_ADDRESS
            # msg['To'] = mail_id
            # msg.set_content('Thank you for Registering to Updating Gen-z.')

            # f = open("templates/hello.txt", "r")
            # msg.add_alternative(f.read(), subtype='html')

            # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            #     smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            #     smtp.send_message(msg)

            flash("Sucessfully Registered!", "success")
            return redirect('/login')
        else:
            flash("Passwords don't match", "danger")
            return redirect("/signup")

    return render_template("sign-up.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        logout_user()
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter_by(username=username).first()
        print(user)
        if not user:
            flash("No such User found, Try Signing Up First", "warning")
            return redirect("/signup")
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                print("Login Done!")
                return redirect("/")
            else:
                flash("Incorrect password", "danger")
                return redirect("login")
    return render_template("log-in.html")


@app.route('/logout')
def logout():
    logout_user()
    flash("Successfully Logged out!")
    return redirect('/login')


@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)


# @app.route('/search', methods=['POST', 'GET'])
# def search():
#     if request.method == "POST":
#         search_string = request.form['search_string']
#         search = "{0}".format(search_string)
#         search = search+'%'

#         results = Songs.query.filter(
#             or_(Songs.name.like(search), Songs.artist.like(search))).all()
#         if len(results) == 0:
#             flash("No such song availabe!")
#         return render_template('search.html', results=results)
#     return render_template('search.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
