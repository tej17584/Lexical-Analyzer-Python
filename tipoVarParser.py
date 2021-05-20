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


class tipoVar2(Enum):
    NOTERMINAL = 1
    APPEND = 2
    OR = 3
    KLEENE = 4
    ACTION = 5
    TERMINAL = 6
    LENCERRADO = 7
    RENCERRADO = 8


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
        self.OrdenDeToken = ""
        self.parameters = []
        self.primeraPos = []

    def getTipoVariable(self):
        return self.tipoVariable.name

    def getAccion(self):
        return self.accion

    def setAccion(self, parametro):
        self.accion = parametro

    def getNombreTerminal(self):
        return self.nombreT

    def setNombreTerminal(self, parametro):
        self.nombreT = parametro

    def getNombreNoTerminal(self):
        return self.nombreNT

    def setNombreNoTerminal(self, parametro):
        self.nombreNT = parametro

    def getIsFunction(self):
        return self.isFunction

    def setIsFunction(self, parametro):
        self.isFunction = parametro

    def getParameters(self):
        return self.parameters.pop()

    def setParameters(self, parametro):
        self.parameters.append(parametro)

    def getPrimeraPos(self):
        return self.primeraPos

    def setAddPrimeraPos(self, parametro):
        self.primeraPos.append(parametro)
