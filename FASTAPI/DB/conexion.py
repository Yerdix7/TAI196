import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

dbNmae= 'usuarios.sqlite'
base_dir= os.path.dirname(os.path.realpath(__file__))
dbUrl=f"sqlite:///{os.path.join(base_dir,dbNmae)}"

engine= create_engine(dbUrl, echo=True)
Session= sessionmaker(bind=engine)
Base = declarative_base()