from ficha import Ficha
from constantes import FICHAS_POR_JUGADOR, CASILLAS_SALIDA

class Jugador:
    def __init__(self, color):
        self.color = color
        self.fichas = [Ficha(self, i+1) for i in range(FICHAS_POR_JUGADOR)]
        self.movimientos_extra = 0
        self.pares_consecutivos = 0
        self.casilla_salida = CASILLAS_SALIDA[self.color]

    def fichas_en_juego(self):
        return [f for f in self.fichas if not f.en_carcel and not f.en_llegada]

    def fichas_en_carcel(self):
        return [f for f in self.fichas if f.en_carcel]

    def todas_en_llegada(self):
        return all(f.en_llegada for f in self.fichas)
