"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Febrero 2021
Programa: AFNDIRECTO.py
Propósito: Este programa calcula un AFN de forma directa
"""

# zona de imports de librerías
from os import terminal_size
from funciones import *
from nodoDirecto import *
from graphviz import Digraph
from pprint import pprint as pp
import time


class AFNDIRECTO:

    def __init__(self, expresionRegular, lenguaje, cadena) -> None:
        self.expresionPostfix = expresionRegular
        self.arrayNodos = []
        self.AFDDirectoFinal = {}
        self.contadorGlobal = 1
        self.contadorGlobalV2 = 0
        self.diccionarioSiguientePos = {}
        self.funciones = funciones()
        self.Destados = []
        self.DestadosV2 = []
        self.lenguaje = lenguaje
        self.AFDConstruidoFinal = []
        self.nodosAceptacion = {}
        # variables para el AFN
        self.AFDGraph = Digraph('finite_state_machine',
                                comment="Diagrama AFN", format="png")
        self.AFDGraph.attr(rankdir='LR', size='30')
        # la shape determinada es el de circle, cuando hallemos estado final usaremos double
        self.AFDGraph.attr('node', shape='circle')
        self.cadenaEvaluarAFD = cadena

    def getAFDDirecto(self):
        """
        REtorna el AFD final
        """
        return self.AFDConstruidoFinal

    def getNodosAceptacion(self):
        """
        REtorna los nodos de aceptacion, el dict
        """
        return self.nodosAceptacion

    def getdiccionarioSiguientePos(self):
        """
        Retorna el diccionario de la siguiente pos
        """
        return self.diccionarioSiguientePos

    def isAnulable(self, Nodos, caracter):
        if(caracter.getIdenficador() == "EPSILON"):
            return True
        else:
            if(self.funciones.isOperandPosftixTokenFinal(caracter)):
                return False
            elif (caracter.getIdenficador() == "OR"):
                nodoC1 = Nodos.pop()
                nodoC2 = Nodos.pop()
                anulableC1 = nodoC1.getAnulable()
                anulableC2 = nodoC2.getAnulable()

                return (anulableC1 or anulableC2)
            elif(caracter.getIdenficador() == "APPEND"):
                nodoC1 = Nodos.pop()
                nodoC2 = Nodos.pop()
                anulableC1 = nodoC1.getAnulable()
                anulableC2 = nodoC2.getAnulable()

                return (anulableC1 and anulableC2)
            elif(caracter.getIdenficador() == "KLEENE"):
                nodoC1 = Nodos.pop()
                anulableC1 = nodoC1.getAnulable()

                return (True)

        return "FALSO"

    def primeraPos(self, Nodos, caracter):
        if(caracter.getIdenficador() == "EPSILON"):
            return ""
        else:
            # si es un caracter, retornamos el mismo id, esa es su primera pos
            if(self.funciones.isOperandPosftixTokenFinal(caracter)):
                nodoC1 = Nodos.pop()
                nodoC1Id = nodoC1.getNodoId()
                return [nodoC1Id]
            elif (caracter.getIdenficador() == "OR"):
                nodoC1 = Nodos.pop()
                nodoC2 = Nodos.pop()
                primeraPosC1 = nodoC1.getPrimeraPos()
                primeraPosC2 = nodoC2.getPrimeraPos()
                if(primeraPosC1 == ""):
                    primeraPosC1 = []

                if(primeraPosC2 == ""):
                    primeraPosC2 = []
                arrayFinalOr = primeraPosC1+primeraPosC2
                arrayFinalOr = list(
                    dict.fromkeys(arrayFinalOr))
                arrayFinalOr.sort()

                return arrayFinalOr
            elif(caracter.getIdenficador() == "APPEND"):
                nodoC1 = Nodos.pop()
                nodoC2 = Nodos.pop()
                anulableC1 = nodoC1.getAnulable()
                primeraPosC1 = nodoC1.getPrimeraPos()
                primeraPosC2 = nodoC2.getPrimeraPos()
                if(primeraPosC1 == ""):
                    primeraPosC1 = []
                if(primeraPosC2 == ""):
                    primeraPosC2 = []
                if(anulableC1):
                    arrayFinalAND = primeraPosC1+primeraPosC2
                else:
                    arrayFinalAND = primeraPosC1

                arrayFinalAND = list(
                    dict.fromkeys(arrayFinalAND))
                arrayFinalAND.sort()

                return arrayFinalAND
            elif(caracter.getIdenficador() == "KLEENE"):
                nodoC1 = Nodos.pop()
                primeraPosC1 = nodoC1.getPrimeraPos()
                if(primeraPosC1 == ""):
                    primeraPosC1 = []
                arrayFinalKleene = primeraPosC1
                arrayFinalKleene = list(
                    dict.fromkeys(arrayFinalKleene))
                arrayFinalKleene.sort()

                return arrayFinalKleene
        return "FALSO"

    def ultimaPos(self, Nodos, caracter):
        if(caracter.getIdenficador() == "EPSILON"):
            return ""
        else:
            # si es un caracter, retornamos el mismo id, esa es su primera pos
            if(self.funciones.isOperandPosftixTokenFinal(caracter)):
                nodoC1 = Nodos.pop()
                nodoC1Id = nodoC1.getNodoId()
                return [nodoC1Id]
            elif (caracter.getIdenficador() == "OR"):
                nodoC1 = Nodos.pop()
                nodoC2 = Nodos.pop()
                ultimaPosC1 = nodoC1.getUltimaPos()
                ultimaPosC2 = nodoC2.getUltimaPos()
                if(ultimaPosC1 == ""):
                    ultimaPosC1 = []

                if(ultimaPosC2 == ""):
                    ultimaPosC2 = []
                arrayFinalOr = ultimaPosC1+ultimaPosC2
                arrayFinalOr = list(
                    dict.fromkeys(arrayFinalOr))
                arrayFinalOr.sort()

                return arrayFinalOr
            elif(caracter.getIdenficador() == "APPEND"):
                nodoC1 = Nodos.pop()
                nodoC2 = Nodos.pop()
                anulableC2 = nodoC2.getAnulable()
                ultimaPosC1 = nodoC1.getUltimaPos()
                ultimaPosC2 = nodoC2.getUltimaPos()
                if(ultimaPosC1 == ""):
                    ultimaPosC1 = []

                if(ultimaPosC2 == ""):
                    ultimaPosC2 = []
                if(anulableC2):
                    arrayFinalAND = ultimaPosC1+ultimaPosC2
                else:
                    arrayFinalAND = ultimaPosC2

                arrayFinalAND = list(
                    dict.fromkeys(arrayFinalAND))
                arrayFinalAND.sort()

                return arrayFinalAND
            elif(caracter.getIdenficador() == "KLEENE"):
                nodoC1 = Nodos.pop()
                ultimaPosC1 = nodoC1.getUltimaPos()
                if(ultimaPosC1 == ""):
                    ultimaPosC1 = []
                arrayFinalKleene = ultimaPosC1
                arrayFinalKleene = list(
                    dict.fromkeys(arrayFinalKleene))
                arrayFinalKleene.sort()

                return arrayFinalKleene
        return "FALSO"

    def siguientePos(self, Nodos, caracter):
        # si es un caracter, retornamos el mismo id, esa es su primera pos
        if(caracter.getIdenficador() == "APPEND"):
            nodoC1 = Nodos.pop()
            nodoC2 = Nodos.pop()

            ultimaPosC1 = nodoC1.getUltimaPos()
            primeraPosC2 = nodoC2.getPrimeraPos()
            if(primeraPosC2 == ""):
                primeraPosC2 = []
            if(ultimaPosC1 == ""):
                ultimaPosC1 = []
            arrayTemporal = []
            for x in ultimaPosC1:
                arrayTemporal = self.diccionarioSiguientePos[int(x)]
                arrayTemporal = arrayTemporal+primeraPosC2
                arrayTemporal = list(
                    dict.fromkeys(arrayTemporal))
                arrayTemporal.sort()
                self.diccionarioSiguientePos[int(x)] = arrayTemporal
        if(caracter.getIdenficador() == "KLEENE"):
            nodoC1 = Nodos.pop()
            ultimaPosC1 = nodoC1.getUltimaPos()
            primeraPosC1 = nodoC1.getPrimeraPos()
            if(ultimaPosC1 == ""):
                ultimaPosC1 = []

            if(primeraPosC1 == ""):
                primeraPosC1 = []
            for x in ultimaPosC1:
                arrayTemporal = self.diccionarioSiguientePos[int(x)]
                arrayTemporal = arrayTemporal+primeraPosC1
                arrayTemporal = list(
                    dict.fromkeys(arrayTemporal))
                arrayTemporal.sort()
                self.diccionarioSiguientePos[int(x)] = arrayTemporal

    def getPosFromLetter(self, caracter):
        """
        Dada una letra, nos retorna el valor de id de esa letra. Puede haber varias
        """
        array = []
        for numero, nodo in self.AFDDirectoFinal.items():
            if(nodo.getCaracterNodo() == caracter.getNombreIdentificador()):
                array.append(nodo.getNodoId())

        return array

    def getFinalStateNumber(self):
        array = []
        for numero, valor in self.diccionarioSiguientePos.items():
            if len(valor) == 0:
                array.append(numero)

        return array

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

    def getStateNumberForArray(self, array):
        for valor in self.AFDConstruidoFinal:
            if(valor[1] == array):
                return valor[0]

    def graficarAFD(self):
        arrayGraficar = self.AFDConstruidoFinal
        idfinal = self.getFinalStateAFN()
        # agregamos el nodo final
        self.AFDGraph.attr('node', shape='doublecircle')
        for x in idfinal:
            self.AFDGraph.node(str(x))
        self.AFDGraph.attr('node', shape='circle')
        for x in arrayGraficar:
            if(len(x[1]) > 0 and len(x[3]) > 0):
                estado1 = self.getStateNumberForArray(x[1])
                esatdo2 = self.getStateNumberForArray(x[3])
                self.AFDGraph.edge(str(estado1), str(
                    esatdo2), self.funciones.fromSetNumbersToSTring(x[2]))
                # esatdo2), (x[2]))
        self.AFDGraph.render('Automatas/AFDDirecto', view=True)

    def mover(self, estado, caracter):
        """
        Esta funcion retorna el siguiente estado
        """
        arrayEvaluar = self.AFDConstruidoFinal
        arrayMover = []
        for estados in estado:
            for x in arrayEvaluar:
                if(x[2] == caracter and len(x[3]) > 0 and estados == x[0]):
                    estadoSiguiente = self.getStateNumberForArray(x[3])
                    if(estadoSiguiente not in arrayMover):
                        arrayMover.append(estadoSiguiente)

        return arrayMover

    def moverV2(self, estado, caracter):
        """
        Esta funcion retorna el siguiente estado
        """
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

    def simularAFD(self):
        start_time = time.perf_counter()
        s = [0]
        for x in self.cadenaEvaluarAFD:
            s = self.moverV2(s, x)
        end_time = time.perf_counter()
        idfinal = self.getFinalStateAFN()
        idEstadosFinalesAceptacion = self.getFinalStateAFNV2()
        print("EStado donde no se pudo mover", s)
        print("Id final", idfinal)
        print("Acá debería haber uno de aceptacion", idEstadosFinalesAceptacion)
        if(len(s) > 0):
            if(s[0] in idfinal):
                print("------------------SIMULACION AFD DIRECTO-------------------")
                print("Sí, la expresion ######## -->", self.cadenaEvaluarAFD,
                      "<---######### es aceptada por el AFD DIRECTO")

                print("--- %s segundos ---" % (end_time - start_time))
                print("--------------------------------------------------")
                print("")

            else:
                print("------------------SIMUJLACION AFD DIRECTO-------------------")
                print("No, el AFD DIRECTO NO acepta la cadena ingresada... :(")

                print("--- %s segundos ---" % (end_time - start_time))
                print("--------------------------------------------------")
                print("")
        else:
            print("------------------SIMUJLACION AFD DIRECTO-------------------")
            print("No, el AFD DIRECTO NO acepta la cadena ingresada... :(")

            print("--- %s segundos ---" % (end_time - start_time))
            print("--------------------------------------------------")
            print("")

    def generateAFNDIRECTO(self):
        # acá se construye el arbol
        for postfixValue in self.expresionPostfix:
            if(self.funciones.isOperandPosftixTokenFinal(postfixValue)):  # * si es una letra
                if(postfixValue.getIdenficador() == "EPSILON"):  # si es una e no lleva numeración
                    nodoPrimerapos = ""
                    nodoUltimaPos = ""
                    nodo = NodoDirecto()
                    nodo.setCaracterNodo(postfixValue.getIdenficador())
                    nodo.setNodoId("")

                    nodo.setAnulable(self.isAnulable(nodo, postfixValue))
                    nodoPrimerapos = [nodo]
                    nodoUltimaPos = [nodo]
                    nodo.setPrimeraPos(self.primeraPos(
                        nodoPrimerapos, postfixValue))
                    nodo.setUltimaPos(self.ultimaPos(
                        nodoUltimaPos, postfixValue))
                    self.AFDDirectoFinal[self.contadorGlobalV2] = nodo
                    self.contadorGlobalV2 += 1
                    self.arrayNodos.append(nodo)  # agregamos el nodo
                else:  # cualquier otra letra INCLUYENDO el # lleva numeracion
                    nodo = NodoDirecto()
                    nodoPrimerapos = ""
                    nodoUltimaPos = ""
                    nodo.setCaracterNodo(postfixValue.getNombreIdentificador())
                    nodo.setNodoId(str(self.contadorGlobal))
                    self.diccionarioSiguientePos[self.contadorGlobal] = []
                    if(postfixValue.getIdenficador() == "ACEPTACION"):
                        self.nodosAceptacion[self.contadorGlobal] = postfixValue.getNombreIdentificador(
                        )
                    self.contadorGlobal += 1  # aumentamos el contador global
                    nodoPrimerapos = [nodo]
                    nodoUltimaPos = [nodo]
                    nodo.setAnulable(self.isAnulable(nodo, postfixValue))
                    nodo.setPrimeraPos(self.primeraPos(
                        nodoPrimerapos, postfixValue))
                    nodo.setUltimaPos(self.ultimaPos(
                        nodoUltimaPos, postfixValue))
                    self.AFDDirectoFinal[self.contadorGlobalV2] = nodo

                    self.contadorGlobalV2 += 1
                    self.arrayNodos.append(nodo)  # agregamos el nodo
            elif(postfixValue.getIdenficador() == "OR"):  # el OR NO se le coloca numero
                nodoOrAnulable = ""
                nodoOrPrimeraPos = ""
                nodoOrUltimaPos = ""
                nodoOr = NodoDirecto()
                nodoOr.setCaracterNodo(postfixValue.getIdenficador())
                nodoOr.setNodoId("")
                nodob = self.arrayNodos.pop()
                nodoa = self.arrayNodos.pop()
                nodoOrAnulable = [nodob, nodoa]
                nodoOrPrimeraPos = [nodob, nodoa]
                nodoOrUltimaPos = [nodob, nodoa]
                nodoOr.setAnulable(self.isAnulable(
                    nodoOrAnulable, postfixValue))
                nodoOr.setPrimeraPos(self.primeraPos(
                    nodoOrPrimeraPos, postfixValue))
                nodoOr.setUltimaPos(self.ultimaPos(
                    nodoOrUltimaPos, postfixValue))
                # agregamos al diccionario global
                self.AFDDirectoFinal[self.contadorGlobalV2] = nodoOr
                self.contadorGlobalV2 += 1
                self.arrayNodos.append(nodoOr)  # agregamos el nodo

            elif(postfixValue.getIdenficador() == "APPEND"):  # el AND NO se le coloca numero
                nodoAndAnulable = ""
                nodoAndPrimeraPos = ""
                nodoAndUltimaPos = ""
                nodoAndSiguientePos = ""
                nodoAnd = NodoDirecto()
                nodoAnd.setCaracterNodo(postfixValue.getIdenficador())
                nodoAnd.setNodoId("")
                nodob = self.arrayNodos.pop()
                nodoa = self.arrayNodos.pop()
                nodoAndAnulable = [nodob, nodoa]
                nodoAndPrimeraPos = [nodob, nodoa]
                nodoAndUltimaPos = [nodob, nodoa]
                nodoAndSiguientePos = [nodob, nodoa]
                nodoAnd.setAnulable(self.isAnulable(
                    nodoAndAnulable, postfixValue))
                nodoAnd.setPrimeraPos(self.primeraPos(
                    nodoAndPrimeraPos, postfixValue))
                nodoAnd.setUltimaPos(self.ultimaPos(
                    nodoAndUltimaPos, postfixValue))
                self.siguientePos(nodoAndSiguientePos, postfixValue)
                # agregamos al diccionario global
                self.AFDDirectoFinal[self.contadorGlobalV2] = nodoAnd
                self.contadorGlobalV2 += 1
                self.arrayNodos.append(nodoAnd)  # agregamos el nodo

            elif(postfixValue.getIdenficador() == "KLEENE"):  # el AND NO se le coloca numero
                nodoKleeneAnulable = ""
                nodoKleenePrimeraPos = ""
                nodoKleeneUltimaPos = ""
                nodoKleeneSiguientePos = ""
                nodoKleene = NodoDirecto()
                nodoKleene.setCaracterNodo(
                    postfixValue.getIdenficador())
                nodoKleene.setNodoId("")
                nodo = self.arrayNodos.pop()
                nodoKleeneAnulable = [nodo]
                nodoKleenePrimeraPos = [nodo]
                nodoKleeneUltimaPos = [nodo]
                nodoKleeneSiguientePos = [nodo]
                nodoKleene.setAnulable(self.isAnulable(
                    nodoKleeneAnulable, postfixValue))
                nodoKleene.setPrimeraPos(self.primeraPos(
                    nodoKleenePrimeraPos, postfixValue))
                nodoKleene.setUltimaPos(self.ultimaPos(
                    nodoKleeneUltimaPos, postfixValue))
                self.siguientePos(nodoKleeneSiguientePos, postfixValue)
                # agregamos al diccionario global
                self.AFDDirectoFinal[self.contadorGlobalV2] = nodoKleene
                self.contadorGlobalV2 += 1
                self.arrayNodos.append(nodoKleene)  # agregamos el nodo

        # self.ArrayNodos tiene el NODO raiz
        # self.AFDDirectoFinal es el ARBOL
        nodoRaiz = self.arrayNodos.pop()
        estadosIniciales = nodoRaiz.getPrimeraPos()
        self.Destados.append(estadosIniciales)
        self.DestadosV2.append(estadosIniciales)
        # print(self.lenguaje)
        # print(self.getPosFromLetter('b'))
        contador = -1
        while len(self.Destados) > 0:
            estadoInterno = self.Destados.pop()
            contador += 1
            letras = self.lenguaje
            for letra in letras:
                if(letra.getIdenficador() != "EPSILON"):
                    posdeLetra = self.getPosFromLetter(letra)
                    siguientePosID = []
                    for id in posdeLetra:
                        if(id in estadoInterno):
                            siguientePosID = siguientePosID + \
                                self.diccionarioSiguientePos[int(id)]

                    if(not(siguientePosID in self.DestadosV2)):
                        self.Destados.append(siguientePosID)
                        self.DestadosV2.append(siguientePosID)
                        self.AFDConstruidoFinal.append(
                            [contador, estadoInterno, letra.getValueIdentificador(), siguientePosID])

                    elif(len(estadoInterno) > 0):
                        self.AFDConstruidoFinal.append(
                            [contador, estadoInterno, letra.getValueIdentificador(), siguientePosID])

        print(self.AFDConstruidoFinal)
        # self.graficarAFD()

        # self.simularAFD()
