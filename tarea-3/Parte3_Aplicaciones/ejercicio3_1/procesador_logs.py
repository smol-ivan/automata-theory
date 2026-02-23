from collections import Counter, defaultdict

COMANDOS_PELIGROSOS = ["rm -rf", "dd", "mkfs"]


def cargar_blacklist(ruta_blacklist):
    """Carga IPs sospechosas desde archivo, una por línea."""
    ips = set()
    try:
        with open(ruta_blacklist, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                ip = linea.strip()
                if ip:
                    ips.add(ip)
    except FileNotFoundError:
        pass
    return ips


def crear_estado():
    """Estructuras en memoria para conteos y estadísticas."""
    return {
        "totales_evento": Counter({"LOGIN_FAIL": 0, "LOGIN_OK": 0, "COMMAND": 0}),
        "alertas_severidad": Counter({"BAJA": 0, "MEDIA": 0, "ALTA": 0}),
        "actividad_minuto": Counter(),
        "actividad_ip": Counter(),
        "login_fail_por_ip_minuto": defaultdict(int),
    }


def procesar_evento(evento, estado, blacklist):
    """Procesa un evento y regresa lista de alertas detectadas en tiempo real."""
    alertas = []

    tipo = evento["tipo"]
    ip = evento["ip"]
    mensaje = evento["mensaje"]
    minuto = evento["minuto"]

    estado["totales_evento"][tipo] += 1
    estado["actividad_minuto"][minuto] += 1
    estado["actividad_ip"][ip] += 1

    if ip in blacklist:
        estado["alertas_severidad"]["BAJA"] += 1
        alertas.append(f"[BAJA] IP en blacklist: {ip} ({evento['timestamp']})")

    if tipo == "COMMAND":
        for cmd in COMANDOS_PELIGROSOS:
            if cmd in mensaje:
                estado["alertas_severidad"]["MEDIA"] += 1
                alertas.append(f"[MEDIA] Comando peligroso '{cmd}' desde {ip} ({evento['timestamp']})")
                break

    if tipo == "LOGIN_FAIL":
        clave = (ip, minuto)
        estado["login_fail_por_ip_minuto"][clave] += 1
        if estado["login_fail_por_ip_minuto"][clave] > 5:
            estado["alertas_severidad"]["ALTA"] += 1
            total = estado["login_fail_por_ip_minuto"][clave]
            alertas.append(f"[ALTA] {total} LOGIN_FAIL para {ip} en {minuto}")

    return alertas
