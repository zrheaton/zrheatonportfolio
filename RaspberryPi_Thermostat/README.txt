This project is a thermostat for my ice barrell but you can use it for really anything. If you're interested in building this same item I've got the directions below. 
Total cost will be between 0 - $50 dependng on what you already have at your house. 

Step 1 - Acquire the materials. You do not need the same exact items that I used but here they are if interested: 

Main Items 
RaspberryPiZeroW - https://www.amazon.com/dp/B0748MPQT4
DS18B20 Temperature Sensors - https://www.amazon.com/dp/B0924NBNZP

Side Items - Jumper wires, Electrical tape, Bread board, maybe a soldering iron.

Step 1 - You'll need to set up your raspberrypi. My go to is that standard - pi imager found on the website: https://www.raspberrypi.com/software/
Step 2 - You'll want to learn a bit about wiring and how breadboards work. My favorite tutorial is this: https://www.youtube.com/watch?v=fq6U5Y14oM4
Step 3 - Pull the containers that you will need. docker pull influxdb:latest & docker pull grafana:latest. Set them both up (fairly straight forward) 
Step 4 - Use the wiring diagram I provided to set up the DS18B20 Temperature Sensors to your RaspberryPi. 
Step 5 - Copy and paste the water sensor code from my github: https://github.com/zrheaton/zrheatonportfolio
Step 6 - Make sure your code is configured to YOUR influxDB. I pulled my credentials out so you can replace yours. 
Step 7 - Don't waste time with InfluxDB syntax. You can build it in the UI and copy it. I also have it set in a file on my github. Just change to your sensor names. 
Step 8 - Add this query to Grafana and you should see data coming through. 
Step 9 - Overrides are the real gold on this project. The data comes in with sensor names and such. You can override the names to make it look pretty. 

Step 10 (Extra) - I added my watersensors.py as a service on my raspberrypi. This way I don't have to set it up with cron or anything. If the pi is on the script runs. 

Do that by modifying the systemd file in /etc/systemd/system/

Something like this will work:


[Unit]
Description=This is the water sensor script
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/stinkypete/Desktop/WaterSensors/WaterSensors.py
WorkingDirectory=/home/stinkypete/Desktop/WaterSensors
StandardOutput=inherit
StandardError=inherit
Restart=always
User=ANYUSER WITH APPROPRIATE PERMISSIONS

[Install]
WantedBy=multi-user.target

------------------------

sudo systemctl daemon-reload
sudo systemctl start <service-name>
sudo systemctl enable <service-name>

sudo systemctl status <service-name>
-------------------

This should get you going! 



