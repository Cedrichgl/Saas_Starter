from fastapi_mail import FastMail, MessageSchema, MessageType

from app.config import get_mail_config


async def send_verification_email(email: str, token: str):
    config = get_mail_config()
    fm = FastMail(config)

    message = MessageSchema(
        subject="Vérification de votre compte",
        recipients=[email],
        body=f"Votre token de vérification : {token}",
        subtype=MessageType.plain,
    )

    await fm.send_message(message)


async def send_reset_email(email: str, token: str):

    config = get_mail_config()
    fm = FastMail(config)

    message = MessageSchema(
        subject="Modification de votre mot de passe",
        recipients=[email],
        # body=f"Votre lien de rénitialisation : {token}",
        body=f"Votre lien de rénitialisation : http://localhost:8000/auth/reset-password?token={token}",
        subtype=MessageType.plain,
    )

    await fm.send_message(message)
