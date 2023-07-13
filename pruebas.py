
from exceptions import *
import time

def consulta_por_fecha_y_hora(a):
    print('Soy funcion 1'+ str(a))

def consulta_por_palabras_o_frases(a):
    print('Soy funcion 2'+ str(a))

def funcion3(a):
    print('Soy funcion 3 ' + str(a))


a = 2
b = 5
for i in range(100):
    a = int(input('ingrese'))
    print(a)
    if  a <= 0:
        break
    elif a != b:
        pass
    
    print('hello')
