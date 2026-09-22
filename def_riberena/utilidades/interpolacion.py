"""Utilidades de interpolación lineal."""


def interpolar_lineal(valor: float, puntos: list[tuple[float, float]]) -> float:
    """
    Interpola linealmente `valor` sobre una serie de puntos (x, y).

    Si el valor queda fuera del rango, se usa el extremo más cercano.
    """
    if not puntos:
        raise ValueError("Se requiere al menos un punto para interpolar.")

    puntos_ordenados = sorted(puntos, key=lambda par: par[0])

    if valor <= puntos_ordenados[0][0]:
        return puntos_ordenados[0][1]
    if valor >= puntos_ordenados[-1][0]:
        return puntos_ordenados[-1][1]

    for indice in range(len(puntos_ordenados) - 1):
        x1, y1 = puntos_ordenados[indice]
        x2, y2 = puntos_ordenados[indice + 1]
        if x1 <= valor <= x2:
            if x2 == x1:
                return y1
            proporcion = (valor - x1) / (x2 - x1)
            return y1 + proporcion * (y2 - y1)

    return puntos_ordenados[-1][1]


def interpolar_bilineal(
    valor_x: float,
    valor_y: float,
    ejes_x: list[float],
    ejes_y: list[float],
    matriz: list[list[float]],
) -> float:
    """
    Interpola bilinealmente sobre una malla regular.

    matriz[i][j] corresponde a ejes_y[i] y ejes_x[j].
    """
    if not ejes_x or not ejes_y:
        raise ValueError("Los ejes de interpolación no pueden estar vacíos.")

    def obtener_indice_y_peso(eje: list[float], valor: float) -> tuple[int, int, float, float]:
        if valor <= eje[0]:
            return 0, 0, 1.0, 0.0
        if valor >= eje[-1]:
            ultimo = len(eje) - 1
            return ultimo, ultimo, 1.0, 0.0

        for indice in range(len(eje) - 1):
            if eje[indice] <= valor <= eje[indice + 1]:
                if eje[indice + 1] == eje[indice]:
                    return indice, indice, 1.0, 0.0
                peso = (valor - eje[indice]) / (eje[indice + 1] - eje[indice])
                return indice, indice + 1, 1.0 - peso, peso

        ultimo = len(eje) - 1
        return ultimo - 1, ultimo, 0.0, 1.0

    ix0, ix1, px0, px1 = obtener_indice_y_peso(ejes_x, valor_x)
    iy0, iy1, py0, py1 = obtener_indice_y_peso(ejes_y, valor_y)

    v00 = matriz[iy0][ix0]
    v01 = matriz[iy0][ix1]
    v10 = matriz[iy1][ix0]
    v11 = matriz[iy1][ix1]

    v0 = v00 * px0 + v01 * px1
    v1 = v10 * px0 + v11 * px1
    return v0 * py0 + v1 * py1
