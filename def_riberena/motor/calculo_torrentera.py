"""Calculo trazable para torrentera recta con enrocado y uña enterrada."""

from dataclasses import dataclass
import math

from def_riberena.motor.calculos_hidraulicos import (
    calcular_tirante_strickler_trapezoidal,
)
from def_riberena.datos.tablas import (
    obtener_coeficiente_contraccion,
    obtener_coeficiente_beta,
    obtener_exponente_x_no_cohesivo,
)


@dataclass(frozen=True)
class DatosTorrentera:
    caudal: float
    periodo_retorno: float
    ancho_fondo: float
    talud_cauce: float
    pendiente: float
    coeficiente_manning: float
    talud_enrocado: float
    peso_especifico_roca: float
    peso_especifico_agua: float
    factor_talud_k1: float
    factor_turbulencia_roca: float
    dm_fondo_mm: float
    empotramiento_adicional: float
    talud_zanja_izq: float
    talud_zanja_der: float
    ancho_minimo_una: float
    longitud_defensa: float
    forma_roca: str = "angular"
    angulo_reposo_roca: float = 41.0


@dataclass(frozen=True)
class ResultadoTorrentera:
    tirante: float
    ancho_superficie: float
    area: float
    perimetro: float
    radio: float
    velocidad: float
    profundidad_hidraulica: float
    froude: float
    d50_requerido: float
    espesor_enrocado: float
    mu: float
    beta: float
    exponente_x: float
    tirante_socavado: float
    socavacion: float
    profundidad_una: float
    rq_roca_por_metro: float
    ancho_una_calculado: float
    ancho_una_adoptado: float
    area_una: float
    volumen_una: float


def _resolver_geometria(ancho_fondo: float, tirante: float, talud: float) -> tuple[float, float, float, float]:
    area = (ancho_fondo + talud * tirante) * tirante
    perimetro = ancho_fondo + 2.0 * tirante * math.sqrt(1.0 + talud ** 2)
    radio = area / perimetro
    ancho_superficie = ancho_fondo + 2.0 * talud * tirante
    return area, perimetro, radio, ancho_superficie


def calcular_k1_talud(talud_horizontal_vertical: float, angulo_reposo: float) -> float:
    """Calcula K1 con el talud de la defensa y el angulo de reposo de la roca.

    La expresion es K1 = sqrt(1 - sen(theta)^2 / sen(phi)^2), donde
    theta = atan(1/Zd). El talud se expresa como Zd horizontal:vertical.
    """
    if talud_horizontal_vertical <= 0:
        raise ValueError("El talud de la defensa debe ser mayor que cero.")
    if not 0 < angulo_reposo < 90:
        raise ValueError("El angulo de reposo debe estar entre 0 y 90 grados.")
    theta = math.atan(1.0 / talud_horizontal_vertical)
    phi = math.radians(angulo_reposo)
    termino = 1.0 - (math.sin(theta) ** 2) / (math.sin(phi) ** 2)
    if termino <= 0:
        raise ValueError("El talud es demasiado empinado para el angulo de reposo indicado.")
    return math.sqrt(termino)


def calcular_d50_manual(velocidad: float, datos: DatosTorrentera) -> float:
    """Calcula D50 con la formula de estabilidad del manual."""
    delta = (
        datos.peso_especifico_roca - datos.peso_especifico_agua
    ) / datos.peso_especifico_agua
    if velocidad < 0 or delta <= 0:
        raise ValueError("La velocidad debe ser valida y la roca debe pesar mas que el agua.")
    if datos.factor_turbulencia_roca <= 0:
        raise ValueError("El factor b de turbulencia debe ser mayor que cero.")
    return math.sqrt(
        (datos.factor_turbulencia_roca / delta)
        * (velocidad ** 2 / (2.0 * 9.81))
        / datos.factor_talud_k1
    )


def calcular_torrentera(datos: DatosTorrentera) -> ResultadoTorrentera:
    """Calcula D50, espesor y uña enterrada para la torrentera."""
    ks = 1.0 / datos.coeficiente_manning
    tirante = calcular_tirante_strickler_trapezoidal(
        datos.caudal,
        datos.ancho_fondo,
        datos.talud_cauce,
        datos.pendiente,
        ks,
    )
    area, perimetro, radio, ancho_superficie = _resolver_geometria(
        datos.ancho_fondo, tirante, datos.talud_cauce
    )
    velocidad = datos.caudal / area
    profundidad_hidraulica = area / ancho_superficie
    froude = velocidad / math.sqrt(9.81 * profundidad_hidraulica)

    d50_requerido = calcular_d50_manual(velocidad, datos)
    espesor = 1.5 * d50_requerido

    mu = obtener_coeficiente_contraccion(velocidad, ancho_superficie)
    beta = obtener_coeficiente_beta(datos.periodo_retorno)
    x, _ = obtener_exponente_x_no_cohesivo(datos.dm_fondo_mm)
    alpha = datos.caudal / (profundidad_hidraulica ** (5.0 / 3.0) * ancho_superficie * mu)
    tirante_socavado = (
        alpha * tirante ** (5.0 / 3.0)
        / (0.68 * datos.dm_fondo_mm ** 0.28 * beta)
    ) ** (1.0 / (x + 1.0))
    socavacion = max(tirante_socavado - tirante, 0.0)

    profundidad_una = socavacion + datos.empotramiento_adicional
    rq = 1.5 * socavacion * espesor * math.sqrt(1.0 + datos.talud_enrocado ** 2)
    ancho_una_calculado = rq / profundidad_una - 0.5 * profundidad_una * (
        datos.talud_zanja_izq + datos.talud_zanja_der
    )
    ancho_una_adoptado = max(ancho_una_calculado, datos.ancho_minimo_una)
    area_una = profundidad_una * (
        ancho_una_adoptado
        + 0.5 * profundidad_una * (datos.talud_zanja_izq + datos.talud_zanja_der)
    )
    return ResultadoTorrentera(
        tirante=tirante,
        ancho_superficie=ancho_superficie,
        area=area,
        perimetro=perimetro,
        radio=radio,
        velocidad=velocidad,
        profundidad_hidraulica=profundidad_hidraulica,
        froude=froude,
        d50_requerido=d50_requerido,
        espesor_enrocado=espesor,
        mu=mu,
        beta=beta,
        exponente_x=x,
        tirante_socavado=tirante_socavado,
        socavacion=socavacion,
        profundidad_una=profundidad_una,
        rq_roca_por_metro=rq,
        ancho_una_calculado=ancho_una_calculado,
        ancho_una_adoptado=ancho_una_adoptado,
        area_una=area_una,
        volumen_una=area_una * datos.longitud_defensa,
    )
