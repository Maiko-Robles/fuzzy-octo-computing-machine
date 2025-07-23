NUM_CASILLAS_TABLERO = 68
NUM_CASILLAS = NUM_CASILLAS_TABLERO

NUM_CASILLAS_LLEGADA = 8

COLORES = ['rojo', 'azul', 'verde', 'amarillo']

FICHAS_POR_JUGADOR = 4

MAX_FICHAS_POR_CASILLA = 2

VALOR_SALIDA = 5

MOV_EXTRA_CAPTURA = 20
MOV_EXTRA_LLEGADA = 10

CASILLAS_SALIDA = {
    "azul": 6,
    "rojo": 23,
    "verde": 40,
    "amarillo": 57
}

ENTRADAS_LLEGADA = {
    "azul": 0,
    "rojo": 17,
    "verde": 34,
    "amarillo": 51
}

# Caminos de llegada (internos) por color
CAMINOS_LLEGADA = {
    "azul": list(range(69, 76)),
    "rojo": list(range(76, 83)),
    "verde": list(range(83, 90)),
    "amarillo": list(range(90, 97))
}

# Índice final de meta
CASILLA_META = 96

