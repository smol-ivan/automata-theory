import argparse
import re


def extraer_urls(texto):
    patron = re.compile(
        r"((https?|ftp):\/\/)?(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(:[0-9]+)?(\/[^\s]*)?"
    )

    urls = []
    for match in patron.finditer(texto):
        urls.append(match.group(0))

    return urls


def leer_texto(args):
    if args.text_file:
        with open(args.text_file, encoding="utf-8") as f:
            return f.read()

    if args.text:
        return args.text

    print("Ingresa el texto a analizar:")
    return input("> ")


def main():
    parser = argparse.ArgumentParser(description="Extractor simple de URLs")
    parser.add_argument(
        "--text-file",
        help="Ruta de archivo de texto a analizar",
    )
    parser.add_argument(
        "--text",
        help="Texto directo a analizar",
    )
    args = parser.parse_args()

    texto = leer_texto(args)
    urls = extraer_urls(texto)

    print("URLs encontradas:")
    if not urls:
        print("No se encontraron URLs.")
        return

    for i, url in enumerate(urls, 1):
        print(f"{i}. {url}")


if __name__ == "__main__":
    main()
