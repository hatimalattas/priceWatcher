import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import today

today = today()


def send_email(report_data):
    # Email you're sending the message from
    from_email = os.environ['SENDER_EMAIL']
    # Password for your email account
    password = os.environ['EMAIL_PASSWORD']

    # print(from_email, password)

    # Email you're sending the message to
    receiver_emails = ["hatimalattas@outlook.com"]
    # receiver_emails = os.environ['RECEIVER_EMAILS']

    # Email subject
    subject = "DAMAC | Booking.com (MOBILE) | Prices Report | " + today

    report_body = f"DAMAC | Booking.com (MOBILE) | Prices Report | {today}\n\n"
    for room_type, prices in report_data.items():
        report_body += f"Room Type: {room_type}\n"
        report_body += "Our Prices: " + ", ".join(prices['our_prices']) + "\n"
        report_body += "Competitor Prices: " + ", ".join(prices['competitors_prices']) + "\n"
        report_body += "-" * 40 + "\n"
    # Email body
    # for room in report_data:
    #     body += f"Room Type: {room['room_type']}\n"
    #     body += "Competitor Prices: " + ", ".join(map(str, room['competitor_prices'])) + "\n"
    #     body += "Our Prices: " + ", ".join(map(str, room['our_prices'])) + "\n"
    #     body += "-" * 40 + "\n"

    # Create a MIME object
    msg = MIMEMultipart()
    msg['From'] = from_email
    # msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body to the email
    msg.attach(MIMEText(report_body, 'plain'))

    # Server information (e.g., Gmail's SMTP server)
    smtp_server = "smtp.gmail.com"  # This is for Gmail
    smtp_port = 587  # Port for TLS/STARTTLS

    # Send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection
    # print("Logging in...")
    server.login(from_email, password)
    text = msg.as_string()
    for receiver_email in receiver_emails:
        server.sendmail(from_email, receiver_email, text)
    server.quit()
