"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: posftixEvaluador.py
Propósito: Este programa toma dos expresiones cualesquiera, no numeros necesariamente y las
convierte en operaciones postfix. Por ejemplo:
entrada: DIGIT + NUMBER
saldría: DIGIT NUMBER +
Esto es para cuando queremos sumar dos valores o diferencia de conjuntos.
V 1.0
"""
from collections import OrderedDict
#! Zona de imports
from funciones import *


class Conversion:
    # Constructor de las variables
    def __init__(self):
        self.top = -1  # ! límite
        # self.capacity = capacity  # capacidad o longitud de la cadena
        # El array se usa como un stack
        self.arrayOperandos = []
        # seteamos la precedencia. La suma y resta es 1, la multiplicacion y division son 2 y la exponenciacion es 3, siguiendo reglas de la aritmética
        self.outputPostfix = []
        self.precedence = {'+': 1, '-': 1}  # diccionario de precedencia
        self.stack2 = []
        self.top2 = -1
        self.concatenado = ''
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

    def pop2(self):
        if self.top2 == -1:
            return
        else:
            self.top2 -= 1
            return self.stack2.pop()

    def push2(self, i):
        self.top2 += 1
        self.stack2.append(i)

    # hace push de un elemento
    def push(self, op):
        self.top += 1  # sumamos al top, en este caso, si es el primer elemento o unico, será 0 porque contiene un -1 por defecto
        self.arrayOperandos.append(op)  # se hace pop

    # Se verifica si la precedencia de un operandor es estrictamente menor que la del primer elemento del stack
    def mayorPrecedencia(self, i):
        try:
            a = self.precedence[i]
            b = self.precedence[self.peekTopOfStack()]
            return True if a <= b else False
        except KeyError:
            return False

    # Main, convierte infix a postfix
    def infixToPostfix(self, exp):
        # Iteramos sobre la exppresión
        for i in exp:
            # Si el caracter es un operando se añade al print final
            if self.funciones.isOperand(i):
                # self.outputPostfix.append(i)
                self.concatenado = self.concatenado+i
            elif self.funciones.is_op(i):
                if(self.concatenado != ''):
                    self.outputPostfix.append(self.concatenado)
                    self.concatenado = ''
                    # print(f'El valor múltiple era: {self.outputPostfix}')
                while len(self.arrayOperandos) > 0 and self.arrayOperandos[-1] != '(' and self.mayorPrecedencia(i):
                    top = self.pop()
                    self.outputPostfix.append(top)
                self.push(i)
            elif i == '(':  # Si tenemos un paréntesis abierto, se agrega al STACK
                self.push(i)
            # Si el caracter entrante es el cierre de paréntesis, hacemos pop y lo mandamos a outputPostfix hasta que encontremos otra abertura de paréntesis
            elif i == ')':
                if(self.concatenado != ''):
                    self.outputPostfix.append(self.concatenado)
                    self.concatenado = ''
                # mientras no sea vacío y sea distinto a "("
                while((not self.isEmpty()) and self.peekTopOfStack() != '('):
                    a = self.pop()  # hacemos pop
                    self.outputPostfix.append(a)  # agregamos al outputPostfix
                    if len(a) == 0:
                        print("No hay signo de cerrado de paréntesis")
                        return -1
                # si llegamos a la condicion del while, entonces retornamos -1 para salir
                if (not self.isEmpty() and self.peekTopOfStack() != '('):
                    return -1
                else:
                    self.pop()  # de lo contrario, hacemos pop de valores
            # Si encontramos un operador
            else:
                # mientras no sea vacío Y su precedencia sea menor a la del primer valor del stack
                while(not self.isEmpty() and self.mayorPrecedencia(i)):
                    # entonces agregamos a la salida el valor del stack
                    self.outputPostfix.append(self.pop())
                self.push(i)  # hacemos push del operando  al stack

        if(self.concatenado != ''):
            self.outputPostfix.append(self.concatenado)

        # HAcemos POP de TODOS los operadores en el stack
        # while not self.isEmpty():
            # self.outputPostfix.append(self.pop())

         # verificamos si existe un paréntesis abierto de más
        while len(self.arrayOperandos):
            caracter = self.pop()
            if caracter == "(":
                print("Hay un signo de paréntesis abierto de más")
                exit(-1)
            self.outputPostfix.append(caracter)

        # Imprimimos
        # print(" ".join(self.outputPostfix))
        return " ".join(self.outputPostfix)

    def operatePostFix(self, expresion):
        local = ""
        for i in expresion:
            # si no es un entero, entonces es un operando
            if(self.funciones.is_op(i) and len(i) < 2):
                preval1 = self.pop2()
                preval2 = self.pop2()
                val1 = set(preval1)
                val2 = set(preval2)
                if(preval1 == "ANY" or preval1 == 'ANY'):
                    val1 = self.funciones.get_ANYSET()
                    val2 = self.funciones.getBetweenComillaSandComillaDoble(
                        preval2)
                    val2 = set(val2)
                    switcher = {
                        '+': val2.union(val1), '-': val2.difference(val1)}
                    self.push2(switcher.get(i))
                elif(preval2 == "ANY" or preval2 == 'ANY'):
                    val2 = self.funciones.get_ANYSET()
                    val1 = self.funciones.getBetweenComillaSandComillaDoble(
                        preval1)
                    val1 = set(val1)
                    switcher = {
                        '+': val2.union(val1), '-': val2.difference(val1)}
                    self.push2(switcher.get(i))
                else:
                    val1 = self.funciones.getBetweenComillaSandComillaDoble(
                        preval1)
                    val2 = self.funciones.getBetweenComillaSandComillaDoble(
                        preval2)
                    val1final = set(val1)
                    val2final = set(val2)
                    # hacemos un switch para saber cual operacion es cual
                    """ switcher = {
                        '+': self.funciones.unionTwoStrings(val2, val1),
                        '-': self.funciones.differenceTwoStrings(val2, val1)} """
                    switcher = {
                        '+': val2final.union(val1final), '-': val2final.difference(val1final)}
                    self.push2(switcher.get(i))
            else:
                for x in i:
                    if(self.funciones.isOperand(x)):
                        local = local+x
                    elif(i == "'+'" or i == "'-'"):
                        local = local+i
                        # si el componente es un integer
                self.push2(local)
                local = ""

        varRetornar = self.pop2()
        # varRetornar.remove('"')
        return varRetornar

#expresion = input('Ingresa una expresión:  ')
#expresion = expresion.replace(' ', '')
#obj = Conversion()
#postFixValue = obj.infixToPostfix(expresion)
#print(f'El resultado es: {postFixValue}')
#strconv = postFixValue.split(' ')
#resultado = obj.operatePostFix(strconv)
#print("tipo de resultado ", type(resultado))
#print(f'El resultado de la operacion es es: {resultado}')
# This code is contributed by Nikhil Kumar Singh(nickzuck_007)
# # This code is contributed by Amarnath Reddy
# https://www.geeksforgeeks.org/stack-set-4-evaluation-postfix-expression/
