"""Fase de presentación de resultados en terminal."""

from def_riberena.datos.tablas import clasificar_particula
from def_riberena.dominio.modelos import DatosEntrada, ResultadoCalculo
from def_riberena.dominio.tipos import TipoFlujo, TipoSuelo


def _formatear(valor: float, decimales: int = 2) -> str:
    """Formatea un número con decimales fijos."""
    return f"{valor:.{decimales}f}"


def _etiqueta_flujo(tipo: TipoFlujo) -> str:
    """Traduce el tipo de flujo a texto legible."""
    return {
        TipoFlujo.SUBCRITICO: "SUBCRÍTICO",
        TipoFlujo.CRITICO: "CRÍTICO",
        TipoFlujo.SUPERCRITICO: "SUPERCRÍTICO",
    }[tipo]


class FasePresentacionResultados:
    """Presenta los resultados del cálculo en consola."""

    def ejecutar(self, datos: DatosEntrada, resultado: ResultadoCalculo) -> None:
        """Muestra el reporte completo."""
        print("\n" + "=" * 60)
        print("  FASE 3: RESULTADOS - DEFENSA RIBEREÑA (ENROCADO)")
        print("=" * 60)

        self._mostrar_encabezado(datos)
        self._mostrar_ancho_cauce(datos, resultado)
        self._mostrar_hidraulica(datos, resultado)
        self._mostrar_socavacion(datos, resultado)
        self._mostrar_enrocado(datos, resultado)
        self._mostrar_resumen_final(resultado)

    def _mostrar_encabezado(self, datos: DatosEntrada) -> None:
        print(f"\n  Sección: {datos.proyecto.nombre_seccion}")
        print(f"  Sector:  {datos.proyecto.sector}")
        print(f"  Q diseno: {_formatear(datos.hidrologia.caudal_diseno)} m3/s")
        print(f"  S:        {_formatear(datos.hidrologia.pendiente, 5)} m/m")
        print(
            f"  B adoptado/efectivo (superficie): "
            f"{_formatear(datos.geometria.ancho_adoptado)} m"
        )

    def _mostrar_ancho_cauce(self, datos: DatosEntrada, resultado: ResultadoCalculo) -> None:
        p = datos.ancho_cauce
        ancho = resultado.ancho_cauce
        print("\n--- Parametros de ancho estable (tablas) ---")
        print(f"  K1 = {_formatear(p.coeficiente_k1, 2)}  ({p.descripcion_k1})")
        print(f"  Fb = {_formatear(p.factor_fondo_fb, 2)}  ({p.descripcion_fb})")
        print(f"  Fs = {_formatear(p.factor_orilla_fs, 2)}  ({p.descripcion_fs})")
        print(f"  K  = {_formatear(p.coeficiente_material_k, 2)}  ({p.descripcion_material_k})")
        print(f"  m  = {_formatear(p.coeficiente_tipo_rio_m, 2)}  ({p.descripcion_tipo_rio})")
        print("\n--- Ancho estable de cauce ---")
        print(f"  Simons y Henderson: {_formatear(ancho.simons_henderson)} m")
        print(f"  Pettis:             {_formatear(ancho.pettis)} m")
        print(f"  Altunin - Manning:  {_formatear(ancho.altunin_manning)} m")
        print(f"  Blench:             {_formatear(ancho.blench)} m")
        print(f"  Recomendación:      {_formatear(ancho.recomendacion_practica)} m")
        print(
            f"  >> B adoptado (superficie): {_formatear(ancho.ancho_adoptado)} m"
        )

    def _mostrar_rugosidad(self, datos: DatosEntrada) -> None:
        r = datos.rugosidad
        print("\n--- Rugosidad del cauce ---")
        print(f"  Tipo:                   {r.descripcion_cauce}")
        print(f"  Coeficiente Strickler Ks: {_formatear(r.coeficiente_strickler, 3)}")
        print(f"  Coeficiente Manning n:    {_formatear(r.coeficiente_manning, 3)}")

    def _mostrar_hidraulica(self, datos: DatosEntrada, resultado: ResultadoCalculo) -> None:
        h = resultado.hidraulica
        self._mostrar_rugosidad(datos)
        print("\n--- Calculo hidraulico ---")
        print(
            f"  B superficie (efectivo): {_formatear(h.ancho_superficie)} m"
        )
        print(f"  B fondo (calculado):     {_formatear(h.ancho_fondo)} m")
        print(f"  Tirante t:              {_formatear(h.tirante)} m")
        print(f"  Area mojada A:          {_formatear(h.area_mojada)} m2")
        print(f"  Perímetro mojado P:     {_formatear(h.perimetro_mojado)} m")
        print(f"  Radio hidráulico R:     {_formatear(h.radio_hidraulico)} m")
        print(f"  Velocidad media V:      {_formatear(h.velocidad_media)} m/s")
        print(f"  Profundidad hidráulica: {_formatear(h.profundidad_hidraulica)} m")
        print(f"  Número de Froude F:     {_formatear(h.numero_froude)}")
        print(f"  Tipo de flujo:          {_etiqueta_flujo(h.tipo_flujo)}")
        print(f"  Carga cinética e:       {_formatear(h.carga_cinetica)} m")
        print(f"  Coeficiente phi:        {_formatear(h.coeficiente_phi)}")
        print(f"  Bordo libre BL:         {_formatear(h.bordo_libre)} m")
        print(f"  Altura de muro Hm:      {_formatear(h.altura_muro)} m")

    def _mostrar_socavacion(self, datos: DatosEntrada, resultado: ResultadoCalculo) -> None:
        s = resultado.socavacion
        print("\n--- Socavación (Lischtvan-Lebediev) ---")
        if datos.suelo.tipo_suelo == TipoSuelo.NO_COHESIVO:
            clasificacion = clasificar_particula(datos.suelo.diametro_medio_mm)
            print(f"  Tipo suelo: NO COHESIVO ({clasificacion})")
            print(f"  Dm:         {_formatear(datos.suelo.diametro_medio_mm)} mm")
        else:
            print("  Tipo suelo: COHESIVO")
            print(f"  Peso esp. gs: {_formatear(datos.suelo.peso_especifico_tn_m3)} Tn/m3")

        print(f"  mu (Tabla 01):          {_formatear(s.coeficiente_contraccion, 3)}")
        print(f"  beta (Tabla 04):        {_formatear(s.coeficiente_beta, 3)}")
        print(f"  x (Tabla 03):           {_formatear(s.exponente_x, 4)}")
        print(f"  1/(x+1):                {_formatear(s.factor_uno_sobre_x_mas_uno, 3)}")
        print(f"  alfa:                   {_formatear(s.coeficiente_alfa, 2)}")
        print(f"  Tirante socavado ts:    {_formatear(s.tirante_socavado)} m")
        print(f"  >> Profundidad Hs:      {_formatear(s.profundidad_socavacion)} m")

    def _mostrar_enrocado(self, datos: DatosEntrada, resultado: ResultadoCalculo) -> None:
        en = datos.enrocado
        e = resultado.enrocado
        print("\n--- Enrocado (Formula de Maynord) ---")
        print(f"  C1 = {_formatear(en.coeficiente_c1, 2)}  ({en.descripcion_c1})")
        print(f"  C2 = {_formatear(en.coeficiente_c2, 2)}  ({en.descripcion_c2})")
        print(f"  Factor intensidad F:    {_formatear(e.factor_intensidad, 4)}")
        print(f"  >> Diámetro D50:        {_formatear(e.diametro_d50)} m")

        print("\n--- Profundidad de uña ---")
        print(f"  >> P_uña:                {_formatear(e.profundidad_puna)} m")
        print(f"  Ancho superior (1.5Pu): {_formatear(e.ancho_superior_puna)} m")
        print(f"  Ancho inferior (Pu):    {_formatear(e.ancho_inferior_puna)} m")

    def _mostrar_resumen_final(self, resultado: ResultadoCalculo) -> None:
        print("\n" + "-" * 60)
        print("  RESUMEN EJECUTIVO")
        print("-" * 60)
        print(f"  Tirante de diseño:     {_formatear(resultado.hidraulica.tirante)} m")
        print(f"  Velocidad:             {_formatear(resultado.hidraulica.velocidad_media)} m/s")
        print(f"  Socavación Hs:         {_formatear(resultado.socavacion.profundidad_socavacion)} m")
        print(f"  Diámetro enrocado D50: {_formatear(resultado.enrocado.diametro_d50)} m")
        print(f"  Profundidad uña:       {_formatear(resultado.enrocado.profundidad_puna)} m")
        print("=" * 60 + "\n")
