# PIR MQTT with RaspberryPi

PIR motion sensor is of kind hc-sr501.
PIRMonitor.py can be launched standalone to test your PIR sensor.

PIRMQTT.py is the main file to launch.

## SystemD integration

Copy the pir.service.sample to pir.service and modify the parameters.

Copy the service to the systemd folder and activate it, e.g.:
```
cp pir.service /etc/systemd/system/
systemctl enable pir
systemctl start pir
systemctl status pir
```

