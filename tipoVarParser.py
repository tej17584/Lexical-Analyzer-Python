"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: tipoVarParser.py
Propósito: Este programa tiene todos los posibles 
"""
#! zona de imports

from enum import Enum
from funciones import funciones


class tipoVar(Enum):
    NOTERMINAL = 1
    APPEND = 2
    OR = 3
    KLEENE = 4
    ACTION = 5
    TERMINAL = 6


class variableProduction_Enum():
    def __init__(self, tipoVariable) -> None:
        """
        ESta funcion es el init
        *@param identificador: es el Enumerador
        *@param valor: es el valor que tendrá
        """
        self.tipoVariable = tipoVariable
        self.accion = ""
        self.nombreT = ""
        self.nombreNT = ""
        self.isFunction = False
        self.parameters = []
        self.primeraPos = []

    def getTipoVariable(self):
        return self.tipoVariable.name

    def getAccion(self):
        return self.accion

    def setAccion(self):
        return self.accion

    def getNombreTerminal(self):
        return self.nombreT

    def setNombreTerminal(self):
        return self.nombreNT

    def getNombreNoTerminal(self):
        return self.nombreNT

    def setNombreNoTerminal(self):
        return self.nombreT

    def getIsFunction(self):
        return self.isFunction

    def setIsFunction(self):
        return self.isFunction

    def getParameters(self):
        return self.parameters.pop()

    def setParameters(self, parametro):
        return self.parameters.append(parametro)

    def getPrimeraPos(self):
        return self.primeraPos

    def setAddPrimeraPos(self, parametro):
        return self.primeraPos.append(parametro)
