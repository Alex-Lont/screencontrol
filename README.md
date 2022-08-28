# LCD controller 
set pin and time via the .env file <br>
## setting up the service
copy service to pi <br>
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
view logs
```
jounralctl -u screencontrol.service
```