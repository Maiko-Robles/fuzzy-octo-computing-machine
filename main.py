from juego import Juego

def main():
    print("Bienvenido a Parqués UN")
    while True:
        modo = input("Modo de juego (real/desarrollador): ").strip().lower()
        if modo in ["real", "desarrollador"]:
            break
        print("❌ Modo inválido. Escribe 'real' o 'desarrollador'.")

    juego = Juego(modo)

    terminado = False
    while not terminado:
        terminado = juego.jugar_turno()

if __name__ == "__main__":
    main()
