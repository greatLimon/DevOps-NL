import sqlalchemy as db
from sqlalchemy.orm import Session, DeclarativeBase, relationship
from sqlalchemy.sql import func

#db
engine = db.create_engine('sqlite:///2.1 Flask/homework/adv.db', echo = True)


class Base(DeclarativeBase): 
    pass

class User(Base):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String)
    token = db.Column(db.String, unique=True)

class Advertisment(Base):
    __tablename__ = "advertisment"
 
    id = db.Column(db.Integer, primary_key=True, index=True)
    header = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

Base.metadata.create_all(bind=engine)


session = Session(autoflush=False, bind=engine)

