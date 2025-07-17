# ficha.py
class Ficha:
    def __init__(self, jugador, id_ficha):
        self.jugador = jugador
        self.id = id_ficha
        self.en_carcel = True
        self.en_llegada = False
        self.posicion = None  # None si está en la cárcel, entero si está en el tablero

    def __str__(self):
        return f"{self.jugador.color[0]}{self.id}"
