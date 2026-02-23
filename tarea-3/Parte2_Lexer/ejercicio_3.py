import os
import re
import sys
from collections import deque

import ply.lex as lex

COLOR_ROJO = "\033[1;31m"
COLOR_RESET = "\033[0m"


class GrepSimplificado:
    tokens = ("LINEA", "LINEA_FINAL")

    def __init__(self, patron, contexto=0):
        self.patron = patron
        self.contexto = contexto
        self.regex = re.compile(re.escape(patron))
        self.coincidencias = 0
        self.lineas_totales = 0
        self.archivos_escaneados = 0
        self.lexer = lex.lex(module=self)

    def t_LINEA(self, t):
        r"[^\n]*\n"
        self._procesar_linea(t.value[:-1])
        return t

    def t_LINEA_FINAL(self, t):
        r"[^\n]+"
        self._procesar_linea(t.value)
        return t

    def t_error(self, t):
        t.lexer.skip(1)

    def _resaltar(self, linea):
        return self.regex.sub(lambda m: f"{COLOR_ROJO}{m.group(0)}{COLOR_RESET}", linea)

    def _procesar_linea(self, linea):
        self.lineas_totales += 1
        self.num_linea_actual += 1

        hay_match = self.regex.search(linea) is not None

        if hay_match:
            self.coincidencias += 1

            for ln, txt in self.buffer_prev:
                if ln not in self.lineas_mostradas:
                    print(f"  {ln}- {txt}")
                    self.lineas_mostradas.add(ln)

            if self.num_linea_actual not in self.lineas_mostradas:
                print(f"  {self.num_linea_actual}: {self._resaltar(linea)}")
                self.lineas_mostradas.add(self.num_linea_actual)

            self.restante_post = self.contexto
        else:
            if self.restante_post > 0 and self.num_linea_actual not in self.lineas_mostradas:
                print(f"  {self.num_linea_actual}- {linea}")
                self.lineas_mostradas.add(self.num_linea_actual)
                self.restante_post -= 1

        self.buffer_prev.append((self.num_linea_actual, linea))

    def buscar_en_archivo(self, ruta):
        try:
            with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                contenido = f.read()
        except OSError:
            return

        self.archivos_escaneados += 1
        self.num_linea_actual = 0
        self.restante_post = 0
        self.buffer_prev = deque(maxlen=self.contexto)
        self.lineas_mostradas = set()

        print(f"\n==> {ruta} <==")
        self.lexer.input(contenido)
        for _ in self.lexer:
            pass

    def buscar_en_directorio(self, directorio):
        for raiz, _, archivos in os.walk(directorio):
            for nombre in archivos:
                self.buscar_en_archivo(os.path.join(raiz, nombre))


def main():
    if len(sys.argv) < 3:
        print(f"Uso: python {sys.argv[0]} <patron> <ruta> [-C num]")
        return

    patron = sys.argv[1]
    ruta = sys.argv[2]
    contexto = 0

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "-C" and i + 1 < len(sys.argv):
            try:
                contexto = int(sys.argv[i + 1])
            except ValueError:
                contexto = 0
            i += 2
        else:
            i += 1

    buscador = GrepSimplificado(patron, max(contexto, 0))

    if os.path.isdir(ruta):
        buscador.buscar_en_directorio(ruta)
    else:
        buscador.buscar_en_archivo(ruta)

    print("\n--- Estadísticas ---")
    print(f"Archivos escaneados: {buscador.archivos_escaneados}")
    print(f"Líneas escaneadas: {buscador.lineas_totales}")
    print(f"Coincidencias: {buscador.coincidencias}")


if __name__ == "__main__":
    main()
