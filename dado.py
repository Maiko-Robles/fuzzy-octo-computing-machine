import random

class Dado:
    def __init__(self, modo):
        self.modo = modo
        self.valor_manual = None

    def lanzar(self):
        if self.modo == "desarrollador":
            if self.valor_manual is None:
                raise ValueError("Debe establecer un valor manual para el dado en modo desarrollador.")
            valor = self.valor_manual
            self.valor_manual = None
            return valor
        else:
            return random.randint(1, 6)
    def set_valor_manual(self, valor):
        if 1 <= valor <= 6:
            self.valor_manual = valor
        else:
            raise ValueError("El valor del dado debe estar entre 1 y 6.")