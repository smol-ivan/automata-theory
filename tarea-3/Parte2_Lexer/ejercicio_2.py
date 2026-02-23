import sys

import ply.lex as lex


class TransformadorCodigo:
    states = (
        ("COMENTARIO_BLOQUE", "exclusive"),
    )

    tokens = (
        "COMENTARIO_LINEA",
        "COMENTARIO_BLOQUE_INICIO",
        "IDENTIFICADOR",
        "ESPACIOS",
        "SALTO",
        "OTRO",
    )

    def __init__(self):
        self.lineas_originales = 0
        self.lineas_finales = 0
        self.comentarios_eliminados = 0
        self.salida = []
        self.lexer = lex.lex(module=self)

    def snake_to_camel(self, snake):
        partes = snake.split("_")
        if not partes:
            return snake
        base = partes[0]
        resto = "".join(p.capitalize() for p in partes[1:] if p)
        return base + resto

    def t_COMENTARIO_LINEA(self, t):
        r"//[^\n]*"
        self.comentarios_eliminados += 1

    def t_COMENTARIO_BLOQUE_INICIO(self, t):
        r"/\*"
        self.comentarios_eliminados += 1
        t.lexer.begin("COMENTARIO_BLOQUE")

    def t_IDENTIFICADOR(self, t):
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        if "_" in t.value:
            self.salida.append(self.snake_to_camel(t.value))
        else:
            self.salida.append(t.value)

    def t_ESPACIOS(self, t):
        r"[ \t]+"
        if not self.salida:
            return
        if self.salida[-1] not in {" ", "\n"}:
            self.salida.append(" ")

    def t_SALTO(self, t):
        r"\n"
        self.lineas_originales += 1
        self.lineas_finales += 1
        if self.salida and self.salida[-1] == " ":
            self.salida.pop()
        self.salida.append("\n")

    def t_OTRO(self, t):
        r"."
        self.salida.append(t.value)

    def t_error(self, t):
        t.lexer.skip(1)

    def t_COMENTARIO_BLOQUE_fin(self, t):
        r"\*/"
        t.lexer.begin("INITIAL")

    def t_COMENTARIO_BLOQUE_salto(self, t):
        r"\n"
        self.lineas_originales += 1

    def t_COMENTARIO_BLOQUE_cualquier(self, t):
        r"."
        pass

    def t_COMENTARIO_BLOQUE_error(self, t):
        t.lexer.skip(1)

    def transformar(self, texto):
        self.lexer.input(texto)
        for _ in self.lexer:
            pass

        if texto and not texto.endswith("\n"):
            self.lineas_originales += 1
            if self.salida and self.salida[-1] != "\n":
                self.lineas_finales += 1

        return "".join(self.salida)


def main():
    if len(sys.argv) < 3:
        print(f"Uso: python {sys.argv[0]} <entrada> <salida>")
        sys.exit(1)

    archivo_entrada = sys.argv[1]
    archivo_salida = sys.argv[2]

    with open(archivo_entrada, "r", encoding="utf-8") as f:
        contenido = f.read()

    transformador = TransformadorCodigo()
    resultado = transformador.transformar(contenido)

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(resultado)

    print("=== Transformación completada ===")
    print(f"Líneas originales: {transformador.lineas_originales}")
    print(f"Líneas finales: {transformador.lineas_finales}")
    print(f"Comentarios eliminados: {transformador.comentarios_eliminados}")

    if transformador.lineas_originales > 0:
        reduccion = 100.0 * (transformador.lineas_originales - transformador.lineas_finales) / transformador.lineas_originales
    else:
        reduccion = 0.0
    print(f"Reducción: {reduccion:.1f}%")


if __name__ == "__main__":
    main()
