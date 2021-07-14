import smtplib
import json
import os

from email.parser import Parser
from email.policy import default
from email.mime.multipart import MIMEMultipart


class EmailHandler:
    def __init__(self, email_content):
        self.config = None
        self.config = self.get_config()
        self.content = email_content

    def get_email_object(self, email_content):
        return Parser(policy=default).parsestr(email_content)

    def modify_email_object(self, email, forward_email):
        sent_to = email["To"]
        sent_from = email["From"]
        subject = email["Subject"]
        
        new_mail = MIMEMultipart('alternative')
        new_mail['Subject'] = f'From: {sent_from} | To: {sent_to} | Subject: {subject}'
        # Send on to new address
        new_mail['To'] = forward_email
        # Send from the address it was sent to
        new_mail['From'] = sent_to

        # attach all email payloads to the new message
        for payload in email.get_payload():
            new_mail.attach(payload)
        
        return new_mail

    def get_config(self):
        if not self.config:
            with open("config.json", "r") as f:
                self.config = json.load(f)
                self.config['smtp_user'] = os.environ.get('SMTP_USER')
                self.config['smtp_password'] = os.environ.get('SMTP_PASSWORD')
                self.config['forward_email'] = os.environ.get('FORWARD_EMAIL')

        return self.config

    def send_mail(self, smtp_server, smtp_port, smtp_user, smtp_password, email):
        with smtplib.SMTP(host=smtp_server, port=smtp_port) as s:
            s.starttls()
            s.login(smtp_user, smtp_password)
            s.send_message(email)

    def handle_mail(self):
        config = self.get_config()
        original_email = self.get_email_object(self.content)
        new_email = self.modify_email_object(original_email, config.get('forward_email'))
        self.send_mail(
            config.get('smtp_server'),
            config.get('smtp_port'),
            config.get('smtp_user'),
            config.get('smtp_password'),
            new_email
        )
        
        print('Finished sending email:')
        print(f'From - {new_email["From"]}')
        print(f'To - {new_email["To"]}')
        print(f'Date - {new_email["Date"]}')
        print(f'Subject - {new_email["Subject"]}')
