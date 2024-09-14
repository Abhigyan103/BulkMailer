import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class MailerService :

    def __init__(self, email=None, password=None, SMTP_SERVER = "smtp.gmail.com", SMTP_PORT = 587) :
        if email is None :
            email = input("Enter login email: ")
        if password is None :
            password = getpass.getpass("Enter login password: ")
        self.server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
        self.server.starttls()
        self.server.login(email,password)

    def __enter__(self):
        return self

    def __exit__(self, *args) :
        try:
            self.server.quit()
        except Exception:
            pass
        finally:
            self.server.close()

    def send_email(self,to_email, subject, messages_list, attachments_list=[]):
        try:
            # Create a message object
            msg = MIMEMultipart()
            msg['From'] = self.server.user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add message body to email
            for message in messages_list:
                msg.attach(MIMEText(message[0], message[1]))

            for attachments in attachments_list:
                with open(attachments, "rb") as attachment:
                    mime_base = MIMEBase('application', 'octet-stream')  # For binary data
                    mime_base.set_payload(attachment.read())  # Set payload

                # Encode in base64
                encoders.encode_base64(mime_base)

                # Add header with the file name
                mime_base.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(attachments)}'
                )
                msg.attach(mime_base)

            # Send the email
            self.server.sendmail(self.server.user, to_email,msg.as_string())
            print(f'Email sent to {to_email}')
        except Exception as e:
            print(f'Failed to send email to {to_email}. Error: {str(e)}')