from flask import Flask, render_template, url_for, request, redirect
from flask import session as login_session
import pyrebase
import os
import json

config = {
  "apiKey": "AIzaSyBUtUudHkVkqZuk33ieZeWBqpfziUrwhrU",
  "authDomain": "flask-form-images-project.firebaseapp.com",
  "projectId": "flask-form-images-project",
  "storageBucket": "flask-form-images-project.appspot.com",
  "messagingSenderId": "619206162796",
  "appId": "1:619206162796:web:e2165aae01b8dfbf9edb49",
  "measurementId": "G-DL24F2GLQ6",
  "databaseURL": "https://flask-form-images-project-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)

app.config['SECRET_KEY'] = 'super-secret-key'

UPLOAD_FOLDER = 'images\\posts\\'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_file(file):
    if request.method == 'POST':
        if file and allowed_file(file.filename):
            filename = file.filename                   
            fn = os.path.join(app.static_folder,UPLOAD_FOLDER, filename)           
            file.save(fn)


@app.route('/')  # '/' for the default page
def home():
    if (db.child("Posts").get().val()==None):
        return render_template('index.html')
    posts = db.child("Posts").get().val()
    return render_template('index.html', posts=posts)


@app.route('/add_post', methods=['GET', 'POST'])  # '/' for the default page
def add_post():
    if request.method == "POST":
        photo = request.files['photo']
        caption = request.form['caption']
        upload_file(photo)
        fullPost = {"photo": photo.filename, "caption": caption}
        db.child("Posts").push(fullPost)
        return render_template('add_post.html')
    else:
        return render_template('add_post.html')


if __name__ == "__main__":  # Makes sure this is the main process
    app.run(debug=True)

