"""The models for our Gist App."""

from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    Date
)

from .meta import Base


class Profile(Base):
    """The profile object."""

    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    favorite_food = Column(Unicode)
    date = Column(Date)
    description = Column(Unicode)


Index('my_index', MyModel.name, unique=True, mysql_length=255)
