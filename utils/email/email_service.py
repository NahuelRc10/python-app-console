import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def enviar_email(email, asunto, contenido="", archivo=None):
    usuario = ""        # Estos datos se extraen de variables de entorno del sistema operativo con la libreria os
    clave = ""          # import os

    mime = MIMEMultipart()

    mime['Subject'] = asunto
    mime['From'] = usuario
    mime['To'] = email

    mime.attach(MIMEText(contenido, 'plain'))

    if archivo is not None:
        with open(archivo, "rb") as attachment:
            base = MIMEBase('application', 'octet-stream')
            base.set_payload(attachment.read())
            encoders.encode_base64(base)
            base.add_header('Content-Disposition', f"attachment; filename= {archivo}")
            mime.attach(base)

    context = ssl.create_default_context()

    servidor_url = "smtp.gmail.com"
    puerto = 587

    with smtplib.SMTP_SSL(servidor_url, puerto, context=context) as servidor:
        servidor.ehlo()
        servidor.login(usuario, clave)
        servidor.sendmail(usuario, email, mime.as_string())
