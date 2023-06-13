import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow)
from mqttGUI import Ui_MainWindow

import paho.mqtt.client as mqtt


broker = "localhost"
pubTopic = "States"
subTopic = "Control"

class Window(QMainWindow, Ui_MainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setupUi(self)

    self.pushButton.clicked.connect(self.pubMsg)

    self.client = mqtt.Client()
    self.client.on_message = self.onMsg
    self.client.connect(broker, 1883)
    self.client.subscribe(subTopic)
    self.client.loop_start()

  def pubMsg(self):
    self.client.publish(pubTopic, "Hello")

  def onMsg(self, client, userdata, msg):
    text = msg.payload.decode("utf-8")
    self.textEdit.append(text)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  win = Window()
  win.show()
  sys.exit(app.exec())