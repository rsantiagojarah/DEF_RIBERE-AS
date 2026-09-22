"""Tipos y enumeraciones del dominio."""

from enum import Enum


class TipoSuelo(str, Enum):
    """Clasificación del suelo para socavación."""

    NO_COHESIVO = "no_cohesivo"
    COHESIVO = "cohesivo"


class TipoFlujo(str, Enum):
    """Clasificación del régimen de flujo según Froude."""

    SUBCRITICO = "subcritico"
    CRITICO = "critico"
    SUPERCRITICO = "supercritico"
