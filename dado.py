
import random

class Dado:
    def __init__(self, modo='real'):
        self.modo = modo

    def lanzar(self):
        if self.modo == 'real':
            return random.randint(1, 6)
        else:
            return int(input("Ingrese el valor del dado (1-6): "))
