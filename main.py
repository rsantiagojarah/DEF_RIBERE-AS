#!/usr/bin/env python3
"""
Calculadora de enrocado - Defensa Ribereña.

Arquitectura monolítica modular por fases:
  1. Ingreso de datos
  2. Motor de cálculo
  3. Presentación de resultados
"""

import io
import sys

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")

from def_riberena.datos.ingreso_datos import FaseIngresoDatos
from def_riberena.motor.motor_calculo import MotorCalculoEnrocado
from def_riberena.presentacion.resultados import FasePresentacionResultados


def mostrar_menu() -> str:
    """Muestra el menú principal y retorna la opción."""
    print("\n" + "=" * 60)
    print("  CALCULADORA DE ENROCADO - DEFENSA RIBEREÑA")
    print("  Memoria de cálculo: Métodos hidráulicos y estructurales")
    print("=" * 60)
    print("\n  1) Cálculo con valores de la memoria (Chaupihuranga)")
    print("  2) Cálculo con ingreso manual de datos")
    print("  3) Salir")
    return input("\n  Seleccione una opción [1]: ").strip() or "1"


def ejecutar_calculo(usar_defectos: bool) -> None:
    """Ejecuta el flujo completo de las tres fases."""
    fase_ingreso = FaseIngresoDatos()
    motor = MotorCalculoEnrocado()
    fase_presentacion = FasePresentacionResultados()

    datos = fase_ingreso.ejecutar(usar_defectos=usar_defectos)

    print("\n" + "=" * 60)
    print("  FASE 2: MOTOR DE CÁLCULO")
    print("=" * 60)
    print("  Ejecutando métodos hidráulicos, socavación y enrocado...")

    resultado = motor.ejecutar(datos)
    fase_presentacion.ejecutar(datos, resultado)


def main() -> None:
    """Punto de entrada de la aplicación."""
    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            ejecutar_calculo(usar_defectos=True)
        elif opcion == "2":
            ejecutar_calculo(usar_defectos=False)
        elif opcion == "3":
            print("\n  Hasta pronto.\n")
            sys.exit(0)
        else:
            print("\n  Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
