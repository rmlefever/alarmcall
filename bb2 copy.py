# active 4.0

import alarminfo
import time
from twilio.rest import Client
import RPi.GPIO as GPIO
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import paho.mqtt.client as mqtt
import socket
import datetime
import json


# contact details
centre = alarminfo.alarminfo["centre"]  # site name
loc = alarminfo.alarminfo["loc"]  # room name
gpio_pin = alarminfo.alarminfo["gpio_pin"]  # GPIO alarm switch pin on pi
phone_numbers = [ alarminfo.alarminfo["sms_1"],alarminfo.alarminfo["sms_2"] ] # Twili

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Callback for successful connection
def on_connect(mclient, userdata, flags, rc):
    print("Connected with result code " + str(rc))

# Callback for disconnection
def on_disconnect(mclient, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection")
    else:   
        print("Disconnected")
    mclient.reconnect()



#mqtt setup
broker_url = alarminfo.alarminfo["broker"]
roomname = alarminfo.alarminfo["roomname"]
broker_port = 1883
mclient = mqtt.Client()
mclient.on_connect = on_connect
mclient.on_disconnect = on_disconnect
mclient.connect(broker_url, broker_port, 60)
topic = alarminfo.alarminfo["topic"] # topic


# find ip
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# get ip
ipad = get_ip_address()


# message content
bodyAct = "EMERGENCY CALL SYSTEM ACTIVATED IN " + centre + " " + loc
bodyRst = "Emergency Call System Reset in " + centre + " " + loc
sys_boot = "Emergency Call System in Monitor Mode at " + centre + " " + loc


# email settings
# user = alarminfo.alarminfo["user"]  # GMAIL Account
# pwd = alarminfo.alarminfo["pwd"]  # GMAIL Password
alm = [alarminfo.alarminfo["alm1"], alarminfo.alarminfo["alm2"]]  # Recipients
# sys = [alarminfo.alarminfo["sys"]]


# twilio credentials
client = Client(alarminfo.alarminfo["twilio1"], alarminfo.alarminfo["twilio2"])
sms_from = alarminfo.alarminfo["sms_from"]  # twilio phone number

    
#MQTT message send
def sendmqtt(): # create json string
   current_time = datetime.datetime.now().strftime("%H:%M")
   x = {  
        "time": current_time,
        "Local_IP": ipad,
        "Local_SSID": roomname,
        "room_name": roomname
   }
   data_out=json.dumps(x) #create JSON object
   print("publish topic",topic, "data out= ",data_out,) # see what we publish
   ret=mclient.publish(topic,data_out,0)    #publish

# SMS definitions

def sendsms():
    try:
        for phone_number in phone_numbers:
            client.messages.create(to=phone_number,
                               from_=sms_from,
                               body=sendbody)
        print('SMS Sent')
    except:
        print("SMS Failed to send")

# Email definitions
def sendmail():
    message = Mail(
        from_email='promisemergencycallsystem@gmail.com',
        to_emails=alm,
        subject=sendbody,
        html_content=sendbody)
    try:
        sg = SendGridAPIClient(alarminfo.alarminfo["SENDGRID_API_KEY"])
        response = sg.send(message)
        print("Email sent successfully")
    except Exception as e:
        print(e.message)




### CODE ###

sendbody = sys_boot  # send intialisation message
print(sendbody) 
messagecounter = 120 # delay for email and text
mqttcounter = 30 # delay for mqtt 
act_state = 0  # Reset alert state
sendmqtt()
time.sleep(3)
print("Press CTRL+C to exit")
try:
    while 1:
        if GPIO.input(gpio_pin) == True and act_state == 0: # if alarm is not active and switch is pressed
                sendbody = bodyAct  # send alarm activated message
                print(sendbody)
                sendsms()
                sendmail()
                act_state = 1
                time.sleep(1)  # wait 1 second

        elif GPIO.input(gpio_pin) == False and act_state == 1:
            sendbody = bodyRst  # send alarm reset message
            print(sendbody)
            sendsms()
            sendmail()
            time.sleep(1)
            act_state = 0

        elif act_state == 1 and messagecounter > 0: # if alarm is active and message counter is greater than 0
            messagecounter = messagecounter - 1
            print(messagecounter)
            time.sleep(1)

        elif act_state == 1 and messagecounter == 0: # if alarm is active and message counter is 0
            sendmqtt()
            sendsms()
            sendmail()
            messagecounter = 120  # Set message counter back to 2 minutes
            time.sleep(1)

        elif act_state == 0 and mqttcounter > 0: # if alarm is not active and mqtt counter is greater than 0
            mqttcounter = mqttcounter - 1
            print(mqttcounter)
            time.sleep(1)

        elif act_state == 0 and mqttcounter == 0: # if alarm is not active and mqtt counter is 0
            sendmqtt()
            mqttcounter = 30    # Set mqtt counter back to 30 seconds
            time.sleep(1)

except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly
    print("\n\nExiting\n\n")
    GPIO.cleanup()

