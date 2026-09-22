"""Tablas de rugosidad Ks y Manning n para cauces naturales."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TipoCauceNatural:
    """Tipo de cauce con sus coeficientes de rugosidad."""

    indice: int
    descripcion: str
    coeficiente_strickler: float
    coeficiente_manning: float


TIPOS_CAUCE_NATURAL = (
    TipoCauceNatural(1, "Cauce con fondo solido sin irregularidades", 40.0, 0.025),
    TipoCauceNatural(2, "Cauces de rio con acarreo irregular", 33.0, 0.030),
    TipoCauceNatural(3, "Cauces de rios con vegetacion", 35.0, 0.029),
    TipoCauceNatural(4, "Cauces naturales con derrubio e irregularidades", 30.0, 0.033),
    TipoCauceNatural(5, "Cauces de rio con fuerte transporte de acarreo", 28.0, 0.035),
    TipoCauceNatural(6, "Torrentes con piedras de tamano de una cabeza", 25.0, 0.040),
    TipoCauceNatural(7, "Torrentes con derrubio grueso y acarreo movil", 20.0, 0.050),
)

INDICE_CAUCE_DEFECTO = 4


def obtener_tipo_cauce(indice: int) -> TipoCauceNatural:
    """Obtiene un tipo de cauce por su indice (1-7)."""
    for tipo in TIPOS_CAUCE_NATURAL:
        if tipo.indice == indice:
            return tipo
    raise ValueError(f"Indice de cauce invalido: {indice}. Use un valor entre 1 y 7.")


def listar_tipos_cauce() -> tuple[TipoCauceNatural, ...]:
    """Retorna todos los tipos de cauce disponibles."""
    return TIPOS_CAUCE_NATURAL
