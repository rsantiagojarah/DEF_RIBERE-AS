"""Calculos hidraulicos: tirante, velocidad y bordo libre."""

import math

from def_riberena.dominio.modelos import DatosEntrada, ResultadoHidraulico
from def_riberena.dominio.tipos import TipoFlujo
from def_riberena.datos.tablas import obtener_coeficiente_phi
from def_riberena.motor.constantes import GRAVEDAD
from def_riberena.motor.geometria_seccion import calcular_ancho_efectivo


def calcular_caudal_strickler_trapezoidal(
    ancho_fondo: float,
    tirante: float,
    talud: float,
    pendiente: float,
    coeficiente_strickler: float,
) -> float:
    """
    Caudal por Strickler en seccion trapezoidal.

    Q = Ks * A * R^(2/3) * S^(1/2)
    A = (B + Z*t) * t
    P = B + 2*t*sqrt(1 + Z^2)
    B = ancho de fondo
    """
    if tirante <= 0 or ancho_fondo <= 0:
        return 0.0

    area = (ancho_fondo + talud * tirante) * tirante
    perimetro = ancho_fondo + 2.0 * tirante * math.sqrt(1.0 + talud ** 2)
    if perimetro <= 0:
        return 0.0

    radio = area / perimetro
    return coeficiente_strickler * area * (radio ** (2.0 / 3.0)) * math.sqrt(pendiente)


def _resolver_tirante_biseccion(
    caudal_objetivo: float,
    evaluar_caudal,
    tirante_minimo: float,
    tirante_maximo: float,
) -> float:
    """Resuelve t por biseccion donde evaluar_caudal(t) = caudal_objetivo."""
    t_bajo = tirante_minimo
    t_alto = tirante_maximo
    q_bajo = evaluar_caudal(t_bajo)
    q_alto = evaluar_caudal(t_alto)

    if q_bajo > q_alto:
        t_bajo, t_alto = t_alto, t_bajo
        q_bajo, q_alto = q_alto, q_bajo

    if caudal_objetivo <= q_bajo:
        return t_bajo
    if caudal_objetivo >= q_alto:
        return t_alto

    for _ in range(80):
        t_medio = (t_bajo + t_alto) / 2.0
        q_medio = evaluar_caudal(t_medio)
        if abs(q_medio - caudal_objetivo) < 1e-6 or (t_alto - t_bajo) < 1e-8:
            return t_medio
        if q_medio < caudal_objetivo:
            t_bajo = t_medio
        else:
            t_alto = t_medio

    return (t_bajo + t_alto) / 2.0


def calcular_tirante_strickler_trapezoidal(
    caudal: float,
    ancho_fondo: float,
    talud: float,
    pendiente: float,
    coeficiente_strickler: float,
) -> float:
    """
    Obtiene t con Strickler trapezoidal y B de fondo.

    Resuelve Q = Ks * ((B + Zt)t) * (((B + Zt)t) / (B + 2t*sqrt(1 + Z^2)))^(2/3) * S^(1/2)
    """
    if ancho_fondo <= 0:
        raise ValueError("El ancho de fondo debe ser mayor que cero.")

    tirante_maximo = max(10.0, ancho_fondo * 2.0)

    def evaluar(t: float) -> float:
        return calcular_caudal_strickler_trapezoidal(
            ancho_fondo,
            t,
            talud,
            pendiente,
            coeficiente_strickler,
        )

    pasos = 200
    t_prev = 1e-4
    q_prev = evaluar(t_prev)

    for indice in range(1, pasos + 1):
        t_curr = tirante_maximo * indice / pasos
        q_curr = evaluar(t_curr)
        if (q_prev - caudal) * (q_curr - caudal) <= 0:
            return _resolver_tirante_biseccion(caudal, evaluar, t_prev, t_curr)
        t_prev, q_prev = t_curr, q_curr

    raise ValueError("No se encontro tirante hidraulico para el caudal y la seccion dados.")


def calcular_geometria_trapezoidal(
    ancho_fondo: float,
    ancho_efectivo: float,
    tirante: float,
    talud: float,
) -> tuple[float, float, float, float]:
    """
    Calcula geometria trapezoidal a partir del ancho de fondo.

    A = (B + Z*t) * t
    P = B + 2*t*sqrt(1 + Z^2)
    y = A / B_efectivo
    R = A / P
    """
    area = (ancho_fondo + talud * tirante) * tirante
    perimetro = ancho_fondo + 2.0 * tirante * math.sqrt(1.0 + talud ** 2)
    radio = area / perimetro if perimetro > 0 else 0.0
    profundidad_hidraulica = area / ancho_efectivo if ancho_efectivo > 0 else tirante
    return area, perimetro, radio, profundidad_hidraulica


def calcular_velocidad_manning(radio: float, pendiente: float, coeficiente_manning: float) -> float:
    """V = R^(2/3) * S^(1/2) / n."""
    return (radio ** (2.0 / 3.0)) * math.sqrt(pendiente) / coeficiente_manning


def clasificar_flujo(numero_froude: float) -> TipoFlujo:
    """Clasifica el regimen segun el numero de Froude."""
    if numero_froude < 0.95:
        return TipoFlujo.SUBCRITICO
    if numero_froude <= 1.05:
        return TipoFlujo.CRITICO
    return TipoFlujo.SUPERCRITICO


def calcular_hidraulica(datos: DatosEntrada) -> ResultadoHidraulico:
    """Ejecuta el calculo hidraulico completo del tramo."""
    caudal = datos.hidrologia.caudal_diseno
    pendiente = datos.hidrologia.pendiente
    ancho_fondo = datos.geometria.ancho_fondo
    talud = datos.geometria.talud_borde

    tirante = calcular_tirante_strickler_trapezoidal(
        caudal,
        ancho_fondo,
        talud,
        pendiente,
        datos.rugosidad.coeficiente_strickler,
    )

    ancho_efectivo = calcular_ancho_efectivo(ancho_fondo, tirante, talud)
    area, perimetro, radio, profundidad_hidraulica = calcular_geometria_trapezoidal(
        ancho_fondo,
        ancho_efectivo,
        tirante,
        talud,
    )
    velocidad = calcular_velocidad_manning(radio, pendiente, datos.rugosidad.coeficiente_manning)

    numero_froude = velocidad / math.sqrt(GRAVEDAD * profundidad_hidraulica)
    carga_cinetica = velocidad ** 2 / (2.0 * GRAVEDAD)
    coeficiente_phi = obtener_coeficiente_phi(caudal)
    bordo_libre = coeficiente_phi * carga_cinetica
    altura_muro = tirante + bordo_libre

    return ResultadoHidraulico(
        ancho_fondo=ancho_fondo,
        ancho_efectivo=ancho_efectivo,
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
