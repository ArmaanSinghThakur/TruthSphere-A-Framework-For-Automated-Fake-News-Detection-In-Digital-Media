from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
import os
import requests


app= Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY']= 'supersecretkey'
app.config['UPLOAD_FOLDER']= 'static/files'

class UploadFileForm(FlaskForm):
    file= FileField("File")
    submit= SubmitField("Upload File")

@app.route("/", methods= ["GET", "POST"])
@app.route("/home", methods= ["GET", "POST"])
def home():
    form= UploadFileForm()
    if form.validate_on_submit():
        file= requests
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config["UPLOAD_FOLDER"],secure_filename(file.filename)))
        return "FILE has been uploaded"
    return render_template("test.html", form= form)


if __name__== "__main__":
    app.run(debug=True)