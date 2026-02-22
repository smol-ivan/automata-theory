import re

class CifradorROT:
    """
    Cifrador ROT-N con validación de patrones
    """
    def __init__(self, n=13):
        self.n = n
        # Patrones que NO se cifran: se detectan y se restauran al final
        self.patrones = [
            (r'https?://[^\s]+', 'URL'),  
            (r'www\.[^\s]+', 'URL_WWW'),
            (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 'EMAIL'),
            (r'\(\d{3}\)\s*\d{3}-\d{4}', 'TELEFONO'),
            (r'\d{1,2}/\d{1,2}/\d{4}', 'FECHA_DMY'),
            (r'\d{4}-\d{1,2}-\d{1,2}', 'FECHA_YMD')
        ]

    def cifrar(self, char):
        '''
        Cifra un solo caracter con ROT-N
        '''
        if char.isalpha():
            # Definir el rango según mayúscula o minúscula
            inicio = ord('A') if char.isupper() else ord('a')
            # Aplicar ROT-N preservando el rango
            desplazado = (ord(char) - inicio + self.n) % 26
            return chr(inicio + desplazado)
        return char

    def cifrar_texto(self, texto):
        '''
        Cifra texto preservando patrones
        '''
        # 1. Guardar patrones encontrados
        patrones_encontrados = {}
        texto_marcado = texto
        contador = 0

        for patron, nombre in self.patrones:
            # Se buscan coincidencias en el texto actual y se reemplazan por #id#
            matches = list(re.finditer(patron, texto_marcado))
            for match in matches:
                # El placeholder usa símbolos/dígitos para que ROT-N no lo altere
                placeholder = f"#{contador}#"
                patrones_encontrados[placeholder] = match.group(0)
                texto_marcado = texto_marcado.replace(match.group(0), placeholder, 1)
                contador += 1

        # 2. Cifrar solo el texto normal (los placeholders se mantienen iguales)
        texto_cifrado = ''.join(self.cifrar(char) for char in texto_marcado)

        # 3. Restaurar cada placeholder con su texto original (URL, email, etc.)
        for placeholder, patron_original in patrones_encontrados.items():
            texto_cifrado = texto_cifrado.replace(placeholder, patron_original)

        return texto_cifrado

    def descifrar_texto(self, texto):
        '''
        Descifra texto (ROT inverso)
        '''
        # Descifrar es aplicar ROT con N inverso: 26 - N
        cifrador_inverso = CifradorROT(n=(26 - self.n) % 26)
        return cifrador_inverso.cifrar_texto(texto)

    def cifrar_archivo(self, entrada, salida):
        '''
        Cifra el contenido de un archivo
        '''
        with open(entrada, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        cifrado = self.cifrar_texto(contenido)

        with open(salida, 'w', encoding='utf-8') as f:
            f.write(cifrado)

        print(f"Archivo cifrado: {salida}")

    def descifrar_archivo(self, entrada, salida):
        '''
        Descifra el contenido de un archivo
        '''
        with open(entrada, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        descifrado = self.descifrar_texto(contenido)

        with open(salida, 'w', encoding='utf-8') as f:
            f.write(descifrado)

        print(f"Archivo descifrado: {salida}")

if __name__ == "__main__":
    output_cifrado_file = "output_ejercicio3_cifrado.txt"
    output_descifrado_file = "output_ejercicio3_descifrado.txt"
    input_file = "entrada_cifrado.txt"
    cifrador = CifradorROT(n=13)
    cifrador.cifrar_archivo(f'./pruebas/{input_file}', f'./salidas/{output_cifrado_file}')
    cifrador.descifrar_archivo(f'./salidas/{output_cifrado_file}', f'./salidas/{output_descifrado_file}')