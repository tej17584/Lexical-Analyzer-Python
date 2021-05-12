"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: tipoVar.py
Propósito: Este programa tiene TODOS los posibles tipos de variable que pueden ser encontradas. Cada una 
V 1.0
"""
#! zona de imports

from enum import Enum
from funciones import funciones

# creamos una clase funciones
funcioncitas = funciones()
valorAny = funcioncitas.get_ANYSET()


class tipoVar(Enum):
    IDENT = 1
    STRING = 2
    NUMBER = 3
    CHAR = 4
    ANY = valorAny
    UNION = 5
    DIFFERENCE = 6
    RANGE = 7
    APPEND = '.'
    KLEENE = '*'
    OR = '|'
    LPARENTESIS = '('
    RPARENTESIS = ')'
    EXCEPT = 9
    KEYWORDS = 10
    EPSILON = 15
    ACEPTACION = ""


class variableER_Enum():
    def __init__(self, identificador, valor) -> None:
        """
        ESta funcion es el init
        *@param identificador: es el Enumerador
        *@param valor: es el valor que tendrá
        """
        self.identificador = identificador
        self.valorIdentificador = valor
        self.nombreIdentificador = ""

    def getIdenficador(self):
        return self.identificador.name

    def getValueIdentificador(self):
        return self.valorIdentificador

    def getValueFromIndentificadorENUM(self):
        return self.identificador.value

    def setNombreIdentificador(self, nombre):
        self.nombreIdentificador = nombre

    def getNombreIdentificador(self):
        return self.nombreIdentificador
