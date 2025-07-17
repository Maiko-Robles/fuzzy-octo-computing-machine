# juego.py
from dado import Dado
from jugador import Jugador
from tablero import Tablero
from constantes import COLORES, VALOR_SALIDA

class Juego:
    def __init__(self, modo='real'):
        self.jugadores = [Jugador(color) for color in COLORES]
        self.tablero = Tablero()
        self.dado1 = Dado(modo)
        self.dado2 = Dado(modo)
        self.turno_actual = 0

    def jugar_turno(self):
        jugador = self.jugadores[self.turno_actual]
        print(f"\n🎲 Turno de {jugador.color}")

        d1 = self.dado1.lanzar()
        d2 = self.dado2.lanzar()
        print(f"Dados: {d1}, {d2}")

        dados = [d1, d2]
        salida = self.obtener_casilla_salida(jugador)
        fichas_sacadas = 0

        # Intentar sacar ficha por cada dado con valor 5
        for dado in dados[:]:  # Copia para modificar la original
            if dado == VALOR_SALIDA and jugador.fichas_en_carcel():
                for ficha in jugador.fichas_en_carcel():
                    if self.tablero.sacar_ficha(ficha, salida):
                        print(f"{ficha} salió de la cárcel con dado {dado}")
                        fichas_sacadas += 1
                        dados.remove(dado)  # usamos ese dado
                        break  # solo una ficha por ese dado

        # Si quedaron dados no usados, permitir mover fichas
        for dado in dados:
            fichas = jugador.fichas_en_juego()
            if not fichas:
                print("No hay fichas disponibles para mover.")
                break

            self.mostrar_estado(jugador)
            print(f"Seleccione ficha para mover {dado} casillas:")
            for i, f in enumerate(fichas):
                print(f"{i+1}. {f}")
            try:
                opcion = int(input("> ")) - 1
                if 0 <= opcion < len(fichas):
                    ficha = fichas[opcion]
                    if not self.tablero.mover_ficha(ficha, dado):
                        print("Movimiento inválido.")
                else:
                    print("Opción inválida.")
            except ValueError:
                print("Entrada inválida.")

        # Verificar si ganó
        if jugador.todas_en_llegada():
            print(f"🎉 ¡{jugador.color} ha ganado! 🎉")
            return True

        # Cambio de turno
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        return False

    def obtener_casilla_salida(self, jugador):
        idx = COLORES.index(jugador.color)
        return (idx * 17) % 68  # Salidas equidistantes en tablero circular

    def mostrar_estado(self, jugador):
        print(f"Estado de fichas de {jugador.color}:")
        for f in jugador.fichas:
            if f.en_carcel:
                estado = "🟥 En cárcel"
            elif f.en_llegada:
                estado = "🟩 En llegada"
            else:
                estado = f"🔲 En casilla {f.posicion}"
            print(f"  {f}: {estado}")
