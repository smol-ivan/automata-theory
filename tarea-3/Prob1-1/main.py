import re


def validar_rfc(rfc):
    """
    Valida RFC mexicano con homoclave
    """
    patron = r""
    return bool(re.fullmatch(patron, rfc))


def validar_matricula_uam(matricula):
    """
    Valida matricula UAM
    """
    patron = r""
    return bool(re.fullmatch(patron, matricula))


def validar_ipv4(ip):
    """
    Valida direccion IPv4
    """
    patron = r""
    return bool(re.fullmatch(patron, ip))


def validar_password_fuertes(password):
    """
    Valida password fuerte
    """
    # Usar lookahead assertinons (?=...)
    pass


if __name__ == "__main__":
    # RFC
    assert validar_rfc("") == True
    assert validar_rfc("") == True
