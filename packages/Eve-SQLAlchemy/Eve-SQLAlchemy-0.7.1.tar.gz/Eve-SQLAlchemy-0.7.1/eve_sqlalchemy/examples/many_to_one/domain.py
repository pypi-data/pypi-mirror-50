"""Basic Many-To-One relationship configuration in SQLAlchemy.

This is taken from the official SQLAlchemy documentation:
http://docs.sqlalchemy.org/en/rel_1_1/orm/basic_relationships.html#many-to-one
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))


class Parent(BaseModel):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child", backref="parents")


class Child(BaseModel):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
