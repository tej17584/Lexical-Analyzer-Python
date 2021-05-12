
# Nombre: Alejandro Tejada
# Curso: Diseño lenguajes de programacion
# Fecha: Abril 2021
# Programa: scannerProyecto2Tejada.py
# Propósito: Este programa tiene como fin leer el file de entrada
# V 1.0

# imports
import pickle
from pprint import pprint as pp


class Scanner():
    def __init__(self) -> None:
        self.diccionarioSiguientePos = {}
        self.AFDConstruidoFinal = []
        self.nodosAceptacion = {}
        self.stringPrueba = ""
        self.abrirFiles()
        self.abrirArchivoPrueba()
        self.simular()

    def abrirFiles(self):
        # abrimos todos los files y asignamos
        infile = open("dicionarioAFDFinal", 'rb')
        self.AFDConstruidoFinal = pickle.load(infile)
        infile.close()
        infile = open("diccionarioSiguientePos", 'rb')
        self.diccionarioSiguientePos = pickle.load(infile)
        infile.close()
        infile = open("diccionarioEstadosAceptacion", 'rb')
        self.nodosAceptacion = pickle.load(infile)
        infile.close()

    def abrirArchivoPrueba(self):
        with open('pruebas.txt', 'r') as f:
            self.stringPrueba = f.read()
        f.close()

    def getStateNumberForArray(self, array):
        for valor in self.AFDConstruidoFinal:
            if(valor[1] == array):
                return valor[0]

    def mover(self, estado, caracter):
        # Esta funcion retorna el siguiente estado
        arrayEvaluar = self.AFDConstruidoFinal
        arrayMover = []
        for estados in estado:
            for x in arrayEvaluar:
                variableIn = (ord(caracter)) in x[2]
                if(variableIn and len(x[3]) > 0 and estados == x[0]):
                    estadoSiguiente = self.getStateNumberForArray(x[3])
                    if(estadoSiguiente not in arrayMover):
                        arrayMover.append(estadoSiguiente)

        return arrayMover

    def getFinalStateAFN(self):
        arrayValores = []
        estadosFinales = self.getFinalStateNumber()
        for valor in self.AFDConstruidoFinal:
            for x in estadosFinales:
                if(str(x) in valor[1]):
                    arrayValores.append(valor[0])

        arrayValores = list(
            dict.fromkeys(arrayValores))
        return arrayValores

    def getFinalStateAFNV2(self):
        arrayValores = []
        estadosFinales = self.getFinalStateNumber()
        for valor in self.AFDConstruidoFinal:
            for x in estadosFinales:
                if(str(x) in valor[1]):
                    if(valor[1] not in arrayValores):
                        arrayValores.append(valor[1])

        return arrayValores

    def getFinalToken(self, tokenArray):
        arrayValores = []
        valorRetornar = ""
        estadosFinales = self.getFinalStateNumber()
        for valor in self.AFDConstruidoFinal:
            for x in estadosFinales:
                if(str(x) in valor[1]):
                    for w in tokenArray:
                        if(w == valor[0]):
                            if(valor[1] not in arrayValores):
                                arrayValores.append(valor[1])

        dictAceptacion = {}
        arrayNumeros = []
        # ahora, miramos cual token es
        for z in arrayValores:
            for estadoPosibles in z:
                for llave, valor in self.nodosAceptacion.items():
                    if(int(estadoPosibles) == llave):
                        dictAceptacion[llave] = valor
                        arrayNumeros.append(llave)

        if(len(dictAceptacion) > 1):
            valorMinimo = min(arrayNumeros)
            for llave, valor in dictAceptacion.items():
                if(valorMinimo == llave):
                    valorRetornar = valor
        else:
            for llave, valor in dictAceptacion.items():
                valorRetornar = valor

        return valorRetornar

    def getFinalStateNumber(self):
        array = []
        for numero, valor in self.diccionarioSiguientePos.items():
            if len(valor) == 0:
                array.append(numero)

        return array

    def simular(self):
        # este método simula
        print("------------------SIMULACION TOKENS INICIADA-------------------")
        S = [0]
        S2 = [0]
        acumulador = ""
        SAcumulado = []
        EstadoACeptacion = []
        for w in self.stringPrueba:
            SAcumulado.append(w)

        SAcumulado.append(" ")
        contador = 0
        while len(SAcumulado) > 0:
            if(contador == len(self.stringPrueba)-1):
                caracterValuar = self.stringPrueba[contador]
                acumulador += caracterValuar
                S = self.mover(S, caracterValuar)
                token = self.getFinalToken(S)
                if(len(token) == 0):
                    print("TOKEN INVALIDO del valor  ", acumulador)
                    break
                else:
                    pp("El token del valor ----> " +
                       acumulador + " <--- es: " + token)
                    break
            caracterValuar = self.stringPrueba[contador]
            caracterValuar2 = self.stringPrueba[contador+1]
            acumulador += caracterValuar
            S = self.mover(S, caracterValuar)
            S2 = self.mover(S, caracterValuar2)

            if(len(S2) == 0 and len(S) > 0):
                token = self.getFinalToken(S)
                if(len(token) == 0):
                    print("TOKEN INVALIDO del valor: ")
                    print(acumulador)
                    S = [0]
                    S2 = [0]
                    acumulador = ""
                    contador -= 1
                else:
                    pp("El token del valor ----> " +
                       acumulador + " <---- es: " + token)
                    S = [0]
                    S2 = [0]
                    acumulador = ""
                    # contador += 1
            elif(len(S) == 0):
                print("TOKEN INVALIDO del valor: ")
                print(acumulador)
                S = [0]
                S2 = [0]
                acumulador = ""

            contador += 1
            popCharacter = SAcumulado.pop()

        print("---------------------------------------------------------------")
        print("")


objeSCanner = Scanner()
