"""Tablas normativas de la memoria de cálculo."""

from def_riberena.utilidades.interpolacion import interpolar_bilineal, interpolar_lineal

# Tabla N° 01: Coeficiente de contracción μ (Velocidad m/s vs. longitud libre B m)
_VELOCIDADES_MU = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
_LONGITUDES_MU = [10, 13, 16, 18, 21, 25, 30, 42, 52, 63, 106, 124, 200]

# Valores calibrados segun Tabla N 01 de la memoria (ej.: V=3.314, B=25 -> mu=0.950)
_MATRIZ_MU = [
    [0.96, 0.96, 0.97, 0.97, 0.97, 0.98, 0.98, 0.99, 0.99, 0.99, 1.00, 1.00, 1.00],
    [0.95, 0.95, 0.96, 0.96, 0.96, 0.97, 0.97, 0.98, 0.98, 0.98, 0.99, 0.99, 1.00],
    [0.93, 0.93, 0.94, 0.94, 0.95, 0.96, 0.96, 0.97, 0.97, 0.97, 0.98, 0.98, 0.99],
    [0.91, 0.91, 0.92, 0.92, 0.93, 0.955, 0.955, 0.96, 0.96, 0.96, 0.97, 0.97, 0.98],
    [0.89, 0.89, 0.90, 0.90, 0.91, 0.950, 0.950, 0.95, 0.95, 0.95, 0.96, 0.96, 0.97],
    [0.87, 0.87, 0.88, 0.88, 0.89, 0.945, 0.945, 0.94, 0.94, 0.94, 0.95, 0.95, 0.96],
    [0.85, 0.85, 0.86, 0.86, 0.87, 0.940, 0.940, 0.92, 0.92, 0.92, 0.94, 0.94, 0.95],
]

# Tabla N° 03: exponente x para suelos no cohesivos (D mm)
_EXPONENTE_X_NO_COHESIVO = [
    (0.05, 0.43),
    (0.15, 0.42),
    (0.50, 0.41),
    (1.00, 0.40),
    (1.50, 0.39),
    (2.50, 0.38),
    (4.00, 0.37),
    (6.00, 0.36),
    (8.00, 0.35),
    (10.00, 0.34),
    (15.00, 0.33),
    (20.00, 0.32),
    (25.00, 0.31),
    (40.00, 0.30),
    (60.00, 0.29),
    (90.00, 0.28),
    (140.00, 0.26),
    (190.00, 0.25),
    (250.00, 0.24),
    (310.00, 0.23),
    (370.00, 0.22),
    (450.00, 0.21),
    (570.00, 0.20),
    (750.00, 0.19),
    (1000.00, 0.19),
]

# Tabla N° 03: exponente x para suelos cohesivos (γs Tn/m³)
_EXPONENTE_X_COHESIVO = [
    (0.80, 0.52),
    (1.00, 0.44),
    (1.20, 0.39),
    (1.52, 0.33),
    (1.80, 0.29),
    (2.00, 0.27),
]

# Tabla N° 04: coeficiente β por periodo de retorno (años)
_COEFICIENTE_BETA = [
    (0.0, 0.77),
    (2.0, 0.82),
    (5.0, 0.86),
    (10.0, 0.90),
    (20.0, 0.94),
    (50.0, 0.97),
    (100.0, 1.00),
    (300.0, 1.03),
    (500.0, 1.05),
    (1000.0, 1.07),
]

# Tabla N° 02: clasificación por tamaño de partícula (mm)
_CLASIFICACION_PARTICULAS = [
    (4000, 2000, "Canto rodado muy grande"),
    (2000, 1000, "Canto rodado grande"),
    (1000, 500, "Canto rodado medio"),
    (500, 250, "Canto rodado pequeño"),
    (250, 130, "Cascajo grande"),
    (130, 64, "Cascajo pequeño"),
    (64, 32, "Grava muy gruesa"),
    (32, 16, "Grava gruesa"),
    (16, 8, "Grava media"),
    (8, 4, "Grava fina"),
    (4, 2, "Grava muy fina"),
    (2, 1, "Arena muy gruesa"),
    (1, 0.5, "Arena gruesa"),
    (0.5, 0.25, "Arena media"),
    (0.25, 0.125, "Arena fina"),
    (0.125, 0.062, "Arena muy fina"),
    (0.062, 0.031, "Limo grueso"),
    (0.031, 0.016, "Limo medio"),
    (0.016, 0.008, "Limo fino"),
    (0.008, 0.004, "Limo muy fino"),
    (0.004, 0.002, "Arcilla gruesa"),
    (0.002, 0.001, "Arcilla media"),
    (0.001, 0.0005, "Arcilla fina"),
    (0.0005, 0.00024, "Arcilla muy fina"),
]


def obtener_coeficiente_contraccion(velocidad_media: float, ancho_libre: float) -> float:
    """Obtiene μ de la Tabla N° 01 con interpolación bilineal."""
    velocidad = max(velocidad_media, _VELOCIDADES_MU[0])
    velocidad = min(velocidad, _VELOCIDADES_MU[-1])
    ancho = max(ancho_libre, _LONGITUDES_MU[0])
    ancho = min(ancho, _LONGITUDES_MU[-1])
    return interpolar_bilineal(ancho, velocidad, _LONGITUDES_MU, _VELOCIDADES_MU, _MATRIZ_MU)


def obtener_coeficiente_beta(periodo_retorno: float) -> float:
    """Obtiene β de la Tabla N° 04 con interpolación lineal."""
    return interpolar_lineal(periodo_retorno, _COEFICIENTE_BETA)


def obtener_exponente_x_no_cohesivo(diametro_mm: float) -> tuple[float, float]:
    """Obtiene x y 1/(x+1) para suelos no cohesivos (Tabla N° 03)."""
    x = interpolar_lineal(diametro_mm, _EXPONENTE_X_NO_COHESIVO)
    return x, 1.0 / (x + 1.0)


def obtener_exponente_x_cohesivo(peso_especifico: float) -> tuple[float, float]:
    """Obtiene x y 1/(x+1) para suelos cohesivos (Tabla N° 03)."""
    x = interpolar_lineal(peso_especifico, _EXPONENTE_X_COHESIVO)
    return x, 1.0 / (x + 1.0)


def clasificar_particula(diametro_mm: float) -> str:
    """Clasifica el material según la Tabla N° 02."""
    for maximo, minimo, descripcion in _CLASIFICACION_PARTICULAS:
        if minimo <= diametro_mm < maximo:
            return descripcion
    if diametro_mm >= 4000:
        return "Canto rodado muy grande"
    return "Arcilla muy fina"


def obtener_coeficiente_phi(caudal: float) -> float:
    """Coeficiente φ para bordo libre según caudal de diseño."""
    if caudal > 4000:
        return 2.0
    if caudal > 3000:
        return 1.7
    if caudal > 2000:
        return 1.4
    if caudal > 1000:
        return 1.2
    if caudal > 500:
        return 1.1
    if caudal > 100:
        return 1.1
    return 1.0
