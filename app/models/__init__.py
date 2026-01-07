"""
Package `app.models`

This package contains all database models for the application.
It exposes the main models through `__all__` for easy import.

Modules:
    - user: Defines the `User` model.
    - post: Defines the `Post` model.

Exports:
    - User: The User model class.
    - Post: The Post model class.

Usage:
    from app.models import User, Post
"""

from .user import User
from .post import Post

__all__ = [
    "User",
    "Post"
]
