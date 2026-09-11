from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os

from routes.jobs import jobs_bp
from database.db import get_db_connection
from routes.auth import auth_bp
from routes.applications import applications_bp

load_dotenv()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

# Register authentication routes
app.register_blueprint(auth_bp)
app.register_blueprint(jobs_bp)
app.register_blueprint(applications_bp)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/test-db")
def test_db():
    try:
        connection = get_db_connection()

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")

        database = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Database connected successfully",
            "database": database
        })

    except Exception as e:
        return jsonify({
            "message": "Database connection failed",
            "error": str(e)
        }), 500


@app.route("/jobs-page")
def jobs_page():
    return render_template("jobs.html")


@app.route("/login-page")
def login_page():
    return render_template("login.html")


@app.route("/signup-page")
def signup_page():
    return render_template("signup.html")

@app.route("/job-details-page")
def job_details_page():
    return render_template("job-details.html")

@app.route("/candidate-dashboard")
def candidate_dashboard():
    return render_template("candidate-dashboard.html")

@app.route("/my-applications-page")
def my_applications_page():
    return render_template("my-applications.html")

@app.route("/employer-dashboard")
def employer_dashboard():
    return render_template("employer-dashboard.html")

@app.route("/create-job")
def create_job_page():
    return render_template("create-job.html")


@app.route("/edit-job")
def edit_job_page():
    return render_template("edit-job.html")


if __name__ == "__main__":
    print("STARTING JOB PORTAL SERVER...")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
