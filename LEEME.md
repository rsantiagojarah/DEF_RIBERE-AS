# Calculadora de Enrocado — Defensa Ribereña

Aplicación de terminal en Python para el cálculo del enrocado de defensas ribereñas, basada en la **Memoria de Cálculo** del proyecto Chaupihuranga (Pasco).

Incluye métodos hidráulicos, socavación (Lischtvan-Lebediev), diámetro de roca (Maynord) y profundidad de uña.

---

## Requisitos

- **Python 3.10 o superior** (probado con Python 3.12)
- No requiere instalar librerías externas (solo biblioteca estándar de Python)

Verifique que Python esté instalado:

```powershell
python --version
```

---

## Cómo ejecutar el programa

### Windows (PowerShell o CMD)

1. Abra una terminal.
2. Vaya a la carpeta del proyecto:

```powershell
cd "C:\Users\CARMEN\desktop\PROYECTOS\DEF_RIBEREÑA"
```

3. Ejecute el programa:

```powershell
python main.py
```

### Atajo desde el Explorador de archivos

1. Abra la carpeta `DEF_RIBEREÑA`.
2. Escriba `cmd` o `powershell` en la barra de direcciones y presione Enter.
3. Escriba `python main.py` y presione Enter.

---

## Menú principal

Al iniciar verá tres opciones:

| Opción | Descripción |
|--------|-------------|
| **1** | Cálculo con valores de la memoria (Chaupihuranga). Usa datos precargados; no pide parámetros. |
| **2** | Cálculo con ingreso manual. Solicita cada dato por terminal (Enter = valor por defecto). |
| **3** | Salir del programa. |

Después de cada cálculo el menú vuelve a mostrarse para repetir o salir.

---

## Flujo del programa (3 fases)

```
FASE 1 — Ingreso de datos     →  Captura parámetros del proyecto
FASE 2 — Motor de cálculo     →  Ejecuta fórmulas y tablas normativas
FASE 3 — Presentación         →  Muestra resultados en consola
```

---

## Valores por defecto (opción 1)

Corresponden al caso de la memoria de cálculo:

| Parámetro | Valor |
|-----------|-------|
| Sección | RIO CHAUPIHURANGA |
| Caudal de diseño Q | 147.20 m³/s |
| Pendiente S | 0.09 m/m |
| Ancho de fondo B | 24.20 m |
| Ancho efectivo (calculado) | B_fondo + 2·Z·t |
| Periodo de retorno | 100 años |
| Diámetro medio Dm | 50 mm (suelo no cohesivo) |
| Tipo de cauce | Cauces naturales con derrubio e irregularidades |
| Coeficiente Strickler Ks | 30 (desde tabla) |
| Coeficiente Manning n | 0.033 (desde tabla) |
| Coeficientes Maynord C1 / C2 | 0.25 / 1.50 |
| Factor de seguridad uña FS | 1.5 |

---

## Estructura del proyecto

```
DEF_RIBEREÑA/
├── main.py                 ← Ejecutar este archivo
├── LEEME.md
├── fuente/
│   └── MEMORIA DE CALCULO.docx
└── def_riberena/
    ├── dominio/            Modelos y tipos de datos
    ├── datos/              Ingreso y tablas normativas (Tablas 01–04)
    ├── motor/              Motor de cálculo
    │   ├── motor_calculo.py
    │   ├── calculos_cauce.py
    │   ├── calculos_hidraulicos.py
    │   ├── calculos_socavacion.py
    │   └── calculos_enrocado.py
    ├── presentacion/       Reporte de resultados
    └── utilidades/         Interpolación de tablas
```

---

## Tablas de rugosidad (Ks y n)

Al ingresar datos manualmente (opción 2) se elige el tipo de cauce natural. El programa asigna automáticamente Ks y n:

| # | Descripción | Ks | n |
|---|-------------|-----|------|
| 1 | Cauce con fondo sólido sin irregularidades | 40 | 0.025 |
| 2 | Cauces de río con acarreo irregular | 33 | 0.030 |
| 3 | Cauces de ríos con vegetación | 35 | 0.029 |
| 4 | Cauces naturales con derrubio e irregularidades | 30 | 0.033 |
| 5 | Cauces de río con fuerte transporte de acarreo | 28 | 0.035 |
| 6 | Torrentes con piedras de tamaño de una cabeza | 25 | 0.040 |
| 7 | Torrentes con derrubio grueso y acarreo móvil | 20 | 0.050 |

Por defecto (opción 1) se usa el tipo **4**, acorde a la memoria de cálculo.

---

## Tablas de ancho estable de cauce

En el ingreso manual (opción 2) se muestran y seleccionan estas tablas:

**K1 — Simons y Henderson (condición de fondo)**

| # | Condición | K1 |
|---|-----------|-----|
| 1 | Fondo arena y orillas de material cohesivo | 4.20 |
| 2 | Fondo y orillas de material cohesivo | 3.60 |
| 3 | Fondo y orillas de grava | 2.90 |
| 4 | Fondo arena y orillas material no cohesivo | 2.80 |

**Fb / Fs — Blench**

| Fb | Material | Valor |
|----|----------|-------|
| 1 | Material fino | 0.80 |
| 2 | Material grueso | 1.20 |

| Fs | Material de orilla | Valor |
|----|-------------------|-------|
| 1 | Materiales sueltos | 0.10 |
| 2 | Materiales ligeramente cohesivos | 0.20 |
| 3 | Materiales cohesivos | 0.30 |

**K / m — Altunin-Manning**

| K | Material del cauce | Valor |
|---|-------------------|-------|
| 1 | Material muy resistente | 3 |
| 2 | Material fácilmente erosionable | 16 |
| 3 | Material aluvial | 12 |
| 4 | Valor práctico | 10 |

| m | Tipo de río | Valor |
|---|-------------|-------|
| 1 | Ríos de montaña | 0.5 |
| 2 | Cauces arenosos | 0.7 |
| 3 | Cauces aluviales | 1.0 |

**Recomendación práctica (B2 según Q)**

| Q (m³/s) | B2 (m) |
|----------|--------|
| 3000 | 200 |
| 2400 | 190 |
| 1500 | 120 |
| 1000 | 100 |
| 500 | 70 |
| 100 | 70 |

Para caudales intermedios se interpola linealmente. Con Q = 147.20 m³/s, B2 = 70 m.

---

## Tablas de enrocado (Maynord)

**C1 — Geometría de la protección**

| # | Descripción | C1 |
|---|-------------|-----|
| 1 | Fondo plano | 0.25 |
| 2 | Talud 1V:3H | 0.28 |
| 3 | Talud 1V:2H | 0.32 |

**C2 — Ubicación de la roca**

| # | Descripción | C2 |
|---|-------------|-----|
| 1 | Tramos en curva | 1.50 |
| 2 | Tramos rectos | 1.25 |

Por defecto: **C1 = Fondo plano (0.25)** y **C2 = Tramos en curva (1.50)**.

---

## Resultados que entrega

- Ancho estable de cauce (Simons, Pettis, Altunin, Blench)
- Tirante, velocidad, número de Froude y bordo libre
- Socavación: coeficientes μ, β, x, α, profundidad Hs
- Enrocado: diámetro D50 (Maynord)
- Profundidad de uña P_uña y dimensiones del pie de talud

---

## Solución de problemas

### `python` no se reconoce como comando

Python no está instalado o no está en el PATH. Instálelo desde [python.org](https://www.python.org/downloads/) marcando la opción **"Add Python to PATH"**.

### Caracteres raros en la consola

El programa configura UTF-8 automáticamente en Windows. Si persisten problemas, ejecute antes:

```powershell
chcp 65001
python main.py
```

### Error al importar `def_riberena`

Asegúrese de ejecutar `main.py` desde la carpeta raíz `DEF_RIBEREÑA`, no desde un subdirectorio.

---

## Referencia

Cálculos basados en: `fuente/MEMORIA DE CALCULO.docx`
