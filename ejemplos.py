# ! Zona de imports
from tipoVar import tipoVar, variableER_Enum
from funciones import funciones
from pprint import pprint as pp
from postFixTokens import *
import difflib
import re
""" c2 = '"+"' not in 'digit+"ABCDEF".'
print(c2)
 """


""" def sortString(str):
    str = ''.join(sorted(str))
    print(str)


# Driver Code
s = "geeksforgeeks"
sortString(s)
 """

""" obj = funciones()
string1 = "abcde"
string2 = "defgh"

resultado = obj.differenceTwoStrings(string1, string2)
print(f'El resultado es {resultado}') """
chars = {':', 'W', 'n', 'Þ', 'Ñ', 'Q', 'Á', '\x80', 'À', '|', 'ò', '¡', '4', 'b', 'T', 'ï', '½', 'õ', 'o', '\x8a', '°', '\x9d', '/', 'ê', '>', '¶', '£', '\\', 'G', 'M', '©', '¤', 'Ó', 'q', 'Ú', 'a', '\x9a', 'X', '\x8d', 'û', 'ú', '®', 'D', 'z', '¨', 'È', '´', 'ð', 'r', '#', 'i', '\x81', '\x97', 'á', ']', 'Ë', '?', 'Ì', 'ô', 'J', '\x9b', '\x84', 'ì', '¯', 'u', 'w', '"', 'Ð', 'h', 'C', 'ö', '\x8c', 'ÿ', 'É', 'Ù', 'Â', 'f', '%', '6', '[', 'Ü', 'ã', '_', 'Ö', 'Õ', 'y', 'k', '\x88', '\x95', '²', 'c', 'ó', ';', '\x91', 'ª', '«', '\x8f', ')', '3', '\x9e', '·', '5', 'Ê', 'ù', '9', '&', 'Z', '\xa0', 'g', 'ý', '¼', '\x7f', '^', 'í', 't', '÷', '\x8e', 'E', '{', '¹', 'I', 'N', 'ü', 'ç', '\x93', '*', 'Û', 'd', '\x9f', 'ß', 'Î', 'B', '\x96', 'ä', 'à', '$', 'R', '!', 'P', 'ñ', '7', 'A', '\x86', 'j', 'Ô', 'e', 'x', 'U', '\x92', '\x99', '»', 'â', '¥', '¾', '³', 'Y', 'Æ', 'ø', '×', '\xad', 'Ò', 'p', 'Ç', '}', 'µ', 'K', 'L', '¬', '\x90', '1', '\x9c', '\x87', 'l', '0', '¿', '§', 'î', '\x89', 'v', 'Ã', '\x98', '¸', 'Ä', ',', 'þ', '<', '`', 'F', 'é', 'O', 'Å', '\x8b', '\x85', '±', 'æ', '\x94', 'Ø', 'Ý', '@', '8', ' ', '¦', 'm', '(', 'H', 'å', 'Í', 'ë', '\x83', 's', '~', '2', '=', '\x82', 'S', 'Ï', 'º',
         'V', 'è', '¢', '.'}


strings = {':', 'W', 'n', 'Þ', 'Ñ', 'Q', 'Á', '\x80', 'À', '|', 'ò', '¡', '4', 'b', 'T', 'ï', '½', 'õ', 'o', '\x8a', '°', '\x9d', '/', 'ê', '>', '¶', '£', '\\', 'G', 'M', '©', '¤', 'Ó', 'q', 'Ú', 'a', '\x9a', 'X', '\x8d', 'û', 'ú', '®', 'D', 'z', '¨', 'È', '´', 'ð', 'r', '#', 'i', '\x81', '\x97', 'á', ']', 'Ë', '?', 'Ì', 'ô', 'J', '\x9b', '\x84', 'ì', '¯', 'u', 'w', 'Ð', 'h', 'C', 'ö', '\x8c', 'ÿ', 'É', 'Ù', 'Â', 'f', '%', '6',
           '[', 'Ü', 'ã', '_', 'Ö', 'Õ', 'y', 'k', '\x88', '\x95', '²', 'c', 'ó', ';', '\x91', 'ª', '«', '\x8f', ')', '3', '\x9e', '·', '5', 'Ê', 'ù', '9', '&', 'Z', '\xa0', 'g', 'ý', '¼', '\x7f', '^', 'í', 't', '÷', '\x8e', 'E', '{', '¹', 'I', 'N', 'ü', 'ç', '\x93', '*', 'Û', 'd', '\x9f', 'ß', 'Î', 'B', '\x96', 'ä', 'à', '$', 'R', '!', 'P', 'ñ', '7', 'A', '\x86', 'j', 'Ô', 'e', 'x', 'U', '\x92', '\x99', '»', 'â', '¥', '¾', '³', 'Y', 'Æ', 'ø', '×', '\xad', 'Ò', 'p', 'Ç', '}', 'µ', 'K', 'L', '¬', '\x90', '1', '\x9c', '\x87', 'l', '0', '¿', '§', 'î', '\x89', 'v', 'Ã', '\x98', '¸', 'Ä', ',', 'þ', '<', '`', 'F', 'é', 'O', 'Å', '\x8b', '\x85', '±', 'æ', '\x94', 'Ø', 'Ý', '@', '8', ' ', '¦', 'm', '(', 'H', 'å', 'Í', 'ë', '\x83', 's', '~', '2', '=', '\x82', 'S', "'", 'Ï', 'º', 'V', 'è', '¢', '.'}


macros = {')', 'þ', 'G', 'M', 'â', 'Ð', 'Ü', 'æ', 'Ø', 'L', '\t', '/', 'H', 'f', '\x80', 'n', '@', '\n', '\x8e', 'W', '\x97', 'ë', 'C', 'k', 'ä', '\x84', '\x98', '\x92', '¼', '\x95', '\x02', '0', 'N', 'Ï', 'Þ', 'r', 'K', 'Z', '\x12', '\x8b', 'ï', '\x89', '¢', 'z', '³', '±', '¤', '\x88', '©', 'E', 'î', 'D', 'w', 'Y', '`', 'é', '»', '\x9e', '6', '\x86', 'x', '\x1c', 'Ç', 'b', 'Ê', 'ó', '½', '¾', 'ì', 'B', '¨', 'Ó', '®', 'ß', 'Ý', 'g', '*', 'Å', '\x91', '&', '\x03', '\x18', 'Ö', '\x19', 'T', '+', '\x1b', 'p', '\x81', 'a', '\x85', '\x0e', 'S', 'o', '¯', '¦', 'à', 'q', '2', '}', 'm', '\x0f', '\x7f', 's', '¶', 'Ã', 'õ', 'Â', '÷', '\x99', '_', '\x1f', 'i', 'ý', 'Ä', '\x82', '¹', '¸', '\x9d', '-', 'v', '\xad', 'J', 'ñ', 'ö', 'ã', 'F',
          'h', 'y', '\x9a', '\\', 'è', 'Ñ', '\x06', 't', '\x0c', 'X', '¡', '\x96', '§', 'A', '·', '3', 'È', '%', '~', '\x8d', 'ú', '^', 'Ë', '\r', '\x8f', '[', '²', 'U', 'ª', '\x07', '\x14', '\x9b', '\x10', '\x83', ':', 'Õ', ',', ' ', '4', 'Ú', '>', '\x8a', '\x11', 'Ù', 'c', '\x15', 'µ', '<', 'ô', '8', '\x0b', 'º', 'É', '\x01', '5', '\x87', '\x9f', '|', 'I', 'Û', '!', 'Á', '\x90', 'ø', '\x17', '$', '×', 'u', '°', '(', '1', '.', '\x05', 'd', 'R', '\x1d', '9', 'V', 'ð', '\x04', '«', '#', 'À', 'Í', 'l', '¿', 'Ô', '=', '\x1e', '\x94', '?', '\x93', '\x16', '¥', 'û', '{', 'Q', '\x00', '\x9c', 'Æ', 'e', 'ê', '\x8c', '\x08', "'", 'Ì', ']', '¬', 'O', 'í', '£', 'á', '\x1a', ';', 'Î', 'j', '´', 'ü', 'ù', 'ò', 'Ò', '\x13', 'å', 'P', 'ç', '\xa0'}
funcioncitas = funciones()
anyset = (funcioncitas.get_ANYSET())
contador = 0
for x in macros:
    contador = contador+1
    if(x == "'"):
        print(" ")


string = 'a"(H)"b'

s = "abcacbAUG|GAC|UGAfjdalfd"
start = string.find('"')
contador = start+1
# print("Contador al inicio", contador)
variableWhile = True
while variableWhile:
    if(string[contador] == '"'):
        variableWhile = False
    else:
        contador = contador+1

# print("contador al final", contador)


setAny = funcioncitas.get_ANYSET()


alterada = funcioncitas.alterateRE("a")
# print(alterada)


string = 'digit(digit)*".ab"digit(digit)*'
string2 = 'hexdigit(hexdigit)*hextermEXCEPTKEYWORDS'
# print(string2[26-len("hexterm")-1])


string1 = "{'J', 'A', 'M', 'C', 'W', 'i', 'b', 'p', 'E', 'r', 'H', 'z', 'T', 'h', 'P', 'a', 'j', 'k', 'v', 'l', 'u', 'f', 'c', 'L', 'Y', 'B', 'V', 'F', 'U', 'Z', 'I', 'Q', 'e', 'K', 't', 's', 'G', 'x', 'o', 'O', 'N', 'D', 'R', 'X', 'q', 'S', 'd', 'm', 'w', 'n', 'y', 'g'}"

string = 'comillas(stringletter(stringletter)*)comillas'

string4 = '((sign)|e)digit(digit)*'
string5 = 'hexdigit(hexdigit)*hextermEXCEPTKEYWORDS'
string6 = 'digit(digit)*'

LParentesis1 = variableER_Enum(tipoVar.LPARENTESIS, ord("("))
Ident1 = variableER_Enum(tipoVar.IDENT, ord("a"))
APPEND1 = variableER_Enum(tipoVar.APPEND, ord("."))
LParentesis2 = variableER_Enum(tipoVar.LPARENTESIS, ord("("))
IDent2 = variableER_Enum(tipoVar.IDENT, ord("b"))
Rparetensis1 = variableER_Enum(tipoVar.RPARENTESIS, ord(")"))
Kleene1 = variableER_Enum(tipoVar.KLEENE, ord("*"))
APPEND2 = variableER_Enum(tipoVar.APPEND, ord("."))
ACEPTACION1 = variableER_Enum(tipoVar.ACEPTACION, ord("#"))
Rparetensis2 = variableER_Enum(tipoVar.RPARENTESIS, ord(")"))
diccionarioValores = {0: LParentesis1, 1: Ident1, 2: APPEND1,
                      3: LParentesis2, 4: IDent2, 5: Rparetensis1,
                      6: Kleene1, 7: APPEND2, 8: ACEPTACION1,
                      9: Rparetensis2}


clasePosftix = ConversionPostfixTokens()
arrayValor = []
for llave, valor in diccionarioValores.items():
    arrayValor.append(valor)
posftix = clasePosftix.infixToPostfix(arrayValor)
# for x in posftix:
#    print(f'EL valor del token es: ', x.getIdenficador())

lenguaje = funcioncitas.getLanguage(posftix)
for x in lenguaje:
    print(x.getIdenficador())
print(f'El lenguaje es {lenguaje}')

# print("el valor es ", Ident1.getIdenficador())
print(chr(34))

stringA = "ab"
setA = set(stringA)
print(str(1) in setA)
pp(chr(13))
pp(chr(10))
pp(chr(9))
stringPrueba = "6H aa"
print(stringPrueba[0])
