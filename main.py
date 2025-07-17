# main.py
from juego import Juego

def main():
    print("Bienvenido a Parqués UN")
    modo = input("Modo de juego (real/desarrollador): ").strip()
    juego = Juego(modo)

    terminado = False
    while not terminado:
        terminado = juego.jugar_turno()

if __name__ == "__main__":
    main()

