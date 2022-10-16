#Archivo de ejemplo para las pruebas unitarias.
#El nombre del archivo debe iniciar con el prefijo test_

#Importar unittest para crear las pruebas unitarias
import unittest

from faker import Faker
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.declarative_base import engine, Base, session

#Importar la clase Logica_mock para utilizarla en las pruebas
from src.logica.Logica import Logica

#Clase de ejemplo, debe tener un nombre que termina con el sufijo TestCase, y conservar la herencia
class testCompetidor(unittest.TestCase):
    
    #Instancia el atributo logica para cada prueba
    def setUp(self):
        self.carreras = []
        self.apuestas = []
        self.logica = Logica()
        self.data_factory = Faker()

    