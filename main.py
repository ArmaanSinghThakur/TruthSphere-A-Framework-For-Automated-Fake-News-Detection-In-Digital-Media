import time

import PIL.ImageShow
import re
import filestorage
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from flask_bootstrap import Bootstrap5
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_uploads import UploadSet, IMAGES, configure_uploads
from imageToText import *
import nltk
import requests
import newspaper
from subprocess import call
from newspaper import Article
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
import os
from sqlalchemy.sql import text
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from VideoToText import *
from truthspear import *





def open_py_file():
    call(["python", "truthspear.py"])



"""open_py_file()"""





#The Basics of downloading the article to memory
def article_extractor(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    txt= article.text
    return txt
URL= "https://newsapi.org/v2/top-headlines?country=us&apiKey=1a2c09b6e88144a98c18a8202d755b45"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
Bootstrap5(app)



login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
# Configure Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
media= UploadSet('media', ('mp4'))


app.config['UPLOAD_FOLDER']= 'static/files'

class UploadFileForm(FlaskForm):
    file= FileField("File")
    submit= SubmitField("Upload File")

class input_field(FlaskForm):
    req= StringField("",validators=[DataRequired()])
    submit1= SubmitField("check")
class text_field(FlaskForm):
    req= StringField("",validators=[DataRequired()])
    submit2= SubmitField("check")
# Create a user_loader callback

@app.route('/register', methods= ["POST", "GET"])
def register():
    form= RegisterForm()
    if form.validate_on_submit():
        email= request.form.get("email")
        name= request.form.get("name")
        password= request.form.get("password")
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            flash("You've already been signed up with that email, please login.")

            return redirect(url_for("login"))
        hash_salted_password= generate_password_hash(password=password, salt_length=8, method='pbkdf2:sha256' )

        new_user= User(
            email=email,
            name=name,
            password=hash_salted_password
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)


        return redirect(url_for("home"))
    return render_template("register.html", form=form)

@app.route('/login1', methods= ["POST", "GET"])
def login1():
    form = LoginForm()
    form1 = RegisterForm()
    if form.validate() and form.submit():
        email = request.form.get("email")
        password = request.form.get("password")

        response = db.session.execute(db.select(User).where(User.email == email))
        user = response.scalar()

        if check_password_hash(user.password, password):
            login_user(user)

    if form1.validate() and form1.submit1():
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        confirm= request.form.get("confirm_password")
        if confirm== password:
            result = db.session.execute(db.select(User).where(User.email == form.email.data))
            user = result.scalar()
            print(result)
        elif user:
            flash("You've already been signed up with that email, please login.")

            return redirect(url_for("login"))
        hash_salted_password = generate_password_hash(password=password, salt_length=8, method='pbkdf2:sha256')

        new_user = User(
            email=email,
            name=name,
            password=hash_salted_password
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)


        return render_template("login.html", form=form, form1=form1)

    return render_template("login1.html", form=form, form1=form1)



@app.route('/login', methods= ["POST", "GET"])
def login():
        email= request.form.get("signup-email")
        password= request.form.get("signup-password")
        password_confirm = request.form.get("signup-password-confirm")
        if password_confirm== password:

            print(email, password)
        else :
            print("password didnt matched")


        return render_template("login.html", )


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)



# CREATE TABLE IN DB with the UserMixin
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

class NEWS( db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    Source: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))
    Title: Mapped[str] = mapped_column(String(1000))
    News: Mapped[str] = mapped_column(String(10000))
    Image: Mapped[str]= mapped_column(String(1000))
    Url: Mapped[str]= mapped_column(String(1000))

with app.app_context():
    db.session.execute(text("DROP TABLE IF EXISTS NEWS;"))
    db.create_all()

    # or book_to_delete = db.get_or_404(Book, book_id)

spl= "T"

app.config["UPLOADED_PHOTOS"]= "static/files"


@app.route("/get_file")
def get_file(photo):
    return send_from_directory(app.config["UPLOADED_PHOTOS"], photo)

def news_finder():
    r= requests.get(URL)
    data = r.json()
    for i in range(0, 15):
        main = data["articles"][i]
        source = main["source"]["name"]
        author = main["author"]
        title = main["title"]
        news = main["content"]
        image= main["urlToImage"]
        url= main["url"]
        date = main["publishedAt"].partition(spl)[0]
        if news== None:
            news= "UNKOWN"
        if author== None:
            author= "UNKOWN"
        if image== None:
            image= "IMG Not found"
        if url== None:
            url= "Url noy found"
        if source== "[Removed]":
            pass
        else:
            News= NEWS(
                Source= source,
                author= author,
                Title= title,
                News= news,
                Image= image,
                Url= url
            )
            db.session.add(News)
            db.session.commit()

with app.app_context():
        db.session.execute(text("DROP TABLE IF EXISTS NEWS;"))
        db.create_all()
        news_finder()


@app.route("/",methods=["POST","GET"])
def home():
    form= input_field()
    form_1= text_field()
    result=""
    if form.submit1.data and form.validate():
        nltk.download('punkt_tab')
        file= request.form.get("req")
        article = article_extractor(file)
        result= manual_testing(article)
        print(result)
        return render_template("index2.html", form=form, form_1=form_1, result=result)
    elif form_1.submit2.data and form_1.validate():
        file = request.form.get("req")
        result = manual_testing(file)
        print(result)
        return render_template("index2.html", form=form, form_1=form_1, result=result)

    return render_template("index2.html", form=form, form_1=form_1, result=result)

@app.route("/check",methods=["POST","GET"] )
def check():
    form = input_field()
    text= request.args.get("videoFile")
    print(text)
    return render_template("index2.html", form= form)

@app.route("/news")
def news():
    with app.app_context():
        db.session.execute(text("DROP TABLE IF EXISTS NEWS;"))
        db.create_all()
        news_finder()
    result = db.session.execute(db.select(NEWS))
    all_news = result.scalars().all()
    for i in range(len(all_news)):
        all_news[i].ranking = len(all_news) - i
    db.session.commit()
    return render_template("news.html", all_news=all_news)

@app.route("/detect_video", methods= ["POST"])
def detect_video():
    result = ""
    form = UploadFileForm()
    if form.validate_on_submit():
        file = request.files["file"]
        filename= secure_filename(file.filename)
        media.save(file, name= filename)

        print(filename)

        return render_template("videos.html", result=result, form=form)
    return render_template("videos.html", result=result, form=form)

store= filestorage

@app.route("/detect_photo", methods=["POST","GET"])
def detect_photo():
    result=""
    form= UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        fs = "FileStorage: "

        file_name = re.sub(fs, "", str(file))
        file_name = re.sub("['/\\']", "", file_name)
        file_name = re.sub("[()]", "", file_name)
        file_name = re.sub("imagejpeg", "", file_name)
        file_name = re.sub("png", "", file_name)
        file_name = re.sub("jpg", "", file_name)
        file_name = re.sub("img", "", file_name)
        file_name = re.sub("[<>]", "", file_name)
        print(file_name)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                               secure_filename(file.filename)))

        photo_url = f"static/files/{file_name}"
        text_main = Image_to_Text.ImgReader(photo_url)
        result = manual_testing(text_main)
        if result == "Fake News":
            result = """The News Was Fake.
                BE AWARE OF FAKE NEWS!
                Try to avoid fake news spreading all over the world and try not to spread fake news.b
                If your news was tech news and it reported to be fake it is because not every tech news is real and if it is real it might be unsure."""

        elif result == "Real News":
            result = """The News Is Real.
                        BE AWARE OF FAKE NEWS!
                        Try to avoid fake news spreading all over the world and try not to spread fake news.
                        To read more news visit our news page. It provides you with today's headlines."""


@app.route("/video_detection",methods=["POST","GET"])
def video_detection():
    result = ""
    form = UploadFileForm()
    if form.validate_on_submit():
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save("static/files/"+filename)
        text= VidToImg(f"static/files/{filename}")
        result= manual_testing(text)

        if result == "Fake News":
            result = """The News Was Fake.
                BE AWARE OF FAKE NEWS!
                Try to avoid fake news spreading all over the world and try not to spread fake news.b
                If your news was tech news and it reported to be fake it is because not every tech news is real and if it is real it might be unsure."""

        elif result == "Real News":
            result = """The News Is Real.
                        BE AWARE OF FAKE NEWS!
                        Try to avoid fake news spreading all over the world and try not to spread fake news.
                        To read more news visit our news page. It provides you with today's headlines."""

        return render_template("videos.html", result=result, form=form)
    return render_template("videos.html", result=result, form=form)



@app.route("/photo_detection",methods=["POST","GET"])
def photo_detection():
    result=""
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        fs= "FileStorage: "

        file_name = re.sub(fs,"", str(file))
        file_name= re.sub("['/\\']", "", file_name)
        file_name= re.sub("[()]", "", file_name)
        file_name = re.sub("[()]", "", file_name)
        file_name = re.sub("imagejpeg", "", file_name)
        file_name = re.sub("image", "", file_name)
        file_name = re.sub("png", "", file_name)
        file_name = re.sub("jpg", "", file_name)
        file_name = re.sub("img", "", file_name)
        file_name = re.sub("[<>]", "", file_name)
        file_name= re.sub("[.]", "", file_name)
        print(file_name)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                       secure_filename(file.filename)))

        photo_url = f"static/files/{file_name}"
        text_main= Image_to_Text.ImgReader(photo_url)
        result = manual_testing(text_main)
        if result== "Fake News":
            result= """The News Was Fake.
                BE AWARE OF FAKE NEWS!
                Try to avoid fake news spreading all over the world and try not to spread fake news.b
                If your news was tech news and it reported to be fake it is because not every tech news is real and if it is real it might be unsure."""

        elif result== "Real News":
            result= """The News Is Real.
                        BE AWARE OF FAKE NEWS!
                        Try to avoid fake news spreading all over the world and try not to spread fake news.
                        To read more news visit our news page. It provides you with today's headlines."""
        return render_template("photos.html", result= result, form=form)
    return render_template("photos.html", result= result, form=form)
# Only logged-in users can access the route


if __name__ == "__main__":
    app.run(debug=True )
