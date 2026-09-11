from flask import Blueprint, request, jsonify
from database.db import get_db_connection
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

applications_bp = Blueprint("applications", __name__)


# ---------------------------------------------------
# APPLY FOR A JOB - CANDIDATE ONLY
# ---------------------------------------------------

@applications_bp.route("/apply/<int:job_id>", methods=["POST"])
def apply_job(job_id):

    try:
        verify_jwt_in_request()

        claims = get_jwt()

        if claims.get("role") != "candidate":
            return jsonify({
                "message": "Only candidates can apply for jobs"
            }), 403

        candidate_id = int(get_jwt_identity())

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check whether job exists
        cursor.execute(
            "SELECT id FROM jobs WHERE id = %s",
            (job_id,)
        )

        job = cursor.fetchone()

        if not job:
            cursor.close()
            connection.close()

            return jsonify({
                "message": "Job not found"
            }), 404

        # Check whether candidate already applied
        cursor.execute(
            """
            SELECT id
            FROM applications
            WHERE job_id = %s AND candidate_id = %s
            """,
            (job_id, candidate_id)
        )

        existing_application = cursor.fetchone()

        if existing_application:
            cursor.close()
            connection.close()

            return jsonify({
                "message": "You have already applied for this job"
            }), 409

        # Create application
        cursor.execute(
            """
            INSERT INTO applications (job_id, candidate_id)
            VALUES (%s, %s)
            """,
            (job_id, candidate_id)
        )

        connection.commit()

        application_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Application submitted successfully",
            "application_id": application_id
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Failed to apply for job",
            "error": str(e)
        }), 500


# ---------------------------------------------------
# VIEW MY APPLICATIONS - CANDIDATE ONLY
# ---------------------------------------------------

@applications_bp.route("/my-applications", methods=["GET"])
def my_applications():

    try:
        verify_jwt_in_request()

        claims = get_jwt()

        if claims.get("role") != "candidate":
            return jsonify({
                "message": "Only candidates can view their applications"
            }), 403

        candidate_id = int(get_jwt_identity())

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                applications.id,
                applications.job_id,
                jobs.title,
                jobs.company,
                jobs.location,
                jobs.job_type,
                applications.status,
                applications.applied_at
            FROM applications
            JOIN jobs
                ON applications.job_id = jobs.id
            WHERE applications.candidate_id = %s
            ORDER BY applications.applied_at DESC
            """,
            (candidate_id,)
        )

        applications = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(applications), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to fetch applications",
            "error": str(e)
        }), 500


# ---------------------------------------------------
# VIEW APPLICATIONS FOR EMPLOYER'S JOBS
# ---------------------------------------------------

@applications_bp.route("/job-applications", methods=["GET"])
def job_applications():

    try:
        verify_jwt_in_request()

        claims = get_jwt()

        if claims.get("role") != "employer":
            return jsonify({
                "message": "Only employers can view job applications"
            }), 403

        employer_id = int(get_jwt_identity())

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                applications.id,
                applications.job_id,
                jobs.title,
                users.id AS candidate_id,
                users.name AS candidate_name,
                users.email AS candidate_email,
                applications.status,
                applications.applied_at
            FROM applications
            JOIN jobs
                ON applications.job_id = jobs.id
            JOIN users
                ON applications.candidate_id = users.id
            WHERE jobs.employer_id = %s
            ORDER BY applications.applied_at DESC
            """,
            (employer_id,)
        )

        applications = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(applications), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to fetch job applications",
            "error": str(e)
        }), 500

# ---------------------------------------------------
# UPDATE APPLICATION STATUS - EMPLOYER ONLY
# ---------------------------------------------------

@applications_bp.route(
    "/applications/<int:application_id>/status",
    methods=["PUT"]
)
def update_application_status(application_id):

    try:
        verify_jwt_in_request()

        claims = get_jwt()

        if claims.get("role") != "employer":
            return jsonify({
                "message": "Only employers can update application status"
            }), 403

        employer_id = int(get_jwt_identity())

        data = request.get_json()

        status = data.get("status")

        if status not in ["Applied", "Shortlisted", "Rejected"]:
            return jsonify({
                "message": "Invalid application status"
            }), 400

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check application and make sure it belongs
        # to a job posted by this employer
        cursor.execute(
            """
            SELECT
                applications.id,
                jobs.employer_id
            FROM applications
            JOIN jobs
                ON applications.job_id = jobs.id
            WHERE applications.id = %s
            """,
            (application_id,)
        )

        application = cursor.fetchone()

        if not application:
            cursor.close()
            connection.close()

            return jsonify({
                "message": "Application not found"
            }), 404

        # Prevent an employer from modifying
        # another employer's application
        if application["employer_id"] != employer_id:
            cursor.close()
            connection.close()

            return jsonify({
                "message": "You can only update applications for your own jobs"
            }), 403

        cursor.execute(
            """
            UPDATE applications
            SET status = %s
            WHERE id = %s
            """,
            (status, application_id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Application status updated successfully",
            "application_id": application_id,
            "status": status
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to update application status",
            "error": str(e)
        }), 500

# ---------------------------------------------------
# CHECK APPLICATION STATUS FOR A SPECIFIC JOB
# ---------------------------------------------------

@applications_bp.route(
    "/application-status/<int:job_id>",
    methods=["GET"]
)
def application_status(job_id):

    try:
        verify_jwt_in_request()

        claims = get_jwt()

        # Only candidates need application status
        if claims.get("role") != "candidate":
            return jsonify({
                "applied": False
            }), 200

        candidate_id = int(get_jwt_identity())

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, status
            FROM applications
            WHERE job_id = %s
              AND candidate_id = %s
            LIMIT 1
            """,
            (job_id, candidate_id)
        )

        application = cursor.fetchone()

        cursor.close()
        connection.close()

        if application:
            return jsonify({
                "applied": True,
                "application_id": application["id"],
                "status": application["status"]
            }), 200

        return jsonify({
            "applied": False
        }), 200

    except Exception as e:
        print("JOB APPLICATIONS ERROR:", repr(e))

        return jsonify({
            "message": "Failed to fetch job applications",
            "error": str(e)
        }),500