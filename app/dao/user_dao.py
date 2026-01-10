from app.models import User
from app.extension import db
from app.dao.base_dao import BaseDao

class UserDao(BaseDao):
    """Handles direct database operations"""

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id: int):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create(user: User):
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(user: User):
        user.soft_delete()
        db.session.commit()
