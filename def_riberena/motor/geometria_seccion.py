"""Relaciones geometricas de la seccion trapezoidal."""


def calcular_ancho_efectivo(ancho_fondo: float, tirante: float, talud: float) -> float:
    """Ancho efectivo a superficie: B_ef = B_fondo + 2*Z*t."""
    return ancho_fondo + 2.0 * talud * tirante


def calcular_ancho_fondo_desde_superficie(
    ancho_superficie: float,
    tirante: float,
    talud: float,
) -> float:
    """Convierte ancho de equilibrio en superficie a ancho de fondo."""
    return max(ancho_superficie - 2.0 * talud * tirante, 0.0)
