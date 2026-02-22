import re


def validar_rfc(rfc):
    """
    Valida RFC mexicano con homoclave
    """
    # 4 letras (incluye Ñ/&) + 6 dígitos (fecha YYMMDD) + 3 caracteres alfanuméricos
    patron = r"[A-ZÑ&]{4}\d{6}[A-Z0-9]{3}"
    # Usamos IGNORECASE para aceptar letras en mayúscula o minúscula
    return bool(re.fullmatch(patron, rfc, re.IGNORECASE))


def validar_matricula_uam(matricula):
    """
    Valida matricula UAM
    """
    # Según los ejemplos, la matrícula tiene 10 dígitos: 2 del año + 8 dígitos
    patron = r"\d{10}"
    return bool(re.fullmatch(patron, matricula))


def validar_ipv4(ip):
    """
    Valida direccion IPv4
    """
    # Definir patrón para un octeto 0-255
    octeto = r"(?:25[0-5]|2[0-4]\d|1?\d?\d)"
    patron = rf"{octeto}(?:\.{octeto}){{3}}"
    return bool(re.fullmatch(patron, ip))


def validar_password_fuertes(password):
    """
    Valida password fuerte
    """
    patron = (
        r'^'
        r'(?=(?:.*[A-Z]){2,})'      # al menos 2 mayúsculas
        r'(?=(?:.*[a-z]){2,})'      # al menos 2 minúsculas
        r'(?=(?:.*\d){2,})'         # al menos 2 dígitos
        r'(?=.*[!@#$%^&*])'         # al menos 1 carácter especial
        r'.{10,}$'                  # longitud mínima 10
    )
    return bool(re.fullmatch(patron, password))


if __name__ == "__main__":
    # RFC
    assert validar_rfc("AAAA850101ABC") == True
    assert validar_rfc("XEXX900315XY9") == True
    assert validar_rfc("AAA850101ABC") == False
    assert validar_rfc("AAAA85010ABC") == False

    # Matricula UAM
    assert validar_matricula_uam("2223456789") == True
    assert validar_matricula_uam("1812345678") == True
    assert validar_matricula_uam("223456789") == False
    assert validar_matricula_uam("22234567890") == False

    # IPv4
    assert validar_ipv4("192.168.1.1") == True
    assert validar_ipv4("10.0.0.255") == True
    assert validar_ipv4("256.1.1.1") == False
    assert validar_ipv4("192.168.1") == False

    # Password fuerte
    assert validar_password_fuertes("Abc123!Xyz456#") == True
    assert validar_password_fuertes("Pass@@Word99") == True
    assert validar_password_fuertes("Password1!") == False
    assert validar_password_fuertes("NODIGITS!@") == False

    print("Todas las pruebas pasaron exitosamente.")