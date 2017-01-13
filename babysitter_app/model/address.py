from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import datetime

from main import Base
from session import rw_session

from user import User

class Address(Base):

  __tablename__ = "address"

  id = Column(Integer, primary_key=True)
  created_at = Column(Date, default=datetime.datetime.now())
  updated_at = Column(Date,
    default=datetime.datetime.now(),
    onupdate=datetime.datetime.now())
  user_id = Column(Integer, ForeignKey('user.id'))
  street_no = Column(Integer, nullable=False)
  street_name = Column(String(50), nullable=False)
  city = Column(String(50), nullable=False)
  province = Column(String(50), nullable=False)
  postal_code = Column(String(50), nullable=False)
  country = Column(String(50), nullable=False)

  user = relationship(User, backref='children')

  def __init__(self, user_id, street_no, street_name, city, province,
      postal_code, country):
    self.user_id = user_id
    self.street_no = street_no
    self.street_name = street_name
    self.city = city
    self.province = province
    self.postal_code = postal_code
    self.country = country

  @staticmethod
  def create_address(user_id, user_addr_info):
    """Create a new address and save to database

    Arguments:
    user_id -- int, user.id
    user_addr_info -- dictionary, information of user

    Returns:
    address_id -- int, address.id
    """
    address_id = None
    with rw_session() as session:
      address = Address(
        user_id,
        user_addr_info['street_no'],
        user_addr_info['street_name'],
        user_addr_info['city'],
        user_addr_info['province'],
        user_addr_info['postal_code'],
        user_addr_info['country']
      )
      session.add(address)
      session.flush()
      address_id = address.id

    return address_id
