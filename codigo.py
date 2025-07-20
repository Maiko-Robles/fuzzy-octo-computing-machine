print ("holA MINDO")










# control_turnos.py
import random

class Dado:
    def __init__(self, modo='real'):
        self.modo = modo
        self.valores_simulados = [5, 2, 3, 4, 6, 1, 2, 2, 2]  # valores de prueba para sandbox
        self.indice_simulado = 0

    def lanzar(self):
        if self.modo == 'real':
            return random.randint(1, 6)
        else:
            # Simular entrada manual con una lista de valores predefinidos
            if self.indice_simulado < len(self.valores_simulados):
                valor = self.valores_simulados[self.indice_simulado]
                self.indice_simulado += 1
                print(f"Valor simulado del dado: {valor}")
                return valor
            else:
                return random.randint(1, 6)


class ControlTurnos:
    def __init__(self, equipos):
        self.equipos = equipos  # lista de nombres de equipos
        self.turno_actual = 0
        self.contador_pares = {equipo: 0 for equipo in equipos}

    def siguiente_turno(self):
        self.turno_actual = (self.turno_actual + 1) % len(self.equipos)

    def obtener_equipo_actual(self):
        return self.equipos[self.turno_actual]

    def registrar_tiro(self, valor_dado):
        equipo = self.obtener_equipo_actual()

        if valor_dado % 2 == 0:
            self.contador_pares[equipo] += 1
            if self.contador_pares[equipo] == 3:
                print(f"{equipo} sacó 3 pares consecutivos. Pierde el turno.")
                self.contador_pares[equipo] = 0
                self.siguiente_turno()
            else:
                print(f"{equipo} repite turno por sacar par.")
        else:
            self.contador_pares[equipo] = 0
            self.siguiente_turno()

    def puede_mover(self, fichas_disponibles):
        return len(fichas_disponibles) > 0


# Ejemplo de uso:
if __name__ == "__main__":
    equipos = ["Rojo", "Verde", "Azul"]
    turno = ControlTurnos(equipos)
    dado = Dado(modo='desarrollador')  # usar modo 'desarrollador' para evitar input()

    rondas = 10  # número limitado de rondas de prueba para evitar bucle infinito en sandbox
    for _ in range(rondas):
        actual = turno.obtener_equipo_actual()
        print(f"\nTurno de {actual}...")
        valor = dado.lanzar()
        print(f"{actual} lanzó un {valor}.")

        turno.registrar_tiro(valor)
        # Simulación ficticia de fichas:
        fichas_disponibles = [1, 2] if valor != 3 else []

        if not turno.puede_mover(fichas_disponibles):
            print(f"{actual} no tiene movimientos disponibles. Pierde el turno.")
            turno.siguiente_turno()
