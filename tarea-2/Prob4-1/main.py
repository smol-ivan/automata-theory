import argparse
import json


def cargar_afd(ruta_afd):
    with open(ruta_afd, encoding="utf-8") as f:
        afd = json.load(f)

    transiciones = {}
    for key, value in afd["transiciones"].items():
        estado, simbolo = key.split(",")
        transiciones[(estado, simbolo)] = value

    return {
        "estados": set(afd["estados"]),
        "alfabeto": set(afd["alfabeto"]),
        "estado_inicial": afd["estado_inicial"],
        "estados_finales": set(afd["estados_finales"]),
        "transiciones": transiciones,
    }


def simular_afd(afd, cadena):
    secuencia = [afd["estado_inicial"]]
    estado_actual = afd["estado_inicial"]

    for simbolo in cadena:
        if simbolo not in afd["alfabeto"]:
            return secuencia, "RECHAZADA", f"Simbolo invalido: {simbolo}"

        if (estado_actual, simbolo) not in afd["transiciones"]:
            return secuencia, "RECHAZADA", "Transicion no definida"

        estado_actual = afd["transiciones"][(estado_actual, simbolo)]
        secuencia.append(estado_actual)

    resultado = "ACEPTADA" if estado_actual in afd["estados_finales"] else "RECHAZADA"
    return secuencia, resultado, None


def main():
    parser = argparse.ArgumentParser(description="Simulador generico de AFD")
    parser.add_argument(
        "--afd-file",
        default="./formato_entrada.json",
        help="Ruta al archivo JSON con la definicion del AFD",
    )
    parser.add_argument("--cadena", help="Cadena a evaluar")
    args = parser.parse_args()

    afd = cargar_afd(args.afd_file)
    cadena = (
        args.cadena
        if args.cadena is not None
        else input("Ingrese la cadena a analizar:")
    )

    secuencia, resultado, error = simular_afd(afd, cadena)

    if error is not None:
        print(error)

    print("Secuencia: ->", secuencia)
    print("Resultado:", resultado)


if __name__ == "__main__":
    main()
