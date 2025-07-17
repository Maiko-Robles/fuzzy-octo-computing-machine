
from constantes import NUM_CASILLAS_TABLERO, NUM_CASILLAS_LLEGADA, MAX_FICHAS_POR_CASILLA

class Tablero:
    def __init__(self):
        self.casillas = [[] for _ in range(NUM_CASILLAS_TABLERO)]
        self.llegadas = {}  # jugador.color -> lista de fichas

    def mover_ficha(self, ficha, pasos):
        if ficha.en_carcel:
            raise ValueError("Ficha en cárcel no puede moverse")
        
        nueva_pos = (ficha.posicion + pasos) % NUM_CASILLAS_TABLERO

        # Verificar bloqueo
        if len(self.casillas[nueva_pos]) >= MAX_FICHAS_POR_CASILLA:
            print("¡Bloqueo! No se puede mover allí.")
            return False

        # Remover ficha de su casilla anterior
        self.casillas[ficha.posicion].remove(ficha)

        # Captura
        if self.casillas[nueva_pos] and self.casillas[nueva_pos][0].jugador != ficha.jugador:
            print(f"¡{ficha} capturó a {self.casillas[nueva_pos][0]}!")
            capturada = self.casillas[nueva_pos].pop(0)
            capturada.en_carcel = True
            capturada.posicion = None
            ficha.jugador.movimientos_extra += 20

        # Mover ficha
        self.casillas[nueva_pos].append(ficha)
        ficha.posicion = nueva_pos
        return True

    def sacar_ficha(self, ficha, salida):
        if not ficha.en_carcel:
            return False
        if len(self.casillas[salida]) < MAX_FICHAS_POR_CASILLA:
            self.casillas[salida].append(ficha)
            ficha.posicion = salida
            ficha.en_carcel = False
            return True
        return False
