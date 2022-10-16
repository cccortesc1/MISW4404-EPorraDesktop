from pickle import TRUE

from unittest import result
from sqlalchemy import false, inspect, true
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.apuesta import Apuesta
from src.modelo.apostador import Apostador
from src.modelo.declarative_base import engine, Base, session
'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
class Logica():

    def __init__(self):
        Base.metadata.create_all(engine)
        
        #Este constructor contiene los datos falsos para probar la interfaz
        self.carreras = []
        # self.carreras = [{'Nombre':'Carrera 1', 'Competidores':[{'Nombre':'Juan Pablo Montoya', 'Probabilidad':0.15},\
        #                                                          {'Nombre':'Kimi Räikkönen', 'Probabilidad':0.2},\
        #                                                           {'Nombre':'Michael Schumacher', 'Probabilidad':0.65}],\
        #                                             'Abierta':True},
        #                   {'Nombre':'Carrera 2', 'Competidores':[{'Nombre':'Usain Bolt', 'Probabilidad':0.72},\
        #                                                          {'Nombre':'Lamont Marcell Jacobs', 'Probabilidad':0.13},\
        #                                                           {'Nombre':'Su Bingtian', 'Probabilidad':0.05},\
        #                                                           {'Nombre':'Robson da Silva', 'Probabilidad':0.1}],\
        #                                             'Abierta':True}]      
        #self.apostadores = [{'Nombre':'Pepe Pérez'},{'Nombre':"Ana Andrade"},{'Nombre':"Aymara Castillo"}]
        self.apostadores = []
        self.apuestas = []
        # self.apuestas = [{'Apostador':'Pepe Pérez', 'Carrera':'Carrera 1', 'Valor':10, 'Competidor':'Juan Pablo Montoya'},\
        #                 {'Apostador':'Ana Andrade', 'Carrera':'Carrera 1', 'Valor':25, 'Competidor':'Michael Schumacher'},\
        #                 {'Apostador':'Aymara Castillo', 'Carrera':'Carrera 1', 'Valor':14, 'Competidor':'Juan Pablo Montoya'},\
        #                 {'Apostador':'Aymara Castillo', 'Carrera':'Carrera 2', 'Valor':45, 'Competidor':'Usain Bolt'}]
        self.ganancias = []
        #self.ganancias = [{'Carrera':'Carrera 1', 'Ganancias':[('Pepe Pérez',13),('Ana Andrade',0), ('Aymara Castillo',15)], 'Ganancias de la casa': 4},\
        #    {'Carrera':'Carrera 2', 'Ganancias':[('Pepe Pérez',32),('Ana Andrade',12), ('Aymara Castillo',34)], 'Ganancias de la casa': -10}]

    def dar_carreras(self):
        carreras = session.query(Carrera).order_by(Carrera.nombre.asc()).all()
        self.carreras = []
        i = 0
        for carrera in carreras:
            Competidores = session.query(Competidor).filter(Competidor.carreraId == carrera.id).all()
            self.carreras.append({'Id':carrera.id, 'Nombre':carrera.nombre, 'Competidores':[], 'Abierta':carrera.abierta,'Ganador':-1}) 

            for comp in Competidores:
                self.carreras[i]["Competidores"].append({'Id': comp.id, 'Nombre':comp.nombre, 'Probabilidad':comp.probabilidad, 'idCarrera': comp.carreraId})
            i += 1    
        return self.carreras.copy()

    def dar_carrera(self, id_carrera):
        self.carreras = self.dar_carreras()
        return self.carreras[id_carrera].copy()
      
    def crear_carrera(self, nombre, competidores):
        xNombre = nombre.strip()
        resultado = False
        self.carreras.append({'Nombre':xNombre, 'Competidores':[], 'Abierta':True})
        if(len(xNombre) > 0):
            resultado = self.crear_carrera_bd(competidores, xNombre)
        return resultado 

    def crear_carrera_bd(self, competidores, xNombre):
        resultado = False
        if(self.validarCantidadCompetidores(competidores) and self.validarSumaProbabilidades(competidores) and self.validarExistenciaCarreraPorNombre(xNombre)):
            vCarrera = Carrera(nombre=xNombre, abierta=True)
            session.add(vCarrera)
            session.commit()
            resultado = True
        return resultado       

    def validarSumaProbabilidades(self, competidores):
        resultado = False
        if(len(competidores) > 1):
            SumProb = 0.0
            for comp in competidores:
                SumProb +=comp["Probabilidad"]
            valorSum = round(SumProb, 1)     
            if (valorSum==1):
                resultado = True
        return resultado

    def validarExistenciaCarreraPorNombre(self, nombreNuevo):
        resultado = True
        Carreras = session.query(Carrera).filter_by(nombre = nombreNuevo).all()
        if(len(Carreras) > 0):
            resultado = False
        return resultado    

    def validarCantidadCompetidores(self, competidores):
        resultado = False
        if(len(competidores) >= 2):
            resultado = True
        return resultado    

    def editar_carrera(self, id, nombre, competidores):
        resultado=False
        if(self.validarSumaProbabilidades(competidores)):
            self.carreras[id]['Nombre'] = nombre
            idCarrera = int(self.carreras[id]['Id'])
            resultado = self.editar_carrera_bd(nombre, idCarrera)
        return resultado 

    def editar_carrera_bd(self, nombre, idCarrera):
        CarreraActual = session.query(Carrera).filter_by(id = idCarrera).one()
        CarreraActual.nombre = nombre
        session.add(CarreraActual)
        session.commit()
        resultado=True
        return resultado   

    def terminar_carrera(self, id, ganador):
        resultado = False
        if(self.val_cantidad_apuestas_carrera(id)):
            self.carreras[id]['Ganador'] = ganador
            self.carreras[id]['Competidores'][ganador]['esGanador']=True
            idCarrera=int(self.carreras[id]['Id'])
            idCompetidor = int(self.carreras[id]['Competidores'][ganador]['Id'])
            probabilidad = float(self.carreras[id]['Competidores'][ganador]['Probabilidad'])
            terminCarrera = self.terminar_carrera_bd(idCarrera, idCompetidor)            
            if(terminCarrera):
                self.calcularGanancias_bd(idCarrera,idCompetidor,probabilidad)
                resultado = True
        return resultado

    def val_cantidad_apuestas_carrera(self, id_carrera):
        resultado = False
        apuestas = self.dar_apuestas_carrera(id_carrera)
        if(len(apuestas)>0):
            resultado = True
        return resultado

    def terminar_carrera_bd(self,idCarrera, ganador):
        resultado = False
        CompetidorActual = session.query(Competidor).filter_by(id = ganador).one()
        CompetidorActual.esGanador = True
        CarreraActual = session.query(Carrera).filter_by(id = idCarrera).one()
        CarreraActual.abierta = False
        session.add(CompetidorActual)
        session.add(CarreraActual)
        session.commit()
        resultado = True
        return resultado

    def calcularGanancias_bd(self, idCarrera, idCompetidor,probabilidad):
        cuota = probabilidad/(1-probabilidad)
        ganancia = 0
        vApuestas = session.query(Apuesta).filter(Apuesta.competidorId == idCompetidor and Apuesta.carreraId == idCarrera).all()
        
        for apuest in vApuestas:
            ganancia = apuest.valor + (apuest.valor/cuota)
            apuest.ganancia = ganancia
            apuest.cuota = cuota
            session.add(apuest)
            session.commit()
            
    def eliminar_carrera(self, id):
        resultado = False
        apuestas = self.dar_apuestas_carrera(id)
        if(len(apuestas) == 0):
            id_carrera_bd = self.carreras[id]['Id']        
            indiceCompetidor = 0
            for comp in self.carreras[id]["Competidores"]:
                self.eliminar_competidor(id, indiceCompetidor)
                indiceCompetidor += 1
            self.eliminar_carrera_bd(id_carrera_bd)
            del self.carreras[id]
            resultado = True
        return resultado    
    
    def eliminar_carrera_bd(self, idCarrera):
        resultado = False
        CarreraActual = session.query(Carrera).filter_by(id = idCarrera).one()
        session.delete(CarreraActual)
        session.commit()
        resultado = True
        return resultado       

    def dar_apostadores(self):
        vApostadores = session.query(Apostador).order_by(Apostador.nombre.asc()).all()
        self.apostadores = []
        for apost in vApostadores:
            self.apostadores.append({'Id': apost.id,'Nombre': apost.nombre})
        return self.apostadores.copy()

    def dar_nombre_apostadores(self, idApostador):
        vApostador = session.query(Apostador).filter_by(id = idApostador).one()
        nombreApostador = vApostador.nombre
        return nombreApostador    

    def dar_nombre_competidor(self, idCompetidor):
        vCompetidor = session.query(Competidor).filter_by(id = idCompetidor).one()
        nombreCompetidor = vCompetidor.nombre
        return nombreCompetidor        

    def aniadir_apostador(self, nombre):
        resultado = False
        self.apostadores.append({'Nombre': nombre})
        if(len(nombre) > 0):
            resultado = self.aniadir_apostador_bd(nombre)
        return resultado 

    def aniadir_apostador_bd(self, xNombre):
        resultado = False
        apostador1 = Apostador(nombre=xNombre)
        session.add(apostador1)
        session.commit();
        resultado = True
        return resultado   
    
    def editar_apostador(self, id, nombre):
        resultado = False        
        self.apostadores[id]['Nombre'] = nombre
        idApostador = self.apostadores[id]['Id']
        resultado = self.editar_apostador_bd(idApostador, nombre)
        return resultado
    
    def editar_apostador_bd(self, idApostador, xNombre):
        resultado = False
        vApostadorActual = session.query(Apostador).filter_by(id = idApostador).one()
        vApostadorActual.nombre = xNombre
        session.add(vApostadorActual)
        session.commit()
        resultado = True
        return resultado

    def eliminar_apostador(self, id):        
        resultado = self.eliminar_apostador_bd(id)
        del self.apostadores[id]
        return resultado

    def eliminar_apostador_bd(self, id):
        resultado = False
        idApostador = self.apostadores[id]['Id']
        ApostadorActual = session.query(Apostador).filter_by(id = idApostador).one()
        session.delete(ApostadorActual)
        session.commit()
        resultado = True
        return resultado

    def dar_competidores_carrera(self, id):
        return self.carreras[id]['Competidores'].copy()

    def dar_competidor(self, id_carrera, id_competidor):
        if(len(self.carreras[id_carrera]['Competidores']) < id_competidor):
            return []
        return self.carreras[id_carrera]['Competidores'][id_competidor].copy()

    def aniadir_competidor(self, id, nombre, probabilidad):
        resultado = False
        self.carreras[id]['Competidores'].append({'Nombre':nombre, 'Probabilidad':probabilidad})
        idCarrera = int(self.carreras[id]["Id"])
        resultado = self.aniadir_competidor_bd(nombre, probabilidad, idCarrera)
        return resultado

    def aniadir_competidor_bd(self, nombre, probabilidad, idCarrera):
        resultado = False
        vCompetidor = Competidor(nombre=nombre, probabilidad=probabilidad, carreraId = idCarrera)
        session.add(vCompetidor)
        session.commit()
        resultado = True
        return resultado

    def editar_competidor(self, id_carrera, id_competidor, nombre, probabilidad):
        resultado = False        
        self.carreras[id_carrera]['Competidores'][id_competidor]['Nombre']=nombre
        self.carreras[id_carrera]['Competidores'][id_competidor]['Probabilidad']=probabilidad
        idCompetidor = int(self.carreras[id_carrera]['Competidores'][id_competidor]['Id'])
        resultado = self.editar_competidor_bd(nombre, probabilidad, idCompetidor)
        return resultado

    def editar_competidor_bd(self, nombre, probabilidad, idCompetidor):
        resultado = False
        CompetidorActual = session.query(Competidor).filter_by(id = idCompetidor).one()
        CompetidorActual.nombre = nombre
        CompetidorActual.probabilidad = probabilidad
        session.add(CompetidorActual)
        session.commit()
        resultado = True
        return resultado
    
    def eliminar_competidor(self, id_carrera, id_competidor):
        idCompetidor = int(self.carreras[id_carrera]['Competidores'][id_competidor]['Id'])
        del self.carreras[id_carrera]['Competidores'][id_competidor]
        resultado = self.eliminar_competidor_bd(idCompetidor)
        return True

    def eliminar_competidor_bd(self, idCompetidor):
        resultado = False
        CompetidorActual = session.query(Competidor).filter_by(id = idCompetidor).one()
        session.delete(CompetidorActual)
        session.commit()
        resultado = True
        return resultado

    def dar_apuestas_carrera(self, id_carrera):
        nombre_carrera =self.carreras[id_carrera]['Nombre']
        self.apuestas = []
        idCarrera = self.carreras[id_carrera]['Id']
        Apuestas = session.query(Apuesta).filter(Apuesta.carreraId == idCarrera).all()
        
        for apues in Apuestas:
            nombreApostador = self.dar_nombre_apostadores(apues.apostadorId)
            nombreCompetidor = self.dar_nombre_competidor(apues.competidorId)
            n_apuesta = {}
            n_apuesta['Id'] = apues.id
            n_apuesta['Apostador'] = nombreApostador
            n_apuesta['Carrera'] = self.carreras[id_carrera]['Nombre']
            n_apuesta['CarreraId'] = str(idCarrera)
            n_apuesta['Valor'] = apues.valor
            n_apuesta['Competidor'] = nombreCompetidor
            n_apuesta['CompetidorId'] = apues.competidorId
            n_apuesta['Ganancia'] = apues.ganancia
            self.apuestas.append(n_apuesta)

        return list(filter(lambda x: x['Carrera']==nombre_carrera, self.apuestas))

    def dar_apuesta(self, id_carrera, id_apuesta):
        return self.dar_apuestas_carrera(id_carrera)[id_apuesta].copy()

    def crear_apuesta(self, apostador, id_carrera, valor, competidor):
        resultado = False
        try:

            idCompetidor = self.obtener_indice_competidor(id_carrera, competidor)        
            idAposador = self.obtener_id_apostador(apostador)
            if(len(self.carreras) > 0 and self.validar_competidor(id_carrera, idCompetidor) and self.validar_apostador(idAposador)):
                n_apuesta = {}
                n_apuesta['Apostador'] = Apostador
                n_apuesta['Carrera'] = self.carreras[id_carrera]['Nombre']
                n_apuesta['CarreraId'] = id_carrera
                n_apuesta['Valor'] = valor
                n_apuesta['IdCompetidor'] = idCompetidor
                n_apuesta['Competidor'] = Competidor
                self.apuestas.append(n_apuesta)
                carreraActual = self.dar_carrera(id_carrera)
                resultado = self.crear_apuesta_bd(valor, idCompetidor, idAposador, carreraActual)
        except:
            resultado = False        
        return resultado 

    def crear_apuesta_bd(self, valor, idCompetidor, idAposador, carreraActual):
        idCarreraBD = carreraActual["Id"]
        idCompetidor = carreraActual["Competidores"][idCompetidor]["Id"]
        vApuesta = Apuesta(valor = valor, cuota = 0, ganancia = 0, carreraId = idCarreraBD, apostadorId = idAposador, competidorId = idCompetidor)
        session.add(vApuesta)
        session.commit()
        resultado = True
        return resultado           

    def obtener_indice_competidor(self, id_carrera, nombre_competidor):
        i=0
        indice = -1
        if(len(self.carreras) > 0):
            for comp in self.carreras[id_carrera]["Competidores"]:
                if(comp["Nombre"] == nombre_competidor):
                    indice = i
                i+=1
        return indice

    def obtener_id_competidor(self, id_carrera, nombre_competidor):
        indice = -1
        if(len(self.carreras) > 0):
            for comp in self.carreras[id_carrera]["Competidores"]:
                if(comp["Nombre"] == nombre_competidor):
                    indice = comp["Id"]
        return indice

    def obtener_indice_apostador(self, nombre_apostador):
        i=0
        for apost in self.apostadores:
            if(apost["Nombre"] == nombre_apostador):
                i+=1
        return i    

    def obtener_id_apostador(self, nombre_apostador):
        i=0
        indice = 0
        for apost in self.apostadores:
            if(apost["Nombre"] == nombre_apostador):
                indice = apost["Id"]
                i+=1
        return indice    
    
    def obtener_id_carrera(self, nombre_carrera):
        i=0
        indice=0
        for carrera in self.carreras:
            if(carrera["Nombre"] == nombre_carrera):
                indice = i
                i+=1
        return indice    

    def validar_competidor(self, id_carrera, id_competidor):
        resultado = False
        vCompetidor = self.dar_competidor(id_carrera, id_competidor)
        if(len(vCompetidor) > 0):
            resultado = True
        return resultado

    def validar_apostador(self, id_apostador):
        resultado = False
        try:
            vApostador = session.query(Apostador).filter_by(id = id_apostador).all()  
            if(len(vApostador) > 0):
                resultado = True
        except ValueError:
            resultado = false

        return resultado      

    def editar_apuesta(self, id_apuesta, apostador, carrera, valor, competidor):
        self.apuestas[id_apuesta]['Apostador'] = apostador
        self.apuestas[id_apuesta]['Carrera'] = carrera
        self.apuestas[id_apuesta]['Valor'] = valor
        self.apuestas[id_apuesta]['Competidor'] = competidor
        
        id_carrera = self.obtener_id_carrera(carrera)
        idCompetidor = self.obtener_id_competidor(id_carrera, competidor)
        idAposador = self.obtener_id_apostador(apostador)        
        IdApuesta =self.apuestas[id_apuesta]['Id']
        ApuestaActual = session.query(Apuesta).filter_by(id = IdApuesta).one()
        ApuestaActual.valor =  valor
        ApuestaActual.apostadorId = idAposador 
        ApuestaActual.competidorId = idCompetidor
        session.add(ApuestaActual)
        session.commit();

    def eliminar_apuesta(self, id_carrera, id_apuesta):        
        nombre_carrera =self.carreras[id_carrera]['Nombre']
        IdApuesta =self.apuestas[id_apuesta]['Id']
        i = 0
        id = 0
        while i < len(self.apuestas):
            if self.apuestas[i]['Carrera'] == nombre_carrera:
                if id == id_apuesta:
                    self.apuestas.pop(i)
                    return self.eliminar_puesta_bd(IdApuesta)    
                else:
                    id+=1
            i+=1

        del self.apuesta[id_apuesta]
        
        return False

    def eliminar_puesta_bd(self, IdApuesta):
        resultado = False
        ApuestaActual = session.query(Apuesta).filter_by(id = IdApuesta).one()
        session.delete(ApuestaActual)
        session.commit()
        resultado = True
        return resultado

    def dar_reporte_ganancias(self, id_carrera, id_competidor):
        resultado = False
        if(self.carreras[id_carrera]['Abierta'] == True):
            terminaCarrera = self.terminar_carrera(id_carrera, id_competidor)
            if(terminaCarrera):
                self.carreras[id_carrera]['Abierta']=False
                n_carrera = self.carreras[id_carrera]['Nombre']
                self.dar_ganancias_bd(id_carrera, id_competidor, n_carrera)
                for ganancias in self.ganancias:
                    if ganancias['Carrera'] == n_carrera:
                        return ganancias['Ganancias'], ganancias['Ganancias de la casa']    
                resultado = True
        return [], 0

    def dar_ganancias_bd(self, idCarrera, idCompetidor, nom_carrera):
        self.ganancias = []
        totalApuestas = 0
        totalGanancias = 0
        gananciasCasa = 0
        self.ganancias.append({'Carrera': nom_carrera, 'Ganancias':[], 'Ganancias de la casa': 0})
        id_competidor_bd = self.carreras[idCarrera]['Competidores'][idCompetidor]['Id']
        apuestas = self.dar_apuestas_carrera(idCarrera)    
        for apuest in apuestas:
            totalApuestas += apuest['Valor']
            if(apuest['CompetidorId'] == id_competidor_bd):
                t = (apuest["Apostador"], apuest["Ganancia"])
                self.ganancias[0]["Ganancias"].append(t)
                totalGanancias += apuest['Ganancia']
        gananciasCasa = totalApuestas - totalGanancias
        self.ganancias[0]['Ganancias de la casa'] = gananciasCasa

        
                



