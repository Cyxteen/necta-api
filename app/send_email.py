# imports
import smtplib, ssl
from email.message import EmailMessage


def send_verification_email(email, username, verification_code):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "dericmiagie@gmail.com"
    receiver_email = email
    password = 'supbegbocazdourx'
    message = EmailMessage()
    message['Subject'] = 'Email Verification'
    message['From'] = sender_email
    message['To'] = email
    message.set_content(f"Hi {username}, \n\nUse the following codes to verify your email account and activate your account\n\nVerification Code: {verification_code}\n\nIf you did not initiate this action please ignore this message.")

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        try:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.send_message(message)
            server.quit()

        except Exception as e:
            # format this error to display an error during message sending
            print("an error occured");


