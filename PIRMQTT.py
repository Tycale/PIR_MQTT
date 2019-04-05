import paho.mqtt.client as mqtt
import sys, time, os, urlparse
from PIRMonitor import PIRState

UPDATE_TIME = 5*60 # 5 min

# Inspired from https://www.cloudmqtt.com/docs/python.html

server_uri = os.environ.get('MQTT_SERVER', 'mqtt://localhost:1883')
username = os.environ.get('MQTT_USERNAME', None)
password = os.environ.get('MQTT_PASSWORD', None)
clientid = os.environ.get('MQTT_CLIENT_ID', None)

topic_pir_state = 'state/{}/pir'.format(clientid)

server_parsed = urlparse.urlparse(server_uri)

mqttc = mqtt.Client(client_id=clientid)
if username and password :
    mqttc.username_pw_set(username, password=password)
mqttc.connect(server_parsed.hostname, port=server_parsed.port, keepalive=60)

upir = PIRState(32) 

def on_connect(client, userdata, flags, rc):
    pass
    #print("rc: " + str(rc))

def on_message(client, obj, msg):
    #print("received message: {} -- {} -- retained {}".format(msg.topic,
    #                                          msg.payload, msg.retain))
    pass

def on_publish(client, obj, mid):
    pass
    #print("pulbish: {}, {} ".format(obj, mid))

def on_subscribe(client, obj, mid, granted_qos):
    pass
    #print("Subscribed: {}, {}, {}".format(mid, granted_qos, obj))

def on_log(client, obj, level, string):
    print(string)

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
# mqttc.on_log = on_log

# Start subscribe
mqttc.subscribe(topic_pir_state, qos=0)

# Monitor states + mqtt loop
rc = 0
last_pir_state = None

time.sleep(1)
while rc == 0:
    pir_state = upir.get_str_pir()
    fmt_date = time.strftime("%Y-%m-%d %H:%M")
    if last_pir_state != pir_state:
        last_pir_state = pir_state
        print("[{}] publishing new pir state {}".format(fmt_date, upir.get_str_pir()))
        mqttc.publish(topic_pir_state, upir.get_str_pir())
    rc = mqttc.loop()
    time.sleep(0.2)
print("[{}] exited ! rc: {}".format(fmt_date, rc))

