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
        self.tipoToken = ""
        self.numeracion = ""
        self.valor = ""

    def getTipoToken(self):
        return self.tipoToken

    def setTipoToken(self, tipo):
        self.tipoToken = tipo

    def getNumeracion(self):
        return self.numeracion

    def setNumeracion(self, valor):
        self.numeracion = valor

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getAllValues(self):
        return [self.tipoToken, self.valor, self.numeracion]
