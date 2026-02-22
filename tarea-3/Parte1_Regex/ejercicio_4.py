import re
from collections import defaultdict


class GeneradorAFND:
    def __init__(self, regex) -> None:
        self.regex = regex
        self.estados = set()
        self.transiciones = defaultdict(lambda: defaultdict(set))
        self.estado_inicial = None
        self.estados_finales = set()
        self.alfabeto = set()
        self.contador_estados = 0

    def nuevo_estado(self):
        """
        Genera un nuevo estado
        """
        estado = f"q{self.contador_estados}"
        self.contador_estados += 1
        self.estados.add(estado)
        return estado

    def validar_regex(self):
        """
        Valida sintaxis de la regex
        """
        # TODO: usar regex para validar regex!
        patron = r"[ab01|*+?()]+"  # Patron que valida parentesis balanceados, etc.
        if not re.fullmatch(patron, self.regex):
            return False

        balance = 0
        prev = ""
        for i, char in enumerate(self.regex):
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:
                    return False

            if char in '|*+?' and (i == 0 or prev in '(|'):
                return False
            if prev == '|' and char in '|)*+?':
                return False
            if char == ')' and prev in '(|':
                return False
            if char in '*+?' and prev in '(|':
                return False
            prev = char

        if balance != 0 or self.regex[-1] == '|':
            return False
        return True

    def parsear(self):
        """Parsea la regex y construye AST"""
        # TODO: Codigo aqui
        # Puedes usar un parser recursivo descendente simple

        tokens = list(self.regex)
        pos = 0

        def parse_expr():
            nonlocal pos
            nodo = parse_concat()
            while pos < len(tokens) and tokens[pos] == '|':
                pos += 1
                derecho = parse_concat()
                nodo = ('or', nodo, derecho)
            return nodo

        def parse_concat():
            nonlocal pos
            nodos = []
            while pos < len(tokens) and tokens[pos] not in ')|':
                nodos.append(parse_factor())
            if not nodos:
                return None
            nodo = nodos[0]
            for siguiente in nodos[1:]:
                nodo = ('concat', nodo, siguiente)
            return nodo

        def parse_factor():
            nonlocal pos
            nodo = parse_base()
            while pos < len(tokens) and tokens[pos] in '*+?':
                op = tokens[pos]
                pos += 1
                if op == '*':
                    nodo = ('star', nodo)
                elif op == '+':
                    nodo = ('plus', nodo)
                else:
                    nodo = ('opt', nodo)
            return nodo

        def parse_base():
            nonlocal pos
            if tokens[pos] == '(':
                pos += 1
                nodo = parse_expr()
                pos += 1  # saltar ')'
                return nodo
            simbolo = tokens[pos]
            pos += 1
            return ('lit', simbolo)

        self.ast = parse_expr()

    def generar_afnd(self):
        """Genera AFND desde la regex"""
        # TODO: Implementacion simplificada
        # del algoritmo de Thompson

        def construir(nodo):
            tipo = nodo[0]

            if tipo == 'lit':
                inicio = self.nuevo_estado()
                fin = self.nuevo_estado()
                simbolo = nodo[1]
                self.alfabeto.add(simbolo)
                self.transiciones[inicio][simbolo].add(fin)
                return inicio, fin

            if tipo == 'concat':
                i1, f1 = construir(nodo[1])
                i2, f2 = construir(nodo[2])
                self.transiciones[f1]['ε'].add(i2)
                return i1, f2

            if tipo == 'or':
                inicio = self.nuevo_estado()
                fin = self.nuevo_estado()
                i1, f1 = construir(nodo[1])
                i2, f2 = construir(nodo[2])
                self.transiciones[inicio]['ε'].update([i1, i2])
                self.transiciones[f1]['ε'].add(fin)
                self.transiciones[f2]['ε'].add(fin)
                return inicio, fin

            if tipo == 'star':
                inicio = self.nuevo_estado()
                fin = self.nuevo_estado()
                i, f = construir(nodo[1])
                self.transiciones[inicio]['ε'].update([i, fin])
                self.transiciones[f]['ε'].update([i, fin])
                return inicio, fin

            if tipo == 'plus':
                inicio = self.nuevo_estado()
                fin = self.nuevo_estado()
                i, f = construir(nodo[1])
                self.transiciones[inicio]['ε'].add(i)
                self.transiciones[f]['ε'].update([i, fin])
                return inicio, fin

            if tipo == 'opt':
                inicio = self.nuevo_estado()
                fin = self.nuevo_estado()
                i, f = construir(nodo[1])
                self.transiciones[inicio]['ε'].update([i, fin])
                self.transiciones[f]['ε'].add(fin)
                return inicio, fin

        self.estado_inicial, fin = construir(self.ast)
        self.estados_finales.add(fin)

    def es_determinista(self):
        """Verifica si el AFND es determinista"""
        # TODO: TU CODIGO AQUI
        for estado in self.estados:
            if 'ε' in self.transiciones[estado] and self.transiciones[estado]['ε']:
                return False
            for simbolo in self.alfabeto:
                if len(self.transiciones[estado][simbolo]) > 1:
                    return False
        return True

    def mostrar_automata(self):
        """Muestra el autómata en formato tabla"""
        print(f"=== Autómata para: {self.regex} ===\n")
        print(f"Estados: {self.estados}")
        print(f"Alfabeto: {self.alfabeto}")
        print(f"Estado inicial: {self.estado_inicial}")
        print(f"Estados finales: {self.estados_finales}\n")
        # Mostrar tabla de transiciones
        # TODO: TU CODIGO AQUI
        alfabeto_ordenado = sorted(self.alfabeto)
        anchos = [max(6, len("Estado"))] + [10 for _ in alfabeto_ordenado]

        def borde():
            return "+" + "+".join("-" * (w + 2) for w in anchos) + "+"

        print("Tabla de transiciones:")
        print(borde())
        encabezado = ["Estado"] + alfabeto_ordenado
        print("| " + " | ".join(t.center(w) for t, w in zip(encabezado, anchos)) + " |")
        print(borde())

        for estado in sorted(self.estados, key=lambda x: int(x[1:])):
            fila = [estado]
            for simbolo in alfabeto_ordenado:
                destinos = sorted(self.transiciones[estado][simbolo], key=lambda x: int(x[1:]))
                celda = "{" + ",".join(destinos) + "}" if destinos else "{}"
                fila.append(celda)
            print("| " + " | ".join(t.center(w) for t, w in zip(fila, anchos)) + " |")

        print(borde())

        # Indicar si es determinista
        if self.es_determinista():
            print("\nTipo de autómata: AFD (Determinista)")
        else:
            print("\nTipo de autómata: AFND (No Determinista)")
        # TODO: Mostrar razón
        if not self.es_determinista():
            for estado in sorted(self.estados, key=lambda x: int(x[1:])):
                if 'ε' in self.transiciones[estado] and self.transiciones[estado]['ε']:
                    print(f"Razón: Desde {estado} hay transiciones ε")
                    return
                for simbolo in sorted(self.alfabeto):
                    if len(self.transiciones[estado][simbolo]) > 1:
                        print(f"Razón: Desde {estado} con '{simbolo}' hay múltiples transiciones")
                        return
        else:
            print("Razón: Cada estado tiene a lo más una transición por símbolo y sin ε")


# Ejemplo de uso
if __name__ == "__main__":
    regex = "(a|b)*abb"
    generador = GeneradorAFND(regex)
    if generador.validar_regex():
        generador.parsear()
        generador.generar_afnd()
        generador.mostrar_automata()
    else:
        print("Error: Expresión regular inválida")
