from pathlib import Path

from lexer_logs import parsear_linea_log
from procesador_logs import cargar_blacklist, crear_estado, procesar_evento
from reporte_html import generar_reporte_html


def main():
    base = Path(__file__).resolve().parent
    ruta_log = base / "pruebas" / "seguridad.log"
    ruta_blacklist = base / "config" / "blacklist.txt"
    ruta_reporte = base / "salidas" / "reporte.html"

    blacklist = cargar_blacklist(ruta_blacklist)
    estado = crear_estado()

    with open(ruta_log, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            evento = parsear_linea_log(linea)
            if evento is None:
                continue

            alertas = procesar_evento(evento, estado, blacklist)
            for alerta in alertas:
                print(alerta)

    generar_reporte_html(estado, ruta_reporte)
    print(f"Reporte generado en: {ruta_reporte}")


if __name__ == "__main__":
    main()
