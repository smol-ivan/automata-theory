# Tarea 3: Teoría de Autómatas (Python)

**Alumno:** Ivan Javier Gordillo Solis  
**Matrícula:** 2223028708

---

## Requisitos

- Python 3.8+
- Librería Python usada en la Parte 2:
  - `ply`

Instalación (si hace falta):

```bash
python -m pip install ply
```

---

## Estructura real del proyecto

```text
tarea-3/
├── README.md
├── Parte1_Regex/
│   ├── ejercicio_1.py
│   ├── ejercicio_2.py
│   ├── ejercicio_3.py
│   ├── ejercicio_4.py
│   └── pruebas/
│       ├── sistema.log
│       ├── entrada_cifrado.txt
│       ├── ej2_log_normal.log
│       ├── ej2_log_limite.log
│       ├── ej2_log_invalido.log
│       ├── ej3_texto_normal.txt
│       ├── ej3_texto_limite.txt
│       └── ej3_texto_invalido.txt
├── Parte2_Lexer/
│   ├── ejercicio_1.py
│   ├── ejercicio_2.py
│   ├── ejercicio_3.py
│   ├── ejercicio_4.py
│   └── pruebas/
│       ├── ej1_normal.txt
│       ├── ej1_limite.txt
│       ├── ej1_invalido.txt
│       ├── ej2_normal.c
│       ├── ej2_limite.c
│       ├── ej2_invalido.c
│       ├── ej3_normal.txt
│       ├── ej3_limite.txt
│       ├── ej3_invalido.txt
│       ├── ej4_normal.c
│       ├── ej4_limite.c
│       └── ej4_invalido.c
├── Parte3_Aplicaciones/
│   └── ejercicio3_1/
│       ├── main.py
│       ├── lexer_logs.py
│       ├── procesador_logs.py
│       ├── reporte_html.py
│       ├── config/
│       │   └── blacklist.txt
│       ├── pruebas/
│       │   ├── seguridad.log
│       │   ├── log_normal.log
│       │   ├── log_muchos_fallos.log
│       │   ├── log_comandos.log
│       │   ├── ej31_normal.log
│       │   ├── ej31_limite.log
│       │   └── ej31_invalido.log
│       └── salidas/
│           └── reporte.html
└── Prob1-1/
    └── main.py
```

---

## Ejecución

> Ejecutar todos los comandos desde la carpeta `tarea-3/`.

### Parte 1 — Regex

#### Ejercicio 1
```bash
python Parte1_Regex/ejercicio_1.py
```

#### Ejercicio 2 (casos de prueba)
```bash
python Parte1_Regex/ejercicio_2.py pruebas/sistema.log
python Parte1_Regex/ejercicio_2.py Parte1_Regex/pruebas/ej2_log_normal.log
python Parte1_Regex/ejercicio_2.py Parte1_Regex/pruebas/ej2_log_limite.log
python Parte1_Regex/ejercicio_2.py Parte1_Regex/pruebas/ej2_log_invalido.log
```

```bash
mkdir -p Parte1_Regex/salidas
python Parte1_Regex/ejercicio_2.py Parte1_Regex/pruebas/ej2_log_normal.log > Parte1_Regex/salidas/ejercicio2_normal.txt
python Parte1_Regex/ejercicio_2.py Parte1_Regex/pruebas/ej2_log_limite.log > Parte1_Regex/salidas/ejercicio2_limite.txt
python Parte1_Regex/ejercicio_2.py Parte1_Regex/pruebas/ej2_log_invalido.log > Parte1_Regex/salidas/ejercicio2_invalido.txt
```

#### Ejercicio 3 (casos de prueba)
```bash
mkdir -p Parte1_Regex/salidas
python Parte1_Regex/ejercicio_3.py Parte1_Regex/pruebas/ej3_texto_normal.txt Parte1_Regex/salidas/ejercicio3_normal_cifrado.txt Parte1_Regex/salidas/ejercicio3_normal_descifrado.txt
python Parte1_Regex/ejercicio_3.py Parte1_Regex/pruebas/ej3_texto_limite.txt Parte1_Regex/salidas/ejercicio3_limite_cifrado.txt Parte1_Regex/salidas/ejercicio3_limite_descifrado.txt
python Parte1_Regex/ejercicio_3.py Parte1_Regex/pruebas/ej3_texto_invalido.txt Parte1_Regex/salidas/ejercicio3_invalido_cifrado.txt Parte1_Regex/salidas/ejercicio3_invalido_descifrado.txt
```

```bash
python Parte1_Regex/ejercicio_3.py Parte1_Regex/pruebas/ej3_texto_normal.txt Parte1_Regex/salidas/ejercicio3_normal_cifrado.txt Parte1_Regex/salidas/ejercicio3_normal_descifrado.txt > Parte1_Regex/salidas/ejercicio3_normal.txt
```

#### Ejercicio 4
```bash
python Parte1_Regex/ejercicio_4.py
```

---

### Parte 2 — Lexer (Python)

#### Ejercicio 1 (casos de prueba)
```bash
python Parte2_Lexer/ejercicio_1.py Parte2_Lexer/pruebas/ej1_normal.txt
python Parte2_Lexer/ejercicio_1.py Parte2_Lexer/pruebas/ej1_limite.txt
python Parte2_Lexer/ejercicio_1.py Parte2_Lexer/pruebas/ej1_invalido.txt
```

```bash
mkdir -p Parte2_Lexer/salidas
python Parte2_Lexer/ejercicio_1.py Parte2_Lexer/pruebas/ej1_normal.txt > Parte2_Lexer/salidas/ejercicio1_normal.txt
python Parte2_Lexer/ejercicio_1.py Parte2_Lexer/pruebas/ej1_limite.txt > Parte2_Lexer/salidas/ejercicio1_limite.txt
python Parte2_Lexer/ejercicio_1.py Parte2_Lexer/pruebas/ej1_invalido.txt > Parte2_Lexer/salidas/ejercicio1_invalido.txt
```

#### Ejercicio 2 (casos de prueba)
```bash
mkdir -p Parte2_Lexer/salidas
python Parte2_Lexer/ejercicio_2.py Parte2_Lexer/pruebas/ej2_normal.c Parte2_Lexer/salidas/ejercicio2_normal_transformado.c
python Parte2_Lexer/ejercicio_2.py Parte2_Lexer/pruebas/ej2_limite.c Parte2_Lexer/salidas/ejercicio2_limite_transformado.c
python Parte2_Lexer/ejercicio_2.py Parte2_Lexer/pruebas/ej2_invalido.c Parte2_Lexer/salidas/ejercicio2_invalido_transformado.c
```

```bash
python Parte2_Lexer/ejercicio_2.py Parte2_Lexer/pruebas/ej2_normal.c Parte2_Lexer/salidas/ejercicio2_normal_transformado.c > Parte2_Lexer/salidas/ejercicio2_normal.txt
```

#### Ejercicio 3 (casos de prueba)
```bash
python Parte2_Lexer/ejercicio_3.py error Parte2_Lexer/pruebas/ej3_normal.txt -C 1
python Parte2_Lexer/ejercicio_3.py error Parte2_Lexer/pruebas/ej3_limite.txt -C 0
python Parte2_Lexer/ejercicio_3.py error Parte2_Lexer/pruebas/ej3_invalido.txt -C 1
```

```bash
mkdir -p Parte2_Lexer/salidas
python Parte2_Lexer/ejercicio_3.py error Parte2_Lexer/pruebas/ej3_normal.txt -C 1 > Parte2_Lexer/salidas/ejercicio3_normal.txt
python Parte2_Lexer/ejercicio_3.py error Parte2_Lexer/pruebas/ej3_limite.txt -C 0 > Parte2_Lexer/salidas/ejercicio3_limite.txt
python Parte2_Lexer/ejercicio_3.py error Parte2_Lexer/pruebas/ej3_invalido.txt -C 1 > Parte2_Lexer/salidas/ejercicio3_invalido.txt
```

#### Ejercicio 4 (casos de prueba)
```bash
python Parte2_Lexer/ejercicio_4.py Parte2_Lexer/pruebas/ej4_normal.c
python Parte2_Lexer/ejercicio_4.py Parte2_Lexer/pruebas/ej4_limite.c
python Parte2_Lexer/ejercicio_4.py Parte2_Lexer/pruebas/ej4_invalido.c
```

```bash
mkdir -p Parte2_Lexer/salidas
python Parte2_Lexer/ejercicio_4.py Parte2_Lexer/pruebas/ej4_normal.c > Parte2_Lexer/salidas/ejercicio4_normal.txt
python Parte2_Lexer/ejercicio_4.py Parte2_Lexer/pruebas/ej4_limite.c > Parte2_Lexer/salidas/ejercicio4_limite.txt
python Parte2_Lexer/ejercicio_4.py Parte2_Lexer/pruebas/ej4_invalido.c > Parte2_Lexer/salidas/ejercicio4_invalido.txt
```

---

### Parte 3 — Aplicaciones

#### Ejercicio 3.1 (casos de prueba)
```bash
python Parte3_Aplicaciones/ejercicio3_1/main.py Parte3_Aplicaciones/ejercicio3_1/pruebas/ej31_normal.log Parte3_Aplicaciones/ejercicio3_1/config/blacklist.txt Parte3_Aplicaciones/ejercicio3_1/salidas/reporte_ej31_normal.html
python Parte3_Aplicaciones/ejercicio3_1/main.py Parte3_Aplicaciones/ejercicio3_1/pruebas/ej31_limite.log Parte3_Aplicaciones/ejercicio3_1/config/blacklist.txt Parte3_Aplicaciones/ejercicio3_1/salidas/reporte_ej31_limite.html
python Parte3_Aplicaciones/ejercicio3_1/main.py Parte3_Aplicaciones/ejercicio3_1/pruebas/ej31_invalido.log Parte3_Aplicaciones/ejercicio3_1/config/blacklist.txt Parte3_Aplicaciones/ejercicio3_1/salidas/reporte_ej31_invalido.html
```

```bash
python Parte3_Aplicaciones/ejercicio3_1/main.py Parte3_Aplicaciones/ejercicio3_1/pruebas/ej31_normal.log Parte3_Aplicaciones/ejercicio3_1/config/blacklist.txt Parte3_Aplicaciones/ejercicio3_1/salidas/reporte_ej31_normal.html > Parte3_Aplicaciones/ejercicio3_1/salidas/ejercicio31_normal.txt
python Parte3_Aplicaciones/ejercicio3_1/main.py Parte3_Aplicaciones/ejercicio3_1/pruebas/ej31_limite.log Parte3_Aplicaciones/ejercicio3_1/config/blacklist.txt Parte3_Aplicaciones/ejercicio3_1/salidas/reporte_ej31_limite.html > Parte3_Aplicaciones/ejercicio3_1/salidas/ejercicio31_limite.txt
python Parte3_Aplicaciones/ejercicio3_1/main.py Parte3_Aplicaciones/ejercicio3_1/pruebas/ej31_invalido.log Parte3_Aplicaciones/ejercicio3_1/config/blacklist.txt Parte3_Aplicaciones/ejercicio3_1/salidas/reporte_ej31_invalido.html > Parte3_Aplicaciones/ejercicio3_1/salidas/ejercicio31_invalido.txt
```

---

## Ubicación de salidas

- `Parte1_Regex/salidas/`
- `Parte2_Lexer/salidas/`
- `Parte3_Aplicaciones/ejercicio3_1/salidas/`

---

## Decisiones de diseño

- Se usó únicamente **Python** para toda la tarea.
- La Parte 2 se implementó con lexer en Python (sin Flex en C).
- Se mantuvo una implementación simple, con archivos y estructuras en memoria.
- Los casos de prueba están separados por sección y por tipo de caso (normal, límite, inválido).

---

## Nota

La **parte Bonus no fue implementada**.
