import paho.mqtt.client as mqtt

broker = "localhost"
topic = "Control"

def connectCallback(client, userdata, flags, rc):
  print("Connected, result code: ", rc)

client = mqtt.Client()
client.on_connect = connectCallback

client.connect(broker, 1883)

client.publish(topic, "1st message to Control topic!")
client.loop()

client.publish(topic, "2nd message to Control topic!")
client.loop()

client.disconnect()