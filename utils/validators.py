import re
import bcrypt
from datetime import datetime

def valida_email(email):
    expresion = "\A(?P<name>[\w\-_]+)@(?P<domain>[\w\-_]+).(?P<toplevel>[\w]+)\Z";
    if re.match(expresion, email, re.IGNORECASE):
        return True
    else:
        return False

def cad_contains_digits(cad):
    return cad.isalpha()

def cad_contains_letters(cad):
    return cad.isdigit()

def get_password_crypt(password):
    #salt = os.environ.get("SECRET_PASS")
    salt = "secret"
    password = password.encode()
    salt = bcrypt.gensalt()
    password_crypt = bcrypt.hashpw(password, salt)
    return password_crypt

def valid_input_string(mensaje1, mensaje2):
    cadena = ""
    while True:
        cadena = input("\t" + mensaje1)
        if not cadena.isalpha():
            print(mensaje2)
            continue
        break
    return cadena

def valid_input_float(n):
    try:
        n = float(n)
        return True
    except ValueError:
        return False

def valida_input_date(mensaje):
    fecha = ""
    while True:
        try:
            fecha = input("\t" + mensaje)
            datetime.strptime(fecha, '%Y-%m-%d')
            break
        except ValueError:
            print("Fecha inválida")
    return fecha

def valida_input_date_hasta(mensaje, fecha_desde):
    fecha = ""
    while True:
        try:
            fecha = input("\t" + mensaje)
            fecha = datetime.strptime(fecha, '%Y-%m-%d')
            #if fecha < fecha_desde:
            #    print("La fecha hasta no puede ser menor a la fecha desde!")
            #    continue
            #else:
            #    break
            break
        except ValueError:
            print("Fecha inválida")
    return fecha