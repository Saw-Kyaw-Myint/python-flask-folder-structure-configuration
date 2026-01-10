from app.extension import db


class User(db.Model):
    """
    Represents a user in the application.

    Attributes:
        id (int): Primary key for the user.
        name (str): Full name of the user, required, max 100 characters.
        profile (str): Optional profile description or profile image URL.
        email (str): Unique email address for the user, required.
        posts (List[Post]): SQLAlchemy relationship to the user's posts
            (back_populates 'user'), with cascade delete behavior.

    Table:
        users
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    posts = db.relationship("Post", back_populates="user", cascade="all, delete-orphan")


db.timeStamp(User)
db.softDelete(User)
