import re


def extraer_urls(texto):
    patron = re.compile(
        r"((https?|ftp):\/\/)?(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(:[0-9]+)?(\/[^\s]*)?"
    )

    urls = []
    for match in patron.finditer(texto):
        urls.append(match.group(0))

    return urls


texto = "Visita https://github.com y también www.google.com para más info"

urls = extraer_urls(texto)

print("URLs encontradas:")
for i, url in enumerate(urls, 1):
    print(f"{i}. {url}")
