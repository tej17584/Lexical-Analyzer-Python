"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: scannerToken.py
Propósito: Esta clase es para guardar los valores de token
V 1.0
"""


class tokenForScanner:
    def __init__(self):
        self.tipo = ""
        self.numeracion = ""
        self.valor = ""

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getNumeracion(self):
        return self.numeracion

    def setNumeracion(self, valor):
        self.numeracion = valor

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getAllValues(self):
        return [self.tipo, self.numeracion, self.valor]
