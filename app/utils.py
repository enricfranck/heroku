import os
import random
from typing import Dict

from redmail import gmail


def send_email(
        email_to: str,
        message: str
) -> Dict[str, str]:
    gmail.username = os.getenv("EMAILS_FROM_EMAIL")
    gmail.password = os.getenv("SMTP_PASSWORD")
    try:
        gmail.send(
            subject="Reset password",
            receivers=[email_to],
            text=f"Your reset code is: {message}"
        )
        return {"message": "Send mail successfully"}
    except Exception as e:
        return {"Error": f"{e}"}


def random_mdp():
    possible = "1234567890"
    length = 6
    return ''.join(random.choice(possible) for _ in range(length))
