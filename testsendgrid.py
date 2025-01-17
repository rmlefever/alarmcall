# python testsendgrid.py recipient@example.com "This is a test email from SendGrid."

import sendgrid
from sendgrid.helpers.mail import *
import alarminfo
import argparse

# Create argument parser
parser = argparse.ArgumentParser(description="Send an email message using SendGrid")
parser.add_argument("recipient_email", nargs='?', help="The recipient's email address")
parser.add_argument("message", nargs='?', help="The message to send")
args = parser.parse_args()

if not args.recipient_email:
    args.recipient_email = input("Enter the recipient's email address: ")
if not args.message:
    args.message = input("Enter the message to send: ")

try:
    sg = sendgrid.SendGridAPIClient(api_key=alarminfo.alarminfo["SENDGRID_API_KEY"])
    from_email = Email(alarminfo.alarminfo["user"])  # Use the Gmail address from alarminfo.py as the sender
    to_email = To(args.recipient_email)
    subject = "Test Email"
    content = Content("text/plain", args.message)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

except Exception as e:
    print(e)
