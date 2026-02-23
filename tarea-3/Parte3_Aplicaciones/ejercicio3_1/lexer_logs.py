import re

PATRON_LOG = re.compile(
    r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '
    r'(?P<tipo>LOGIN_FAIL|LOGIN_OK|COMMAND) '
    r'(?P<ip>(?:\d{1,3}\.){3}\d{1,3}) '
    r'(?P<mensaje>.*)$'
)


def parsear_linea_log(linea):
    """Parsea una línea de log con el formato definido en el ejercicio."""
    texto = linea.strip()
    if not texto:
        return None

    match = PATRON_LOG.match(texto)
    if not match:
        return None

    evento = match.groupdict()
    evento["minuto"] = evento["timestamp"][:16]  # YYYY-MM-DD HH:MM
    return evento
