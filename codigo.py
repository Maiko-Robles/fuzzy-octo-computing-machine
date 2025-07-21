print ("holA MINDO")











import random
from collections import deque

class Dado:
    def __init__(self, modo='real'):
        self.modo = modo  # 'real' o 'desarrollador'
        self.historial_pares = []

    def lanzar(self):
        if self.modo == 'real':
            valor = random.randint(1, 6)
        else:
            valor = int(input("🔧 Modo desarrollador - Ingresa valor del dado (1-6): "))
        self._registrar_par(valor)
        return valor

    def _registrar_par(self, valor):
        if valor % 2 == 0:
            self.historial_pares.append(valor)
        else:
            self.historial_pares = []

    def tres_pares_consecutivos(self):
        return len(self.historial_pares) >= 3


class ControlTurnos:
    def __init__(self, equipos: list[str], modo_dado='real'):
        self.equipos = deque(equipos)  # nombres o IDs de los equipos
        self.turno_actual = self.equipos[0]
        self.jugadores_saltados = set()
        self.dado = Dado(modo_dado)

    def avanzar_turno(self):
        self.equipos.rotate(-1)
        self.turno_actual = self.equipos[0]

    def jugar_turno(self, fichas_equipo: list):
        print(f"\n🎲 Turno del equipo: {self.turno_actual}")

        if self.turno_actual in self.jugadores_saltados:
            print("⛔ Turno perdido por 3 pares consecutivos.")
            self.jugadores_saltados.remove(self.turno_actual)
            self.avanzar_turno()
            return

        dado_valor = self.dado.lanzar()
        print(f"🎯 {self.turno_actual} lanzó un {dado_valor}")

        if self.dado.tres_pares_consecutivos():
            print("🚫 ¡Tres pares consecutivos! Pierde el próximo turno.")
            self.jugadores_saltados.add(self.turno_actual)
            self.dado.historial_pares.clear()
            self.avanzar_turno()
            return

        ficha = self.seleccionar_ficha(fichas_equipo, dado_valor)

        if ficha:
            resultado = ficha.mover(dado_valor)
            if resultado == "llegada":
                print("🎉 Ficha llegó: se otorgan +10 casillas.")
                ficha.mover(10)
            elif resultado == "captura":
                print("💥 Ficha capturada: se otorgan +20 casillas.")
                ficha.mover(20)
        else:
            print("⚠️ Ninguna ficha puede moverse. Turno perdido.")

        if dado_valor % 2 == 0:
            print("🔁 Dado par: repite turno.")
        else:
            self.avanzar_turno()

    def seleccionar_ficha(self, fichas: list, dado_valor: int):
        for ficha in fichas:
            if ficha.puede_mover(dado_valor):
                return ficha
        return None

    def asignar_modo_dado(self, modo: str):
        self.dado = Dado(modo)