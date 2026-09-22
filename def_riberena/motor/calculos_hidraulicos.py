"""Cálculos hidráulicos: tirante, velocidad y bordo libre."""

import math

from def_riberena.dominio.modelos import DatosEntrada, ResultadoHidraulico
from def_riberena.dominio.tipos import TipoFlujo
from def_riberena.datos.tablas import obtener_coeficiente_phi
from def_riberena.motor.constantes import GRAVEDAD


def calcular_tirante_strickler(
    caudal: float,
    coeficiente_strickler: float,
    ancho: float,
    pendiente: float,
) -> float:
    """t = (Q / (Ks * B * S^(1/2)))^(3/5)."""
    denominador = coeficiente_strickler * ancho * math.sqrt(pendiente)
    return (caudal / denominador) ** (3.0 / 5.0)


def calcular_geometria_trapezoidal(
    ancho: float,
    tirante: float,
    talud: float,
) -> tuple[float, float, float, float]:
    """
    Calcula geometria de seccion trapezoidal.

    Talud Z en formato H:V (horizontal : vertical).
    A = (B + Z*t) * t
    P = B + 2*t*sqrt(1 + Z^2)
    y = A / T,  con T = B + 2*Z*t
    R = A / P
    """
    area = (ancho + talud * tirante) * tirante
    perimetro = ancho + 2.0 * tirante * math.sqrt(1.0 + talud ** 2)
    ancho_superficial = ancho + 2.0 * talud * tirante
    radio = area / perimetro if perimetro > 0 else 0.0
    profundidad_hidraulica = area / ancho_superficial if ancho_superficial > 0 else tirante
    return area, perimetro, radio, profundidad_hidraulica


def calcular_velocidad_manning(radio: float, pendiente: float, coeficiente_manning: float) -> float:
    """V = R^(2/3) * S^(1/2) / n."""
    return (radio ** (2.0 / 3.0)) * math.sqrt(pendiente) / coeficiente_manning


def clasificar_flujo(numero_froude: float) -> TipoFlujo:
    """Clasifica el régimen según el número de Froude."""
    if numero_froude < 0.95:
        return TipoFlujo.SUBCRITICO
    if numero_froude <= 1.05:
        return TipoFlujo.CRITICO
    return TipoFlujo.SUPERCRITICO


def calcular_hidraulica(datos: DatosEntrada) -> ResultadoHidraulico:
    """Ejecuta el cálculo hidráulico completo del tramo."""
    caudal = datos.hidrologia.caudal_diseno
    pendiente = datos.hidrologia.pendiente
    ancho = datos.geometria.ancho_adoptado
    talud = datos.geometria.talud_borde

    tirante = calcular_tirante_strickler(
        caudal,
        datos.rugosidad.coeficiente_strickler,
        ancho,
        pendiente,
    )

    area, perimetro, radio, profundidad_hidraulica = calcular_geometria_trapezoidal(
        ancho, tirante, talud
    )
    velocidad = calcular_velocidad_manning(radio, pendiente, datos.rugosidad.coeficiente_manning)

    numero_froude = velocidad / math.sqrt(GRAVEDAD * profundidad_hidraulica)
    carga_cinetica = velocidad ** 2 / (2.0 * GRAVEDAD)
    coeficiente_phi = obtener_coeficiente_phi(caudal)
    bordo_libre = coeficiente_phi * carga_cinetica
    altura_muro = tirante + bordo_libre

    return ResultadoHidraulico(
        tirante=tirante,
        area_mojada=area,
        perimetro_mojado=perimetro,
        radio_hidraulico=radio,
        velocidad_media=velocidad,
        profundidad_hidraulica=profundidad_hidraulica,
        numero_froude=numero_froude,
        tipo_flujo=clasificar_flujo(numero_froude),
        carga_cinetica=carga_cinetica,
        coeficiente_phi=coeficiente_phi,
        bordo_libre=bordo_libre,
        altura_muro=altura_muro,
    )
