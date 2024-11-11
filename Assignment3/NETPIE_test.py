import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import json
import random
import ssl

port = 1883
Server_ip = "broker.netpie.io"

Subscribe_Topic = "@msg/chat"
Publish_Topic = "@msg/chat"

Client_ID = "bf5b60c9-7708-457f-817f-449e54769423"
Token = "k4DUq8QpdyGNvfBV9T1pc97dgGLuUiV3"
Secret = "zfGTLHsriJfgSeJdQ18QmG1PzC1M9SbP"

MqttUser_Pass = {"username": Token, "password": Secret}

# Callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(Subscribe_Topic)

#callback for publish
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client(protocol=mqtt.MQTTv311, client_id=Client_ID, clean_session=True)
client.on_connect = on_connect
client.on_message = on_message

client.subscribe(Subscribe_Topic)
client.username_pw_set(Token, Secret)
client.connect(Server_ip, port)
client.loop_start()

while True:
    data = {
        "Temp": random.randrange(30, 40),
        "Humi": random.randrange(50, 80)
    }
    data_out = json.dumps(data)
    client.publish(Publish_Topic, data_out, retain=True)
    print("Publish.....")
    time.sleep(2)
