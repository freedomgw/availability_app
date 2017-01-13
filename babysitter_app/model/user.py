from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_utils import PasswordType

import datetime

from main import Base
from session import rw_session

class User(Base):

  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  created_at = Column(Date, default=datetime.datetime.now())
  updated_at = Column(Date, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
  name = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False, unique=True)
  password = Column(PasswordType(
    schemes=[
      'pbkdf2_sha512'
    ]
  ))

  def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.password = password

  def verify_password(self, password):
    return self.password == password

  @staticmethod
  def get_user_by_id(user_id):
    user = None
    with rw_session() as session:
      user = session.query(User).get(user_id)
    return user

  @staticmethod
  def create_user(user_info):
    user = None
    with rw_session() as session:
      user = User(user_info['name'], user_info['email'], user_info['password'])
      session.add(user)
      session.flush()
    return user

  @staticmethod
  def get_user_by_email(session, email):
    q = session.query(User)
    q = q.filter(User.email == email)
    return q.first()
