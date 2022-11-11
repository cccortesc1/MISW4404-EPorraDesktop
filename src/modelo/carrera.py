from sqlalchemy import Boolean, Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Carrera(Base):
    __tablename__ = 'carrera'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    abierta = Column(Boolean, unique=False, default=True)