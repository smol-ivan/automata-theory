import re
from collections import Counter

def analizar_log(archivo):
    '''
    Analiza archivo de log y extrae informacin relevante
    '''
    with open(archivo, "r", encoding="utf-8") as f:
        contenido = f.read()

    # a) Extraer errores
    patron_errores = (
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'    # Timestamp
        r'.*\[ERROR\]'                              # Etiqueta [ERROR]
        r'\s*(.*)'                                  # Mensaje de error
    )
    errores = re.findall(patron_errores, contenido)

    # b) Extraer direcciones IP
    patron_ip = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    ips = re.findall(patron_ip, contenido)

    # c) Extraer archivos
    patron_archivos = r'(/[\w\/.]+)'
    archivos = re.findall(patron_archivos, contenido)

    # d) Contar por tipo
    patron_tipo = r'\[(ERROR|INFO|WARNING)\]'
    tipos = re.findall(patron_tipo, contenido)
    contador = Counter(tipos)

    # e) Extaer tiempos
    patron_tiempo = r'(\d+ms)'
    tiempos = re.findall(patron_tiempo, contenido)

    # Mostrar resultados
    print("=== Análisis de sistema.log ===")
    print("ERRORES encontrados:")
    for timestamp, mensaje in errores:
        print(f"[{timestamp}] {mensaje}")
    
    print("IPs detectadas:")
    for ip in ips:
        print(ip)
    
    print("Archivos mencionados:")
    for archivo in archivos:
        print(archivo)
    
    print("Resumen por tipo:")
    for tipo in ['ERROR', 'INFO', 'WARNING']:
        print(f"{tipo}: {contador[tipo]}")
    
    print("Tiempos de ejecución:")
    for tiempo in tiempos:
        print(tiempo)

if __name__ == "__main__":
    analizar_log("./pruebas/sistema.log")
