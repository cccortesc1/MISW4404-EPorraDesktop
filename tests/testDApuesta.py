#Archivo de ejemplo para las pruebas unitarias.
#El nombre del archivo debe iniciar con el prefijo test_

#Importar unittest para crear las pruebas unitarias
import random
import unittest

from faker import Faker
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.apuesta import Apuesta
from src.modelo.apostador import Apostador
from src.modelo.declarative_base import engine, Base, session

#Importar la clase Logica_mock para utilizarla en las pruebas
from src.logica.Logica import Logica

#Clase de ejemplo, debe tener un nombre que termina con el sufijo TestCase, y conservar la herencia
class TestApuestas(unittest.TestCase):

    #Instancia el atributo logica para cada prueba
    def setUp(self):
        self.carreras = []
        self.apuestas = []
        self.logica = Logica()
        self.data_factory = Faker()

    #Prueba para crear 3 apostadores
    def test_Apostador(self):
        if(len(session.query(Apostador).all())==0):
            apostador1 = Apostador(nombre=self.data_factory.name())

            session.add(apostador1)
            session.commit();

    #Sin pasar una carrera el resultado debe ser validar que devuelve False
    def test_crear_apuesta_sin_carrera(self):
        self.carreras = []
        idApostador = 0 
        id_carrera = -1
        valor = self.data_factory.random_int(min=100, max=10000)
        idCompetidor = 1 
        xApuesta = self.logica.crear_apuesta(idApostador, id_carrera, valor, idCompetidor)
        self.assertFalse(xApuesta)

    #Dado un competidor no existente el resultado debe ser validar que devuelve None
    def test_crear_apuesta_apostador_noExistente(self):
        self.logica.carreras = self.logica.dar_carreras()
        idApostador = 0 #idApostador
        id_carrera = 0
        valor = self.data_factory.random_int(min=100, max=10000)
        competidor = -1 #idCompetidor
        xApuesta = self.logica.crear_apuesta(idApostador, id_carrera, valor, competidor)
        self.assertFalse(xApuesta)

    #Dado un competidor y una carrera sin apostador el resultado debe ser validar que devuelve False
    def test_crear_apuesta_competidor_Existente(self):
        self.logica.carreras = self.logica.dar_carreras()
        xCompetidor = session.query(Competidor).get(1)      
        apostador = -1
        id_carrera = 0
        valor = self.data_factory.random_int(min=100, max=10000)
        competidor = xCompetidor.nombre
        xApuesta = self.logica.crear_apuesta(apostador, id_carrera, valor, competidor)
        self.assertFalse(xApuesta)    

    #Dado un competidor, una carrera y un apostador el resultado debe ser crear la carrera
    def test_crear_apuesta_completa(self):
        self.carreras = self.logica.dar_carreras()
        self.apostadores = self.logica.dar_apostadores()
        xApostador = session.query(Apostador).get(1)                                      
        xCompetidor = session.query(Competidor).get(1)                                      
        apostador = xApostador.nombre 
        id_carrera = 0
        valor = self.data_factory.random_int(min=100, max=10000)
        competidor = xCompetidor.nombre
        xApuesta = self.logica.crear_apuesta(apostador, id_carrera, valor, competidor)
        self.assertTrue(xApuesta)    

    #Dado un competidor, una carrera y un apostador el resultado debe ser crear la carrera
    def test_crear_apuesta_ganancias(self):
        self.carreras = self.logica.dar_carreras()
        self.apostadores = self.logica.dar_apostadores()
        xApostador = session.query(Apostador).get(1)                                      
        xCompetidor = session.query(Competidor).get(7) 
        apostador = xApostador.nombre 
        id_carrera = 2
        valor = self.data_factory.random_int(min=100, max=10000)
        competidor = xCompetidor.nombre
        xApuesta = self.logica.crear_apuesta(apostador, id_carrera, valor, competidor)
        self.assertTrue(xApuesta)        

    #Prueba marcar competidor como ganador y terminar la carrera
    def test_terminar_carrera(self):
        self.logica.carreras = self.logica.dar_carreras()
        idCarrera = 0
        idCompetidor = 0
        carrera = self.logica.terminar_carrera(idCarrera,idCompetidor)
        self.assertTrue(carrera)    
    
    #Prueba marcar competidor como ganador y terminar la carrera sin apuesta, debe retornar falso
    def test_terminar_carrera_sin_apuestas(self):
        self.logica.carreras = self.logica.dar_carreras()
        idCarrera = 1
        idCompetidor = 1
        carrera = self.logica.terminar_carrera(idCarrera,idCompetidor)
        self.assertFalse(carrera)        

    #Dado un competidor ganador y una carrera se genera el reporte de ganancias
    def test_generar_reporte_ganancias(self):    
        self.logica.carreras = self.logica.dar_carreras()
        idCarrera = 2
        idCompetidor = 0
        carrera = self.logica.dar_reporte_ganancias(idCarrera,idCompetidor)
        self.assertTrue(carrera)        

    def test_zeliminar_apuestas(self):    
        i = 0
        #     '''Eliminar Apuestas'''
        for apuest in self.logica.apuestas:
            self.logica.eliminar_apuesta(0, i)
            i += 1

        self.assertGreaterEqual(i, 0)            

    def test_zeliminar_apostadores(self):    
        i = 0
        #     '''Eliminar Apostadores'''
        iApos = 0
        for aposta in self.logica.apostadores:
            self.logica.eliminar_apostador(iApos)    
            iApos += 1

        self.assertGreaterEqual(iApos, 0)    

    def test_zeliminar_carreras(self):    
        i = 0
        #     '''Eliminar carreras'''
        iCarre = 0    
        for carrera in self.logica.carreras:
            self.logica.eliminar_carrera(iCarre)    
            iCarre += 1

        self.assertGreaterEqual(iCarre, 0)    

    # def tearDown(self):
    #     i = 0
    #     #     '''Eliminar Apuestas'''
    #     for apuest in self.logica.apuestas:
    #         self.logica.eliminar_apuesta(0, i)
    #         i += 1

    #     iApos = 0
    #     for aposta in self.logica.apostadores:
    #         self.logica.eliminar_apostador(iApos)    
    #         iApos += 1

    #     iCarre = 0    
    #     for carrera in self.logica.carreras:
    #         self.logica.eliminar_carrera(iCarre)    
    #         iCarre += 1