from jugador import Jugador
from dado import Dado
from tablero import Tablero
from constantes import COLORES, VALOR_SALIDA, MOV_EXTRA_CAPTURA, MOV_EXTRA_LLEGADA

class Juego:
    def __init__(self, modo):
        self.jugadores = [Jugador(color) for color in COLORES]
        self.tablero = Tablero()
        self.dado1 = Dado(modo)
        self.dado2 = Dado(modo)
        self.turno_actual = 0
        self.ultima_ficha_movida = None
        self.rondas_dobles = 0

    def jugar_turno(self):
        jugador = self.jugadores[self.turno_actual]
        print(f"\n🎲 Turno de {jugador.color}")

        d1 = self.dado1.lanzar()
        d2 = self.dado2.lanzar()
        print(f"Dados: {d1}, {d2}")

        if d1 == 5 and d2 == 5:
            self.sacar_fichas(jugador, 2)
            self.mostrar_estado(jugador)
        elif d1 == 5 or d2 == 5:
            otro = d2 if d1 == 5 else d1
            self.sacar_fichas(jugador, 1)
            self.mostrar_estado(jugador)
            if self.puede_mover(jugador, otro):
                self.mover_con_dado(jugador, otro)
        elif d1 + d2 == 5:
            self.sacar_fichas(jugador, 1)
            self.mostrar_estado(jugador)
        else:
            primero, segundo = self.elegir_orden_dados(d1, d2)
            movido = self.intentar_mover_ficha(jugador, primero)
            if not movido and (d1 == 5 or d2 == 5):
                self.sacar_fichas(jugador, 1)
            if self.puede_mover(jugador, segundo):
                self.intentar_mover_ficha(jugador, segundo)

        if self.ultima_ficha_movida:
            if self.ultima_ficha_movida.en_llegada:
                print("🎯 ¡Ficha llegó a la meta! +10 movimientos")
                self.mover_con_dado(jugador, MOV_EXTRA_LLEGADA)
            elif self.ultima_ficha_movida.en_carcel:
                print("💥 ¡Captura! +20 movimientos")
                self.mover_con_dado(jugador, MOV_EXTRA_CAPTURA)

        if jugador.todas_en_llegada():
            print(f"🎉 ¡{jugador.color} ha ganado! 🎉")
            return True

        self.mostrar_estado(jugador)

        if d1 == d2:
            print("🔁 Dados iguales: ¡Repite turno!")
            self.rondas_dobles += 1
            if self.rondas_dobles == 3:
                if self.ultima_ficha_movida:
                    print("🚫 3 pares dobles seguidos. Última ficha regresa a la cárcel.")
                    self.tablero.enviar_a_carcel(self.ultima_ficha_movida)
                    self.mostrar_estado(jugador)
                self.rondas_dobles = 0
            return False
        else:
            self.rondas_dobles = 0
            self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
            return False

    def sacar_fichas(self, jugador, cantidad):
        salidas = jugador.casilla_salida
        sacadas = 0
        for ficha in jugador.fichas:
            if ficha.en_carcel:
                if self.tablero.sacar_ficha(ficha, salidas):
                    print(f"{ficha} salió de la cárcel con dado 5")
                    sacadas += 1
                    if sacadas == cantidad:
                        break

    def puede_mover(self, jugador, pasos):
        return any(self.tablero.puede_mover(ficha, pasos) for ficha in jugador.fichas)

    def mover_con_dado(self, jugador, pasos):
        if not self.puede_mover(jugador, pasos):
            print(f"No hay fichas para mover con dado {pasos}.")
            return
        self.intentar_mover_ficha(jugador, pasos)

    def intentar_mover_ficha(self, jugador, dado):
        self.mostrar_estado(jugador)
        opciones = [
            f for f in jugador.fichas if self.tablero.puede_mover(f, dado)
        ]
        if not opciones:
            return False
        print(f"Selecciona ficha para mover {dado} casillas:")
        for i, f in enumerate(opciones, 1):
            print(f"{i}. {f}")
        while True:
            try:
                eleccion = int(input("> "))
                if 1 <= eleccion <= len(opciones):
                    ficha = opciones[eleccion - 1]
                    resultado = self.tablero.mover_ficha(ficha, dado)
                    self.ultima_ficha_movida = ficha
                    return resultado
            except:
                break
        return False

    def mostrar_estado(self, jugador):
        print(f"Estado de fichas de {jugador.color}:")
        for ficha in jugador.fichas:
            if ficha.en_carcel:
                estado = "🟥 En cárcel"
            elif ficha.en_llegada:
                estado = "🏁 En llegada"
            else:
                estado = f"🔲 En casilla {ficha.posicion}"
            print(f"  {ficha}: {estado}")

    def elegir_orden_dados(self, d1, d2):
        if d1 == d2:
            return d1, d2
        print("¿Con cuál dado deseas mover primero?")
        print(f"1. Usar {d1}")
        print(f"2. Usar {d2}")
        while True:
            eleccion = input("> ")
            if eleccion == "1":
                return d1, d2
            elif eleccion == "2":
                return d2, d1

