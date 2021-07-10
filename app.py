from flask import Flask, render_template
from flask.helpers import url_for
from flask.wrappers import Response

from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId

from flask import jsonify, request


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/task33"

mongo = PyMongo(app)


@app.route("/")
def home():
    data = render_template("homepage.html")
    return data


@app.route("/add")
def add():
    add = render_template("add.html")
    return add


@app.route("/upd")
def update():
    update = render_template("update.html")
    return update


@app.route("/del")
def delete():
    delete = render_template("delete.html")
    return delete


@app.route('/create', methods=["POST"])
def add_student():
    db = {
        "name": request.form.get("name"),
        "roll_no": request.form.get("roll"),
        "marks": request.form.get("marks"),
        "age": request.form.get("age")
    }

    mongo.db.studentdata.insert(db)
    resp = jsonify("User added Successfully")
    resp.status_code = 200
    return resp


@app.route('/read', methods=["GET"])
def students():
    students = mongo.db.studentdata.find()
    resp = dumps(students)
    return resp


@app.route('/delete', methods=['POST'])
def delete_students():
    id = request.form.get("id")
    db = {
        "_id": ObjectId(id)
    }

    mongo.db.studentdata.delete_one(db)
    resp = jsonify("User deleted successfully")
    resp.status_code = 200

    return resp


@app.route('/update', methods=['POST'])
def update_students():
    id = request.form.get("id")
    db = {
        "_id": ObjectId(id)
    }
    data = {
        "name": request.form.get("name"),
        "roll_no": request.form.get("roll"),
        "marks": request.form.get("marks"),
        "age": request.form.get("age")
    }

    mongo.db.studentdata.update_one(db, {"$set": data})
    resp = jsonify("User Updated successfully")
    resp.status_code = 200

    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }
    resp = jsonify(message)
    return resp


if __name__ == "__main__":
    app.run(debug=True)
