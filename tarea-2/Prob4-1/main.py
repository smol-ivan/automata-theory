import json

with open("./formato_entrada.json") as f:
    afd = json.load(f)

estados = set(afd["estados"])
alfabeto = set(afd["alfabeto"])
estado_inicial = afd["estado_inicial"]
estados_finales = set(afd["estados_finales"])

transiciones = {}
for key, value in afd["transiciones"].items():
    estado, simbolo = key.split(",")
    transiciones[(estado, simbolo)] = value

cadena = input("Ingrese la cadena a analizar (solo binario):")
secuencia = []

secuencia.append(estado_inicial)
estado_actual = estado_inicial

for i in range(len(cadena)):
    # Con un simbolo invalido se rechaza la cadena
    if simbolo not in alfabeto:
        print(f"Simbolo invalido: {simbolo}")
        break

    # No hay manejo de error por transicion no definida

    # Funcion de transicion
    # Por conveniencia se uso un dirrccionario por lo que:
    # Acceder con la clave (estado_actual, simbolo) es equivalente a evaluar
    # usando la funcion de transicion t(estado, simbolo)
    estado_actual = transiciones[(estado_actual, simbolo)]

    # Guardar en historial de estados
    secuencia.append(estado_actual)

if estado_actual in estados_finales:
    resultado = "ACEPTADA"
else:
    resultado = "RECHAZADA"

print("Secuencia: ->", secuencia)
print("Resultado: ", resultado)
