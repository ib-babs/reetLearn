# #!/usr/bin/python3
# from sqlalchemy import Column, BLOB, String, ForeignKey, Boolean
# from models.base_model import BaseModel, Base


# class UserProgress(BaseModel, Base):
#     __tablename__ = 'users_progress'
#     user_id = Column(ForeignKey('users.id'), nullable=False)
#     completed = Column(Boolean, default=False)
#     course_id = Column(ForeignKey('courses.id'), nullable=False)
