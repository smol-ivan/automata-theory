import sys
from collections import Counter

import ply.lex as lex


class AnalizadorTexto:
    tokens = (
        "EMAIL",
        "URL",
        "PALABRA_COMPUESTA",
        "PALABRA",
        "NUMERO",
        "ESPACIO",
        "PUNTUACION",
    )

    t_EMAIL = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    t_URL = r"https?://[^\s]+|www\.[^\s]+"
    t_PALABRA_COMPUESTA = r"[a-zA-Z]+(?:-[a-zA-Z]+)+"
    t_PALABRA = r"[a-zA-Z]+"
    t_NUMERO = r"\d+"
    t_ESPACIO = r"[ \t\n]+"
    t_PUNTUACION = r"[.,;:!¡?¿()\[\]{}\"'`…-]"

    def __init__(self):
        self.frecuencia_palabras = Counter()
        self.total_numeros = 0
        self.suma_longitudes = 0
        self.emails = set()
        self.urls = set()
        self.palabras_compuestas = set()
        self.lexer = lex.lex(module=self)

    def t_EMAIL(self, t):
        self.emails.add(t.value)
        return t

    def t_URL(self, t):
        self.urls.add(t.value)
        return t

    def t_PALABRA_COMPUESTA(self, t):
        palabra = t.value.lower()
        self.palabras_compuestas.add(palabra)
        self.frecuencia_palabras[palabra] += 1
        self.suma_longitudes += len(palabra)
        return t

    def t_PALABRA(self, t):
        palabra = t.value.lower()
        self.frecuencia_palabras[palabra] += 1
        self.suma_longitudes += len(palabra)
        return t

    def t_NUMERO(self, t):
        self.total_numeros += 1
        return t

    def t_ESPACIO(self, t):
        pass

    def t_PUNTUACION(self, t):
        return t

    def t_error(self, t):
        t.lexer.skip(1)

    def analizar(self, texto):
        self.lexer.input(texto)
        for _ in self.lexer:
            pass

    def mostrar_estadisticas(self):
        total_palabras = sum(self.frecuencia_palabras.values())
        promedio = (self.suma_longitudes / total_palabras) if total_palabras else 0.0

        print("=== Estadísticas del Texto ===")
        print(f"Total de palabras: {total_palabras}")
        print(f"Total de números: {self.total_numeros}")
        print(f"Longitud promedio: {promedio:.2f} caracteres")

        print("Top 10 palabras más frecuentes:")
        for i, (palabra, freq) in enumerate(self.frecuencia_palabras.most_common(10), start=1):
            print(f"{i}. {palabra} ({freq} veces)")

        print("Emails encontrados:")
        for email in sorted(self.emails):
            print(f"- {email}")

        print("URLs encontradas:")
        for url in sorted(self.urls):
            print(f"- {url}")

        print("Palabras compuestas:")
        for palabra in sorted(self.palabras_compuestas):
            print(f"- {palabra}")


def main():
    if len(sys.argv) < 2:
        print(f"Uso: python {sys.argv[0]} <archivo>")
        sys.exit(1)

    ruta = sys.argv[1]
    with open(ruta, "r", encoding="utf-8") as f:
        texto = f.read()

    analizador = AnalizadorTexto()
    analizador.analizar(texto)
    analizador.mostrar_estadisticas()


if __name__ == "__main__":
    main()
