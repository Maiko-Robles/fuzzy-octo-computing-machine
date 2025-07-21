from constantes import NUM_CASILLAS, CASILLAS_LLEGADA

class Tablero:
    def __init__(self):
        self.casillas = [[] for _ in range(NUM_CASILLAS)]

        self.casillas_llegada = {
            "rojo": [[] for _ in range(7)],
            "verde": [[] for _ in range(7)],
            "amarillo": [[] for _ in range(7)],
            "azul": [[] for _ in range(7)]
        }

    def mover_ficha(self, ficha, pasos):
        if ficha.en_carcel:
            return False

        # Movimiento dentro de la llegada
        if ficha.en_llegada:
            actual = ficha.pasos_llegada
            nuevo = actual + pasos
            if nuevo >= 7:
                return False  # ya llegó al final
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
        if not ficha.en_carcel:
            return False
        if len(self.casillas[casilla_salida]) >= 2:
            return False
        ficha.en_carcel = False
        ficha.posicion = casilla_salida
        self.casillas[casilla_salida].append(ficha)
        return True

    def detectar_captura(self, color, posicion):
        for f in self.casillas[posicion]:
            if f.color != color and not f.en_llegada:
                f.en_carcel = True
                f.posicion = None
                return f
        return None

    def enviar_a_carcel(self, ficha):
        if ficha.en_carcel or ficha.en_llegada:
            return False
        if ficha.posicion is not None:
            self.casillas[ficha.posicion].remove(ficha)
        ficha.posicion = None
        ficha.en_carcel = True
        return True

    def puede_mover(self, ficha, pasos):
        if ficha.en_carcel:
            return False
        if ficha.en_llegada:
            return ficha.pasos_llegada + pasos < 7
        return True

    def es_llegada(self, ficha, pasos):
        if ficha.posicion is None:
            return False
        entrada = CASILLAS_LLEGADA[ficha.color][0]
        return (ficha.posicion + pasos) % NUM_CASILLAS == entrada
