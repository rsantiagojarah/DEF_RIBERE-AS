"""Cálculo del enrocado: Maynord y profundidad de uña."""

import math

from def_riberena.dominio.modelos import (
    DatosEntrada,
    ResultadoEnrocado,
    ResultadoHidraulico,
    ResultadoSocavacion,
)
from def_riberena.motor.constantes import GRAVEDAD


def calcular_factor_intensidad_maynord(
    velocidad: float,
    profundidad_hidraulica: float,
    coeficiente_c2: float,
) -> float:
    """F = C2 * V / sqrt(g * y)."""
    return coeficiente_c2 * velocidad / math.sqrt(GRAVEDAD * profundidad_hidraulica)


def calcular_diametro_d50(
    tirante: float,
    coeficiente_c1: float,
    factor_intensidad: float,
) -> float:
    """d50 = t * C1 * F^3 (Fórmula de Maynord)."""
    return tirante * coeficiente_c1 * (factor_intensidad ** 3)


def redondear_superior(valor: float, paso: float) -> float:
    """Redondea hacia arriba al múltiplo de `paso` más cercano."""
    if paso <= 0:
        return valor
    return math.ceil(valor / paso) * paso


def calcular_enrocado(
    datos: DatosEntrada,
    hidraulica: ResultadoHidraulico,
    socavacion: ResultadoSocavacion,
) -> ResultadoEnrocado:
    """Calcula diámetro de roca y profundidad de uña."""
    factor = calcular_factor_intensidad_maynord(
        hidraulica.velocidad_media,
        hidraulica.profundidad_hidraulica,
        datos.enrocado.coeficiente_c2,
    )

    diametro = calcular_diametro_d50(
        hidraulica.tirante,
        datos.enrocado.coeficiente_c1,
        factor,
    )

    profundidad_calculada = datos.estructural.factor_seguridad_puna * socavacion.profundidad_socavacion
    profundidad_puna = redondear_superior(
        profundidad_calculada,
        datos.estructural.redondeo_puna_m,
    )

    return ResultadoEnrocado(
        factor_intensidad=factor,
        diametro_d50=diametro,
        profundidad_puna=profundidad_puna,
        ancho_superior_puna=1.5 * profundidad_puna,
        ancho_inferior_puna=profundidad_puna,
    )
