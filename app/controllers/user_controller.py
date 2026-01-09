from flask import current_app, jsonify, request
from pydantic import ValidationError

from app.extension import db
from app.helpers.commons import format_pydantic_errors
from app.models import User
from app.request.user_request import UserCreateRequest
from app.schema.user_schema import UserSchema
from config.logging import logger

# Schemas
users_schema = UserSchema(many=True)
user_schema = UserSchema()


def get_users():
    """
    Retrieve all users from the database.

    This endpoint fetches all User records, serializes them using UserSchema,
    and returns a JSON response.

    Steps:
        1. Query all users from the database.
        2. Log that the endpoint was called.
        3. Serialize the users using UserSchema.
        4. Return the serialized data as JSON.

    Returns:
        Response (JSON):
            - 200 OK with a list of all users
    """
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200


def create_user():
    """
    Create a new user in the database.

    This endpoint accepts JSON input, validates it with Pydantic's
    UserCreateRequest, checks for duplicate emails, and creates a new
    user record if validation passes.

    Expected JSON payload:
        {
            "name": "<user_name>",
            "email": "<user_email>"
        }

    Steps:
        1. Validate input using Pydantic UserCreateRequest.
        2. If validation fails, return 400 with formatted errors.
        3. Check if a user with the given email already exists.
        4. If email exists, return 400 with an error message.
        5. Create a new User object and add it to the database.
        6. Commit the session.
        7. Serialize the created user and return as JSON.

    Returns:
        Response (JSON):
            - 201 Created with the newly created user if successful
            - 400 Bad Request if validation fails or email already exists
    """
    try:
        # Validate input using Pydantic
        data = UserCreateRequest.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"errors": format_pydantic_errors(e)}), 400

    existing_user = User.query.filter_by(email=data.email).first()
    if existing_user:
        return (
            jsonify(
                {"errors": [{"field": "email", "message": "Email already exists"}]}
            ),
            400,
        )

    # Create user
    user = User(name=data.name, email=data.email)
    db.session.add(user)
    db.session.commit()

    # Return serialized single user
    return jsonify(user_schema.dump(user)), 201
