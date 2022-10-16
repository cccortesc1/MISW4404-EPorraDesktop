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
class testCarrera(unittest.TestCase):

		#Instancia el atributo logica para cada prueba
		def setUp(self):
			self.carreras = []
			self.logica = Logica()
			self.data_factory = Faker()

		#Prueba para crear carrera sin competidores
		def test_crear_carrera(self):
			nombreCarrera = self.data_factory.name()
			self.carreras = [{'id':1,'Nombre':nombreCarrera, 'Competidores':[],\
                                             'Abierta':True}]

			nombreCarrera=self.carreras[0]['Nombre']
			competidores = self.carreras[0]['Competidores']								 
			carrerar = self.logica.crear_carrera( nombreCarrera, competidores)
			self.assertFalse(carrerar)

		#Prueba para crear carrera validando que el nombre carrera no sea vacío, por lo tanto, debe retornar falso
		def test_crear_carrera_nombre_vacio(self):
			self.carreras = [{'Id':2,'Nombre':'', 'Competidores':[{'Id':'1', 'Nombre':'Juan Pablo Montoya', 'Probabilidad':0.15},\
                                                          {'Id':'2', 'Nombre':'Kimi Räikkönen', 'Probabilidad':0.2},\
                                                           {'Id':'3', 'Nombre':'Michael Schumacher', 'Probabilidad':0.65}],\
                                             'Abierta':True}]

			nombreCarrera=self.carreras[0]['Nombre']
			competidores = self.carreras[0]['Competidores']								 
			carrerar = self.logica.crear_carrera(nombreCarrera, competidores)
			self.assertFalse(carrerar)

		#Prueba para crear carrera validando que contenga más de un competidor
		def test_crear_carrera_con_competidores(self):
			nombreCarrera = self.data_factory.name()
			nombreComp1 = self.data_factory.name()
			nombreComp2 = self.data_factory.name()
			nombreComp3 = self.data_factory.name()
			
			self.carreras = [{'Id':'0', 'Nombre':nombreCarrera, 'Competidores':[], 'Abierta':True}]
			
			competidores = [{'Id':'4', 'Nombre':nombreComp1, 'Probabilidad':0.15},
                                                          {'Id':'5', 'Nombre': nombreComp2, 'Probabilidad':0.2},\
                                                           {'Id':'6', 'Nombre': nombreComp3, 'Probabilidad':0.65}]
			idCarrera = 0
			nombreCarrera=self.carreras[0]['Nombre']
			carrerar = self.logica.crear_carrera(nombreCarrera, competidores)
			
			xCarrera = session.query(Carrera).get(1)
			idCarrera = xCarrera.id
			self.carreras[0]['Id'] = idCarrera
			self.logica.carreras = self.carreras

			for compe in competidores:
				NombreComp = compe["Nombre"]
				ProbabilidadComp = compe["Probabilidad"]
				self.logica.aniadir_competidor(0, NombreComp, ProbabilidadComp)

			xCompetidores = session.query(Competidor).filter_by(carreraId = idCarrera).all()
			self.assertGreater(len(xCompetidores), 0)  

		#Prueba para crear carrera se debe validar que la sumatoria de las probabilidades da como resultado 1
		def test_crear_carrera_val_probabilidades(self):
			nombreCarrera = self.data_factory.name()
			nombreComp1 = self.data_factory.name()
			nombreComp2 = self.data_factory.name()
			nombreComp3 = self.data_factory.name()

			self.carreras = [{'Id':3,'Nombre': nombreCarrera, 'Competidores':[{'Id':'7', 'Nombre': nombreComp1, 'Probabilidad':0.15},\
                                                          {'Id':'8', 'Nombre':nombreComp2, 'Probabilidad':0.2},\
                                                           {'Id':'9', 'Nombre':nombreComp3 , 'Probabilidad':0.1}],\
                                             'Abierta':True}]

			nombreCarrera=self.carreras[0]['Nombre']
			competidores = self.carreras[0]['Competidores']			

			carrerar = self.logica.crear_carrera(nombreCarrera, competidores)
			
			self.assertFalse(carrerar)

		#Prueba para crear carrera validando que no exista una carrera con el mismo nombre
		def test_crear_carrera_validar_nombre(self):

			xCarrera = session.query(Carrera).get(1)
			idCarrera = xCarrera.id
			nombreCarrera = xCarrera.nombre

			self.carreras = [{'Id':'0', 'Nombre':nombreCarrera, 'Competidores':[], 'Abierta':True}]
			
			competidores = [{'Id':'4', 'Nombre':'Juan Pablo Montoya', 'Probabilidad':0.15},
                                                          {'Id':'5', 'Nombre':'Kimi Räikkönen', 'Probabilidad':0.2},\
                                                           {'Id':'6', 'Nombre':'Michael Schumacher', 'Probabilidad':0.65}]
			self.carreras[0]['Id'] = idCarrera
			self.logica.carreras = self.carreras

			carrerar = self.logica.crear_carrera(nombreCarrera, competidores)

			self.assertFalse(carrerar)	

		#Prueba para devolver los datos de las carrera creadas
		def test_dar_carreras(self):
			carreras = self.logica.dar_carreras()
			self.assertGreaterEqual(len(carreras), 0)

		#Prueba para crear carrera sin apuestas
		def test_crear_carrera_vsin_apuestas(self):
			nombreCarrera = self.data_factory.name()
			nombreComp1 = self.data_factory.name()
			nombreComp2 = self.data_factory.name()
			nombreComp3 = self.data_factory.name()
			
			self.carreras = []
			self.logica.carreras = self.logica.dar_carreras()
			self.logica.carreras.append({'Id':'2', 'Nombre':nombreCarrera, 'Competidores':[], 'Abierta':True, 'Ganador':-1})
			
			competidores = [{'Id':'4', 'Nombre':nombreComp1, 'Probabilidad':0.15},
                                                          {'Id':'5', 'Nombre': nombreComp2, 'Probabilidad':0.2},\
                                                           {'Id':'6', 'Nombre': nombreComp3, 'Probabilidad':0.65}]
			idCarrera = 1
			
			
			nombreCarrera=self.logica.carreras[idCarrera]['Nombre']
			self.logica.crear_carrera(nombreCarrera, competidores)
			
			self.logica.dar_carreras()

			for compe in competidores:
				NombreComp = compe["Nombre"]
				ProbabilidadComp = compe["Probabilidad"]
				self.logica.aniadir_competidor(1, NombreComp, ProbabilidadComp)

			
			idCarreraBd = self.logica.carreras[idCarrera]['Id']
			xCompetidores = session.query(Competidor).filter_by(carreraId = idCarreraBd).all()
			self.assertGreater(len(xCompetidores), 0)  

		#Prueba para crear carrera sin apuestas
		def test_crear_carrera_zpara_reporte_ganancias(self):
			nombreCarrera = self.data_factory.name()
			nombreComp1 = self.data_factory.name()
			nombreComp2 = self.data_factory.name()
			nombreComp3 = self.data_factory.name()
			
			self.carreras = []
			self.logica.carreras = self.logica.dar_carreras()
			self.logica.carreras.append({'Id':'2', 'Nombre':nombreCarrera, 'Competidores':[], 'Abierta':True, 'Ganador':-1})
			
			competidores = [{'Id':'4', 'Nombre':nombreComp1, 'Probabilidad':0.15},
                                                          {'Id':'5', 'Nombre': nombreComp2, 'Probabilidad':0.2},\
                                                           {'Id':'6', 'Nombre': nombreComp3, 'Probabilidad':0.65}]
			idCarrera = 2
			
			
			nombreCarrera=self.logica.carreras[idCarrera]['Nombre']
			self.logica.crear_carrera(nombreCarrera, competidores)
			
			self.logica.dar_carreras()

			for compe in competidores:
				NombreComp = compe["Nombre"]
				ProbabilidadComp = compe["Probabilidad"]
				self.logica.aniadir_competidor(2, NombreComp, ProbabilidadComp)

			
			idCarreraBd = self.logica.carreras[idCarrera]['Id']
			xCompetidores = session.query(Competidor).filter_by(carreraId = idCarreraBd).all()
			self.assertGreater(len(xCompetidores), 0)  	
	
		 
		# def tearDown(self):
		# 	'''Abre la sesión'''
		# 	self.session = session()

		# 	'''Consulta todos los Competidores'''
		# 	busquedaComp = session.query(Competidor).all()

		# 	'''Borra todos los Competidores'''
		# 	for comp in busquedaComp:
		# 		session.delete(comp)

		# 	'''Consulta todos los Carreras'''
		# 	busquedaCar = self.session.query(Carrera).all()

		# 	'''Borra todos los Competidores'''
		# 	for car in busquedaCar:
		# 		session.delete(car)	

		# 	session.commit()
		# 	session.close()   											 