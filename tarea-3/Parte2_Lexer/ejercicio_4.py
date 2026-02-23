import re
import sys

import ply.lex as lex


class AnalizadorComplejidad:
    tokens = ("LINEA", "LINEA_FINAL")

    def __init__(self):
        self.complejidad = 1
        self.profundidad = 0
        self.max_profundidad = 0
        self.lineas_codigo = 0
        self.lineas_comentario = 0
        self.lineas_largas = 0

        self.identificadores = []
        self.code_smells = []

        self.en_bloque_comentario = False
        self.funcion_actual_inicio = None
        self.funcion_actual_base = None

        self.lexer = lex.lex(module=self)

    def t_LINEA(self, t):
        r"[^\n]*\n"
        self._procesar_linea(t.value[:-1], t.lexer.lineno)
        t.lexer.lineno += 1
        return t

    def t_LINEA_FINAL(self, t):
        r"[^\n]+"
        self._procesar_linea(t.value, t.lexer.lineno)
        return t

    def t_error(self, t):
        t.lexer.skip(1)

    def detectar_code_smell(self, tipo, linea, detalle=None):
        self.code_smells.append((tipo, linea, detalle))
        if detalle:
            print(f"CODE_SMELL [{tipo}] en linea {linea}: {detalle}")
        else:
            print(f"CODE_SMELL [{tipo}] en linea {linea}")

    def agregar_identificador(self, nombre, linea):
        self.identificadores.append(nombre)
        if len(nombre) == 1 and nombre not in {"i", "j", "k"}:
            self.detectar_code_smell("VAR_UNA_LETRA", linea, nombre)

    def _procesar_linea(self, linea, numero_linea):
        if len(linea) > 80:
            self.lineas_largas += 1
            self.detectar_code_smell("LINEA_LARGA", numero_linea)

        trabajo = linea

        if self.en_bloque_comentario:
            self.lineas_comentario += 1
            if "*/" in trabajo:
                self.en_bloque_comentario = False
                trabajo = trabajo.split("*/", 1)[1]
            else:
                return

        while "/*" in trabajo:
            antes, despues = trabajo.split("/*", 1)
            if antes.strip():
                self._procesar_codigo_en_linea(antes, numero_linea)
            self.lineas_comentario += 1
            if "*/" in despues:
                trabajo = despues.split("*/", 1)[1]
            else:
                self.en_bloque_comentario = True
                return

        if "//" in trabajo:
            codigo, _coment = trabajo.split("//", 1)
            if codigo.strip():
                self._procesar_codigo_en_linea(codigo, numero_linea)
            self.lineas_comentario += 1
            return

        if trabajo.strip():
            self._procesar_codigo_en_linea(trabajo, numero_linea)

    def _procesar_codigo_en_linea(self, codigo, numero_linea):
        self.lineas_codigo += 1

        for _ in re.finditer(r"\b(if|else|while|for|case)\b", codigo):
            self.complejidad += 1
        self.complejidad += codigo.count("&&")
        self.complejidad += codigo.count("||")

        for ch in codigo:
            if ch == "{":
                self.profundidad += 1
                if self.profundidad > self.max_profundidad:
                    self.max_profundidad = self.profundidad
            elif ch == "}":
                self.profundidad = max(0, self.profundidad - 1)

        for nombre in re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", codigo):
            self.agregar_identificador(nombre, numero_linea)

        if self.funcion_actual_inicio is None:
            if re.search(r"\b[a-zA-Z_][a-zA-Z0-9_]*\s+\**\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\([^;]*\)\s*\{", codigo):
                self.funcion_actual_inicio = numero_linea
                self.funcion_actual_base = self.profundidad - 1

        if self.funcion_actual_inicio is not None:
            if self.profundidad <= self.funcion_actual_base:
                longitud = numero_linea - self.funcion_actual_inicio + 1
                if longitud > 50:
                    self.detectar_code_smell("FUNCION_LARGA", self.funcion_actual_inicio, f"{longitud} líneas")
                self.funcion_actual_inicio = None
                self.funcion_actual_base = None

    def analizar_archivo(self, ruta):
        with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
            contenido = f.read()

        self.lexer.lineno = 1
        self.lexer.input(contenido)
        for _ in self.lexer:
            pass

    def mostrar_metricas(self):
        ratio_comentarios = (self.lineas_comentario / self.lineas_codigo) if self.lineas_codigo else 0.0
        if self.identificadores:
            longitud_promedio = sum(len(x) for x in self.identificadores) / len(self.identificadores)
        else:
            longitud_promedio = 0.0

        print("\n=== Métricas de Complejidad ===")
        print(f"Complejidad ciclomática: {self.complejidad}")
        print(f"Profundidad máxima de anidamiento: {self.max_profundidad}")
        print(f"Líneas de código: {self.lineas_codigo}")
        print(f"Líneas de comentarios: {self.lineas_comentario}")
        print(f"Ratio código/comentarios: {ratio_comentarios:.2f}")
        print(f"Longitud promedio de identificadores: {longitud_promedio:.2f}")
        print(f"Líneas largas (>80 chars): {self.lineas_largas}")

        print("\n=== Evaluación ===")
        if self.complejidad > 10:
            print("Complejidad alta - considerar refactorizar")
        if self.max_profundidad > 4:
            print("Anidamiento profundo - simplificar lógica")
        if ratio_comentarios < 0.1:
            print("Pocos comentarios - mejorar documentación")


def main():
    if len(sys.argv) < 2:
        print(f"Uso: python {sys.argv[0]} <archivo.c>")
        sys.exit(1)

    analizador = AnalizadorComplejidad()
    analizador.analizar_archivo(sys.argv[1])
    analizador.mostrar_metricas()


if __name__ == "__main__":
    main()
