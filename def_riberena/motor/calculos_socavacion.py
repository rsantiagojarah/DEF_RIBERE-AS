"""Cálculo de socavación (Método Lischtvan-Lebediev)."""

from def_riberena.datos.tablas import (
    clasificar_particula,
    obtener_coeficiente_beta,
    obtener_coeficiente_contraccion,
    obtener_exponente_x_cohesivo,
    obtener_exponente_x_no_cohesivo,
)
from def_riberena.dominio.modelos import DatosEntrada, ResultadoHidraulico, ResultadoSocavacion
from def_riberena.dominio.tipos import TipoSuelo


def calcular_coeficiente_alfa(
    caudal: float,
    tirante_medio: float,
    ancho: float,
    coeficiente_contraccion: float,
) -> float:
    """α = Q / (tm^(5/3) * B * μ)."""
    return caudal / (tirante_medio ** (5.0 / 3.0) * ancho * coeficiente_contraccion)


def calcular_tirante_socavado_no_cohesivo(
    coeficiente_alfa: float,
    tirante: float,
    diametro_mm: float,
    coeficiente_beta: float,
    exponente_x: float,
) -> float:
    """ts = (α * t^(5/3) / (0.68 * Dm^0.28 * β))^(1/(x+1))."""
    numerador = coeficiente_alfa * (tirante ** (5.0 / 3.0))
    denominador = 0.68 * (diametro_mm ** 0.28) * coeficiente_beta
    return (numerador / denominador) ** (1.0 / (exponente_x + 1.0))


def calcular_tirante_socavado_cohesivo(
    coeficiente_alfa: float,
    tirante: float,
    peso_especifico: float,
    coeficiente_beta: float,
    exponente_x: float,
) -> float:
    """ts = (α * t^(5/3) / (0.60 * γs^1.18 * β))^(1/(x+1))."""
    numerador = coeficiente_alfa * (tirante ** (5.0 / 3.0))
    denominador = 0.60 * (peso_especifico ** 1.18) * coeficiente_beta
    return (numerador / denominador) ** (1.0 / (exponente_x + 1.0))


def calcular_socavacion(
    datos: DatosEntrada,
    hidraulica: ResultadoHidraulico,
) -> ResultadoSocavacion:
    """Calcula la profundidad de socavación Hs."""
    caudal = datos.hidrologia.caudal_diseno
    # Ancho efectivo = adoptado = superficie del agua (T)
    ancho = datos.geometria.ancho_adoptado
    tirante = hidraulica.tirante
    tirante_medio = hidraulica.profundidad_hidraulica

    coeficiente_contraccion = obtener_coeficiente_contraccion(
        hidraulica.velocidad_media,
        ancho,
    )
    coeficiente_beta = obtener_coeficiente_beta(datos.hidrologia.periodo_retorno)

    if datos.suelo.tipo_suelo == TipoSuelo.COHESIVO:
        exponente_x, factor = obtener_exponente_x_cohesivo(datos.suelo.peso_especifico_tn_m3)
        tirante_socavado = calcular_tirante_socavado_cohesivo(
            calcular_coeficiente_alfa(caudal, tirante_medio, ancho, coeficiente_contraccion),
            tirante,
            datos.suelo.peso_especifico_tn_m3,
            coeficiente_beta,
            exponente_x,
        )
    else:
        exponente_x, factor = obtener_exponente_x_no_cohesivo(datos.suelo.diametro_medio_mm)
        clasificar_particula(datos.suelo.diametro_medio_mm)
        coeficiente_alfa = calcular_coeficiente_alfa(
            caudal,
            tirante_medio,
            ancho,
            coeficiente_contraccion,
        )
        tirante_socavado = calcular_tirante_socavado_no_cohesivo(
            coeficiente_alfa,
            tirante,
            datos.suelo.diametro_medio_mm,
            coeficiente_beta,
            exponente_x,
        )

    profundidad_socavacion = max(tirante_socavado - tirante, 0.0)

    return ResultadoSocavacion(
        coeficiente_contraccion=coeficiente_contraccion,
        coeficiente_beta=coeficiente_beta,
        exponente_x=exponente_x,
        factor_uno_sobre_x_mas_uno=factor,
        coeficiente_alfa=calcular_coeficiente_alfa(
            caudal,
            tirante_medio,
            ancho,
            coeficiente_contraccion,
        ),
        tirante_socavado=tirante_socavado,
        profundidad_socavacion=profundidad_socavacion,
    )
