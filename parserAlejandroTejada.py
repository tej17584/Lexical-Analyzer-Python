"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: parserAlejandroTejada.py
Propósito: Es el parser
V 2.0
"""

import pickle


class parserFinal():

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

    def Expr(self):
        self.StatSeq()

    def StatSeq(self):
        while (self.lookAheadToken.getNumeracion() == 5 or self.lookAheadToken.getNumeracion() == 2 or self.lookAheadToken.getNumeracion() == 8):
            self.Stat()
            self.Expect(3)

    def Stat(self):
        value = 0
        # self.Expresssion(value)
        value = self.Expression(value)
        print("El Resultado de la operacion es: ", value)

    def Expression(self, result):
        result1, result2 = 0, 0
        result1 = self.Term(result1)
        while(self.lookAheadToken.getNumeracion() == 4 or self.lookAheadToken.getNumeracion() == 5):
            if(self.lookAheadToken.getNumeracion() == 4):
                self.Expect(4)
                result2 = self.Term(result2)
                result1 = int(result1)
                result2 = int(result2)
                result1 += result2
            elif(self.lookAheadToken.getNumeracion() == 5):
                self.Expect(5)
                result2 = self.Term(result2)
                result1 = int(result1)
                result2 = int(result2)
                result1 -= result2

        result = result1
        return result

    def Term(self, result):
        result1, result2 = 1, 1
        result1 = self.Factor(result1)
        while(self.lookAheadToken.getNumeracion() == 6 or self.lookAheadToken.getNumeracion() == 7):
            if(self.lookAheadToken.getNumeracion() == 6):
                self.Expect(6)
                result2 = self.Factor(result2)
                result1 = int(result1)
                result2 = int(result2)
                result1 *= result2
            elif(self.lookAheadToken.getNumeracion() == 7):
                self.Expect(7)
                result2 = self.Factor(result2)
                result1 = int(result1)
                result2 = int(result2)
                result1 /= result2

        result = result1
        return result

    def Factor(self, result):
        sign = 1
        if(self.lookAheadToken.getNumeracion() == 5):
            self.Expect(5)
            sign = -1
        if(self.lookAheadToken.getNumeracion() == 2):
            result = self.Number(result)
            result *= sign
        elif(self.lookAheadToken.getNumeracion() == 8):
            self.Expect(8)
            result = self.Expression(result)
            self.Expect(9)
            result *= sign

        return result

    def Number(self, result):
        self.Expect(2)
        result = self.getNumber()
        return result

    def Parser(self):
        self.GetNewToken()
        # llamamos al primer simbolo de la gramatica
        self.Expr()

    # ?---------------------------------------------------------------

    def printERROROnScreen(self, tokenId):
        for x in self.tokensScaneadosV2:
            if(x.getNumeracion() == tokenId):
                if(x.getTipoToken() == "ERROR"):
                    errorPrint = x.getValor()
                    print(f'{errorPrint} expected')
                elif(x.getTipoToken() != "ERROR"):
                    errorPrint = x.getTipoToken()
                    print(f'{errorPrint} expected')


obj = parserFinal()
