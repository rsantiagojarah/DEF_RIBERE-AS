"""Fase de ingreso de datos por terminal."""

from types import SimpleNamespace

from def_riberena.datos.tablas_ancho_cauce import (
    CONDICIONES_FONDO_K1,
    FACTORES_FONDO_FB,
    FACTORES_ORILLA_FS,
    INDICE_FB_DEFECTO,
    INDICE_FS_DEFECTO,
    INDICE_K1_DEFECTO,
    INDICE_K_DEFECTO,
    INDICE_M_DEFECTO,
    MATERIALES_CAUCE_K,
    TIPOS_RIO_M,
    OpcionTabla,
    obtener_ancho_recomendacion_practica,
    obtener_condicion_fondo_k1,
    obtener_factor_fondo_fb,
    obtener_factor_orilla_fs,
    obtener_material_cauce_k,
    obtener_tipo_rio_m,
)
from def_riberena.datos.tablas_enrocado import (
    COEFICIENTES_C1,
    COEFICIENTES_C2,
    INDICE_C1_DEFECTO,
    INDICE_C2_DEFECTO,
)
from def_riberena.datos.tablas_rugosidad import (
    INDICE_CAUCE_DEFECTO,
    listar_tipos_cauce,
    obtener_tipo_cauce,
)
from def_riberena.dominio.modelos import (
    DatosAnchoCauce,
    DatosEnrocado,
    DatosEntrada,
    DatosEstructurales,
    DatosGeometricos,
    DatosHidrologicos,
    DatosProyecto,
    DatosRugosidad,
    DatosSuelo,
)
from def_riberena.dominio.tipos import TipoSuelo
from def_riberena.utilidades.formatear_tabla import (
    formatear_tabla_doble_valor,
    formatear_tabla_opciones,
    formatear_tabla_pares,
)


def _leer_texto(mensaje: str, valor_defecto: str) -> str:
    """Lee texto con valor por defecto."""
    entrada = input(f"{mensaje} [{valor_defecto}]: ").strip()
    return entrada if entrada else valor_defecto


def _leer_numero(mensaje: str, valor_defecto: float) -> float:
    """Lee un numero flotante con valor por defecto."""
    while True:
        entrada = input(f"{mensaje} [{valor_defecto}]: ").strip()
        if not entrada:
            return valor_defecto
        try:
            return float(entrada.replace(",", "."))
        except ValueError:
            print("  Valor invalido. Ingrese un numero.")


def _imprimir_tabla(texto_tabla: str) -> None:
    """Imprime una tabla con sangria uniforme."""
    for linea in texto_tabla.splitlines():
        print(f"  {linea}")


def _leer_opcion_tabla(
    titulo: str,
    opciones: tuple[OpcionTabla, ...],
    indice_defecto: int,
    nombre_valor: str = "Valor",
) -> OpcionTabla:
    """Muestra una tabla en terminal y lee la opcion seleccionada."""
    print(f"\n  {titulo}")
    _imprimir_tabla(formatear_tabla_opciones(opciones, nombre_valor))

    maximo = len(opciones)
    while True:
        entrada = input(f"  Seleccione [ {indice_defecto} ]: ").strip()
        if not entrada:
            indice = indice_defecto
        else:
            try:
                indice = int(entrada)
            except ValueError:
                print(f"  Opcion invalida. Use un numero del 1 al {maximo}.")
                continue

        try:
            for opcion in opciones:
                if opcion.indice == indice:
                    return opcion
            raise ValueError(f"Indice invalido: {indice}. Use un valor entre 1 y {maximo}.")
        except ValueError as error:
            print(f"  {error}")


def _mostrar_recomendacion_practica(caudal: float) -> None:
    """Muestra la tabla de recomendacion practica y el valor para el caudal."""
    print("\n  RECOMENDACION PRACTICA (Tabla Q vs ancho B2):")
    pares = [
        ("3000", "200"),
        ("2400", "190"),
        ("1500", "120"),
        ("1000", "100"),
        ("500", "70"),
        ("100", "70"),
    ]
    _imprimir_tabla(formatear_tabla_pares(pares, "Q (m3/s)", "B2 (m)", ancho_col1=12))
    ancho = obtener_ancho_recomendacion_practica(caudal)
    print(f"  >> Para Q = {caudal:g} m3/s  =>  B2 = {ancho:.2f} m")


def _crear_datos_ancho_cauce(
    indice_k1: int,
    indice_fb: int,
    indice_fs: int,
    indice_k: int,
    indice_m: int,
) -> DatosAnchoCauce:
    """Construye DatosAnchoCauce a partir de indices de tabla."""
    k1 = obtener_condicion_fondo_k1(indice_k1)
    fb = obtener_factor_fondo_fb(indice_fb)
    fs = obtener_factor_orilla_fs(indice_fs)
    material_k = obtener_material_cauce_k(indice_k)
    tipo_m = obtener_tipo_rio_m(indice_m)

    return DatosAnchoCauce(
        indice_condicion_fondo_k1=k1.indice,
        descripcion_k1=k1.descripcion,
        coeficiente_k1=k1.valor,
        indice_factor_fondo_fb=fb.indice,
        descripcion_fb=fb.descripcion,
        factor_fondo_fb=fb.valor,
        indice_factor_orilla_fs=fs.indice,
        descripcion_fs=fs.descripcion,
        factor_orilla_fs=fs.valor,
        indice_material_cauce_k=material_k.indice,
        descripcion_material_k=material_k.descripcion,
        coeficiente_material_k=material_k.valor,
        indice_tipo_rio_m=tipo_m.indice,
        descripcion_tipo_rio=tipo_m.descripcion,
        coeficiente_tipo_rio_m=tipo_m.valor,
    )


def _leer_parametros_ancho_cauce(caudal: float, defecto: DatosAnchoCauce) -> DatosAnchoCauce:
    """Ingreso interactivo de tablas para ancho estable de cauce."""
    print("\n--- Parametros de ancho estable de cauce ---")

    k1 = _leer_opcion_tabla(
        "Condiciones de fondo de rio (K1 - Simons y Henderson):",
        CONDICIONES_FONDO_K1,
        defecto.indice_condicion_fondo_k1 or INDICE_K1_DEFECTO,
        nombre_valor="K1",
    )
    fb = _leer_opcion_tabla(
        "Factor de fondo Fb (Blench):",
        FACTORES_FONDO_FB,
        defecto.indice_factor_fondo_fb or INDICE_FB_DEFECTO,
        nombre_valor="Fb",
    )
    fs = _leer_opcion_tabla(
        "Factor de orilla Fs (Blench):",
        FACTORES_ORILLA_FS,
        defecto.indice_factor_orilla_fs or INDICE_FS_DEFECTO,
        nombre_valor="Fs",
    )
    material_k = _leer_opcion_tabla(
        "Coeficiente material del cauce K (Altunin - Manning):",
        MATERIALES_CAUCE_K,
        defecto.indice_material_cauce_k or INDICE_K_DEFECTO,
        nombre_valor="K",
    )
    tipo_m = _leer_opcion_tabla(
        "Coeficiente tipo de rio m (Altunin - Manning):",
        TIPOS_RIO_M,
        defecto.indice_tipo_rio_m or INDICE_M_DEFECTO,
        nombre_valor="m",
    )

    _mostrar_recomendacion_practica(caudal)

    return DatosAnchoCauce(
        indice_condicion_fondo_k1=k1.indice,
        descripcion_k1=k1.descripcion,
        coeficiente_k1=k1.valor,
        indice_factor_fondo_fb=fb.indice,
        descripcion_fb=fb.descripcion,
        factor_fondo_fb=fb.valor,
        indice_factor_orilla_fs=fs.indice,
        descripcion_fs=fs.descripcion,
        factor_orilla_fs=fs.valor,
        indice_material_cauce_k=material_k.indice,
        descripcion_material_k=material_k.descripcion,
        coeficiente_material_k=material_k.valor,
        indice_tipo_rio_m=tipo_m.indice,
        descripcion_tipo_rio=tipo_m.descripcion,
        coeficiente_tipo_rio_m=tipo_m.valor,
    )


def _mostrar_resumen_ancho_cauce(datos: DatosAnchoCauce, caudal: float) -> None:
    """Resume las tablas de ancho de cauce seleccionadas."""
    print("\n  Parametros de ancho estable (tablas):")
    print(f"    K1 = {datos.coeficiente_k1:g}  ({datos.descripcion_k1})")
    print(f"    Fb = {datos.factor_fondo_fb:g}  ({datos.descripcion_fb})")
    print(f"    Fs = {datos.factor_orilla_fs:g}  ({datos.descripcion_fs})")
    print(f"    K  = {datos.coeficiente_material_k:g}  ({datos.descripcion_material_k})")
    print(f"    m  = {datos.coeficiente_tipo_rio_m:g}  ({datos.descripcion_tipo_rio})")
    ancho = obtener_ancho_recomendacion_practica(caudal)
    print(f"    Recomendacion practica B2 = {ancho:.2f} m  (Q = {caudal:g} m3/s)")


def _leer_opcion_tipo_cauce(indice_defecto: int) -> DatosRugosidad:
    """Lee el tipo de cauce natural y asigna Ks y n desde la tabla."""
    print("\n  Tipo de cauce natural (Ks y n):")
    filas = tuple(
        SimpleNamespace(
            indice=tipo.indice,
            descripcion=tipo.descripcion,
            valor1=tipo.coeficiente_strickler,
            valor2=tipo.coeficiente_manning,
        )
        for tipo in listar_tipos_cauce()
    )
    _imprimir_tabla(formatear_tabla_doble_valor(filas, "Ks", "n", ancho_descripcion=46))

    while True:
        entrada = input(f"  Seleccione [ {indice_defecto} ]: ").strip()
        if not entrada:
            indice = indice_defecto
        else:
            try:
                indice = int(entrada)
            except ValueError:
                print("  Opcion invalida. Use un numero del 1 al 7.")
                continue

        try:
            tipo = obtener_tipo_cauce(indice)
            return DatosRugosidad(
                indice_tipo_cauce=tipo.indice,
                descripcion_cauce=tipo.descripcion,
                coeficiente_strickler=tipo.coeficiente_strickler,
                coeficiente_manning=tipo.coeficiente_manning,
            )
        except ValueError as error:
            print(f"  {error}")


def _mostrar_resumen_rugosidad(rugosidad: DatosRugosidad) -> None:
    print(f"    Ks = {rugosidad.coeficiente_strickler:g}, n = {rugosidad.coeficiente_manning:g}")
    print(f"    ({rugosidad.descripcion_cauce})")


def _leer_parametros_enrocado(defecto: DatosEnrocado) -> DatosEnrocado:
    """Ingreso interactivo de coeficientes C1 y C2 (Maynord)."""
    print("\n--- Parametros de enrocado (Maynord) ---")

    c1 = _leer_opcion_tabla(
        "Coeficiente C1 (geometria de la proteccion):",
        COEFICIENTES_C1,
        defecto.indice_coeficiente_c1 or INDICE_C1_DEFECTO,
        nombre_valor="C1",
    )
    c2 = _leer_opcion_tabla(
        "Coeficiente C2 (ubicacion de la roca):",
        COEFICIENTES_C2,
        defecto.indice_coeficiente_c2 or INDICE_C2_DEFECTO,
        nombre_valor="C2",
    )

    return DatosEnrocado(
        indice_coeficiente_c1=c1.indice,
        descripcion_c1=c1.descripcion,
        coeficiente_c1=c1.valor,
        indice_coeficiente_c2=c2.indice,
        descripcion_c2=c2.descripcion,
        coeficiente_c2=c2.valor,
    )


def _mostrar_resumen_enrocado(enrocado: DatosEnrocado) -> None:
    print("\n  Parametros de enrocado (Maynord):")
    print(f"    C1 = {enrocado.coeficiente_c1:g}  ({enrocado.descripcion_c1})")
    print(f"    C2 = {enrocado.coeficiente_c2:g}  ({enrocado.descripcion_c2})")


def _leer_opcion_suelo(valor_defecto: TipoSuelo) -> TipoSuelo:
    """Lee el tipo de suelo."""
    texto_defecto = "1" if valor_defecto == TipoSuelo.NO_COHESIVO else "2"
    print("  Tipo de suelo:")
    print("    1) No cohesivo (granular)")
    print("    2) Cohesivo")
    while True:
        entrada = input(f"  Seleccione [ {texto_defecto} ]: ").strip()
        if not entrada:
            return valor_defecto
        if entrada == "1":
            return TipoSuelo.NO_COHESIVO
        if entrada == "2":
            return TipoSuelo.COHESIVO
        print("  Opcion invalida. Use 1 o 2.")


class FaseIngresoDatos:
    """Recopila los datos del proyecto desde la terminal."""

    def ejecutar(self, usar_defectos: bool = False) -> DatosEntrada:
        """Ejecuta el ingreso interactivo de datos."""
        print("\n" + "=" * 60)
        print("  FASE 1: INGRESO DE DATOS - DEFENSA RIBERENA (ENROCADO)")
        print("=" * 60)

        if usar_defectos:
            print("\n  Usando valores de la memoria de calculo (Chaupihuranga).")
            datos = DatosEntrada()
            _mostrar_resumen_ancho_cauce(datos.ancho_cauce, datos.hidrologia.caudal_diseno)
            print("\n  Rugosidad del cauce:")
            _mostrar_resumen_rugosidad(datos.rugosidad)
            _mostrar_resumen_enrocado(datos.enrocado)
            return datos

        defecto = DatosEntrada()

        print("\n--- Datos del proyecto ---")
        proyecto = DatosProyecto(
            nombre_seccion=_leer_texto("Nombre de la seccion", defecto.proyecto.nombre_seccion),
            sector=_leer_texto("Sector", defecto.proyecto.sector),
        )

        print("\n--- Datos hidrologicos ---")
        hidrologia = DatosHidrologicos(
            caudal_diseno=_leer_numero("Caudal de diseno Q (m3/s)", defecto.hidrologia.caudal_diseno),
            pendiente=_leer_numero("Pendiente S (m/m)", defecto.hidrologia.pendiente),
            periodo_retorno=_leer_numero("Periodo de retorno (anios)", defecto.hidrologia.periodo_retorno),
        )

        ancho_cauce = _leer_parametros_ancho_cauce(hidrologia.caudal_diseno, defecto.ancho_cauce)

        print("\n--- Geometria del tramo ---")
        geometria = DatosGeometricos(
            ancho_adoptado=_leer_numero(
                "Ancho adoptado/efectivo B a superficie del agua (m)",
                defecto.geometria.ancho_adoptado,
            ),
            talud_borde=_leer_numero("Talud de borde Z (H:V)", defecto.geometria.talud_borde),
        )

        print("\n--- Propiedades del suelo ---")
        tipo_suelo = _leer_opcion_suelo(defecto.suelo.tipo_suelo)
        suelo = DatosSuelo(
            tipo_suelo=tipo_suelo,
            diametro_medio_mm=_leer_numero("Diametro medio Dm (mm)", defecto.suelo.diametro_medio_mm),
            peso_especifico_tn_m3=_leer_numero(
                "Peso especifico gs (Tn/m3)",
                defecto.suelo.peso_especifico_tn_m3,
            ),
        )

        print("\n--- Rugosidad del cauce ---")
        rugosidad = _leer_opcion_tipo_cauce(
            defecto.rugosidad.indice_tipo_cauce or INDICE_CAUCE_DEFECTO
        )

        enrocado = _leer_parametros_enrocado(defecto.enrocado)

        print("\n--- Parametros estructurales ---")
        estructural = DatosEstructurales(
            factor_seguridad_puna=_leer_numero(
                "Factor de seguridad una FS",
                defecto.estructural.factor_seguridad_puna,
            ),
            redondeo_puna_m=_leer_numero(
                "Redondeo una (m)",
                defecto.estructural.redondeo_puna_m,
            ),
        )

        return DatosEntrada(
            proyecto=proyecto,
            hidrologia=hidrologia,
            geometria=geometria,
            ancho_cauce=ancho_cauce,
            suelo=suelo,
            rugosidad=rugosidad,
            enrocado=enrocado,
            estructural=estructural,
        )
