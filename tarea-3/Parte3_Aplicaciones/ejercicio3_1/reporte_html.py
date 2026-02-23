def generar_reporte_html(resumen, ruta_salida):
    """Genera reporte HTML estático con tablas y gráfica de actividad por minuto."""
    totales_evento = resumen["totales_evento"]
    alertas = resumen["alertas_severidad"]

    top_ips = sorted(resumen["actividad_ip"].items(), key=lambda x: x[1], reverse=True)
    actividad_minuto = sorted(resumen["actividad_minuto"].items(), key=lambda x: x[0])

    etiquetas = [m for m, _ in actividad_minuto]
    valores = [c for _, c in actividad_minuto]

    filas_ips = "\n".join(
        f"<tr><td>{ip}</td><td>{conteo}</td></tr>" for ip, conteo in top_ips
    )

    html = f"""<!doctype html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\" />
  <title>Reporte de Seguridad</title>
  <script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script>
</head>
<body>
  <h1>Reporte de Seguridad</h1>

  <h2>Resumen de eventos</h2>
  <table border=\"1\" cellpadding=\"6\">
    <tr><th>Evento</th><th>Total</th></tr>
    <tr><td>LOGIN_FAIL</td><td>{totales_evento['LOGIN_FAIL']}</td></tr>
    <tr><td>LOGIN_OK</td><td>{totales_evento['LOGIN_OK']}</td></tr>
    <tr><td>COMMAND</td><td>{totales_evento['COMMAND']}</td></tr>
  </table>

  <h2>Alertas por severidad</h2>
  <table border=\"1\" cellpadding=\"6\">
    <tr><th>Severidad</th><th>Total</th></tr>
    <tr><td>BAJA</td><td>{alertas['BAJA']}</td></tr>
    <tr><td>MEDIA</td><td>{alertas['MEDIA']}</td></tr>
    <tr><td>ALTA</td><td>{alertas['ALTA']}</td></tr>
  </table>

  <h2>IPs más activas</h2>
  <table border=\"1\" cellpadding=\"6\">
    <tr><th>IP</th><th>Eventos</th></tr>
    {filas_ips}
  </table>

  <h2>Actividad por minuto</h2>
  <canvas id=\"graficaActividad\" width=\"900\" height=\"320\"></canvas>
  <script>
    const etiquetas = {etiquetas};
    const valores = {valores};
    new Chart(document.getElementById('graficaActividad'), {{
      type: 'line',
      data: {{
        labels: etiquetas,
        datasets: [{{
          label: 'Eventos por minuto',
          data: valores,
          borderWidth: 2,
          fill: false,
          tension: 0
        }}]
      }}
    }});
  </script>
</body>
</html>
"""

    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        archivo.write(html)
