from jugador import Jugador 
from dado import Dado
from tablero import Tablero
from tkinter import messagebox
from constantes import COLORES, MOV_EXTRA_CAPTURA, MOV_EXTRA_LLEGADA, CAMINOS_LLEGADA, ENTRADAS_LLEGADA

class Juego:
    def __init__(self, modo, mostrar_mensaje=None, seleccionar_ficha=None, orden_dados=None, actualizar_gui=None):
        self.actualizar_gui = actualizar_gui
        self.jugadores = [Jugador(color) for color in COLORES]
        self.tablero = Tablero()
        self.dado1 = Dado(modo)
        self.dado2 = Dado(modo)
        self.turno_actual = 0
        self.resultado_ultimo_movimiento = None
        self.ultima_ficha_movida = None
        self.rondas_dobles = 0

        self.mostrar_mensaje = mostrar_mensaje
        self.seleccionar_ficha = seleccionar_ficha
        self.orden_dados = orden_dados

    def jugar_turno(self):
        jugador = self.jugadores[self.turno_actual]

        d1 = self.dado1.lanzar()
        d2 = self.dado2.lanzar()
        self.mostrar_mensaje(f"Dados: {d1}, {d2}")

        if d1 == 5 and d2 == 5:
            self.mostrar_mensaje("🎁 ¡Doble 5! Sacas 2 fichas.")
            self.sacar_fichas(jugador, 2)

        elif d1 == 5 or d2 == 5:
            self.mostrar_mensaje("🎁 ¡Un 5! Sacas 1 ficha.")
            self.sacar_fichas(jugador, 1)

        elif d1 + d2 == 5:
            self.mostrar_mensaje("🎁 ¡Suma 5! Sacas 1 ficha.")
            self.sacar_fichas(jugador, 1)
        
        primero, segundo = self.elegir_orden_dados(d1, d2)

        movido = self.intentar_mover_ficha(jugador, primero)

        if not movido and (primero == 5 or segundo == 5):
            self.sacar_fichas(jugador, 1)

        if self.puede_mover(jugador, segundo):
            self.intentar_mover_ficha(jugador, segundo)

        if self.ultima_ficha_movida:
            if movido == "llegada":
                self.mostrar_mensaje("¡Ficha llegó a la meta! +10 movimientos")
                self.mover_con_dado(jugador, MOV_EXTRA_LLEGADA)
            elif movido == "captura":
                self.mostrar_mensaje("¡Captura! +20 movimientos")
                self.mover_con_dado(jugador, MOV_EXTRA_CAPTURA)

        if jugador.todas_en_llegada():
            self.mostrar_mensaje(f"¡{jugador.color} ha ganado! ")
            return True

        if d1 == d2:
            self.mostrar_mensaje("Dados iguales: ¡Repite turno!")
            self.rondas_dobles += 1
            if self.rondas_dobles == 3:
                if self.ultima_ficha_movida:
                    self.mostrar_mensaje("3 pares dobles seguidos. Última ficha regresa a la cárcel.")
                    self.tablero.enviar_a_carcel(self.ultima_ficha_movida)
                self.rondas_dobles = 0
            return False
        else:
            self.rondas_dobles = 0
            self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
            return False

    def sacar_fichas(self, jugador, cantidad):
        salidas = jugador.casilla_salida
        sacadas = 0
        for ficha in jugador.fichas_en_carcel():
            if sacadas == cantidad:
                break
            if self.tablero.sacar_ficha(ficha, salidas):
                self.mostrar_mensaje(f"{ficha} salió de la cárcel con dado 5")
                sacadas += 1

    def puede_mover(self, jugador, pasos):
        return any(self.tablero.puede_mover(ficha, pasos) for ficha in jugador.fichas)

    def mover_con_dado(self, jugador, pasos):
        opciones = [f for f in jugador.fichas if self.tablero.puede_mover(f, pasos)]
        if not opciones:
            messagebox.showinfo("Sin movimientos", f"No hay fichas para mover con dado {pasos}.")
            return

        ficha = self.seleccionar_ficha(opciones, pasos)
        if ficha:
            self.tablero.mover_ficha(ficha, pasos)
            self.ultima_ficha_movida = ficha
            if self.actualizar_gui:
                self.actualizar_gui()

    def intentar_mover_ficha(self, jugador, dado):
        opciones = [f for f in jugador.fichas if self.tablero.puede_mover(f, dado)]
        

        if not opciones:
            return False

        ficha = self.seleccionar_ficha(opciones, dado)
        if ficha is not None:
            resultado = self.tablero.mover_ficha(ficha, dado)
            self.ultima_ficha_movida = ficha
            self.resultado_ultimo_movimiento = resultado
            if self.actualizar_gui:
                self.actualizar_gui()
            return resultado
        else:
            self.mostrar_mensaje("❌ No se seleccionó ninguna ficha válida.")
            return False

    def elegir_orden_dados(self, d1, d2):
        if d1 == d2:
            return d1, d2
        if self.orden_dados:
            return self.orden_dados(d1, d2)
        return d1, d2
