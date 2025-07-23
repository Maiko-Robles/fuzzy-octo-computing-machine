import tkinter as tk
from tkinter import messagebox
from juego import Juego
from constantes import CAMINOS_LLEGADA, CASILLAS_SALIDA 

class Visual:
    CASILLA = 30
    ANCHO = 17
    ALTO = 17
    TAM_TABLERO = CASILLA * ANCHO

    zona_carcel = {
        "rojo": [(1, 1), (2, 1), (1, 2), (2, 2)],
        "verde": [(14, 1), (15, 1), (14, 2), (15, 2)],
        "amarillo": [(14, 14), (15, 14), (14, 15), (15, 15)],
        "azul": [(1, 14), (2, 14), (1, 15), (2, 15)]
    }

    camino_externo = [
        *((x, 8) for x in range(1)),
        *((x, 7) for x in range(8)),
        *((7, x) for x in range(7, -1, -1)),
        *((x, 0) for x in range(8, 10)),
        *((9, x) for x in range(1, 8)),
        *((x, 7) for x in range(9, 17)),
        *((16, x) for x in range(8, 10)),
        *((x, 9) for x in range(15, 8, -1)),
        *((9, x) for x in range(9, 17)),
        *((x, 16) for x in range(8, 6, -1)),
        *((7, x) for x in range(15, 8, -1)),
        *((x, 9) for x in range(7, -1, -1)),
    ]

    COLORES = {
        "rojo": "#FF4C4C",
        "verde": "#4CFF4C",
        "amarillo": "#FFFF4C",
        "azul": "#4C4CFF"
    }

    llegadas = {
    "rojo": [(8, y) for y in range(1, 9)],
    "verde": [(x, 8) for x in range(15, 7, -1)], 
    "amarillo": [(8, y) for y in range(15, 7, -1)],
    "azul": [(x, 8) for x in range(1, 9)], 
    "meta": [(8,8) for x in range(1)],
}

    def __init__(self, root):
        self.root = root
        self.root.title("Parchis UN")
        self.modo_var = tk.StringVar()
        self.menu()

    def dibujar_casilla(self, canvas, x, y, color="white", borde="black"):
        x0 = x * self.CASILLA
        y0 = y * self.CASILLA
        canvas.create_rectangle(x0, y0, x0 + self.CASILLA, y0 + self.CASILLA, fill=color, outline=borde)

    def dibujar_tablero(self, canvas):
        canvas.create_rectangle(0, 0, self.TAM_TABLERO, self.TAM_TABLERO, fill="white")

        for i, (x, y) in enumerate(self.camino_externo):
            self.dibujar_casilla(canvas, x, y, color="#CCCCCC")
            canvas.create_text((x + 0.5) * self.CASILLA, (y + 0.5) * self.CASILLA, text=str(i + 1), font=("Arial", 8))
        for color, indice in CASILLAS_SALIDA.items():
            if indice < len(self.camino_externo):
                x, y = self.camino_externo[indice]
                self.dibujar_casilla(canvas, x, y, color=self.COLORES[color], borde="black")
                canvas.create_text((x + 0.5) * self.CASILLA,(y + 0.5) * self.CASILLA,text="🚪",font=("Arial", 10, "bold"),fill="black")
        for color, casillas in self.llegadas.items():
            if color != "meta":
                for i, (x, y) in enumerate(casillas):
                    self.dibujar_casilla(canvas, x, y, color=self.COLORES[color])
                    canvas.create_text((x + 0.5) * self.CASILLA, (y + 0.5) * self.CASILLA, text=str(i + 1), font=("Arial", 7))
            else:
                self.dibujar_casilla(canvas, x, y, color="white")
                canvas.create_text((x + 0.5) * self.CASILLA,(y + 0.5) * self.CASILLA,text="🏁",font=("Arial", 14))

    def menu(self):
        #Modo de juego
        tk.Label(self.root, text="Seleccione un modo de juego:", font=("Arial", 12)).pack(pady=10)
        tk.Radiobutton(self.root, text="Modo REAL", variable=self.modo_var, value="real").pack()
        tk.Radiobutton(self.root, text="Modo Desarrollador", variable=self.modo_var, value="desarrollador").pack()
        #Botones inicio
        tk.Button(self.root, text="Iniciar Juego", command=self.iniciar_juego).pack(pady=10)
        tk.Button(self.root, text="Salir", command=self.root.quit).pack(pady=5)

    def mostrar_tablero(self):
        self.tablero = tk.Toplevel(self.root)
        self.tablero.title("Tablero de Juego")
        self.canvas = tk.Canvas(self.tablero, width=self.TAM_TABLERO, height=self.TAM_TABLERO)
        self.canvas.pack()

        self.mensaje_var = tk.StringVar()
        self.mensaje_label = tk.Label(self.tablero, textvariable=self.mensaje_var, font=("Arial", 12), fg="black")
        self.mensaje_label.pack(pady=5)

        tk.Button(self.tablero, text="Jugar Turno", command=self.turno).pack(pady=10)
        self.dibujar_tablero(self.canvas)
        self.actualizar_fichas()

    def iniciar_juego(self):
        modo = self.modo_var.get()
        if not modo:
            messagebox.showwarning("Selecciona un modo", "Por favor selecciona un modo de juego antes de iniciar.")
            return

        self.root.withdraw()
        self.juego = Juego(modo,mostrar_mensaje=self.mostrar_mensaje,seleccionar_ficha=self.mostrar_fichas_para_elegir,orden_dados=self.elegir_orden_dados, actualizar_gui=self.actualizar_fichas)
        self.mostrar_tablero()

    def turno(self):
        boton_turno = None
        for widget in self.tablero.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") == "Jugar Turno":
                widget.config(state="disabled")
                boton_turno = widget
                break

        jugador = self.juego.jugadores[self.juego.turno_actual]
        self.mostrar_mensaje(f"\n🎲 Turno de {jugador.color}")

        if self.juego.dado1.modo == "desarrollador":
            d1, d2 = self.elegir_orden_dados(1, 2)
            self.juego.dado1.set_valor_manual(d1)
            self.juego.dado2.set_valor_manual(d2)

        terminado = self.juego.jugar_turno()

        if terminado:
            messagebox.showinfo("Fin del Juego", f"¡El jugador {jugador.color} ha ganado!")
            self.tablero.destroy()
            self.root.quit()
            return

        self.actualizar_fichas()

        # Reactivar botón al final del turno solo si no terminó el juego
        if boton_turno:
            boton_turno.config(state="normal")

    def actualizar_fichas(self):
        self.canvas.delete("ficha")

        for jugador in self.juego.jugadores:
            for ficha in jugador.fichas:
                if ficha.posicion is None:
                    continue

                if ficha.en_llegada:
                    camino = CAMINOS_LLEGADA[ficha.color.lower()]
                    if ficha.pasos_llegada < len(camino):
                        x, y = camino[ficha.pasos_llegada]
                else:
                    if ficha.posicion is not None and ficha.posicion < len(self.camino_externo):
                        x, y = self.camino_externo[ficha.posicion]
                    else:
                        continue

                self.dibujar_ficha(x, y, ficha.color.lower(), ficha.id)

        for jugador in self.juego.jugadores:
            color = jugador.color.lower()
            en_carcel = [f for f in jugador.fichas if f.posicion is None]
            for i, ficha in enumerate(en_carcel):
                if i < 4:
                    x, y = self.zona_carcel[color][i]
                    self.dibujar_ficha(x, y, color, ficha.id)

    def dibujar_ficha(self, x, y, color, numero):
        x0 = x * self.CASILLA + 5
        y0 = y * self.CASILLA + 5
        x1 = x0 + self.CASILLA - 10
        y1 = y0 + self.CASILLA - 10
        self.canvas.create_oval(x0, y0, x1, y1, fill=self.COLORES[color], tags="ficha")
        self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(numero), tags="ficha")

    def mostrar_fichas_para_elegir(self, opciones, dado):
        seleccion = tk.StringVar()
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Mover ficha {dado} casillas")
        tk.Label(ventana, text="Selecciona una ficha:").pack(pady=10)

        for ficha in opciones:
            texto = f"Ficha {ficha.id} ({ficha.color})"
            boton = tk.Button(
                ventana,
                text=texto,
                command=lambda f=ficha: (seleccion.set(str(f.id)), ventana.destroy())
            )
            boton.pack(pady=2)

        self.root.wait_variable(seleccion)

        for ficha in opciones:
            if str(ficha.id) == seleccion.get():
                return ficha

        return None

    def mover_ficha_gui(self, ficha, dado, ventana):
        ventana.destroy()
        resultado = self.juego.tablero.mover_ficha(ficha, dado)
        self.juego.ultima_ficha_movida = ficha
        self.actualizar_fichas()
        self.jugar_turno()

    def elegir_orden_dados(self, d1, d2):
        if self.juego.dado1.modo == "desarrollador":
            ventana = tk.Toplevel(self.root)
            ventana.title("Modo desarrollador - Ingresar dados manualmente")

            tk.Label(ventana, text="Introduce el valor del primer dado:").pack(pady=5)
            entrada_d1 = tk.Entry(ventana)
            entrada_d1.pack()

            tk.Label(ventana, text="Introduce el valor del segundo dado:").pack(pady=5)
            entrada_d2 = tk.Entry(ventana)
            entrada_d2.pack()

            confirmado = tk.BooleanVar(value=False)

            def confirmar():
                try:
                    val1 = int(entrada_d1.get())
                    val2 = int(entrada_d2.get())
                    if not (1 <= val1 <= 6 and 1 <= val2 <= 6):
                        raise ValueError
                    self.dado_dev1 = val1
                    self.dado_dev2 = val2
                    confirmado.set(True)
                    ventana.destroy()
                except ValueError:
                    messagebox.showerror("Entrada inválida", "Los valores deben ser números entre 1 y 6.")

            tk.Button(ventana, text="Confirmar", command=confirmar).pack(pady=10)

            self.root.wait_variable(confirmado)
            return self.dado_dev1, self.dado_dev2
        else:
            jugador = self.juego.jugadores[self.juego.turno_actual]
            fichas_jugables = [
                f for f in jugador.fichas if f.posicion is not None
            ]

            # Si todas están en la cárcel, no mostrar ventana (el orden da igual)
            if not fichas_jugables:
                return d1, d2 if d1 == d2 else (d1, d2)
            if d1 == d2:
                return d1, d2

            ventana = tk.Toplevel(self.root)
            ventana.title("Elegir orden de dados")
            seleccion = tk.StringVar(value="1")

            tk.Label(ventana, text="¿Con qué dado deseas mover primero?").pack(pady=10)
            tk.Radiobutton(ventana, text=f"{d1} primero", variable=seleccion, value="1").pack()
            tk.Radiobutton(ventana, text=f"{d2} primero", variable=seleccion, value="2").pack()

            confirmado = tk.BooleanVar(value=False)

            def confirmar():
                confirmado.set(True)
                ventana.destroy()

            tk.Button(ventana, text="Confirmar", command=confirmar).pack(pady=10)
            self.root.wait_variable(confirmado)

            return (d1, d2) if seleccion.get() == "1" else (d2, d1)
    
    def mostrar_mensaje(self, texto):
        self.mensaje_var.set(texto)

        if not self.tablero or not self.tablero.winfo_exists():
            return

        continuar = tk.BooleanVar()
        boton = tk.Button(self.tablero, text="Continuar", command=lambda: continuar.set(True))
        boton.pack(pady=5)

        self.tablero.wait_variable(continuar)
        boton.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Visual(root)
    root.mainloop()
