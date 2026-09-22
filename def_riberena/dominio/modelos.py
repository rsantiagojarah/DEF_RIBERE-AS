"""Modelos de datos del dominio."""

from dataclasses import dataclass, field

from def_riberena.dominio.tipos import TipoFlujo, TipoSuelo


@dataclass
class DatosProyecto:
    """Datos generales del proyecto."""

    nombre_seccion: str = "RIO CHAUPIHURANGA"
    sector: str = "0+000 km al 0+400 km"


@dataclass
class DatosHidrologicos:
    """Parámetros hidrológicos de diseño."""

    caudal_diseno: float = 147.20
    pendiente: float = 0.09
    periodo_retorno: float = 100.0


@dataclass
class DatosGeometricos:
    """Parametros geometricos del tramo."""

    ancho_fondo: float = 24.2
    talud_borde: float = 0.5


@dataclass
class DatosAnchoCauce:
    """Parametros de tablas para el calculo del ancho estable."""

    indice_condicion_fondo_k1: int = 3
    descripcion_k1: str = "Fondo y orillas de grava"
    coeficiente_k1: float = 2.90

    indice_factor_fondo_fb: int = 1
    descripcion_fb: str = "Material fino"
    factor_fondo_fb: float = 0.80

    indice_factor_orilla_fs: int = 1
    descripcion_fs: str = "Materiales sueltos"
    factor_orilla_fs: float = 0.10

    indice_material_cauce_k: int = 3
    descripcion_material_k: str = "Material aluvial"
    coeficiente_material_k: float = 12.0

    indice_tipo_rio_m: int = 1
    descripcion_tipo_rio: str = "Para rios de montana"
    coeficiente_tipo_rio_m: float = 0.5


@dataclass
class DatosSuelo:
    """Propiedades del suelo del lecho."""

    tipo_suelo: TipoSuelo = TipoSuelo.NO_COHESIVO
    diametro_medio_mm: float = 50.0
    peso_especifico_tn_m3: float = 1.52


@dataclass
class DatosRugosidad:
    """Coeficientes de rugosidad segun tipo de cauce natural."""

    indice_tipo_cauce: int = 4
    descripcion_cauce: str = "Cauces naturales con derrubio e irregularidades"
    coeficiente_strickler: float = 30.0
    coeficiente_manning: float = 0.033


@dataclass
class DatosEnrocado:
    """Parametros para el calculo del diametro de roca (Maynord)."""

    indice_coeficiente_c1: int = 1
    descripcion_c1: str = "Fondo plano"
    coeficiente_c1: float = 0.25

    indice_coeficiente_c2: int = 1
    descripcion_c2: str = "Tramos en curva"
    coeficiente_c2: float = 1.50


@dataclass
class DatosEstructurales:
    """Parámetros estructurales de la defensa."""

    factor_seguridad_puna: float = 1.5
    redondeo_puna_m: float = 0.10


@dataclass
class DatosEntrada:
    """Conjunto de datos de entrada al motor."""

    proyecto: DatosProyecto = field(default_factory=DatosProyecto)
    hidrologia: DatosHidrologicos = field(default_factory=DatosHidrologicos)
    geometria: DatosGeometricos = field(default_factory=DatosGeometricos)
    ancho_cauce: DatosAnchoCauce = field(default_factory=DatosAnchoCauce)
    suelo: DatosSuelo = field(default_factory=DatosSuelo)
    rugosidad: DatosRugosidad = field(default_factory=DatosRugosidad)
    enrocado: DatosEnrocado = field(default_factory=DatosEnrocado)
    estructural: DatosEstructurales = field(default_factory=DatosEstructurales)


@dataclass
class AnchosEquilibrio:
    """Anchos de equilibrio por metodo (superficie o fondo)."""

    simons_henderson: float
    pettis: float
    altunin_manning: float
    blench: float
    recomendacion_practica: float


@dataclass
class ResultadoAnchoCauce:
    """Resultados de los metodos de ancho estable."""

    equilibrio_superficie: AnchosEquilibrio
    equilibrio_fondo: AnchosEquilibrio
    ancho_fondo: float
    ancho_efectivo: float


@dataclass
class ResultadoHidraulico:
    """Resultados hidraulicos del tramo."""

    ancho_fondo: float
    ancho_efectivo: float
    tirante: float
    area_mojada: float
    perimetro_mojado: float
    radio_hidraulico: float
    velocidad_media: float
    profundidad_hidraulica: float
    numero_froude: float
    tipo_flujo: TipoFlujo
    carga_cinetica: float
    coeficiente_phi: float
    bordo_libre: float
    altura_muro: float


@dataclass
class ResultadoSocavacion:
    """Resultados del método Lischtvan-Lebediev."""

    coeficiente_contraccion: float
    coeficiente_beta: float
    exponente_x: float
    factor_uno_sobre_x_mas_uno: float
    coeficiente_alfa: float
    tirante_socavado: float
    profundidad_socavacion: float


@dataclass
class ResultadoEnrocado:
    """Resultados del cálculo del enrocado."""

    factor_intensidad: float
    diametro_d50: float
    profundidad_puna: float
    ancho_superior_puna: float
    ancho_inferior_puna: float


@dataclass
class ResultadoCalculo:
    """Resultado integral del motor de cálculo."""

    ancho_cauce: ResultadoAnchoCauce
    hidraulica: ResultadoHidraulico
    socavacion: ResultadoSocavacion
    enrocado: ResultadoEnrocado
