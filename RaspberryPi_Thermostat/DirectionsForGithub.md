Step 1 - Built Wiring Diagram - Post 
Step 2 - Set up influxDB Container 
Step 3 - Wrote Code to export data to influx DB
Step 4 - Set up grafana container 
Step 5 - Built the query for water sensors grafana using influx....you can use influxe's GUI and then copy the query. 
Step 6 - Added some overrides in Grafana to make the charts pretty. 
Step 7 - Went back to pi to set my script up as a service so I don't have to run it all the time. 
Step 7 - Enjoyed. 





This is to configure it as a service


[Unit]
Description=This is the water sensor script
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/stinkypete/Desktop/WaterSensors/WaterSensors.py
WorkingDirectory=/home/stinkypete/Desktop/WaterSensors
StandardOutput=inherit
StandardError=inherit
Restart=always
User=stinkypete

[Install]
WantedBy=multi-user.target



------------------------

Need to do - 

ID Each sensor 

Build out grafana 
do screenshots 




from(bucket: "WaterSensorBucket")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_field"] == "temp_fahrenheit")
  |> filter(fn: (r) => r["sensor"] == "28-3ce1d443105c" or r["sensor"] == "28-3ce1d4437d35" or r["sensor"] == "28-3ce1d4431624")
  |> map(fn: (r) => ({
        r with
        sensor_name: if r["sensor"] == "28-3ce1d443105c" then "Sensor A" else if r["sensor"] == "28-3ce1d4437d35" then "Sensor B" else "Sensor C"
  }))
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")




