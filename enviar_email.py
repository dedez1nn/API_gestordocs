import smtplib
from email.message import EmailMessage

class Email:
    def __init__(self, remetente, senha, destinatario, assunto):
        self.remetente = remetente
        self.senha = senha
        self.destinatario = destinatario
        self.assunto = assunto

    def enviar_email_com_anexo_base64(self, corpo_email, pdf_bytes, nome_arquivo):
        try:
            msg = EmailMessage()
            msg['From'] = self.remetente
            msg['To'] = ", ".join(self.destinatario)
            msg['Subject'] = self.assunto
            msg.set_content(corpo_email)

            msg.add_attachment(
                pdf_bytes,
                maintype='application',
                subtype='pdf',
                filename=nome_arquivo
            )

            # Tente diferentes portas e métodos
            portas = [587, 465, 25]

            for porta in portas:
                try:
                    if porta == 587:
                        with smtplib.SMTP('smtp.gmail.com', porta, timeout=30) as smtp:
                            smtp.starttls()
                            smtp.login(self.remetente, self.senha)
                            smtp.send_message(msg)
                    else:
                        with smtplib.SMTP_SSL('smtp.gmail.com', porta, timeout=30) as smtp:
                            smtp.login(self.remetente, self.senha)
                            smtp.send_message(msg)

                    print(f"✅ Email enviado via porta {porta}")
                    return 1

                except Exception as e:
                    print(f"❌ Porta {porta} falhou: {e}")
                    continue

            return 0

        except Exception as e:
            print(f"Erro ao enviar o e-mail: {e}")
            return 0