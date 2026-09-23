"""Presentacion del calculo de torrentera recta."""

from def_riberena.motor.calculo_torrentera import DatosTorrentera, ResultadoTorrentera


def _f(valor: float, decimales: int = 3) -> str:
    return f"{valor:.{decimales}f}"


def mostrar_resultado_torrentera(datos: DatosTorrentera, resultado: ResultadoTorrentera) -> None:
    print("\n" + "=" * 60)
    print("  RESULTADOS - TORRENTERA RECTA")
    print("=" * 60)
    print("\n  --- Datos de diseno ---")
    print(f"  Qd:                         {_f(datos.caudal)} m3/s")
    print(f"  Tr:                         {_f(datos.periodo_retorno, 1)} anios")
    print(f"  Ancho de fondo b:           {_f(datos.ancho_fondo)} m")
    print(f"  Talud del cauce Z:          {_f(datos.talud_cauce)} H:V")
    print(f"  Pendiente S:                {_f(datos.pendiente, 5)} m/m")

    print("\n  --- Hidraulica trapezoidal ---")
    print(f"  Tirante y:                  {_f(resultado.tirante)} m")
    print(f"  Ancho de superficie T:      {_f(resultado.ancho_superficie)} m")
    print(f"  Area mojada A:              {_f(resultado.area)} m2")
    print(f"  Perimetro mojado P:         {_f(resultado.perimetro)} m")
    print(f"  Radio hidraulico R:         {_f(resultado.radio)} m")
    print(f"  Profundidad hidraulica D:   {_f(resultado.profundidad_hidraulica)} m")
    print(f"  Velocidad media V:          {_f(resultado.velocidad)} m/s")
    print(f"  Numero de Froude Fr:        {_f(resultado.froude)}")
    if resultado.froude >= 1.0:
        print("  ADVERTENCIA: Fr >= 1; revisar el metodo para alta pendiente.")

    print("\n  --- Enrocado: formula del manual ---")
    print(f"  Factor b turbulencia:       {_f(datos.factor_turbulencia_roca, 2)}")
    print(f"  D50 requerido:              {_f(resultado.d50_requerido)} m")
    print(f"  Espesor adoptado er=1.5D50: {_f(resultado.espesor_enrocado)} m")
    print(f"  Forma de roca:              {datos.forma_roca}")
    print(f"  Angulo de reposo phi:       {_f(datos.angulo_reposo_roca, 1)} grados")
    print(f"  Peso especifico roca:       {_f(datos.peso_especifico_roca)} Tnf/m3")
    print(f"  Peso especifico agua:       {_f(datos.peso_especifico_agua)} Tnf/m3")
    delta = (datos.peso_especifico_roca - datos.peso_especifico_agua) / datos.peso_especifico_agua
    print(f"  K1 / Delta:                 {_f(datos.factor_talud_k1, 3)} / {_f(delta, 3)}")

    print("\n  --- Socavacion y una enterrada ---")
    print(f"  mu (Tabla 01 interpolada):  {_f(resultado.mu)}")
    print(f"  beta (Tabla 04 interpolada):{_f(resultado.beta)}")
    print(f"  x (Tabla 03 interpolada):   {_f(resultado.exponente_x)}")
    print(f"  Tirante socavado ts:        {_f(resultado.tirante_socavado)} m")
    print(f"  Socavacion ds:              {_f(resultado.socavacion)} m")
    print(f"  Profundidad una Du:         {_f(resultado.profundidad_una)} m")
    print(f"  Rq requerido:               {_f(resultado.rq_roca_por_metro)} m2/m")
    print(f"  Ancho una calculado bu:     {_f(resultado.ancho_una_calculado)} m")
    print(f"  Ancho una adoptado bu:      {_f(resultado.ancho_una_adoptado)} m")
    print(f"  Area transversal una:       {_f(resultado.area_una)} m2/m")
    print(f"  Volumen una total:          {_f(resultado.volumen_una)} m3")
    print("\n  Nota: L se utiliza para obtener el volumen total de la una.")
    print("=" * 60)
