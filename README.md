# LCD controller 
*designed to run on a raspberry pi*   

Controller to script for LCD screen to turn off at night and in the morning.  
controls screen via a NPN BJT wired accross the switch with the base going to a pin via a series 10k resistor.  
BJT's collector wired to one side of the button and the  emitter to the other.  
define the pin and times in the .env file.  

## Environment File

 - SCREEN_PIN pin which base is connected to. set up for bcm mode of the GPIOs
 - ON_TIME time which screen turns on
 - OFF_TIME time which screen turns off

## Service File

default setting for service, change if in a different location.  
- User=root 
- WorkingDirectory=/home/pi/screencontrol
- ExecStart=/usr/bin/python /home/pi/screencontrol/screen.py 
- Restart=always

User must run as root as using the GPIO pin on the raspberry pi.  
WorkingDirectory so script know where the the log and status file are.  
ExecStart so the service knows where the script is.  
Restart policy, script is a infinite loop, but just incase.

## Setting up the service

copy service to pi
```
sudo cp screencontrol.service /lib/systemd/system/screencontrol.service
```
set file permissions
```
sudo chmod 644 /lib/systemd/system/screencontrol.service
```
load service
```
sudo systemctl daemon-reload
sudo systemctl enable screencontrol.service
```

start service
```
sudo systemctl start screencontrol.service
sudo systemctl status screencontrol.service
```
### Logs
will create a log file screen.log in script folder, log is limited to 5mB.

### txt file
screen.txt is used to hold the current state of the screen for reboots. also allows you to manual interact with screen if you need to change its state. 