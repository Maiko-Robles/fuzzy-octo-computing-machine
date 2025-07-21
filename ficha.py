class Ficha:
    def __init__(self, jugador, id_ficha):
        self.jugador = jugador
        self.id = id_ficha
        self.en_carcel = True
        self.en_llegada = False
        self.posicion = None
        self.pasos_llegada = 0  # <--- NECESARIO para manejar llegada

    @property
    def color(self):
        return self.jugador.color

    def __str__(self):
        return f"{self.jugador.color[0]}{self.id}"
