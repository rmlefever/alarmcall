This is code to run an alarm call system using raspberry pi and an alarm call button such as the Honeywell AC030 Intruder Alarm Panic Button with Key PA/Distress Button

Install Cheat Sheet
mkdir alarm
 git clone https://github.com/rmlefever/alarmcall.git
 cd alarmcall/
 cp active.py /home/pi/alarm
cd ..
Ls
python3 -m venv /home/pi/alarm/venv # creates a venv directory in whatever directory we use it in 
source /home/pi/alarm/venv/bin/activate # activates it
pip install twilio 
pip install sendgrid 
pip install paho-mqtt  
pip install RPi.GPIO
 vi alarminfo.py (copy edited contents from alarm folder)
i = insert
o= insert on next line
Control-v paste
Esc - exit out of editing mode
: wq Enter
ggdG - wipe file
dd - delete line (eg, dd3 deletes three lines)
:q! = Quit without saving
Setting up the autorun

sudo vi /lib/systemd/system/activepy.service
i = insert

[Unit]
Description=Active Pi Service
After=multi-user.target

[Service]
Type=idle

User=pi
ExecStart=/home/pi/alarm/venv/bin/python /home/pi/alarm/active.py 



Restart=always
RestartSec=30

[Install]

WantedBy=multi-user.target

Esc - exit out of editing mode
: wq Enter

To initiate:


sudo chmod 644 /lib/systemd/system/activepy.service

To activate:


sudo systemctl daemon-reload
sudo systemctl enable activepy.service
sudo systemctl start activepy.service
sudo systemctl status activepy.service

sudo systemctl daemon-reload && sudo systemctl enable activepy.service && sudo systemctl start activepy.service && sudo systemctl status activepy.service

