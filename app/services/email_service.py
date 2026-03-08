import resend
from flask import current_app


class EmailService:

    @staticmethod
    def send_password_reset(email, reset_url):

        resend.api_key = current_app.config["RESEND_API_KEY"]

        resend.Emails.send({
            "from": current_app.config["EMAIL_SENDER"],
            "to": [email],
            "subject": "Réinitialisation du mot de passe",
            "html": f"""
            <h2>Réinitialisation du mot de passe</h2>

            <p>Clique sur le bouton ci-dessous pour changer ton mot de passe.</p>

            <a href="{reset_url}" 
            style="padding:10px 20px;background:#2563eb;color:white;text-decoration:none;border-radius:6px;">
            Réinitialiser mon mot de passe
            </a>

            <p>Ce lien expire dans 1 heure.</p>
            """
        })