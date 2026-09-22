"""Tablas de coeficientes C1 y C2 para la formula de Maynord."""

from def_riberena.datos.tablas_ancho_cauce import OpcionTabla

# Coeficiente C1 segun geometria de la proteccion
COEFICIENTES_C1 = (
    OpcionTabla(1, "Fondo plano", 0.25),
    OpcionTabla(2, "Talud 1V:3H", 0.28),
    OpcionTabla(3, "Talud 1V:2H", 0.32),
)

# Coeficiente C2 segun ubicacion de la roca
COEFICIENTES_C2 = (
    OpcionTabla(1, "Tramos en curva", 1.50),
    OpcionTabla(2, "Tramos rectos", 1.25),
)

INDICE_C1_DEFECTO = 1
INDICE_C2_DEFECTO = 1


def obtener_coeficiente_c1(indice: int) -> OpcionTabla:
    """Obtiene C1 por indice (1-3)."""
    for opcion in COEFICIENTES_C1:
        if opcion.indice == indice:
            return opcion
    raise ValueError(f"Indice C1 invalido: {indice}. Use un valor entre 1 y 3.")


def obtener_coeficiente_c2(indice: int) -> OpcionTabla:
    """Obtiene C2 por indice (1-2)."""
    for opcion in COEFICIENTES_C2:
        if opcion.indice == indice:
            return opcion
    raise ValueError(f"Indice C2 invalido: {indice}. Use un valor entre 1 y 2.")
