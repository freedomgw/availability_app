from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from main import Base
from session import rw_session

from role import Role

class UserRole(Base):

  __tablename__ = "user_role"

  user_id = Column(Integer, ForeignKey('user.id'), nullable=False, primary_key=True)
  role_id = Column(Integer, ForeignKey('role.id'), nullable=False, primary_key=True)

  user = relationship("User", foreign_keys=[user_id])
  role = relationship("Role", foreign_keys=[role_id])

  def __init__(self, user_id, role_id):
    self.user_id = user_id
    self.role_id = role_id


  @staticmethod
  def is_babysitter(session, user_id):
    babysitter_role_id = Role.get_babysitter_role_id()
    q = session.query(UserRole)
    q = q.filter(UserRole.user_id == user_id)
    q = q.filter(UserRole.role_id == babysitter_role_id)
    return q.first() is not None


  @staticmethod
  def create_user_role(user_id, role_id):
    with rw_session() as session:
      user_role = UserRole(user_id, role_id)
      session.add(user_role)

