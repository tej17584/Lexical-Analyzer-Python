"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: postfixTokensScanner.py
Propósito: ESte programa toma el listado de objetos que leimos linealmente y lo pasa a postfix
V 2.0
"""

#! Zona de imports
from funciones import *
from tipoVar import *
from pprint import pprint as pp


class ConversionPostfixScanner:
    # Constructor de las variables
    def __init__(self):
        self.top = -1
        # self.capacity = capacity  # capacidad o longitud de la cadena
        # El array se usa como un stack
        self.arrayOperandos = []
        # seteamos la precedencia. La suma y resta es 1, la multiplicacion y division son 2 y la exponenciacion es 3, siguiendo reglas de la aritmética
        self.outputPostfix = []
        # diccionario de precedencia version 2
        self.precedenceV2 = {'OR': 1, 'APPEND': 2}
        self.funciones = funciones()

    # Funcion para verificar si el caracter es un operador
    def isOperador(self, tokenObject):
        if tokenObject.getTipoVariable() == 'OR' or tokenObject.getTipoVariable() == 'APPEND':
            return True
        return False

    # Funcion para verificar que el caracter no sea un operador
    def notOperador(self, tokenObject):
        if (tokenObject.getTipoVariable() == 'NOTERMINAL'
            or tokenObject.getTipoVariable() == 'TERMINAL'
                or tokenObject.getTipoVariable() == 'ACTION'):
            return True
        return False

    # método para ver si el stack esta vacío
    def isEmpty(self):
        return True if self.top == -1 else False

    # Retorna el valor de la cima del stack
    def peekTopOfStack(self):
        return self.arrayOperandos[-1]

    # hace pop de un elemento del stack
    def pop(self):
        if not self.isEmpty():  # si no esta vacío
            self.top -= 1  # el top es -1 para indicar que es vacío
            return self.arrayOperandos.pop()  # entonces jalamos
        else:
            return "$"  # de lo contrario un valor espaecial

    # Se verifica si la precedencia de un operandor es estrictamente menor que la del primer elemento del stack
    def mayorPrecedencia(self, i):
        try:
            a = self.precedenceV2[i.getTipoVariable()]
            bnuevo = self.peekTopOfStack()
            b = self.precedenceV2[bnuevo.getTipoVariable()]
            return True if a <= b else False
        except KeyError:
            return False

    # hace push de un elemento
    def push(self, op):
        self.top += 1  # sumamos al top, en este caso, si es el primer elemento o unico, será 0 porque contiene un -1 por defecto
        self.arrayOperandos.append(op)  # se hace pop

    # ? Método principal para convertir
    def infixToPostfixProducciones(self, exp):
        # Iteramos sobre la exppresión
        # for llave, i in exp.items():
        for i in exp:
            # Si el caracter es un operando se añade al print final
            if i.getTipoVariable() == "NOMBREPROD":
                self.outputPostfix.append(i)
            elif self.notOperador(i):
                self.outputPostfix.append(i)
            elif self.isOperador(i):
                while (len(self.arrayOperandos) > 0 and
                       self.arrayOperandos[-1].getTipoVariable() != 'LENCERRADO_OR' and
                       self.arrayOperandos[-1].getTipoVariable() != 'LENCERRADO_WHILE' and
                       self.arrayOperandos[-1].getTipoVariable() != 'LENCERRADO_CORCHETE' and
                       self.mayorPrecedencia(i)):
                    top = self.pop()
                    self.outputPostfix.append(top)
                self.push(i)
            # Si tenemos un paréntesis abierto, se agrega al STACK
            elif (i.getTipoVariable() == 'LENCERRADO_OR' or
                  i.getTipoVariable() == 'LENCERRADO_WHILE' or
                  i.getTipoVariable() == 'LENCERRADO_CORCHETE'):
                self.outputPostfix.append(i)
                self.push(i)
            # Si el caracter entrante es el cierre de paréntesis, hacemos pop y lo mandamos a outputPostfix hasta que encontremos otra abertura de paréntesis
            elif (i.getTipoVariable() == 'RENCERRADO_OR' or
                  i.getTipoVariable() == 'RENCERRADO_WHILE' or
                  i.getTipoVariable() == 'RENCERRADO_CORCHETE'):
                # mientras no sea vacío y sea distinto a "("
                while((not self.isEmpty()) and self.peekTopOfStack().getTipoVariable() != 'LENCERRADO_OR'
                      and self.peekTopOfStack().getTipoVariable() != 'LENCERRADO_WHILE'
                      and self.peekTopOfStack().getTipoVariable() != 'LENCERRADO_CORCHETE'):
                    a = ""
                    a = self.pop()  # hacemos pop
                    self.outputPostfix.append(a)  # agregamos al outputPostfix
                    if (a == ""):
                        print("No hay signo de cerrado de paréntesis")
                        return -1
                self.outputPostfix.append(i)
                # si llegamos a la condicion del while, entonces retornamos -1 para salir
                if (not self.isEmpty() and self.peekTopOfStack().getTipoVariable() != 'LENCERRADO_OR'
                        and self.peekTopOfStack().getTipoVariable() != 'LENCERRADO_WHILE'
                        and self.peekTopOfStack().getTipoVariable() != 'LENCERRADO_CORCHETE'):
                    return -1
                else:
                    self.pop()  # de lo contrario, hacemos pop de valores
        # HAcemos POP de TODOS los operadores en el stack
        # while not self.isEmpty():
         #   self.outputPostfix.append(self.pop())

         # verificamos si existe un paréntesis abierto de más
        while len(self.arrayOperandos):
            caracter = self.pop()
            if (caracter.getTipoVariable() == "LENCERRADO_OR" or
                caracter.getTipoVariable() == "LENCERRADO_WHILE" or
                    caracter.getTipoVariable() == "LENCERRADO_CORCHETE"):
                return "ERRORPOSTFIX"
            self.outputPostfix.append(caracter)

        # Imprimimos
        #print(" ".join(self.outputPostfix))
        return self.outputPostfix


""" funcioncitas = funciones()
expresion = input('Ingresa una expresión:  ')
expresion = expresion.replace(' ', '')
obj = ConversionPostfixTokens()
expresionAlterada = funcioncitas.alterateREPosftixToken(expresion)
postFixValue = obj.infixToPostfix(expresionAlterada)
print(f'El resultado es: {postFixValue}') """
#strconv = postFixValue.split(' ')
#resultado = obj.operatePostFix(strconv)
#print("tipo de resultado ", type(resultado))
#print(f'El resultado de la operacion es es: {resultado}')
# This code is contributed by Nikhil Kumar Singh(nickzuck_007)
# # This code is contributed by Amarnath Reddy
# https://www.geeksforgeeks.org/stack-set-4-evaluation-postfix-expression/
