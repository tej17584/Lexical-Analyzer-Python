"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Febrero 2021
Programa: nodoDirecto.py
Propósito: Este programa contiene el valor que guardará cada nodo, en especial, los siugientes
--Anulable //Bool 
--PrimeraPost //array
--UltimaPos //array
"""


class NodoDirecto:

    def __init__(self) -> None:
        self.nodoID = ""  # es el id del nodo. Si no es vacío sino letra le asignamos un valor
        self.anulable = True  # Ver si es anulable o no el nodo. ES anulable si el lenguaje produce la cadena vacía. Por lo genera es * y e
        # conjunto de numeros de las primeras posiciones. Las reglas se definen en la tabla
        self.primeraPos = []
        self.ultimaPos = []  # conjunto de números de las ultimas posiciones. Las reglas se definen en la tabla. La diferencia es que este es HIJO DERECHO
        self.caracter = ""  # El caracter de este nodo
        self.siguientePos = ""

    def getNodoId(self):
        return self.nodoID

    def getAnulable(self):
        return self.anulable

    def getPrimeraPos(self):
        return self.primeraPos

    def getUltimaPos(self):
        return self.ultimaPos

    def getCaracterNodo(self):
        return self.caracter

    def setCaracterNodo(self, caracter):
        self.caracter = caracter

    def setNodoId(self, nodoID):
        self.nodoID = nodoID

    def setAnulable(self, anulable):
        self.anulable = anulable

    def setPrimeraPos(self, primeraPos):
        self.primeraPos = primeraPos

    def setUltimaPos(self, ultimaPos):
        self.ultimaPos = ultimaPos

    def getSiguientePos(self):
        return self.siguientePos

    def setSiguientePos(self, siguientePos):
        self.siguientePos = siguientePos

    def getAllNodoValues(self):
        return [self.nodoID, self.anulable, self.primeraPos, self.ultimaPos]
