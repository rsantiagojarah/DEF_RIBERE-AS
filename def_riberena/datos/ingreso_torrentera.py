"""Ingreso de datos para el calculo de torrentera recta."""

from def_riberena.datos.ingreso_datos import _leer_numero
from def_riberena.datos.tablas_rugosidad import INDICE_CAUCE_DEFECTO, listar_tipos_cauce, obtener_tipo_cauce
from def_riberena.motor.calculo_torrentera import (
    DatosTorrentera,
    calcular_k1_talud,
)


def _leer_rugosidad() -> tuple[float, float]:
    print("\n  Rugosidad de la torrentera:")
    for tipo in listar_tipos_cauce():
        print(f"    {tipo.indice}) {tipo.descripcion} | Ks={tipo.coeficiente_strickler:g} | n={tipo.coeficiente_manning:g}")
    indice = int(_leer_numero("Seleccione tipo de cauce", INDICE_CAUCE_DEFECTO))
    tipo = obtener_tipo_cauce(indice)
    return tipo.coeficiente_manning, tipo.coeficiente_strickler


def _leer_factor_b() -> float:
    print("\n  Factor b de la formula del manual:")
    print("    1) Mucha turbulencia + piedras redondas + sin movimiento | b=1.40 | Manual p.89")
    print("    2) Otro valor sustentado por estudio o referencia")
    opcion = input("  Seleccione condicion [1]: ").strip() or "1"
    if opcion == "1":
        return 1.40
    if opcion == "2":
        return _leer_numero("  Ingrese factor b sustentado", 1.40)
    raise ValueError("Seleccione una opcion valida para el factor b.")


def _leer_angulo_reposo() -> float:
    print("\n  Angulo de reposo o friccion interna phi de la roca:")
    print("    1) Granito/roca del ejemplo del manual | phi=38 grados | Cuadro 12")
    print("    2) Riprap angular de referencia FHWA/ODOT | phi=41 grados")
    print("    3) Valor de ensayo o ficha tecnica de cantera")
    opcion = input("  Seleccione origen de phi [2]: ").strip() or "2"
    if opcion == "1":
        return 38.0
    if opcion == "2":
        return 41.0
    if opcion == "3":
        return _leer_numero("  Ingrese phi sustentado (grados)", 41.0)
    raise ValueError("Seleccione una opcion valida para phi.")


def ingresar_datos_torrentera() -> DatosTorrentera:
    print("\n" + "=" * 60)
    print("  CALCULO DE TORRENTERA RECTA - D50, ENROCADO Y UNA")
    print("=" * 60)
    print("\n  El caudal y el periodo de retorno se ingresan como datos de diseno.")

    caudal = _leer_numero("Caudal de diseno Q (m3/s)", 147.20)
    periodo = _leer_numero("Periodo de retorno Tr (anios)", 100.0)
    ancho = _leer_numero("Ancho de fondo b (m)", 24.2)
    talud_cauce = _leer_numero("Talud del cauce Z (H:V)", 0.5)
    pendiente = _leer_numero("Pendiente longitudinal S (m/m)", 0.09)
    n, _ = _leer_rugosidad()

    print("\n  Parametros de enrocado - formula de estabilidad del manual:")
    talud_enrocado = _leer_numero("Talud del enrocado Zd (H:V)", 2.0)
    gamma_roca = _leer_numero("Peso especifico de roca (Tnf/m3)", 2.55)
    gamma_agua = _leer_numero("Peso especifico del agua (Tnf/m3)", 1.00)
    print("  Forma de la roca: 1) angular [recomendado]  2) redondeada")
    forma = input("  Seleccione forma [1]: ").strip() or "1"
    if forma not in {"1", "2"}:
        raise ValueError("Seleccione 1 para roca angular o 2 para roca redondeada.")
    forma_roca = "angular" if forma == "1" else "redondeada"
    angulo_reposo = _leer_angulo_reposo()
    k1 = calcular_k1_talud(talud_enrocado, angulo_reposo)
    factor_turbulencia = _leer_factor_b()
    print(f"  K1 = {k1:.3f}; b = {factor_turbulencia:.2f}")

    print("\n  Socavacion no cohesiva (Lischtvan-Levediev):")
    dm = _leer_numero("Diametro medio del fondo Dm (mm)", 50.0)
    em = _leer_numero("Empotramiento adicional em (m)", 0.30)

    print("\n  Geometria de la zanja de la una:")
    zu1 = _leer_numero("Talud izquierdo de zanja Zu1 (H:V)", 0.5)
    zu2 = _leer_numero("Talud derecho de zanja Zu2 (H:V)", 0.5)
    ancho_min = _leer_numero("Ancho transversal minimo constructivo bu (m)", 1.0)
    longitud = _leer_numero("Longitud longitudinal de defensa L (m)", 100.0)

    return DatosTorrentera(
        caudal=caudal,
        periodo_retorno=periodo,
        ancho_fondo=ancho,
        talud_cauce=talud_cauce,
        pendiente=pendiente,
        coeficiente_manning=n,
        talud_enrocado=talud_enrocado,
        peso_especifico_roca=gamma_roca,
        peso_especifico_agua=gamma_agua,
        factor_talud_k1=k1,
        factor_turbulencia_roca=factor_turbulencia,
        dm_fondo_mm=dm,
        empotramiento_adicional=em,
        talud_zanja_izq=zu1,
        talud_zanja_der=zu2,
        ancho_minimo_una=ancho_min,
        longitud_defensa=longitud,
        forma_roca=forma_roca,
        angulo_reposo_roca=angulo_reposo,
    )
