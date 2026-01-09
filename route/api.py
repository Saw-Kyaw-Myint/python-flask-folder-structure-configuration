from flask import Blueprint

from app.controllers.auth_controller import get_me, login_user
from app.controllers.user_controller import create_user, get_users
from app.extension import limiter
from app.helpers.commons import before_middleware
from app.middleware.user_middleware import user_middleware

# ///////// implement Blueprint //////////////////////
user_bp = Blueprint("user", __name__, url_prefix="/users")
auth_bp = Blueprint("auth", __name__)


# Apply rate limit to the whole blueprint
limiter.limit("5 per minute")(user_bp)

# Route

# Auth Route
auth_bp.route("/login", methods=["POST"])(login_user)
auth_bp.route("/me", methods=["GET"])(get_me)

# User Route
before_middleware(user_bp, user_middleware)
user_bp.route("/", methods=["GET"])(get_users)
# @limiter.limit("10 per minute")  can set single limit
user_bp.route("/create", methods=["POST"])(create_user)

# export all Blueprint
__all__ = ["user_bp", "auth_bp"]
