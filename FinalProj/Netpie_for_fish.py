import serial
import time
import string
import sys
# import Adafruit_DHT
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json
import random
import ssl
import sys
import requests
import RPi.GPIO as GPIO
from datetime import datetime
import requests

# NETPIE
port = 1883 # default port
Server_ip = "broker.netpie.io"


Subscribe_Topic = "@msg/Pi2/DHT11"
Publish_Topic = "@shadow/data/update"

Client_ID = "152f5bb3-c983-4c38-8820-b00fb47ff1e0"
Token = "RSWi9vrA4HfsjhXT79dbeEgCBpgym3ZW"
Secret = "qJyjtEjcNJHRdbyeBj1kRgL3wF2WoyFk"

MqttUser_Pass = {"username":Token,"password":Secret}

sensor_data = {"Temp": 0, "Light": 0, "Turbinity": 0}


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(Subscribe_Topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# NETPIE
client = mqtt.Client(protocol=mqtt.MQTTv311,client_id=Client_ID, clean_session=True)
client.on_connect = on_connect
client.on_message = on_message

client.subscribe(Subscribe_Topic)
client.username_pw_set(Token,Secret)
client.connect(Server_ip, port)
client.loop_start()


url = "https://notify-api.line.me/api/notify"
token = "H71DKEntyeYy8vTFxuZByY0gcPiiZKkeiTl04Qks9Mq"
headers = {'Authorization': 'Bearer ' + token}

# For display value
try:
    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1  # Set a small timeout
    )
    print(f"Connected to: {ser.portstr}")
except serial.SerialException as e:
    print(f"Failed to connect: {e}")
    exit()

while True:
    data = ser.readline().decode('utf-8').strip()
    data = data.split()

    if len(data) >= 3:
        sensor_data["Temp"] = float(''.join(filter(str.isdigit, data[0]))) / 10000
        sensor_data["Light"] = int(''.join(filter(str.isdigit, data[1])))
        sensor_data["Turbinity"] = float(''.join(filter(str.isdigit, data[2]))) / 100
    sensor_data["Temp"] = random.randint(30, 40)
    sensor_data["Light"] = random.randint(30, 40)
    sensor_data["Turbinity"] = random.randint(30, 40)
    
    temperature = sensor_data["Temp"]
    light_intensity = sensor_data["Light"]
    turbinity = sensor_data["Turbinity"]
    
    data_out=json.dumps({"data": sensor_data}) 
    client.publish(Publish_Topic, data_out, retain= True)
    print ("Publish.....")
    
    if light_intensity >= 60 or temperature >= 25 or turbinity >= 20:
        print('Data is sent')
        st = ( f'\nCurrent temperature: {temperature}\n' f'Current light level: {light_intensity}\n' f'Current turbidity: {turbinity}\n' )
        msg = {
        'message': (None, st),
        'imageFile': open("/home/user/Desktop/dead_fish_two.jpeg","r+b" ),
        #'imageFullsize': open("/home/user/Desktop/dead_fish_two.jpeg"),
        }

        res = requests.post(url, headers=headers, files=msg)

    time.sleep(10)
