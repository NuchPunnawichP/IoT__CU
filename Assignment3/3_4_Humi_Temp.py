import paho.mqtt.client as mqtt
import time
import json
import random

# NETPIE MQTT Broker
Server_ip = "broker.netpie.io"
port = 1883

# NETPIE Credentials (from your NETPIE project)
Client_ID = "bf5b60c9-7708-457f-817f-449e54769423"
Token = "k4DUq8QpdyGNvfBV9T1pc97dgGLuUiV3"
Secret = "zfGTLHsriJfgSeJdQ18QmG1PzC1M9SbP"

# Topic for updating Shadow in NETPIE
Shadow_Update_Topic = "@shadow/data/update"

# Callback function for connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to NETPIE successfully!")
    else:
        print("Failed to connect. Code:", rc)

# Initialize MQTT client and set callbacks
client = mqtt.Client(protocol=mqtt.MQTTv311, client_id=Client_ID, clean_session=True)
client.on_connect = on_connect

# Set username and password for NETPIE
client.username_pw_set(Token, Secret)

# Connect to NETPIE
client.connect(Server_ip, port)
client.loop_start()

# Publish data to NETPIE Shadow in a loop
try:
    while True:
        # Example data to publish
        data = {
            "data": {
                "Temp": random.randrange(30, 40),  # Simulated temperature value
                "Humi": random.randrange(50, 80)   # Simulated humidity value
            }
        }
        data_out = json.dumps(data)
        client.publish(Shadow_Update_Topic, data_out, retain=True)
        print("Published to Shadow:", data_out)
        time.sleep(2)
except KeyboardInterrupt:
    print("Stopped publishing data.")
    client.loop_stop()
    client.disconnect()