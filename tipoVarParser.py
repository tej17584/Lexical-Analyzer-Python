"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: tipoVarParser.py
Propósito: Este programa tiene todos los posibles  tipos de objetos que tendra el PArser
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
    LENCERRADO_OR = 7
    RENCERRADO_OR = 8
    NOMBREPROD = 9
    LENCERRADO_WHILE = 10
    RENCERRADO_WHILE = 11
    LENCERRADO_CORCHETE = 12
    RENCERRADO_CORCHETE = 13


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
        self.parameters = ""
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

    def setOrdenToken(self, parametro):
        self.OrdenDeToken = parametro

    def getOrdenToken(self):
        return self.OrdenDeToken

    def setNombreNoTerminal(self, parametro):
        self.nombreNT = parametro

    def getIsFunction(self):
        return self.isFunction

    def setIsFunction(self):
        self.isFunction = True

    def getParameters(self):
        return self.parameters

    def setParameters(self, parametro):
        self.parameters = parametro

    def getPrimeraPos(self):
        return self.primeraPos

    def setAddPrimeraPos(self, parametro):
        self.primeraPos.append(parametro)

    def getParametroGeneral(self):
        """ if(self.accion == "" and self.nombreNT == "" and self.nombreT != ""):
            return self.nombreT
        elif(self.accion == "" and self.nombreNT != "" and self.nombreT == ""):
            return self.nombreNT
        elif (self.accion != "" and self.nombreNT == "" and self.nombreT == ""):
            return self.accion """

        return [self.tipoVariable.name, self.nombreT, self.nombreNT, self.accion, self.parameters, self.primeraPos, self.OrdenDeToken]
