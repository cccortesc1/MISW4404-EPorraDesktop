from sqlalchemy import Boolean,Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base


class Competidor(Base):
    __tablename__ = 'competidor'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    probabilidad = Column(Float)
    esGanador = Column(Boolean, default=False)
    carreraId = Column(Integer, ForeignKey('carrera.id'))