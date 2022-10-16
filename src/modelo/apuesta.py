from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Apuesta(Base):
    __tablename__ = 'apuesta'

    id = Column(Integer, primary_key=True)
    valor = Column(Float)
    cuota = Column(Float)
    ganancia = Column(Float)
    carreraId = Column(Integer, ForeignKey('carrera.id'))
    apostadorId = Column(Integer, ForeignKey('apostador.id'))
    competidorId = Column(Integer, ForeignKey('competidor.id'))
    