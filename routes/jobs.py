from flask import Blueprint, request, jsonify
from database.db import get_db_connection
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

jobs_bp = Blueprint("jobs", __name__)


# ---------------------------------------------------
# GET ALL JOBS
# ---------------------------------------------------

@jobs_bp.route("/jobs", methods=["GET"])
def get_jobs():

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                title,
                company,
                location,
                salary,
                description,
                requirements,
                job_type,
                employer_id,
                created_at
            FROM jobs
            ORDER BY created_at DESC
        """)

        jobs = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(jobs), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to fetch jobs",
            "error": str(e)
        }), 500


# ---------------------------------------------------
# GET SINGLE JOB
# ---------------------------------------------------

@jobs_bp.route("/jobs/<int:job_id>", methods=["GET"])
def get_job(job_id):

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                title,
                company,
                location,
                salary,
                description,
                requirements,
                job_type,
                employer_id,
                created_at
            FROM jobs
            WHERE id = %s
        """, (job_id,))

        job = cursor.fetchone()

        cursor.close()
        connection.close()

        if not job:
            return jsonify({
                "message": "Job not found"
            }), 404

        return jsonify(job), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to fetch job",
            "error": str(e)
        }), 500


# ---------------------------------------------------
# CREATE JOB - EMPLOYER ONLY
# ---------------------------------------------------

@jobs_bp.route("/jobs", methods=["POST"])
def create_job():

    try:
        verify_jwt_in_request()

        claims = get_jwt()

        if claims.get("role") != "employer":
            return jsonify({
                "message": "Only employers can create jobs"
            }), 403

        employer_id = int(get_jwt_identity())

        data = request.get_json()

        title = data.get("title")
        company = data.get("company")
        location = data.get("location")
        salary = data.get("salary")
        description = data.get("description")
        requirements = data.get("requirements")
        job_type = data.get("job_type")

        if not title or not company or not location or not description or not requirements or not job_type:
            return jsonify({
                "message": "Required fields are missing"
            }), 400

        if job_type not in ["Full-time", "Part-time", "Internship"]:
            return jsonify({
                "message": "Invalid job type"
            }), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO jobs
            (title, company, location, salary, description, requirements, job_type, employer_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            title,
            company,
            location,
            salary,
            description,
            requirements,
            job_type,
            employer_id
        ))

        connection.commit()

        job_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Job created successfully",
            "job_id": job_id
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Failed to create job",
            "error": str(e)
        }), 500


# ---------------------------------------------------
# UPDATE JOB - EMPLOYER ONLY
# ---------------------------------------------------

@jobs_bp.route("/jobs/<int:job_id>", methods=["PUT"])
def update_job(job_id):

    try:
        verify_jwt_in_request()

        claims = get_jwt()

        if claims.get("role") != "employer":
            return jsonify({
                "message": "Only employers can update jobs"
            }), 403

        employer_id = int(get_jwt_identity())

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT employer_id FROM jobs WHERE id = %s",
            (job_id,)
        )

        job = cursor.fetchone()

        if not job:
            cursor.close()
            connection.close()

            return jsonify({
                "message": "Job not found"
            }), 404

        if job["employer_id"] != employer_id:
            cursor.close()
            connection.close()

            return jsonify({
                "message": "You can only update your own jobs"
            }), 403

        data = request.get_json()

        title = data.get("title")
        company = data.get("company")
        location = data.get("location")
        salary = data.get("salary")
        description = data.get("description")
        requirements = data.get("requirements")
        job_type = data.get("job_type")

        if not title or not company or not location or not description or not requirements or not job_type:
            cursor.close()
            connection.close()

            return jsonify({
                "message": "Required fields are missing"
            }), 400

        if job_type not in ["Full-time", "Part-time", "Internship"]:
            cursor.close()
            connection.close()

            return jsonify({
                "message": "Invalid job type"
            }), 400

        cursor.execute("""
            UPDATE jobs
            SET
                title = %s,
                company = %s,
                location = %s,
                salary = %s,
                description = %s,
                requirements = %s,
                job_type = %s
            WHERE id = %s
        """, (
            title,
            company,
            location,
            salary,
            description,
            requirements,
            job_type,
            job_id
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Job updated successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to update job",
            "error": str(e)
        }), 500


# ---------------------------------------------------
# DELETE JOB - EMPLOYER ONLY
# ---------------------------------------------------

@jobs_bp.route("/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):

    try:
        verify_jwt_in_request()

        claims = get_jwt()

        if claims.get("role") != "employer":
            return jsonify({
                "message": "Only employers can delete jobs"
            }), 403

        employer_id = int(get_jwt_identity())

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT employer_id FROM jobs WHERE id = %s",
            (job_id,)
        )

        job = cursor.fetchone()

        if not job:
            cursor.close()
            connection.close()

            return jsonify({
                "message": "Job not found"
            }), 404

        if job["employer_id"] != employer_id:
            cursor.close()
            connection.close()

            return jsonify({
                "message": "You can only delete your own jobs"
            }), 403

        cursor.execute(
            "DELETE FROM jobs WHERE id = %s",
            (job_id,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Job deleted successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to delete job",
            "error": str(e)
        }), 500