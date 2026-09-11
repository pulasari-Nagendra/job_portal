from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def jwt_required_with_role(required_role):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Check whether a valid JWT exists
                verify_jwt_in_request()

                # Get information stored inside the JWT
                claims = get_jwt()

                # Get user's role
                user_role = claims.get("role")

                # Check role
                if user_role != required_role:
                    return jsonify({
                        "message": "Access denied. You do not have permission."
                    }), 403

                return func(*args, **kwargs)

            except Exception as e:
                return jsonify({
                    "message": "Invalid or missing token",
                    "error": str(e)
                }), 401

        return wrapper

    return decorator