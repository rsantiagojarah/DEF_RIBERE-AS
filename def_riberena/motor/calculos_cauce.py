"""Calculo del ancho estable de cauce."""

import math

from def_riberena.datos.tablas_ancho_cauce import obtener_ancho_recomendacion_practica
from def_riberena.dominio.modelos import AnchosEquilibrio, DatosEntrada, ResultadoAnchoCauce
from def_riberena.motor.geometria_seccion import (
    calcular_ancho_efectivo,
    calcular_ancho_fondo_desde_superficie,
)


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


def _calcular_anchos_superficie(datos: DatosEntrada) -> AnchosEquilibrio:
    """Calcula anchos de equilibrio a nivel de superficie del agua."""
    caudal = datos.hidrologia.caudal_diseno
    pendiente = datos.hidrologia.pendiente
    parametros = datos.ancho_cauce

    return AnchosEquilibrio(
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
    )


def _convertir_equilibrio_a_fondo(
    equilibrio_superficie: AnchosEquilibrio,
    tirante: float,
    talud: float,
) -> AnchosEquilibrio:
    """Convierte anchos de equilibrio de superficie a fondo usando Z y t."""

    def convertir(ancho_superficie: float) -> float:
        return calcular_ancho_fondo_desde_superficie(ancho_superficie, tirante, talud)

    return AnchosEquilibrio(
        simons_henderson=convertir(equilibrio_superficie.simons_henderson),
        pettis=convertir(equilibrio_superficie.pettis),
        altunin_manning=convertir(equilibrio_superficie.altunin_manning),
        blench=convertir(equilibrio_superficie.blench),
        recomendacion_practica=convertir(equilibrio_superficie.recomendacion_practica),
    )


def calcular_ancho_cauce(
    datos: DatosEntrada,
    tirante: float,
) -> ResultadoAnchoCauce:
    """Calcula anchos de equilibrio y compara con el tramo adoptado."""
    talud = datos.geometria.talud_borde
    ancho_fondo = datos.geometria.ancho_fondo
    ancho_efectivo = calcular_ancho_efectivo(ancho_fondo, tirante, talud)

    equilibrio_superficie = _calcular_anchos_superficie(datos)
    equilibrio_fondo = _convertir_equilibrio_a_fondo(equilibrio_superficie, tirante, talud)

    return ResultadoAnchoCauce(
        equilibrio_superficie=equilibrio_superficie,
        equilibrio_fondo=equilibrio_fondo,
        ancho_fondo=ancho_fondo,
        ancho_efectivo=ancho_efectivo,
    )
