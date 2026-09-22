"""Orquestador del motor de calculo."""

from def_riberena.dominio.modelos import DatosEntrada, ResultadoCalculo
from def_riberena.motor.calculos_cauce import calcular_ancho_cauce
from def_riberena.motor.calculos_enrocado import calcular_enrocado
from def_riberena.motor.calculos_hidraulicos import calcular_hidraulica
from def_riberena.motor.calculos_socavacion import calcular_socavacion


class MotorCalculoEnrocado:
    """Motor principal que ejecuta todas las fases de calculo."""

    def ejecutar(self, datos: DatosEntrada) -> ResultadoCalculo:
        """Ejecuta el flujo completo de calculo."""
        hidraulica = calcular_hidraulica(datos)
        ancho_cauce = calcular_ancho_cauce(datos, hidraulica.tirante)
        socavacion = calcular_socavacion(datos, hidraulica)
        enrocado = calcular_enrocado(datos, hidraulica, socavacion)

        return ResultadoCalculo(
            ancho_cauce=ancho_cauce,
            hidraulica=hidraulica,
            socavacion=socavacion,
            enrocado=enrocado,
        )
