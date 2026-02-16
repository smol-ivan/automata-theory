import argparse
import unicodedata


class Ocurrencia:
    def __init__(self, palabra, raiz, linea, columna):
        self.palabra = palabra
        self.raiz = raiz
        self.linea = linea
        self.columna = columna

    def __str__(self):
        ROJO = "\033[31m"
        RESET = "\033[0m"

        resaltada = self.palabra.replace(
            self.raiz,
            f"{ROJO}{self.raiz}{RESET}",
            1,
        )

        return f"Linea {self.linea}, Col {self.columna}: {resaltada}"


def normalizar(texto):
    """
    Para mitigar la dificultad de implementacion, al no usar una representacion
    para el lenguaje de las vocales (MAY + MIN) con acentos, se opto por una normalizacion
    no es mas que trbajar con minusculas y sin acentos
    """
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(char for char in texto if unicodedata.category(char) != "Mn")
    return texto


def generar_transiciones(raiz, alfabeto):
    transiciones = {}
    n = len(raiz)

    s_0 = "s0"
    trash = "t"
    estados = [f"q{i}" for i in range(1, n + 1)]
    s_f = f"q{n}"

    for simbolo in alfabeto:
        transiciones[(s_0, simbolo)] = "q1" if simbolo == raiz[0] else trash
        transiciones[(trash, simbolo)] = "q1" if simbolo == raiz[0] else trash

    for i in range(1, n):
        for simbolo in alfabeto:
            if simbolo == raiz[i]:
                transiciones[(f"q{i}", simbolo)] = f"q{i + 1}"
            else:
                transiciones[(f"q{i}", simbolo)] = trash

    # Una vez que la palabra se encuentra en el estado de aceptacion
    # cualquier simbolo adicional no cambia el resultado
    for simbolo in alfabeto:
        transiciones[(s_f, simbolo)] = s_f

    return transiciones


def buscar_raiz(texto, raiz):
    """
    La deteccion de la raiz se realiza durante el recorrido de la palabra. Una vez detectada, se
    continua leyendo la palabra completa para poder reportarla. Se regista la ocurrencia usando la informacion del
    'cursor' implementado
    """
    alfabeto = set("abcdefghijklmnopqrstuvwxyz")
    transiciones = generar_transiciones(raiz, alfabeto)

    ocurrencias = []
    estado_actual = "s0"

    linea = 1
    columna = 0

    # Se ira guardando la palabra que se este recorriendo
    palabra_actual = ""
    # Flag de control
    inicio_palabra = None
    raiz_encontrada = False

    for simbolo in texto:
        if simbolo == "\n":
            # Si hay un salto de linea puede que la ultima palabra tenga la raiz
            if palabra_actual and raiz_encontrada:
                ocurrencias.append(
                    Ocurrencia(palabra_actual, raiz, linea, inicio_palabra)
                )

            linea += 1
            columna = 0
            estado_actual = "s0"
            inicio_palabra = None
            raiz_encontrada = False
            palabra_actual = ""
            continue

        columna += 1

        if simbolo not in alfabeto:
            # Cuando haya puntos finales, comas, etc. Ver si la palabra anterior fue aceptada
            if palabra_actual and raiz_encontrada:
                ocurrencias.append(
                    Ocurrencia(palabra_actual, raiz, linea, inicio_palabra)
                )

            estado_actual = "s0"
            inicio_palabra = None
            palabra_actual = ""
            raiz_encontrada = False
            continue

        # Inicio de nueva palabra
        if palabra_actual == "":
            inicio_palabra = columna

        palabra_actual += simbolo

        # Transicion al siguiente estado
        estado_actual = transiciones[(estado_actual, simbolo)]

        # Estado de aceptacion, palabra aceptada, seguir leyendo palabra completa
        # si aun falta
        if estado_actual == f"q{len(raiz)}":
            raiz_encontrada = True

    if palabra_actual and raiz_encontrada:
        ocurrencias.append(Ocurrencia(palabra_actual, raiz, linea, inicio_palabra))

    return ocurrencias


def main():
    parser = argparse.ArgumentParser(
        description="Buscador de palabras que contienen una raiz"
    )
    parser.add_argument(
        "--text-file",
        default="texto.txt",
        help="Ruta al archivo de texto para analizar",
    )
    parser.add_argument("--raiz", help="Raiz a buscar")
    args = parser.parse_args()

    with open(args.text_file, encoding="utf-8") as f:
        texto = normalizar(f.read())

    raiz = (
        normalizar(args.raiz) if args.raiz is not None else normalizar(input("Raiz: "))
    )

    ocurrencias = buscar_raiz(texto, raiz)

    for ocurrencia in ocurrencias:
        print(ocurrencia)

    print(f"\nTotal: {len(ocurrencias)} ocurencias")


if __name__ == "__main__":
    main()
