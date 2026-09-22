"""Cálculo del ancho estable de cauce."""

import math

from def_riberena.datos.tablas_ancho_cauce import obtener_ancho_recomendacion_practica
from def_riberena.dominio.modelos import DatosEntrada, ResultadoAnchoCauce


def calcular_simons_henderson(caudal: float, coeficiente_k1: float) -> float:
    """B = K1 * Q^(1/2)."""
    return coeficiente_k1 * math.sqrt(caudal)


def calcular_pettis(caudal: float) -> float:
    """B = 4.44 * Q^(1/2)."""
    return 4.44 * math.sqrt(caudal)


def calcular_altunin_manning(
    caudal: float,
    pendiente: float,
    coeficiente_manning: float,
    coeficiente_material_k: float,
    coeficiente_tipo_rio_m: float,
) -> float:
    """B = (Q^(1/2) / S^(1/5)) * (n * K^(5/3))^(3/(3+5m))."""
    exponente = 3.0 / (3.0 + 5.0 * coeficiente_tipo_rio_m)
    factor = (coeficiente_manning * (coeficiente_material_k ** (5.0 / 3.0))) ** exponente
    return (math.sqrt(caudal) / (pendiente ** 0.2)) * factor


def calcular_blench(caudal: float, factor_fondo: float, factor_orilla: float) -> float:
    """B = 1.81 * sqrt(Q * Fb / Fs)."""
    return 1.81 * math.sqrt(caudal * factor_fondo / factor_orilla)


def calcular_ancho_cauce(datos: DatosEntrada) -> ResultadoAnchoCauce:
    """Calcula y compara los métodos de ancho estable."""
    caudal = datos.hidrologia.caudal_diseno
    pendiente = datos.hidrologia.pendiente
    parametros = datos.ancho_cauce

    return ResultadoAnchoCauce(
        simons_henderson=calcular_simons_henderson(caudal, parametros.coeficiente_k1),
        pettis=calcular_pettis(caudal),
        altunin_manning=calcular_altunin_manning(
            caudal,
            pendiente,
            datos.rugosidad.coeficiente_manning,
            parametros.coeficiente_material_k,
            parametros.coeficiente_tipo_rio_m,
        ),
        blench=calcular_blench(
            caudal,
            parametros.factor_fondo_fb,
            parametros.factor_orilla_fs,
        ),
        recomendacion_practica=obtener_ancho_recomendacion_practica(caudal),
        ancho_adoptado=datos.geometria.ancho_adoptado,
    )
