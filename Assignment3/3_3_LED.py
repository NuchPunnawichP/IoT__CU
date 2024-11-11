import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import json
import random
import ssl

port = 1883
Server_ip = "broker.netpie.io" 

Subscribe_Topic = "@msg/LED"
Publish_Topic = "@shadow/data/update"

Client_ID = "063c3874-0b64-45dc-9ff5-678e12dcebd8"
Token = "kKP8kgMMBCRZ6ow2kkF7Ssv7pufUexR7"
Secret = "VQPN6QRH5vi8EQPkXWF2mciWJHXWGfGs"

MqttUser_Pass = {"username":Token,"password":Secret}

LED_Status = "on"
sensor_data = {"Temp": 0, "Humi": 0, "LED" : LED_Status}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(Subscribe_Topic)

def on_message(client, userdata, msg):
    global LED_Status
    data_receive = msg.payload.decode("UTF-8")
    if data_receive == "on" or data_receive == "off":
        LED_Status = data_receive  # Update LED status
        print(f"LED Status updated to {LED_Status}")


client = mqtt.Client(protocol=mqtt.MQTTv311,client_id=Client_ID, clean_session=True)
client.on_connect = on_connect
client.on_message = on_message

client.subscribe(Subscribe_Topic)
client.username_pw_set(Token,Secret)
client.connect(Server_ip, port)
client.loop_start()

while True:
        sensor_data["Temp"] = random.randrange(30, 40)
        sensor_data["Humi"] = random.randrange(50, 80)
        sensor_data["LED"] = LED_Status
        data_out=json.dumps({"data": sensor_data}) # encode object to JSON
        print(data_out)
        client.publish(Publish_Topic, data_out, retain= True)
        print ("Publish.....")
        time.sleep(2)