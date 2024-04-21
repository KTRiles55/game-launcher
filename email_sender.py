import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_confirmation_email(recipient_email):
    # Email configuration
    sender_email = "TechWizardsCSUN@outlook.com"
    sender_password = "Comp380CSUN"
    subject = "Thank you for registering!"

    # Email content
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    body = "Thank you for registering with Tech-Wizards! We appreciate your interest!"
    message.attach(MIMEText(body, 'plain'))

    # Sending the email
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:  # Update SMTP server details
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
