"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: posftixTokens.py
Propósito: ESte programa toma el listado de tokens y lo convierte en posftix
V 1.0
"""

#! Zona de imports
from funciones import *
from tipoVar import *
from pprint import pprint as pp


class ConversionPostfixTokens:
    # Constructor de las variables
    def __init__(self):
        self.top = -1
        # self.capacity = capacity  # capacidad o longitud de la cadena
        # El array se usa como un stack
        self.arrayOperandos = []
        # seteamos la precedencia. La suma y resta es 1, la multiplicacion y division son 2 y la exponenciacion es 3, siguiendo reglas de la aritmética
        self.outputPostfix = []
        self.precedenceV2 = {'OR': 1, 'APPEND': 2,
                             'KLEENE': 3, '?': 3, "+": 3}  # diccionario de precedencia version 2
        self.concatenado = ''
        self.validacion = False
        self.funciones = funciones()

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
            a = self.precedenceV2[i.getIdenficador()]
            bnuevo = self.peekTopOfStack()
            b = self.precedenceV2[bnuevo.getIdenficador()]
            return True if a <= b else False
        except KeyError:
            return False

    # hace push de un elemento
    def push(self, op):
        self.top += 1  # sumamos al top, en este caso, si es el primer elemento o unico, será 0 porque contiene un -1 por defecto
        self.arrayOperandos.append(op)  # se hace pop

    # ? Método principal para convertir
    def infixToPostfix(self, exp):
        # Iteramos sobre la exppresión
        # for llave, i in exp.items():
        for i in exp:
            # Si el caracter es un operando se añade al print final
            if self.funciones.isOperandPosftixTokenFinal(i):
                #s = self.numberToLetter(i)
                """ if(i != "ε"):
                    s = i.lower()
                else:
                    s = i """
                self.outputPostfix.append(i)
            elif self.funciones.is_op_PosftixTokenFinal(i):
                while len(self.arrayOperandos) > 0 and self.arrayOperandos[-1].getIdenficador() != 'LPARENTESIS' and self.mayorPrecedencia(i):
                    top = self.pop()
                    self.outputPostfix.append(top)
                self.push(i)
            elif i.getIdenficador() == 'LPARENTESIS':  # Si tenemos un paréntesis abierto, se agrega al STACK
                self.push(i)
            # Si el caracter entrante es el cierre de paréntesis, hacemos pop y lo mandamos a outputPostfix hasta que encontremos otra abertura de paréntesis
            elif i.getIdenficador() == 'RPARENTESIS':
                # mientras no sea vacío y sea distinto a "("
                while((not self.isEmpty()) and self.peekTopOfStack().getIdenficador() != 'LPARENTESIS'):
                    a = ""
                    a = self.pop()  # hacemos pop
                    self.outputPostfix.append(a)  # agregamos al outputPostfix
                    if (a == ""):
                        print("No hay signo de cerrado de paréntesis")
                        return -1
                # si llegamos a la condicion del while, entonces retornamos -1 para salir
                if (not self.isEmpty() and self.peekTopOfStack().getIdenficador() != 'LPARENTESIS'):
                    return -1
                else:
                    self.pop()  # de lo contrario, hacemos pop de valores
        # HAcemos POP de TODOS los operadores en el stack
        # while not self.isEmpty():
         #   self.outputPostfix.append(self.pop())

         # verificamos si existe un paréntesis abierto de más
        while len(self.arrayOperandos):
            caracter = self.pop()
            if caracter.getIdenficador() == "LPARENTESIS":
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
