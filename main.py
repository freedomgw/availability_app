from bottle import Bottle, run
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sys import argv

import babysitter_app.babysitter_app

app = Bottle()

# configure Session class with desired options
Session = sessionmaker(expire_on_commit=False)
# we create the engine, which the Session will use for connection resources
engine = create_engine('mysql+pymysql://root:@localhost/availability_db_dev', pool_recycle=60)
# associate it with our custom Session class
Session.configure(bind=engine)
# create a Session
session = Session()

Base = declarative_base()

if __name__ == '__main__':
  app.merge(babysitter_app.babysitter_app.app)
  run(app, host='localhost', port=8080)
