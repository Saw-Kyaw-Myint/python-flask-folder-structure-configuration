from app.extension import db


class Post(db.Model):
    """
    Represents a blog post or user-generated content in the database.

    Attributes:
        id (int): Primary key for the post.
        title (str): Title of the post, required, max 200 characters.
        body (str): Content/body of the post, optional.
        user_id (int): Foreign key linking to the User who created the post.
        user (User): SQLAlchemy relationship to the User model (back_populates 'posts').

    Table:
        posts
    """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="posts")


# shorthand add fields
db.timeStamp(Post)
db.softDelete(Post)
