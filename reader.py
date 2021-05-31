"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: reader.py
Propósito: Este programa tiene como propósito leer el archivo con extension .ATG
V 1.0
"""

# ! Zona de imports
from os import remove
from tipoVarParser import tipoVar2, variableProduction_Enum
from funciones import funciones
from pprint import pprint as pp
from posftixEvaluador import *
from tipoVar import *
from postFixTokensScanner import *
import re
import pickle


class Reader:
    """
    La clase Reader lee el file y lo guarda en una estructura de datos adecuada
    """

    def __init__(self) -> None:
        self.rutaFile = "ATGFilesExamples\Expr.atg"
        self.streamCompleto = ""
        self.dictArchivoEntrada = ""
        self.lineasArchivo = []
        self.blockedLines = []
        self.lineasArchivoWithNumber = {}
        self.lineasPalabras = {}
        self.jsonFinal = {}  # diccionario final
        self.nombreCompilador = ""
        self.funciones = funciones()
        self.posftixEvaluador = Conversion()
        self.isChar = False
        self.isToken = False
        self.isKeyword = False
        self.isEXCET = False
        self.isProduction = False
        self.producciones = []
        self.productionsBlocked = []
        self.tokens = []
        self.acumuladorExcept = ""  # el acumulador para saber que hay que exceptuar
        self.boolComillasPunto = False
        self.dictPrimeraPos = {}  # esta es la primera pos
        self.bannedPositionsString = []  # estas son las posiciones banneadas de stirngs
        self.diccionarioProduccionesFinal = {}
        self.diccionarioProduccionesFinalV2 = {}
        self.tabsForFile = 1
        self.diccionarioTokenValue = {}
        self.contadorGlobalTokens = 1
        self.readDocumentAndPoblateStream()
        self.readDocument()

    def readDocumentAndPoblateStream(self):
        """
        Lee el documento ENTERO y lo guarda en una variable,
        es un stream continuo y contiene como llave la linea
        """
        with open(self.rutaFile, "r", encoding='utf-8') as f:
            self.lineasArchivo = f.readlines()
        f.close()

        contador = 0
        for x in self.lineasArchivo:
            self.lineasArchivoWithNumber[(contador)] = x
            contador = contador+1
        # print("Stream completo ", self.streamCompleto)

    def getTokensFinales(self):
        """
        REtorna los tokens
        """
        return self.jsonFinal["TOKENS"]

    def getCharactersFinales(self):
        """
        REtorna los characters
        """
        return self.jsonFinal["CHARACTERS"]

    def getKeywordsFinales(self):
        """
        REtorna los KEYWORDS
        """
        return self.jsonFinal["KEYWORDS"]

    def checkIfCharExists(self, character):

        for llave, valor in self.jsonFinal.items():
            for x, y in valor.items():
                if(x == character and llave == "CHARACTERS"):
                    return True, y

        return False, []

    def checkIfMoreCharExist(self, character):
        arrayLocal = []
        for llave, valor in self.jsonFinal.items():
            for x, y in valor.items():
                for valorCaracter in character:
                    if(x == valorCaracter.replace(".", "") and llave == "CHARACTERS"):
                        arrayLocal.append(valorCaracter)

        return arrayLocal

    def TokenMultiLinea(self, tokenEnorme, lineadelToken):
        newTokenValue = ""
        # obtenemos la linea del token general
        lineaTokenHeader = self.lineasPalabras["TOKENS"]
        line = self.lineasArchivoWithNumber[lineadelToken]
        line = line.rstrip("\n")  # eliminamos la linea
        # line = line.replace(" ", "")  # quitamos el espacio en blanco
        lineaArray = line.split("=")
        newTokenValue = newTokenValue+lineaArray[1]
        varExit = True
        contadorInterno = lineadelToken+1
        while varExit:
            line = self.lineasArchivoWithNumber[contadorInterno]
            line = line.rstrip("\n")  # eliminamos la linea
            # line = line.replace(" ", "")  # quitamos el espacio en blanco
            if(line[len(line)-1] == "."):
                newTokenValue = newTokenValue+line.replace(".", "")
                varExit = False
            else:
                newTokenValue = newTokenValue+line

            contadorInterno += 1
        return newTokenValue

    def productionMultiLine(self, lineadelProduction):
        """
        Retorna la produccion multilinea. Este método es complementario
        *@param lineadelProduction:  la linea de la produccion
        """
        newProductionValue = ""
        # obtenemos la linea del token general
        lineaTokenHeader = self.lineasPalabras["PRODUCTIONS"]
        line = self.lineasArchivoWithNumber[lineadelProduction]
        line = line.rstrip("\n")  # eliminamos la linea
        # line = line.replace(" ", "")  # quitamos el espacio en blanco
        lineaArray = line.split("=", 1)
        newProductionValue = newProductionValue+lineaArray[1]
        varExit = True
        contadorInterno = lineadelProduction+1
        while varExit:
            line = self.lineasArchivoWithNumber[contadorInterno]
            line = line.rstrip("\n")  # eliminamos la linea
            # line = line.replace(" ", "")  # quitamos el espacio en blanco
            if(line[len(line)-1] == "."):
                newProductionValue = newProductionValue+line.replace(".", "")
                varExit = False
            else:
                newProductionValue = newProductionValue+line

            contadorInterno += 1
        return newProductionValue

    def replaceMultiLineProduction(self, numeroLinea):
        """
        Retorna la produccion multilinea.
        *@param numeroLinea: el numero de linea donde encontramos la production de multilinea
        """
        # Seteamos variables
        counter = 1
        isMultiLine = False
        newProduction = ""
        # iteramos en todo el archivo leido
        for line in self.lineasArchivo:
            # la linea la reemplazamos los saltos del inea
            line = line.replace("\n", "")
            # si la produccion es multiline
            if(isMultiLine):
                # se appendea a las lineas bloqueadas temporalmente
                self.blockedLines.append(counter)
                # luego si ya llegamos al final si ya topamos, entonces miramos donde dejarla
                if(line[len(line)-1] != "."):
                    newProduction += line
                # de lo contrario vamos acumulando
                else:
                    newProduction += line
                    break
            # si es multilinea falso y el contador donde iniciamos es igual a la linea que vamos y si
            # la linea no tiene punto final entonces apendeamos a la produccion de retorno todo el split
            if(isMultiLine == False and counter == numeroLinea
               and line[len(line)-1] != "."):
                array = line.split("=", 1)
                newProduction += array[1]
                isMultiLine = True
            counter += 1

        return newProduction

    def primeraPosProducciones(self):
        """
        calcula la primeraPosProducciones pos de las producciones
        *@param ninguno: ninguno
        """
        for x in reversed(self.producciones):
            # se hace un for reversed
            # variables para "encerrar" las condiciones
            isOrProduction = False
            noTerminalBool = False
            terminalBool = False
            for index in range(len(self.diccionarioProduccionesFinalV2[x])):
                llave = self.diccionarioProduccionesFinalV2[x][index]
                arrayTemporalProducciones = []
                # si la variable es de tipo NO terminal, significa que lo primero que necesitamos
                # es la primera pos
                if llave.getTipoVariable() == "NOTERMINAL":
                    self.dictPrimeraPos[x] = self.dictPrimeraPos[llave.getNombreNoTerminal(
                    )]
                    # agregamos la lllave del no terminal
                    break
                elif llave.getTipoVariable() == "TERMINAL":
                    # el array temporal tiene la llave del nombre del terminal
                    arrayTemporalProducciones.append(llave.getNombreTerminal())
                    self.dictPrimeraPos[x] = arrayTemporalProducciones
                    # agregamos al dict d eprimera pos el array temporal de las producciones
                    for i in range(index+1, len(self.diccionarioProduccionesFinalV2[x])):
                        # El indice 2 contiene las producciones finales
                        Indice2 = self.diccionarioProduccionesFinalV2[x][i]
                        if(isOrProduction and Indice2.getTipoVariable() != "RENCERRADO_OR"):
                            # si es un Rencerrado
                            if(Indice2.getTipoVariable() == "NOTERMINAL" and noTerminalBool == False):
                                noTerminalBool = True
                                for primPos in self.dictPrimeraPos[Indice2.getNombreNoTerminal()]:
                                    arrayTemporalProducciones.append(primPos)
                                    self.dictPrimeraPos[x] = arrayTemporalProducciones
                            if(Indice2.getTipoVariable() == "TERMINAL" and terminalBool == False):
                                terminalBool = True
                                arrayTemporalProducciones.append(
                                    Indice2.getNombreTerminal())
                                self.dictPrimeraPos[x] = arrayTemporalProducciones
                        # de lo contrario si es un LencerradoOR
                        elif(Indice2.getTipoVariable() == "LENCERRADO_OR"):
                            isOrProduction = True
                        elif(Indice2.getTipoVariable() == "RENCERRADO_OR"):
                            isOrProduction = False
                    break
        print("############################", self.dictPrimeraPos)

    def addPrimeraPosObjects(self):
        """
        Coloca la primera pos dentro de los objetos que necesitamos iterar
        *@param ninguno: ninguno
        """
        for key in self.diccionarioProduccionesFinal:
            estoyOr = False
            yaAgregue = False
            definicion = self.diccionarioProduccionesFinal[key]
            # print("key")
            # print(key)
            for objProdIndex in range(len(definicion)):
                #     print(definicion[objProdIndex].getTipoCharProd())
                # print()
                # print()
                objProdActual = definicion[objProdIndex]
                objProdFuturo = ""
                if(objProdIndex != len(definicion)-1):
                    objProdFuturo = definicion[objProdIndex+1]
                if(objProdActual.getTipoVariable() == "LENCERRADO_WHILE" and objProdFuturo.getTipoVariable() == "NOTERMINAL"):
                    for i in self.dictPrimeraPos[objProdFuturo.getNombreNoTerminal()]:
                        objProdActual.setAddPrimeraPos(i)
                    break
                elif(objProdActual.getTipoVariable() == "LENCERRADO_OR" and objProdFuturo.getTipoVariable() == "NOTERMINAL"):
                    for i in self.dictPrimeraPos[objProdFuturo.getNombreNoTerminal()]:
                        objProdActual.setAddPrimeraPos(i)
                elif(objProdActual.getTipoVariable() == "LENCERRADO_WHILE" and objProdFuturo.getTipoVariable() == "LENCERRADO_OR"):
                    for i in range(objProdIndex+1, len(definicion)):
                        if(estoyOr and yaAgregue == False):
                            if(definicion[i].getTipoVariable() == "TERMINAL" or definicion[i].getTipoVariable() == "NOTERMINAL"):
                                yaAgregue == True
                                if(definicion[i].getTipoVariable() == "TERMINAL"):
                                    defi = definicion[i].getPrimeraPos()
                                    for defiPos in defi:
                                        objProdActual.setAddPrimeraPos(defiPos)
                        elif(definicion[i].getTipoVariable() == "LENCERRADO_OR"):
                            estoyOr = True
                        elif(definicion[i].getTipoVariable() == "ROR"):
                            estoyOr = False

                        if(objProdActual.getTipoVariable() == "RENCERRADOL"):
                            break
                elif(objProdActual.getTipoVariable() == "LENCERRADO_OR" and objProdFuturo.getTipoVariable() == "TERMINAL"):
                    for i in objProdFuturo.getPrimeraPos():
                        objProdActual.setAddPrimeraPos(i)
                elif(objProdActual.getTipoVariable() == "LENCERRADO_CORCHETE" and objProdFuturo.getTipoVariable() == "TERMINAL"):
                    for i in objProdFuturo.getPrimeraPos():
                        objProdActual.setAddPrimeraPos(i)
        """ for i, proddd in self.diccionarioProduccionesFinal.items():
            print(i)
            for prodobj in proddd:
                print(prodobj.getParametroGeneral())
            print()
            print()
            print() """

    def getProductionCompose(self, line, indice, lastProduction):
        """
        Retorna la produccion pero compuesta, es decir que a partir del line, indice y la produccion
        simple nos retorna ese valor.
        *@param line: el numero de linea
        *@param indice: el index donde estamos
        *@param lastProduction: la produccion anterior
        """
        newProduction = ""
        newProduction = lastProduction
        cont = 0
        for i in line:
            if(int(cont) > int(indice)):
                if(i.isalpha()):
                    self.productionsBlocked.append(cont)
                    newProduction += i
                else:
                    break
            cont += 1

        return newProduction

    def replaceProduccion(self, productionAcumulada):
        """
        Reemplaza la produccion con valores dummy
        *@param productionAcumulada: el numero de linea
        """
        productionAcumulada = productionAcumulada.replace(" ", "")
        productionAcumulada = productionAcumulada.replace(")", "")

        return productionAcumulada

    def writeParser(self):
        """
        Crea el parser con partes quemadas y con partes de codigo
        """
        f = open("parserAlejandroTejada.py", "w", encoding="utf8")
        f.write('''
import pickle


class parserAlejandro():

    def __init__(self) -> None:
        self.tokensScaneados = ""  # los tokens leidos
        self.tokensScaneadosV2 = []
        self.tokensMapeados = ""
        self.lastToken = ""
        self.lookAheadToken = ""
        self.leerTokensAndMap()
        self.Parser()

    def leerTokensAndMap(self):
        infile = open("arrayTokensLeidos", 'rb')
        self.tokensScaneados = pickle.load(infile)
        infile.close()

        infile = open("diccionarioTokensMapeados", 'rb')
        self.tokensMapeados = pickle.load(infile)
        infile.close()

        for llave, valor in self.tokensMapeados.items():
            for x in self.tokensScaneados:
                valoresToken = x.getAllValues()
                if(llave == valoresToken[0]):
                    x.setNumeracion(valor)
                elif(valoresToken[0] == "ERROR" and (valoresToken[1] == llave)):
                    x.setNumeracion(valor)

        for x in range(len(self.tokensScaneados)):
            if(self.tokensScaneados[x].getNumeracion() != ""):
                self.tokensScaneadosV2.append(self.tokensScaneados[x])

    def Expect(self, tokenId):
        if(self.lookAheadToken.getNumeracion() == tokenId):
            #print("llamare un nuevo token con tokenID: ", tokenId)
            self.GetNewToken()
        else:
            self.printERROROnScreen(tokenId)

    def GetNewToken(self):
        self.lastToken = self.lookAheadToken
        if(len(self.tokensScaneadosV2) > 0):
            self.lookAheadToken = self.tokensScaneadosV2.pop(0)
        else:
            self.lookAheadToken = self.lookAheadToken

    def getNumber(self):
        if(self.lookAheadToken.getValor() != "+" and self.lookAheadToken.getValor() != "-" and self.lookAheadToken.getValor() != "*" and self.lookAheadToken.getValor() != "/" and self.lookAheadToken.getValor() != ";"):
            return int(self.lastToken.getValor())
        else:
            return self.lastToken.getValor()

    def getVar(self):
        return self.lookAheadToken.getValor()

        ''')
        for key, produccion in self.diccionarioProduccionesFinal.items():
            print(key)
            f.write('\n')
            # primero instanciamos el postfix y hacemos que pueda evaluar las expresiones
            instanciaPostfix = ConversionPostfixScanner()
            postfix = instanciaPostfix.infixToPostfixProducciones(
                produccion)
            # estas variables sirven para formar los valores de la escena y de los parametros
            hasParameters = False
            productionAnterior = False
            for x in postfix:
                print(x.getParametroGeneral())
                if(x.getTipoVariable() == "NOMBREPROD"):
                    productionAnterior = False
                    if(x.getParameters() == ""):
                        nombreNoTerminal = x.getNombreNoTerminal()
                        f.write(" "*self.tabsForFile*4 +
                                'def ' + nombreNoTerminal + '(self):')
                    else:
                        sizePrimeraPos = len(x.getParameters())
                        f.write(" "*self.tabsForFile*4 + 'def ' + x.getNombreNoTerminal() +
                                '(self, ' + x.getParameters()[4:sizePrimeraPos] + '):')
                        hasParameters = True
                    f.write('\n')
                    self.tabsForFile += 1
                elif(x.getTipoVariable() == "TERMINAL"):
                    productionAnterior = False
                    posToken = self.tokens.index(
                        x.getNombreTerminal()) + 1
                    f.write(" "*self.tabsForFile*4 +
                            'self.Expect(' + str(posToken) + ')')
                    f.write('\n')
                elif(x.getTipoVariable() == "NOTERMINAL"):
                    productionAnterior = False
                    params = ""
                    if(x.getParameters() != ""):
                        sizePrimeraPos = len(x.getParameters())
                        params = x.getParameters()[4:sizePrimeraPos]
                        f.write(" "*self.tabsForFile*4 + params +
                                ' = self.' + x.getNombreNoTerminal()+'(' + params + ')')
                    else:
                        f.write(" "*self.tabsForFile*4 +
                                'self.' + x.getNombreNoTerminal()+'()')
                    f.write('\n')
                elif(x.getTipoVariable() == "RENCERRADO_WHILE"):
                    # si nos topamos con una abertura de while
                    productionAnterior = False
                    self.tabsForFile -= 1
                    f.write('\n')
                elif(x.getTipoVariable() == "LENCERRADO_WHILE"):
                    # si encontramos donde termina el while
                    count, sintaxis, productionAnterior = 0, "", False
                    sizePrimeraPos = len(x.getPrimeraPos())
                    for i in x.getPrimeraPos():
                        count += 1
                        posToken = self.tokens.index(i) + 1
                        sintaxis += "self.lookAheadToken.getNumeracion() == " + str(posToken)
                        if(count < sizePrimeraPos):
                            sintaxis += " or "
                    # esta funcion escribe las tabs x4 (porque 4 espacios son una)
                    f.write(" "*self.tabsForFile*4 + 'while ' + sintaxis + ':')
                    self.tabsForFile += 1
                    f.write('\n')
                elif(x.getTipoVariable() == "RENCERRADO_OR"):
                    # si nos topamos con un OR derecha, entonces hacemos que las tabs cambien
                    productionAnterior = True
                    self.tabsForFile -= 1
                    f.write('\n')
                elif(x.getTipoVariable() == "LENCERRADO_OR"):
                    # si nos topamos con un tipo OR encerrado, entonces hacemos ese valor
                    count, sintaxis = 0, ""
                    sizePrimeraPos = len(x.getPrimeraPos())
                    for w in x.getPrimeraPos():
                        count += 1
                        posToken = self.tokens.index(w) + 1
                        sintaxis += "self.lookAheadToken.getNumeracion() == " + str(posToken)
                        if(count < sizePrimeraPos):
                            sintaxis += " or "
                    #esto es para agregar ifs a las cosas
                    condition = "if"
                    if(productionAnterior):
                        condition = "elif"
                    f.write(" "*self.tabsForFile*4 +
                            condition + '(' + sintaxis + '):')
                    self.tabsForFile += 1
                    f.write('\n')
                elif(x.getTipoVariable() == "ACTION"):
                    # si es una accion entonces escribimos la accion dentro del file
                    productionAnterior = False
                    f.write(" "*self.tabsForFile*4 + x.getAccion())
                    f.write('\n')
                elif(x.getTipoVariable() == "RENCERRADO_CORCHETE"):
                    # si nos topamos con un corchete encerrado
                    productionAnterior = False
                    self.tabsForFile -= 1
                    f.write('\n')
                elif(x.getTipoVariable() == "LENCERRADO_CORCHETE"):
                    # si nos topamos
                    count, sintaxis, productionAnterior = 0, "", False
                    sizePrimeraPos = len(x.getPrimeraPos())
                    for w in x.getPrimeraPos():
                        count += 1
                        posToken = self.tokens.index(w) + 1
                        sintaxis += "self.lookAheadToken.getNumeracion() == " + str(posToken)
                        if(count < sizePrimeraPos):
                            sintaxis += " or "
                    f.write(" "*self.tabsForFile*4 + 'if(' + sintaxis + '):')
                    self.tabsForFile += 1
                    f.write('\n')

            if(hasParameters):
                f.write(" "*self.tabsForFile*4 + "return result")
                f.write('\n')
            self.tabsForFile -= 1
        f.write('\n')

        f.write('''
    def Parser(self):
        self.GetNewToken()
        self.Expr()


    def printERROROnScreen(self, tokenId):
        for x in self.tokensScaneadosV2:
            if(x.getNumeracion() == tokenId):
                if(x.getTipoToken() == "ERROR"):
                    errorPrint = x.getValor()
                    print(f'{errorPrint} expected')
                elif(x.getTipoToken() != "ERROR"):
                    errorPrint = x.getTipoToken()
                    print(f'{errorPrint} expected')


obj = parserAlejandro()

        ''')
        f.close()

    def construccionProducciones(self):
        """
        Método principal de la construccion de producciones. 
        """
        localDictProductions = self.jsonFinal["PRODUCTIONS"]
        # print(self.producciones)
        # print(self.tokens)
        for llave in localDictProductions:
            # print(llave)
            definicion = localDictProductions[llave]
            # este array es la nueva produccion
            produccionFinal = []
            # variables del flujo de parametros
            hasParameters = False
            esSintax = False
            isOneToken = False
            # esta variables e por si es sintaxis
            isSintaxis = ""
            # variables como el token
            token = ""
            parametrosProduction = ""
            acumulado = ""
            exprecion = ""
            #self.diccionarioProduccionesFinal[llave] = []
            #arrayProdTemp = self.diccionarioProduccionesFinal[llave]
            arrayProdTemp = []
            self.productionsBlocked = []
            if("<" in llave and ">" in llave):
                indexLlaveMenor = llave.find("<")
                indexLlaveMayor = llave.find(">")
                keyLimpio = llave[0:indexLlaveMenor]
                parameters = llave[indexLlaveMenor+1:indexLlaveMayor]
                newTipoVar = variableProduction_Enum(tipoVar2.NOMBREPROD)
                newTipoVar.setNombreNoTerminal(keyLimpio)
                newTipoVar.setParameters(parameters)
                newTipoVar.setIsFunction()
                arrayProdTemp.append(newTipoVar)
            else:
                newTipoVar = variableProduction_Enum(tipoVar2.NOMBREPROD)
                newTipoVar.setNombreNoTerminal(llave)
                newTipoVar.setIsFunction()
                arrayProdTemp.append(newTipoVar)
            for index in range(len(definicion)-1):
                if(index not in self.productionsBlocked):
                    acumulado += definicion[index]
                    # print(acumulado)
                    produccionActual = definicion[index]
                    lookAheadProduction = definicion[index+1]
                    if(produccionActual == "(" and lookAheadProduction == "."):
                        self.productionsBlocked.append(index)
                        self.productionsBlocked.append(index+1)
                        esSintax = True
                    elif(produccionActual == "." and lookAheadProduction == ")"):
                        self.productionsBlocked.append(index)
                        self.productionsBlocked.append(index+1)
                        newTipoVar = variableProduction_Enum(tipoVar2.ACTION)
                        newTipoVar.setAccion(isSintaxis)
                        arrayProdTemp.append(newTipoVar)
                        produccionFinal.append(isSintaxis)
                        isSintaxis = ""
                        esSintax = False
                        acumulado = ""
                    elif(esSintax):
                        isSintaxis += definicion[index]
                    elif(produccionActual == "(" and lookAheadProduction == "$"):
                        self.productionsBlocked.append(index)
                        self.productionsBlocked.append(index+1)
                        newTipoVar = variableProduction_Enum(
                            tipoVar2.LENCERRADO_OR)
                        newTipoVar.setNombreTerminal("($")
                        arrayProdTemp.append(newTipoVar)
                        produccionFinal.append("($")
                        acumulado = ""
                    elif(produccionActual == "$" and lookAheadProduction == ")"):
                        # print("sintax")
                        # print(sintax)
                        self.productionsBlocked.append(index)
                        self.productionsBlocked.append(index+1)
                        newTipoVar = variableProduction_Enum(
                            tipoVar2.RENCERRADO_OR)
                        newTipoVar.setNombreTerminal("$)")
                        arrayProdTemp.append(newTipoVar)
                        produccionFinal.append("$)")
                        acumulado = ""
                    elif(produccionActual == "'" or produccionActual == '"'):
                        acumulado = ""
                        if(isOneToken == False):
                            isOneToken = True
                        else:
                            # print(token)
                            # produccionFinal.append(token)
                            if(token in self.tokens):
                                numToken = self.tokens.index(token) + 1
                            else:
                                self.tokens.append(token)
                                numToken = len(self.tokens)
                            newTipoVar = variableProduction_Enum(
                                tipoVar2.TERMINAL)
                            newTipoVar.setNombreTerminal(token)
                            newTipoVar.setAddPrimeraPos(token)
                            # appendemaos al diccionario de tokens
                            if(numToken == self.contadorGlobalTokens):
                                self.diccionarioTokenValue[token] = self.contadorGlobalTokens
                                self.contadorGlobalTokens += 1
                            newTipoVar.setOrdenToken(numToken)
                            arrayProdTemp.append(newTipoVar)
                            token = ""
                            isOneToken = False
                    elif(isOneToken):
                        token += definicion[index]
                    elif(hasParameters == True and produccionActual == ">"):
                        newTipoVar.setParameters(parametrosProduction)
                        arrayProdTemp.append(newTipoVar)
                        produccionFinal.append(parametrosProduction)
                        hasParameters = False
                        acumulado = ""
                        parametrosProduction = ""
                    elif(hasParameters):
                        if(produccionActual != ">" and produccionActual != "<"):
                            parametrosProduction += definicion[index]
                    elif(self.replaceProduccion(acumulado) in self.producciones and not(lookAheadProduction.isalpha())):
                        acumNuevo = self.replaceProduccion(acumulado)
                        newTipoVar = variableProduction_Enum(
                            tipoVar2.NOTERMINAL)
                        newTipoVar.setNombreNoTerminal(acumNuevo)
                        newTipoVar.setIsFunction()
                        if(lookAheadProduction == "<"):
                            hasParameters = True
                        # produccionFinal.append(
                            # self.replaceProduccion(acumulado))
                        else:
                            arrayProdTemp.append(newTipoVar)
                        produccionFinal.append(acumNuevo)
                        acumulado = ""
                    elif(self.replaceProduccion(acumulado) in self.producciones):
                        produccion = self.getProductionCompose(
                            definicion, index, acumulado)
                        # produccionFinal.append(produccion.replace(" ", ""))
                        produccion = self.replaceProduccion(produccion)
                        newTipoVar = variableProduction_Enum(
                            tipoVar2.NOTERMINAL)
                        newTipoVar.setNombreNoTerminal(produccion)
                        newTipoVar.setIsFunction()
                        # arrayProdTemp.append(newTipoVar)
                        indexProd = definicion.find(produccion)
                        acum = ""
                        contLocal = 0
                        boolLocal = False
                        definicionLocal = definicion[indexProd:len(definicion)]
                        for i in definicionLocal:
                            acum += i
                            contLocal += 1
                            if(acum == produccion):
                                if(definicionLocal[contLocal] == "<"):
                                    hasParameters = True
                                    boolLocal = True
                        if(boolLocal == False):
                            arrayProdTemp.append(newTipoVar)
                        produccionFinal.append(produccion)
                        acumulado = ""
                    elif(self.replaceProduccion(acumulado) in self.tokens and not(lookAheadProduction.isalpha())):
                        # print("token")
                        # print(acumulado)
                        # produccionFinal.append(acumulado.replace(" ", ""))
                        acumuladoNuevo = self.replaceProduccion(acumulado)
                        if(acumuladoNuevo in self.tokens):
                            numToken = self.tokens.index(acumuladoNuevo) + 1
                        else:
                            self.tokens.append(acumuladoNuevo)
                            numToken = len(self.tokens)
                        newTipoVar = variableProduction_Enum(
                            tipoVar2.TERMINAL)
                        newTipoVar.setNombreTerminal(acumuladoNuevo)
                        # print("token: ", acumulado)
                        newTipoVar.setAddPrimeraPos(acumuladoNuevo)
                        newTipoVar.setOrdenToken(numToken)
                        # agregamos al dict global
                        if(numToken == self.contadorGlobalTokens):
                            self.diccionarioTokenValue[acumuladoNuevo] = self.contadorGlobalTokens
                            self.contadorGlobalTokens += 1
                        arrayProdTemp.append(newTipoVar)
                        produccionFinal.append(acumuladoNuevo)
                        acumulado = ""
                    elif(produccionActual == "{"):
                        newTipoVar = variableProduction_Enum(
                            tipoVar2.LENCERRADO_WHILE)
                        newTipoVar.setNombreTerminal("{")
                        arrayProdTemp.append(newTipoVar)
                        produccionFinal.append(produccionActual)
                        acumulado = ""
                    elif(produccionActual == "}"):
                        newTipoVar = variableProduction_Enum(
                            tipoVar2.RENCERRADO_WHILE)
                        newTipoVar.setNombreTerminal("}")
                        arrayProdTemp.append(newTipoVar)
                        produccionFinal.append(produccionActual)
                        acumulado = ""
                    elif(produccionActual == "["):
                        newTipoVar = variableProduction_Enum(
                            tipoVar2.LENCERRADO_CORCHETE)
                        newTipoVar.setNombreTerminal("[")
                        arrayProdTemp.append(newTipoVar)
                        produccionFinal.append(produccionActual)
                        acumulado = ""
                    elif(produccionActual == "]"):
                        newTipoVar = variableProduction_Enum(
                            tipoVar2.RENCERRADO_CORCHETE)
                        newTipoVar.setNombreTerminal("]")
                        arrayProdTemp.append(newTipoVar)
                        produccionFinal.append(produccionActual)
                        acumulado = ""
                    elif(produccionActual == "|"):
                        newTipoVar = variableProduction_Enum(
                            tipoVar2.OR)
                        newTipoVar.setNombreTerminal("|")
                        arrayProdTemp.append(newTipoVar)
                        produccionFinal.append(produccionActual)
                        acumulado = ""
                    elif(produccionActual == "#"):
                        newTipoVar = variableProduction_Enum(tipoVar2.APPEND)
                        newTipoVar.setNombreTerminal("#")
                        arrayProdTemp.append(newTipoVar)
                        produccionFinal.append(produccionActual)
                        acumulado = ""
            newArrayProduction = []
            for objIndex in range(len(arrayProdTemp)):
                productionActual = arrayProdTemp[objIndex]
                if(objIndex == len(arrayProdTemp)-1):
                    nextProduction = arrayProdTemp[objIndex]
                else:
                    nextProduction = arrayProdTemp[objIndex+1]
                newArrayProduction.append(productionActual)
                if(not isinstance(nextProduction, str)):
                    if(
                        (nextProduction.getTipoVariable() == "ACTION" or nextProduction.getTipoVariable(
                        ) == "TERMINAL" or nextProduction.getTipoVariable() == "NOTERMINAL") and productionActual.getTipoVariable() != "OR" and productionActual.getTipoVariable() != "LENCERRADO_OR" and
                        productionActual.getTipoVariable(
                        ) != "LENCERRADO_CORCHETE" and productionActual.getTipoVariable() != "LENCERRADO_WHILE"
                        and productionActual.getTipoVariable() != "NOMBREPROD" and objIndex != len(arrayProdTemp)-1
                    ):
                        tipoCharProd = variableProduction_Enum(tipoVar2.APPEND)
                        tipoCharProd.setNombreTerminal("#")
                        newArrayProduction.append(tipoCharProd)
            self.diccionarioProduccionesFinal[llave] = newArrayProduction
            keyLocal = llave.replace(" ", "")
            if("<" in llave and ">" in llave):
                keyLocal = llave[0:llave.find("<")].replace(" ", "")
            self.diccionarioProduccionesFinalV2[keyLocal] = newArrayProduction

    def replaceCharValues(self, charValue):
        acumulable = ""
        arrayNumeros = []
        if('..' in charValue):
            arrayCharsRango = charValue.split(' ')
            # encontramos los rangos
            for x in arrayCharsRango:
                if('CHR(' in x):
                    posicionInicialCHR = x.index('(')
                    posicionFInalCHR = x.index(')')
                    numeroChar = int(
                        x[int(posicionInicialCHR+1): int(posicionFInalCHR)])
                    arrayNumeros.append(numeroChar)
                    # reemplazamos los CHR de una vez
                    valorChar = chr(
                        int(x[int(posicionInicialCHR+1): int(posicionFInalCHR)]))
                    stringReplace = 'CHR(' +\
                        x[int(posicionInicialCHR+1):int(posicionFInalCHR)] +\
                        ')'
                    # print("")
                    charValue = charValue.replace(
                        stringReplace,  valorChar)

            for x in arrayCharsRango:
                if(x == ".."):
                    maximoValor = max(arrayNumeros)
                    minimoValor = min(arrayNumeros)
                    acumulador = ""
                    # Ya teniendo los rangos, iteramos
                    for valor in range(minimoValor+1, maximoValor):
                        acumulador += (chr(valor))
                    stringReplace = '..'
                    # print("")
                    charValue = charValue.replace(
                        stringReplace, acumulador)
        else:
            arrayChars = charValue.split(' ')
            for x in arrayChars:
                if('CHR(' in x):
                    posicionInicialCHR = x.index('(')
                    posicionFInalCHR = x.index(')')
                    valorChar = chr(
                        int(x[int(posicionInicialCHR+1): int(posicionFInalCHR)]))
                    stringReplace = 'CHR(' +\
                        x[int(posicionInicialCHR+1):int(posicionFInalCHR)] +\
                        ')'
                    # print("")
                    if(valorChar == '"'):
                        charValue = charValue.replace(
                            stringReplace, valorChar)
                    else:
                        charValue = charValue.replace(
                            stringReplace, '"' + valorChar + '"')

        return charValue

    def readDocument(self):
        """
        Lee el documento de entrada linea por linea y va guardandolo en un diccionario, esa será la estructura.
        Luego, verifica en toda las lineas cual es la linea donde estan los tokens que nos interesan.
        """
        # Leemos las lineas donde estan las palabras especiales y guardamos el número  de linea.
        # Esto nos puede servir luego.
        count = 0
        for line in self.lineasArchivo:
            line = line.rstrip("\n")  # eliminamos la linea
            line = line.replace(" ", "")  # quitamos el espacio en blanco
            if "COMPILER" in line:
                self.nombreCompilador = self.funciones.removerPalabraSingle(
                    line, "COMPILER")
                self.lineasPalabras["COMPILER"] = count
            if line == "CHARACTERS" or line == "CHARACTER":
                self.lineasPalabras[line] = count
            if line == "TOKENS" or line == "TOKEN":
                self.lineasPalabras[line] = count
            if line == "KEYWORDS" or line == "KEYWORD":
                self.lineasPalabras[line] = count
            if ("END" in line) and (self.funciones.removerPalabraSingle(line, "END") == ((self.nombreCompilador+"."))
                                    or self.funciones.removerPalabraSingle(line, "END") == ((self.nombreCompilador))):
                self.lineasPalabras["END"] = count
            if line == "PRODUCTIONS" or line == "PRODUCTION":
                self.lineasPalabras[line] = count
            count += 1

        count2 = 0
        for line in self.lineasArchivo:
            line = line.rstrip("\n")  # eliminamos la linea
            line2 = line.replace(" ", "")  # quitamos el espacio en blanco
            # Dependiendo del tipo de valor, seteamos el valor de la booleana,
            # de esa forma iteramos
            if(line2 == "CHARACTERS" or line2 == "CHARACTER"):
                self.isChar = True
                self.isKeyword = False
                self.isToken = False
                self.isProduction = False
                # creamos la entrada de valor en el dict final
                self.jsonFinal["CHARACTERS"] = {}
            elif(line2 == "TOKENS" or line2 == "TOKEN"):
                self.isChar = False
                self.isKeyword = False
                self.isToken = True
                self.isProduction = False
                # creamos la entrada de valor en el dict final
                self.jsonFinal["TOKENS"] = {}
            elif(line2 == "KEYWORDS" or line2 == "KEYWORD"):
                self.isChar = False
                self.isKeyword = True
                self.isToken = False
                self.isProduction = False
                # creamos la entrada de valor en el dict final
                self.jsonFinal["KEYWORDS"] = {}
            elif(line2 == "PRODUCTIONS" or line2 == "PRAGMAS"):
                self.isChar = False
                self.isKeyword = False
                self.isToken = False
                self.isProduction = True
                # creamos la entrada de valor en el dict final
                self.jsonFinal["PRODUCTIONS"] = {}

            # ? ----------------------------------------- CHARACTERES SECTIONS---------------------------------------------------
            if((self.isChar == True) and (self.isKeyword == False) and (self.isToken == False) and (self.isProduction == False)):
                # hacemos split con el '=', esto es un ARRAY
                charSplit = line.split("=")
                if(type(charSplit) != None and len(charSplit) > 1 and charSplit[0] != "CHARACTERS"):
                    localDictChar = {}
                    charName = str(charSplit[0].replace(" ", ""))
                    charValue = charSplit[1]
                    charValue1 = charValue.replace(" ", "")
                    # removemos el punto del character
                    if(charValue1[len(charValue1)-1] == "."):
                        charValue1 = charValue1[0:len(charValue1)-1]
                    if(charValue[len(charValue)-1] == "."):
                        charValue = charValue[0:len(charValue)-1]
                    # extramos los valores unicos la
                    localEvaluador = Conversion()
                    arrayCharValue = localEvaluador.infixToPostfix(
                        charValue1)  # convertimos a posftix
                    arrayCharValue = arrayCharValue.split(' ')
                    # verificamos si existe más de un valor por sustituir
                    arrayCharacters = self.checkIfMoreCharExist(arrayCharValue)
                    for x in arrayCharacters:
                        x = x.replace('.', '')
                        # esta función retorna el valor del char a sustiuir y su contenido
                        charExists, array = self.checkIfCharExists(x)
                        if(charExists and len(x) > 0 and len(array) > 0):  # si existe
                            if(isinstance(array, str)):
                                array = array.replace('.', '')
                                charValue1 = charValue1.replace(
                                    x, array)  # reemplazamos el valor
                            elif(isinstance(array, set)):
                                setString = self.funciones.fromSetToSTring(
                                    array)
                                setString = setString.replace('.', '')
                                charValue1 = charValue1.replace(
                                    x, setString)  # reemplazamos el valor
                    for x in arrayCharacters:
                        x = x.replace('.', '')
                        # esta función retorna el valor del char a sustiuir y su contenido
                        charExists, array = self.checkIfCharExists(x)
                        if(charExists and len(x) > 0 and len(array) > 0):  # si existe
                            if(isinstance(array, str)):
                                array = array.replace('.', '')
                                charValue = charValue.replace(
                                    x, array)  # reemplazamos el valor
                            elif(isinstance(array, set)):
                                setString = self.funciones.fromSetToSTring(
                                    array)
                                setString = setString.replace('.', '')
                                charValue = charValue.replace(
                                    x, setString)  # reemplazamos el valor
                    #! verificamos si hay un .. en el character
                    if('..' in charValue1 and ('CHR(' not in charValue1)):
                        charValue1Modificado = self.funciones.getRangeFromLetters(
                            charValue1)
                        charValue1 = charValue1Modificado
                    # ? Ahora verificamos si tiene algún CHAR
                    if('CHR(' in charValue):
                        if('-' in charValue or '+' in charValue):
                            signoMas = False
                            signoMenos = False
                            splitporOperando = []
                            charASumador = []
                            if('+' in charValue):
                                signoMas = True
                                signoMenos = False
                            elif('-' in charValue):
                                signoMenos = True
                                signoMas = False
                            if(signoMas == True and signoMenos == False):
                                splitporOperando = charValue.split('+')
                            elif(signoMas == False and signoMenos == True):
                                splitporOperando = charValue.split('-')
                            charAOperar = ""
                            for x in splitporOperando:
                                if('CHR(' in x):
                                    charAOperar = x  # este el que nos interesa sustutuir
                            for y in splitporOperando:
                                if('CHR(' not in y):
                                    # este char es el que SUMA
                                    charASumador.append(y.replace(" ", ""))
                            sustitucionTokens = self.replaceCharValues(
                                charAOperar)
                            localEvaluador2 = Conversion()
                            # reemplzamos valores
                            postfixCharValue = localEvaluador2.infixToPostfix(
                                charValue.replace(" ", ""))  # hacemos la expresion postfix
                            # hacemos split
                            postfixCharValue = postfixCharValue.split(' ')
                            contador = 0
                            for w in postfixCharValue:
                                if(w == charAOperar.replace(" ", "")):
                                    postfixCharValue[contador] = self.funciones.getBetweenComillaSandComillaDoble(
                                        sustitucionTokens.replace(" ", ""))
                                elif(w in charASumador):
                                    postfixCharValue[contador] = self.funciones.getBetweenComillaSandComillaDoble(
                                        w)
                                contador += 1
                             # operamos el postfix, para que nos lo retorne bien
                            operatedCharValue = localEvaluador2.operatePostFix(
                                postfixCharValue)
                            # si resulta que no es operable no actualizamos
                            if(operatedCharValue != "NO_OPERABLE"):
                                # operatedCharValue = operatedCharValue.replace(
                                #    '"', '')  # reemplazamos los '"' con vacíos
                                charValue1 = operatedCharValue  # igaualamos
                                charValue1 = charValue1  # agregamos
                        else:
                            sustitucionTokens = self.replaceCharValues(
                                charValue.replace(" ", ""))
                            charValue1 = sustitucionTokens
                        # verificamos si hay un símbolo de operar
                    if('+' in charValue1 or '-' in charValue1):
                        localEvaluador2 = Conversion()
                        charValue1 = charValue1.replace(" ", "")
                        if("'+'" in charValue1 or "'-'" in charValue1):
                            arrayPartido = charValue.split(' ')
                            postfixCharValue = localEvaluador2.infixToPostfix(
                                arrayPartido)  # hacemos la expresion postfix
                            # hacemos split
                            postfixCharValue = postfixCharValue.split(' ')
                            # operamos el postfix, para que nos lo retorne bien
                            operatedCharValue = localEvaluador2.operatePostFix(
                                postfixCharValue)
                            # si resulta que no es operable no actualizamos
                            if(operatedCharValue != "NO_OPERABLE"):
                                # operatedCharValue = operatedCharValue.replace(
                                #    '"', '')  # reemplazamos los '"' con vacíos
                                charValue1 = operatedCharValue  # igaualamos
                                charValue1 = charValue1  # agregamos
                        else:
                            postfixCharValue = localEvaluador2.infixToPostfix(
                                charValue1)  # hacemos la expresion postfix
                            # hacemos split
                            postfixCharValue = postfixCharValue.split(' ')
                            # operamos el postfix, para que nos lo retorne bien
                            operatedCharValue = localEvaluador2.operatePostFix(
                                postfixCharValue)
                            # si resulta que no es operable no actualizamos
                            if(operatedCharValue != "NO_OPERABLE"):
                                # operatedCharValue = operatedCharValue.replace(
                                #    '"', '')  # reemplazamos los '"' con vacíos
                                charValue1 = operatedCharValue  # igaualamos
                                charValue1 = charValue1  # agregamos

                    localDictChar[charName] = charValue1
                    self.jsonFinal["CHARACTERS"].update(localDictChar)

            # ? ----------------------------------------- FINALIZA CHARACTERES SECTIONS---------------------------------------------------
            # ? -----------------------------------------KEYWORDS SECTION ----------------------------------------------------------------
            elif((self.isChar == False) and (self.isKeyword == True) and (self.isToken == False) and (self.isProduction == False)):
                # hacemos split con el '=', esto es un ARRAY
                keywordSplit = line.split("=")
                if(type(keywordSplit) != None and len(keywordSplit) > 1 and keywordSplit[0] != "KEYWORDS"):
                    localDictKeyWord = {}
                    keyName = str(keywordSplit[0].replace(" ", ""))
                    keyValue = keywordSplit[1]
                    # removemos el punto del character
                    if(keyValue[len(keyValue)-1] == "."):
                        keyValue = keyValue[0:len(keyValue)-1]
                    localDictKeyWord[keyName] = keyValue
                    self.jsonFinal["KEYWORDS"].update(localDictKeyWord)
            # ? -----------------------------------------FINALIZA KEYWORDS SECTION ----------------------------------------------------------------
            # ? -----------------------------------------TOKENS SECTION ----------------------------------------------------------------
            elif((self.isChar == False) and (self.isKeyword == False) and (self.isToken == True) and (self.isProduction == False)):
                # hacemos split con el '=', esto es un ARRAY
                tokenSplit = line.split("=")
                if(type(tokenSplit) != None and len(tokenSplit) > 1 and tokenSplit[0] != "TOKENS"):
                    localTokenDict = {}
                    tokenName = str(tokenSplit[0].replace(" ", ""))
                    tokenValue = tokenSplit[1]
                    self.tokens.append(tokenName)
                    self.diccionarioTokenValue[tokenName] = self.contadorGlobalTokens
                    self.contadorGlobalTokens += 1
                    # removemos el punto del character
                    # además de remover verificamos que no sea de doble línea
                    if(tokenValue[len(tokenValue)-1] == "."):
                        tokenValue = tokenValue[0:len(tokenValue)-1]
                        localTokenDict[tokenName] = tokenValue
                        self.jsonFinal["TOKENS"].update(localTokenDict)
                    else:  # si por el contrario no termina en punto iteramos
                        tokenValue = self.TokenMultiLinea(tokenValue, count2)
                        localTokenDict[tokenName] = tokenValue
                        self.jsonFinal["TOKENS"].update(localTokenDict)
            # ? -----------------------------------------FINALIZA TOKENS SECTION ----------------------------------------------------------------
            # ? -----------------------------------------PRODUCTIONS  SECTION ----------------------------------------------------------------
            elif((self.isChar == False) and (self.isKeyword == False) and
                 (self.isToken == False) and (self.isProduction == True)
                 and count2 not in self.blockedLines):
                # print("soy produccion")
                # pp(line)
                productionSplit = line.split("=", 1)
                if(type(productionSplit) != None and len(productionSplit) > 1
                   and productionSplit[0] != "PRODUCTIONS"):
                    localProductDict = {}
                    productionName = str(productionSplit[0])
                    productionName = productionName.replace("  ", "")
                    productionValue = productionSplit[1]
                    varFinal = ""
                    if("<" in productionName and ">" in productionName):
                        acumulado = ""
                        for i in productionName:
                            if(i != "<"):
                                acumulado += i
                            else:
                                varFinal = acumulado.replace(" ", "")
                                self.producciones.append(
                                    #acumulado.replace(" ", "")
                                    varFinal)
                                break
                    else:
                        varFinal = productionName.replace(" ", "")
                        self.producciones.append(
                            varFinal)
                    # además de remover verificamos que no sea de doble línea
                    if(productionValue[len(productionValue)-1] == "."):
                        productionValue = productionValue[0:len(
                            productionValue)-1]
                        # Reemplazamos los valores de cerradura de sintaxis y otras
                        productionValue = productionValue.replace("  ", "")
                        productionValue = productionValue.replace("(. ", "(.")
                        productionValue = productionValue.replace(" .)", ".)")
                        localProductDict[productionName] = productionValue
                        # localProductDict[productionName] = productionValue
                        self.jsonFinal["PRODUCTIONS"].update(localProductDict)
                    else:  # si por el contrario no termina en punto iteramos

                        self.blockedLines.append(count2+1)
                        productionValue = self.replaceMultiLineProduction(
                            count2+1)
                        # Reemplazamos los valores de cerradura de sintaxis y otras
                        productionValue = productionValue.replace("  ", "")
                        productionValue = productionValue.replace("(. ", "(.")
                        productionValue = productionValue.replace(" .)", ".)")
                        localProductDict[productionName] = productionValue
                        # localProductDict[productionName] = productionValue
                        self.jsonFinal["PRODUCTIONS"].update(localProductDict)
            # ? -----------------------------------------FINALIZA PRODUCTIONS SECTION ----------------------------------------------------------------
                    #
            count2 += 1

        # Si incluso luego de todo esto no es aún set lo volvemos set
        for llave, valor in self.jsonFinal["CHARACTERS"].items():
            if(isinstance(valor, str)):
                valor = self.funciones.getBetweenComillaSandComillaDoble(
                    valor)
                newValor = self.funciones.fromSetToOrd(valor)
                self.jsonFinal["CHARACTERS"][llave] = set(newValor)
            elif(isinstance(valor, set)):
                newValor = self.funciones.fromSetToOrd(valor)
                self.jsonFinal["CHARACTERS"][llave] = newValor
        # print(self.jsonFinal["CHARACTERS"])

        # ahora valuamos Susituimos el valor de los tokens por otros mas conocidos
        # ? ----------------------------------------------------CREACION TOKENS---------------------------------------------------
        for llaveToken, valorToken in self.jsonFinal["TOKENS"].items():
            newValorToken = self.funciones.substituLlavesCorchetes(valorToken)
            newValorTokenAskVerification = self.funciones.alterateAskChain(
                newValorToken)
            newValorToken = self.funciones.substituLlavesCorchetesV2(
                newValorTokenAskVerification)
            newValorToken = newValorToken.replace(" ", "")
            # acá empieza la logica de sustiticion
            # print("VAlor por el token ", newValorToken)
            localDict = {}
            contadorDictTokens = 0
            acumuladorStrings = ""
            acumuladorExcept = ""

            for x in newValorToken:
                if(x == '(' and (contadorDictTokens not in self.bannedPositionsString)):
                    newTipoVar = variableER_Enum(tipoVar.LPARENTESIS, ord(x))
                    localDict[contadorDictTokens] = newTipoVar
                elif(x == ')' and (contadorDictTokens not in self.bannedPositionsString)):
                    newTipoVar = variableER_Enum(tipoVar.RPARENTESIS, ord(x))
                    localDict[contadorDictTokens] = newTipoVar
                elif(x == '*' and (contadorDictTokens not in self.bannedPositionsString)):
                    newTipoVar = variableER_Enum(tipoVar.KLEENE, ord(x))
                    localDict[contadorDictTokens] = newTipoVar
                elif(x == 'ε' and (contadorDictTokens not in self.bannedPositionsString)):
                    newTipoVar = variableER_Enum(tipoVar.EPSILON, ord(x))
                    localDict[contadorDictTokens] = newTipoVar
                elif(x == '|' and (contadorDictTokens not in self.bannedPositionsString)):
                    newTipoVar = variableER_Enum(tipoVar.OR, ord(x))
                    localDict[contadorDictTokens] = newTipoVar
                elif(x == '"' and (contadorDictTokens not in self.bannedPositionsString)):
                    contadorComillas = 0
                    for y in newValorToken:
                        if(y == '"'):
                            contadorComillas += 1
                    if(contadorComillas >= 2):
                        start = newValorToken.find('"')
                        if(start+1 not in self.bannedPositionsString):
                            contador = start+1
                            # agregamos esta posicion como ya no usable
                            posicionInicialString = contador
                            # print("Contador al inicio", posicionInicialString)
                            variableWhile = True
                            while variableWhile:
                                if(newValorToken[contador] == '"'):
                                    variableWhile = False
                                else:
                                    contador = contador+1
                            # agregamos esta posicion como ya no usable
                            posicionFinalString = contador
                            # print("contador al final", posicionFinalString)
                            # agregamos TODAS las posiciones banneadas
                            for x in range(posicionInicialString, posicionFinalString+1):
                                self.bannedPositionsString.append(x)
                            """ valorEntrecomillas = re.findall(
                                r'"(.*?)"', newValorToken[posicionInicialString-1:posicionFinalString]) """
                            valorEntrecomillasInicial = newValorToken[posicionInicialString: posicionFinalString]
                            if('.' in valorEntrecomillasInicial):
                                self.boolComillasPunto = True
                            # le agregamos los puntos
                            valorEntrecomillasFinal = self.funciones.alterateRE(
                                valorEntrecomillasInicial)
                            indexdePalabra = newValorToken.find(
                                valorEntrecomillasInicial)
                            if(indexdePalabra != 1):
                                # agregamos un append para mantener la unidad
                                newTipoVar = variableER_Enum(
                                    tipoVar.APPEND, ord("."))
                                localDict[contadorDictTokens] = newTipoVar
                                # self.bannedPositionsString.append(
                                # contadorDictTokens)
                                contadorDictTokens += 1
                            contadorInter = contadorDictTokens
                            if(self.boolComillasPunto):
                                for w in valorEntrecomillasFinal:
                                    if(w == '_'):
                                        varNuevaAppend = ""
                                        varNuevaAppend = variableER_Enum(
                                            tipoVar.APPEND, ord("."))
                                        localDict[contadorInter] = varNuevaAppend
                                        self.boolComillasPunto = False
                                    else:
                                        variableNueva = ""
                                        setNuevo = set()
                                        setNuevo.add(ord(w))
                                        variableNueva = variableER_Enum(
                                            tipoVar.STRING, setNuevo)
                                        localDict[contadorInter] = variableNueva
                                    """ self.bannedPositionsString.append(
                                        contadorInter) """
                                    contadorInter = contadorInter+1
                            else:
                                for w in valorEntrecomillasFinal:
                                    if(w == '.'):
                                        varNuevaAppend = ""
                                        varNuevaAppend = variableER_Enum(
                                            tipoVar.APPEND, ord("."))
                                        localDict[contadorInter] = varNuevaAppend
                                        self.boolComillasPunto = False
                                    else:
                                        variableNueva = ""
                                        setNuevo = set()
                                        setNuevo.add(ord(w))
                                        variableNueva = variableER_Enum(
                                            tipoVar.STRING, setNuevo)
                                        localDict[contadorInter] = variableNueva
                                    """ self.bannedPositionsString.append(
                                        contadorInter) """
                                    contadorInter = contadorInter+1
                            # print("el valor es :", valorEntrecomillasFinal)
                            """ if(newValorToken[contadorDictTokens+1] != '' or newValorToken[contadorDictTokens+1] != ' ' and self.boolComillasPunto):
                                print("el valor es :", valorEntrecomillasFinal)
                                contadorDictTokens = start
                            else:
                                print("el valor es :", valorEntrecomillasFinal)
                                contadorDictTokens = start """
                        contadorDictTokens = start
                else:  # de lo contrario acumulamos
                    if(contadorDictTokens not in self.bannedPositionsString):
                        acumuladorStrings += x
                        wordExists, value = self.checkIfCharExists(
                            acumuladorStrings)
                        if(wordExists and len(value) > 0):  # si existe el char
                            # convertimos los strings a ints
                            # funcioncitas.fromSetToOrd(value)
                            newValueSet = value
                            newTipoVarEntero = variableER_Enum(
                                tipoVar.IDENT, newValueSet)
                            newTipoVarEntero.setNombreIdentificador(
                                acumuladorStrings)
                            start = newValorToken.find(acumuladorStrings)
                            localDict[contadorDictTokens] = newTipoVarEntero
                            longitud = len(newValorToken)
                            if((contadorDictTokens+1) < longitud):
                                if(newValorToken[contadorDictTokens-len(acumuladorStrings)] == ')' or
                                   newValorToken[contadorDictTokens-len(acumuladorStrings)] == ']' or
                                   newValorToken[contadorDictTokens-len(acumuladorStrings)] == '}') and (newValorToken[contadorDictTokens+1] == '(' or
                                                                                                         newValorToken[contadorDictTokens+1] == '[' or
                                                                                                         newValorToken[contadorDictTokens+1] == '{'):

                                    appendAnterior = variableER_Enum(
                                        tipoVar.APPEND, ord('.'))
                                    appendSiguiente = variableER_Enum(
                                        tipoVar.APPEND, ord('.'))
                                    resta = contadorDictTokens - \
                                        len(acumuladorStrings)+1
                                    localDict[contadorDictTokens] = appendAnterior
                                    localDict[resta] = newTipoVarEntero
                                    localDict[resta+1] = appendSiguiente
                                    contadorDictTokens += 1

                                else:
                                    if((newValorToken[contadorDictTokens+1] == '(' or
                                        newValorToken[contadorDictTokens+1] == '[' or
                                            newValorToken[contadorDictTokens+1] == '{')):
                                        newTipoVar = variableER_Enum(
                                            tipoVar.APPEND, ord('.'))
                                        localDict[contadorDictTokens +
                                                  1] = newTipoVar
                                        contadorDictTokens += 1
                                    elif(newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == '*' or
                                            newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == ')' or
                                            newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == ']' or
                                            newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == '}'):
                                        indexdePalabra = newValorToken.find(
                                            acumuladorStrings)
                                        newTipoVar = variableER_Enum(
                                            tipoVar.APPEND, ord('.'))
                                        resta = contadorDictTokens - \
                                            len(acumuladorStrings)+1
                                        localDict[contadorDictTokens] = newTipoVar
                                        localDict[resta] = newTipoVarEntero
                                        contadorDictTokens += 1

                            elif(newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == '*' or newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == ')' or newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == ']' or newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == '}'):
                                newTipoVar = variableER_Enum(
                                    tipoVar.APPEND, ord('.'))
                                resta = contadorDictTokens - \
                                    len(acumuladorStrings)+1
                                localDict[contadorDictTokens] = newTipoVar
                                localDict[resta] = newTipoVarEntero
                                contadorDictTokens += 1

                            # agregamos TODAS las posiciones banneadas
                            acumuladorStrings = ""
                        """ elif(acumuladorStrings == "EXCEPT"):
                            # colocamos la variable global en true
                            self.isEXCET = True
                            acumuladorStrings = ""
                        elif(self.isEXCET):
                            self.acumuladorExcept += x
                            if(self.acumuladorExcept == "KEYWORDS"):
                                self.acumuladorExcept = ""
                                self.isEXCET = False
                                newTipoVar = variableER_Enum(
                                    tipoVar.EXCEPT, self.jsonFinal["KEYWORDS"])
                                newTipoVar.setNombreIdentificador("KEYWORDS")
                                localDict[contadorDictTokens] = newTipoVar """

                contadorDictTokens += 1

            contadorDictTokens += 1
            newTipoVar = variableER_Enum(
                tipoVar.APPEND, ord("."))
            localDict[contadorDictTokens] = newTipoVar
            contadorDictTokens += 1
            newTipoVar = variableER_Enum(
                tipoVar.ACEPTACION, ('#-'+llaveToken))
            newTipoVar.setNombreIdentificador(llaveToken)
            localDict[contadorDictTokens] = newTipoVar
            contadorDictTokens += 1
            # ahora cerramos el parentesis
            newTipoVar = variableER_Enum(
                tipoVar.RPARENTESIS, ord(")"))
            localDict[contadorDictTokens] = newTipoVar
            contadorDictTokens += 1
            # creamos un nuevo diccionario
            localDictEncerrado = {}
            contadorEncerrado = contadorDictTokens
            newTipoVar = variableER_Enum(
                tipoVar.LPARENTESIS, ord("("))
            localDictEncerrado[contadorEncerrado] = newTipoVar
            contadorEncerrado += 1
            for llave, valor in localDict.items():
                localDictEncerrado[contadorEncerrado] = valor
                contadorEncerrado += 1

            self.jsonFinal["TOKENS"][llaveToken] = localDictEncerrado
            contadorDictTokens = 0
            self.bannedPositionsString = []
        # ? ----------------------------------------------------FINALIZA CREACION TOKENS---------------------------------------------------
        # ? ----------------------------------------------------CREACION DE PRODUCCIONES---------------------------------------------------
        self.construccionProducciones()
        self.primeraPosProducciones()
        self.addPrimeraPosObjects()
        # Hacemos dump del diccionario de tokens
        filename = 'diccionarioTokensMapeados'
        outfile = open(filename, 'wb')
        pickle.dump(self.diccionarioTokenValue, outfile)
        outfile.close()
        """ print("-------------------------------- TOKENS MAPEADOS")
        for llave, valor in self.diccionarioTokenValue.items():
            print(f'Llave del token:  {llave} y el valor es: {valor}') """
        print("conviertiendo a postfix las cosas")
        cont = 0
        for key, produccion in self.diccionarioProduccionesFinal.items():
            cont += 1
            # print(key)
            # print(produccion)
            postfixInstProd = ConversionPostfixScanner()
            postfixProd = postfixInstProd.infixToPostfixProducciones(
                produccion)
            # print(postfixProd)
            for index in postfixProd:
                print(index.getParametroGeneral())
            print()
            # if(cont == 4):
            #     break

        # ! Creacion de Scanner
        self.writeParser()
        # ? ----------------------------------------------------FINALIZA CREACION DE PRODUCCIONES---------------------------------------------------
        # print(self.jsonFinal["CHARACTERS"])
        """ for llave, valor in self.jsonFinal["TOKENS"].items():
            print("LLAVE: ", llave)
            # print(self.jsonFinal["TOKENS"][llave])
            for numeroItem, valorItem in valor.items():
                print(
                    f'Identificador: {valorItem.getIdenficador()} value: {valorItem.getValueIdentificador()}')
                # print(valorItem) """

        """ for x, y in self.jsonFinal.items():
            for valor, pedazito in y.items():
                print(valor)
                print(f'Tipo de la llave {type(valor)}')
                print(pedazito)
                print(f'Tipo del valor {type(pedazito)}') """
        # print("Nombre compilador: "+self.nombreCompilador)
        # pp(self.lineasPalabras)


reader = Reader()
