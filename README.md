# Rpi-Fan-Contol
This script is designed to control a PWM fan connected to the standard GPIO pins on the Raspberry Pi 5. Since the new Raspberry Pi 5 no longer includes fan settings in the `raspi-config` menu, this script provides a way to manage fan speed.
The script is set up to run with `systemd`, but it can also be executed as a standalone Python script. Note that it requires root privileges to write logs to /var/log/fan_control.log.
The script is configured for the Noctua NF-A4x10 5V PWM fan. If you connect a different fan, you may need to adjust the PWM frequency settings accordingly. Ensure the fan is connected to GPIO Pin 18.

If you want to run this script as a systemd service, please refer to the example service file below:

```
[Unit]
Description=CPU fan service
After=multi-user.target
[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /home/pi/fan_control.py
[Install]
WantedBy=multi-user.target
```
