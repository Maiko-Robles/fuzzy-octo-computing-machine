from constantes import NUM_CASILLAS, CAMINOS_LLEGADA, MOV_EXTRA_CAPTURA, MOV_EXTRA_LLEGADA

class Tablero:
    def __init__(self):
        self.casillas = [[] for _ in range(NUM_CASILLAS)]

        self.casillas_llegada = {
            "azul": [[] for _ in range(8)],
            "rojo": [[] for _ in range(8)],
            "verde": [[] for _ in range(8)],
            "amarillo": [[] for _ in range(8)],
        }

    def mover_ficha(self, ficha, pasos):
        if ficha.posicion is None:
            return False

        if ficha.en_llegada:
            actual = ficha.pasos_llegada
            nuevo = actual + pasos
            if nuevo >= 7:
                return False
            self.casillas_llegada[ficha.color][actual].remove(ficha)
            self.casillas_llegada[ficha.color][nuevo].append(ficha)
            ficha.pasos_llegada = nuevo
            return True

        pos_actual = ficha.posicion
        nueva_pos = (pos_actual + pasos) % NUM_CASILLAS

        if self.es_llegada(ficha, pasos):
            self.casillas[pos_actual].remove(ficha)
            ficha.posicion = None
            ficha.en_llegada = True
            ficha.pasos_llegada = 0
            self.casillas_llegada[ficha.color][0].append(ficha)
            return "llegada"

        # Movimiento normal
        if ficha in self.casillas[pos_actual]:
            self.casillas[pos_actual].remove(ficha)

        capturada = self.detectar_captura(ficha.color, nueva_pos)
        if capturada:
            self.casillas[nueva_pos].clear()

        self.casillas[nueva_pos].append(ficha)
        ficha.posicion = nueva_pos

        if capturada:
            return "captura"
        return True

    def sacar_ficha(self, ficha, casilla_salida):
        if ficha.posicion is not None:
            return False
        if len(self.casillas[casilla_salida]) >= 2:
            return False
        ficha.posicion = casilla_salida
        self.casillas[casilla_salida].append(ficha)
        return True

    def detectar_captura(self, color, posicion):
        fichas_en_casilla = self.casillas[posicion]
        if len(fichas_en_casilla) == 1:
            f = fichas_en_casilla[0]
            if f.color != color and not f.en_llegada:
                f.posicion = None
                return f
        return None

    def enviar_a_carcel(self, ficha):
        if ficha.posicion is None or ficha.en_llegada:
            return False
        if ficha.posicion is not None:
            self.casillas[ficha.posicion].remove(ficha)
        ficha.posicion = None
        return True

    def puede_mover(self, ficha, pasos):
        if ficha.posicion is None:
            return False
        if ficha.en_llegada:
            return ficha.pasos_llegada + pasos < 7
        else:
            return True

    def es_llegada(self, ficha, pasos):
        if ficha.posicion is None:
            return False
        entrada = CAMINOS_LLEGADA[ficha.color][0]
        return (ficha.posicion + pasos) % NUM_CASILLAS == entrada
