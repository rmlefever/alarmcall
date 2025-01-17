import twilio
from twilio.rest import Client
import alarminfo
import argparse
from twilio.base.exceptions import TwilioRestException

# Create argument parser
parser = argparse.ArgumentParser(description="Send an SMS message")
parser.add_argument("telephone", nargs='?', help="The recipient's telephone number")
parser.add_argument("message", nargs='?', help="The message to send")
args = parser.parse_args()

if not args.telephone:
    args.telephone = input("Enter the recipient's telephone number: ")
if not args.message:
    args.message = input("Enter the message to send: ")

try:
    client = Client(alarminfo.alarminfo["twilio1"], alarminfo.alarminfo["twilio2"])

    message = client.messages.create(
        body=args.message,
        to=args.telephone,
        from_= alarminfo.alarminfo["sms_from"]
    )
except TwilioRestException as e:
    print (e)
