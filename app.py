from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import certifi
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Application configuration
app.config["MONGO_URI"] = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/flask_practice"
)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# Initialize MongoDB
mongo = PyMongo(app, tlsCAFile=certifi.where())


# Health check endpoint
# This endpoint does not depend on MongoDB.
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


# Home page -> list students
@app.route("/")
def index():
    students = mongo.db.students.find()
    return render_template("index.html", students=students)


# Add student
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]

        mongo.db.students.insert_one({
            "name": name,
            "email": email,
            "course": course
        })

        return redirect(url_for("index"))

    return render_template("add_student.html")


# Update student
@app.route("/update/<student_id>", methods=["GET", "POST"])
def update_student(student_id):
    student = mongo.db.students.find_one({
        "_id": ObjectId(student_id)
    })

    if request.method == "POST":
        new_name = request.form["name"]
        new_email = request.form["email"]
        new_course = request.form["course"]

        mongo.db.students.update_one(
            {"_id": ObjectId(student_id)},
            {
                "$set": {
                    "name": new_name,
                    "email": new_email,
                    "course": new_course
                }
            }
        )

        return redirect(url_for("index"))

    return render_template(
        "update_student.html",
        student=student
    )


# Delete student
@app.route("/delete/<student_id>")
def delete_student(student_id):
    mongo.db.students.delete_one({
        "_id": ObjectId(student_id)
    })

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )