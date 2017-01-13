from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import datetime

from main import Base
from session import rw_session

class Role(Base):
  BABYSITTER_ROLE = 'babysitter'

  __tablename__ = "role"

  id = Column(Integer, primary_key=True)
  created_at = Column(Date, default=datetime.datetime.now())
  updated_at = Column(Date,
    default=datetime.datetime.now(),
    onupdate=datetime.datetime.now())
  description = Column(String(50), nullable=False)

  @staticmethod
  def get_babysitter_role_id():
    """Get the role id of the description, babysitter

    Returns:
    None or babysitter_role_id
    """
    babysitter_role_id = None
    with rw_session() as session:
      q = session.query(Role)
      q = q.filter(Role.description == Role.BABYSITTER_ROLE)
      babysitter_role_id = q.one().id
    return babysitter_role_id