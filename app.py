# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite2'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # False
# db = SQLAlchemy(app)
#
#
# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100))
#     data = db.Column(db.LargeBinary)
#     complete = db.Column(db.Boolean)
#
#
# def render_picture(data):
#     render_pic = base64.b64encode(data).decode('ascii')
#     return render_pic
#
#
# @app.route("/")
# def home():
#     todo_list = Todo.query.all()
#     return render_template("index.html", todo_list=todo_list)  # , image=image)
#
#
# from werkzeug.utils import secure_filename
# import os
# @app.route("/add", methods=["POST"])
# def add():
#     title = request.form.get("title")
#     f = request.files['inputFile']
#     f.save(secure_filename(f.filename))
#     file = request.files['inputFile']
#     data = file.read()
#     # render_file = render_picture(data)
#     new_todo = Todo(title=title, data=data, complete=False)
#     db.session.add(new_todo)
#     db.session.commit()
#     return redirect(url_for("home"))

# @app.route("/update/<int:todo_id>")
# def update(todo_id):
#     todo = Todo.query.filter_by(id=todo_id).first()
#     todo.complete = not todo.complete
#     db.session.commit()
#     return redirect(url_for("home"))
#
#
# @app.route("/delete/<int:todo_id>")
# def delete(todo_id):
#     todo = Todo.query.filter_by(id=todo_id).first()
#     db.session.delete(todo)
#     db.session.commit()
#     return redirect(url_for("home"))
#
#
# if __name__ == "__main__":
#     db.create_all()
#     app.debug = True
#     app.run(host="192.168.219.158", port="8000")

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import base64
import os
from PIL import Image

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    data = db.Column(db.LargeBinary)
    complete = db.Column(db.Boolean)
    filepath = db.Column(db.String(100))


def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic


@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)  # , image=image)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    file = request.files['inputFile']
    filenm = secure_filename(file.filename)
    fp = os.path.join("static", filenm)
    file.save(fp)
    data = file.read()
    new_todo = Todo(title=title, data=data, filepath=fp, complete=False)
    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/access/<int:todo_id>")
def access(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    pth = todo.filepath
    pth = rf'/{pth}'
    imgFiles = ['jpg', 'png', 'jpeg']
    return render_template("down.html", path=pth)  # , image=image)


if __name__ == "__main__":
    db.create_all()
    app.debug = True
    app.run(debug=True, host="192.168.200.133", port="8000")
    # app.run()
