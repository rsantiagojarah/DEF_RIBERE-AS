"""Tablas para el calculo del ancho estable de cauce."""

from dataclasses import dataclass

from def_riberena.utilidades.interpolacion import interpolar_lineal


@dataclass(frozen=True)
class OpcionTabla:
    """Opcion seleccionable de una tabla normativa."""

    indice: int
    descripcion: str
    valor: float


# Condiciones de fondo de rio - K1 (Simons y Henderson)
CONDICIONES_FONDO_K1 = (
    OpcionTabla(1, "Fondo arena y orillas de material cohesivo", 4.20),
    OpcionTabla(2, "Fondo y orillas de material cohesivo", 3.60),
    OpcionTabla(3, "Fondo y orillas de grava", 2.90),
    OpcionTabla(4, "Fondo arena y orillas material no cohesivo", 2.80),
)

# Factor de fondo Fb (Blench)
FACTORES_FONDO_FB = (
    OpcionTabla(1, "Material fino", 0.80),
    OpcionTabla(2, "Material grueso", 1.20),
)

# Factor de orilla Fs (Blench)
FACTORES_ORILLA_FS = (
    OpcionTabla(1, "Materiales sueltos", 0.10),
    OpcionTabla(2, "Materiales ligeramente cohesivos", 0.20),
    OpcionTabla(3, "Materiales cohesivos", 0.30),
)

# Coeficiente material del cauce K (Altunin - Manning)
MATERIALES_CAUCE_K = (
    OpcionTabla(1, "Material de cauce muy resistente", 3.0),
    OpcionTabla(2, "Material facilmente erosionable", 16.0),
    OpcionTabla(3, "Material aluvial", 12.0),
    OpcionTabla(4, "Valor practico", 10.0),
)

# Coeficiente tipo de rio m (Altunin - Manning)
TIPOS_RIO_M = (
    OpcionTabla(1, "Para rios de montana", 0.5),
    OpcionTabla(2, "Para cauces arenosos", 0.7),
    OpcionTabla(3, "Para cauces aluviales", 1.0),
)

# Recomendacion practica: caudal Q (m3/s) vs ancho B2 (m)
_RECOMENDACION_Q_ANCHO = (
    (100.0, 70.0),
    (500.0, 70.0),
    (1000.0, 100.0),
    (1500.0, 120.0),
    (2400.0, 190.0),
    (3000.0, 200.0),
)

INDICE_K1_DEFECTO = 3
INDICE_FB_DEFECTO = 1
INDICE_FS_DEFECTO = 1
INDICE_K_DEFECTO = 3
INDICE_M_DEFECTO = 1


def _obtener_opcion(opciones: tuple[OpcionTabla, ...], indice: int) -> OpcionTabla:
    for opcion in opciones:
        if opcion.indice == indice:
            return opcion
    maximo = len(opciones)
    raise ValueError(f"Indice invalido: {indice}. Use un valor entre 1 y {maximo}.")


def obtener_condicion_fondo_k1(indice: int) -> OpcionTabla:
    return _obtener_opcion(CONDICIONES_FONDO_K1, indice)


def obtener_factor_fondo_fb(indice: int) -> OpcionTabla:
    return _obtener_opcion(FACTORES_FONDO_FB, indice)


def obtener_factor_orilla_fs(indice: int) -> OpcionTabla:
    return _obtener_opcion(FACTORES_ORILLA_FS, indice)


def obtener_material_cauce_k(indice: int) -> OpcionTabla:
    return _obtener_opcion(MATERIALES_CAUCE_K, indice)


def obtener_tipo_rio_m(indice: int) -> OpcionTabla:
    return _obtener_opcion(TIPOS_RIO_M, indice)


def obtener_ancho_recomendacion_practica(caudal: float) -> float:
    """Obtiene B2 de la tabla de recomendacion practica con interpolacion lineal."""
    return interpolar_lineal(caudal, list(_RECOMENDACION_Q_ANCHO))
