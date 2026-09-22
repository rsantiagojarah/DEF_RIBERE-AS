"""Formateo de tablas ASCII para la terminal."""


def _formatear_valor_tabla(valor: float) -> str:
    """Formatea un valor numerico para celdas de tabla."""
    return f"{valor:g}"


def formatear_tabla_opciones(
    opciones: tuple,
    nombre_valor: str,
    ancho_descripcion: int = 48,
) -> str:
    """
    Genera una tabla ASCII con columnas: #, Descripcion, Valor.

    Cada opcion debe tener atributos: indice, descripcion, valor.
    """
    col_num = max(2, len(str(max(o.indice for o in opciones))))
    col_val = max(len(nombre_valor), max(len(_formatear_valor_tabla(o.valor)) for o in opciones))

    sep = (
        f"+{'-' * (col_num + 2)}+"
        f"{'-' * (ancho_descripcion + 2)}+"
        f"{'-' * (col_val + 2)}+"
    )

    encabezado = (
        f"| {'#':<{col_num}} | "
        f"{'Descripcion':<{ancho_descripcion}} | "
        f"{nombre_valor:>{col_val}} |"
    )

    filas = []
    for opcion in opciones:
        descripcion = opcion.descripcion[:ancho_descripcion]
        valor = _formatear_valor_tabla(opcion.valor)
        filas.append(
            f"| {opcion.indice:>{col_num}} | "
            f"{descripcion:<{ancho_descripcion}} | "
            f"{valor:>{col_val}} |"
        )

    return "\n".join([sep, encabezado, sep, *filas, sep])


def formatear_tabla_doble_valor(
    filas: tuple,
    nombre_col1: str,
    nombre_col2: str,
    ancho_descripcion: int = 48,
) -> str:
    """
    Genera tabla con columnas: #, Descripcion, Valor1, Valor2.

    Cada fila debe tener: indice, descripcion, valor1, valor2.
    """
    col_num = max(2, len(str(max(f.indice for f in filas))))
    col1 = max(len(nombre_col1), max(len(_formatear_valor_tabla(f.valor1)) for f in filas))
    col2 = max(len(nombre_col2), max(len(_formatear_valor_tabla(f.valor2)) for f in filas))

    sep = (
        f"+{'-' * (col_num + 2)}+"
        f"{'-' * (ancho_descripcion + 2)}+"
        f"{'-' * (col1 + 2)}+"
        f"{'-' * (col2 + 2)}+"
    )

    encabezado = (
        f"| {'#':<{col_num}} | "
        f"{'Descripcion':<{ancho_descripcion}} | "
        f"{nombre_col1:>{col1}} | "
        f"{nombre_col2:>{col2}} |"
    )

    lineas = []
    for fila in filas:
        descripcion = fila.descripcion[:ancho_descripcion]
        lineas.append(
            f"| {fila.indice:>{col_num}} | "
            f"{descripcion:<{ancho_descripcion}} | "
            f"{_formatear_valor_tabla(fila.valor1):>{col1}} | "
            f"{_formatear_valor_tabla(fila.valor2):>{col2}} |"
        )

    return "\n".join([sep, encabezado, sep, *lineas, sep])


def formatear_tabla_pares(
    pares: list[tuple[str, str]],
    titulo_col1: str,
    titulo_col2: str,
    ancho_col1: int = 12,
) -> str:
    """Genera tabla de dos columnas (pares clave-valor)."""
    ancho_col2 = max(len(titulo_col2), max(len(v) for _, v in pares))
    sep = f"+{'-' * (ancho_col1 + 2)}+{'-' * (ancho_col2 + 2)}+"
    encabezado = f"| {titulo_col1:<{ancho_col1}} | {titulo_col2:>{ancho_col2}} |"
    filas = [f"| {k:<{ancho_col1}} | {v:>{ancho_col2}} |" for k, v in pares]
    return "\n".join([sep, encabezado, sep, *filas, sep])
