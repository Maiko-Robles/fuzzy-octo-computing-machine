
import random

class Dado:
    def __init__(self, modo='real'):
        self.modo = modo

    def lanzar(self):
        if self.modo == 'real':
            return random.randint(1, 6)
        else:
            while True:
                try:
                    valor = int(input("Ingrese el valor del dado (1-6): "))
                    if 1 <= valor <= 6:
                        return valor
                    else:
                        print("❌ El valor debe estar entre 1 y 6.")
                except ValueError:
                    print("❌ Entrada inválida. Debe ser un número entero.")
