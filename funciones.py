"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: functions.py
Propósito: ESte programa tiene funciones útiles
V 1.0
"""
import json


class funciones():
    def __init__(self) -> None:
        self.arrayOperandos = []
        self.precedenceV2 = {'|': 1, '.': 2,
                             '*': 3, '?': 3, "+": 3}  # diccionario de precedencia version 2
        self.dictionaryNTL = {"0": "A", "1": "B", "2": "C",
                              "3": "D", "4": "E", "5": "F",
                              "6": "G", "7": "H",
                              "8": "I", "9": "J"}
        self.ANYSET = set([chr(char) for char in range(0, 256)])

    def get_ANYSET(self):
        """
        Retorna el set de ANYSET
        """
        return self.ANYSET

    def getLastTokenValueFromDict(self, dictionary):
        """
        Retorna el valor de la ultima llave de un diccionario
        """
        arrayInterno = []
        nombreToken = ""
        for llave, valor in dictionary.items():
            arrayInterno.append(llave)

        return arrayInterno[-1]

    def printPrettyDictionary(self, d, indent=0):
        """
        this function prints pretty the dictionary,
        extracted from: https://stackoverflow.com/questions/3229419/how-to-pretty-print-nested-dictionaries
        """
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                self.printPrettyDictionary(value, indent+1)
            else:
                print('\t' * (indent+1) + str(value))

    def getDumpJson(self, dictionary):
        """
        REtorna el dump de un diccionario para ser impreso en formato JSON
        dictionary: el diccionario para ser droppeado
        """
        return json.dumps(dictionary, indent=2, default=str)

    def removerPalabraSingle(self, string, palabra):
        """
        Remueve la palabra del string y los espacios extra que contenga el string.
        Útil si la linea solamente tiene dos valores. Como:
        COMPILER AdaCS
        Nos retorna: AdaCS
        """
        string = string.replace(str(palabra), "")
        newString = string.replace(" ", "")
        return newString

    def isOperand(self, ch):
        """
        REtorna TRUE si el caracter ingresado es un alfanumerico, FALSE de lo contrario
        *@param ch: el caracter a ser probado
        """
        if ch != "+" and ch != "-":
            return True
        return False

    def isOperandPosftixToken(self, ch):
        """
        REtorna TRUE si el caracter ingresado es un alfanumerico, FALSE de lo contrario
        *@param ch: el caracter a ser probado
        """
        if ch.isalnum() or ch == "ε" or ch == "#":
            return True
        return False

    def isOperandPosftixTokenFinal(self, ch):
        """
        REtorna TRUE si el caracter ingresado es un alfanumerico, FALSE de lo contrario
        *@param ch: el caracter a ser probado
        """
        if ch.getIdenficador() == "IDENT" or ch.getIdenficador() == "EPSILON" or ch.getIdenficador() == "STRING" or ch.getIdenficador() == "ACEPTACION":
            return True
        return False

    def is_op(self, a):
        """
        Testeamos si el caracter de entrada es un operando
        *@param a: caracter a ser probado
        """
        if (a == '+' or a == '-') and (a != "'+'" or a != "'-'"):
            return True
        return False

    def is_op_PosftixToken(self, a):
        """
        Testeamos si el caracter de entrada es un operando
        *@param a: caracter a ser probado
        """
        if a == '+' or a == '.' or a == '*' or a == '?' or a == '|':
            return True
        return False

    def is_op_PosftixTokenFinal(self, a):
        """
        Testeamos si el caracter de entrada es un operando
        *@param a: caracter a ser probado
        """
        if a.getIdenficador() == 'APPEND' or a.getIdenficador() == 'KLEENE' or a.getIdenficador() == 'OR':
            return True
        return False

    def getLanguage(self, RE):
        """
        DAda una expresion regular, esto extrae el lenguaje, osea los caracteres unicos
        """
        #lenguaje = ''.join(set(str(RE)))
        lenguaje = RE
        newLenguaje = []
        arrayLocal = []
        for x in lenguaje:
            if(x.getIdenficador() == "IDENT" or x.getIdenficador() == "EPSILON" or x.getIdenficador() == "STRING"):
                if(x.getNombreIdentificador() not in arrayLocal):
                    arrayLocal.append(x.getNombreIdentificador())
                    newLenguaje.append(x)
        return newLenguaje

    def alterateAskChain(self, exp):
        """
        ESta funcion altera una cadena o expresion regular, y si encuentra un simbolo de + entonces lo sustitye por el equivalente
        *@param: exp: la expresion a ser valuada y que se le quite el simbolo de más
        """
        value = "?" in exp
        if(value == False):
            return exp
        else:
            index = exp.find('?')
            if exp[index-1] == ")":
                dentro = ""
                for i in reversed(exp[0:index-1]):
                    dentro += i
                    if i == "[":
                        dentro = dentro[::-1]
                        cantidad1 = len(dentro)
                        cantidad2 = len(exp[0:index-1])
                        ignore = cantidad2 - cantidad1
                        dentro = dentro[1:len(dentro)]
                        # print(dentro)
                        # print(exp[0:2])
                        return self.alterateAskChain(exp[0:ignore] + "(" + "(" + dentro + ")" + "|ε)" + exp[index+1:len(exp)])
            else:
                return self.alterateAskChain(exp[0:index-1] + "(" + "(" + exp[index-1] + ")" + "|ε)" + exp[index+1:len(exp)])

    def substituLlavesCorchetes(self, expresion):
        """
        Sustiuye las aberturas de corchetes y de llaves y sus cerraduras por los equivalentes.
        *@param expresion: la expresion a cambiar
        """
        newExpresion = ""
        for x in expresion:
            if(x == "]"):
                newExpresion = newExpresion+')?'
            elif(x == "}"):
                newExpresion = newExpresion+')*'
            else:
                newExpresion += x

        return newExpresion

    def substituLlavesCorchetesV2(self, expresion):
        """
        Sustiuye las aberturas de corchetes y de llaves y sus cerraduras por los equivalentes.
        *@param expresion: la expresion a cambiar
        """
        newExpresion = ""
        for x in expresion:
            if(x == "]"):
                newExpresion = newExpresion+')?'
            elif(x == "}"):
                newExpresion = newExpresion+')*'
            if(x == "["):
                newExpresion = newExpresion+'('
            elif(x == "{"):
                newExpresion = newExpresion+'('
            else:
                newExpresion += x

        return newExpresion

    def fromSetToOrd(self, setToOrd):
        """
        Esta funcion convierte un set con characteres a un set de ords
        *@param setToOrd: el set a ser convertido
        """
        newSet = set()
        for x in setToOrd:
            newSet.add(ord(x))
        return newSet

    def fromOrdToString(self, ordToString):
        """
        Esta funcion convierte un set de ints en strings
        *@param setToOrd: el set a ser convertido
        """
        newSet = set()
        for x in ordToString:
            newSet.add(chr(x))
        return newSet

    def fromSetToSTring(self, setToTransform):
        """
        Esta funcion convierte un set a un string concatenado
        *@param setToTransform: el set a convertir
        """
        nuevoString = ""
        for x in setToTransform:
            nuevoString += x

        return nuevoString

    def fromSetNumbersToSTring(self, setToTransform):
        """
        Esta funcion convierte un set a un string concatenado
        *@param setToTransform: el set a convertir
        """
        if(isinstance(setToTransform, int)):
            return str(setToTransform)
        else:
            nuevoString = ""
            for x in setToTransform:
                nuevoString += chr(x)

        return nuevoString

    def alterateRE(self, RE):
        """
        Altera una expresión regular agregándole puntos a la concatenacion para ser mas legible para el postfix
        *@param RE: la expresión regular original
        """
        nuevaRE = ""
        contador = 0
        if('.' in RE):
            for x in range(0, len(RE)):
                # print("EN EL CICLO S  ", RE[x])
                # print("EN el ITER ES : ", RE[x+1:x+2])
                nuevaRE += RE[x]
                if(self.isOperand(RE[x]) or RE[x] == ")" or RE[x] == "*" or RE[x] == "#"):
                    contador += 1
                if(RE[x+1:x+2] != " " and contador == 1):
                    if(self.isOperand(RE[x+1:x+2]) or RE[x+1:x+2] == "("):
                        nuevaRE += "_"
                        contador = 0
                    else:
                        contador = 0
        else:
            for x in range(0, len(RE)):
                # print("EN EL CICLO S  ", RE[x])
                # print("EN el ITER ES : ", RE[x+1:x+2])
                nuevaRE += RE[x]
                if(self.isOperand(RE[x]) or RE[x] == ")" or RE[x] == "*" or RE[x] == "#"):
                    contador += 1
                if(RE[x+1:x+2] != " " and contador == 1):
                    if(self.isOperand(RE[x+1:x+2]) or RE[x+1:x+2] == "("):
                        nuevaRE += "."
                        contador = 0
                    else:
                        contador = 0
        return nuevaRE

    def alterateREPosftixToken(self, RE):
        """
        Altera una expresión regular agregándole puntos a la concatenacion para ser mas legible para el postfix
        *@param RE: la expresión regular original
        """
        nuevaRE = ""
        contador = 0
        for x in range(0, len(RE)):
            #print("EN EL CICLO S  ", RE[x])
            #print("EN el ITER ES : ", RE[x+1:x+2])
            nuevaRE += RE[x]
            if(self.isOperandPosftixToken(RE[x]) or RE[x] == ")" or RE[x] == "*" or RE[x] == "?" or RE[x] == "+" or RE[x] == "#"):
                contador += 1
            if(RE[x+1:x+2] != " " and contador == 1):
                if(self.isOperandPosftixToken(RE[x+1:x+2]) or RE[x+1:x+2] == "("):
                    nuevaRE += "."
                    contador = 0
                else:
                    contador = 0
        return nuevaRE

    def getRangeFromLetters(self, linea):
        """
        ESta funcion obtiene el rango de entre dos valores y entre lineas
        *@param linea: es la linea
        """
        arryLine = linea.split("..")
        newLine = ""
        arrayIntegers = []
        for letra in arryLine:
            for char in letra:
                if(char.isalpha()):
                    print(char)
                    arrayIntegers.append(ord(char))
                    break

        for char in range(arrayIntegers[0], arrayIntegers[1]+1):
            newLine += chr(char)

        return newLine

    def sortString(self, str):
        """
        Hace sort de un string
        extraido de: https://www.geeksforgeeks.org/sort-string-characters/
        *@param: str: el string hacer sort
        """
        str = ''.join(sorted(str))
        return str

    def unionTwoStrings(self, string1, string2):
        """
        Une dos strings. Elimina duplicados.
        *@param: string1: el string a unir
        *@param: string2: el string a sumarle
        """
        res = ""
        temp = string1
        for i in string2:
            if i not in temp:
                string1 += i

        return string1

    def differenceTwoStrings(self, string1, string2):
        """
        Une dos strings. Elimina duplicados.
        *@param: string1: el string a unir
        *@param: string2: el string a sumarle
        """
        res = ""
        temp = string1
        for i in string2:
            if i in temp:
                string1 = string1.replace(i, '')

        return string1

    def getBetweenComillaSandComillaDoble(self, value):
        """
        VErifica si en un posible valor a sumar lo que hay es comilla doble o comilla simple. Si es simple,
        retornamos solo eso, si es doble quitamos lo doble
        El criterio es que si hay dos, es porque esta entre ellos el operando
        *@param: value: el string a valuar
        """
        contadorComilla = 0
        contadorComillaSimple = 0
        for x in value:
            if x == '"':
                contadorComilla += 1
            elif x == "'":
                contadorComillaSimple += 1

        if(contadorComilla == 2 and contadorComillaSimple < 2):
            return value.replace('"', '')
        elif(contadorComilla < 2 and contadorComillaSimple >= 2):
            value = value.replace("'", '')
            return value
        elif(contadorComilla > 2):
            print("ACA")
            print(value)

        return value
