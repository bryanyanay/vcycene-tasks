import serial
import struct
from pynput import keyboard
from datetime import datetime

# don't use pynput? we may want to switch to the keyboard package, apparently this one only detects spaces if the correct terminal window is in focus

port = "\\\\.\\CNCA0"       # port to read from
filePath = "dataRecord.txt" # file to write to

def readLine(port):
  """
  reads 16 bytes from port (which is a pySerial object)
   - if less than 16 bytes are read, returns False
   - otherwise returns dictionary of the data
  """
  # with serial.Serial(port, timeout=2) as s:
  #   s.set_buffer_size(rx_size=12800, tx_size=12800)
  #   print("\n>>> receiving from ", port, " ...")
  #   dataBin = s.read(16)
  #   print("received: ", dataBin)
  
  print("\n>>> receiving from ", port.name, " ...")
  dataBin = port.read(16)
  print("received: ", dataBin)

  if len(dataBin) != 16:
    print("NOT 16 bytes!")
    return False
  
  data = struct.unpack("<bbbHHIIx", dataBin)

  dataDict = {
    "temps": [data[0], data[1], data[2]],
    "pres": [data[3], data[4]],
    "gasres": [data[5], data[6]]
  }

  print("unpacked to: ", dataDict)
  return dataDict

def writeLine(filePath, data):
  """
  Writes a data line to the file at filePath
   - appends the new data
  Data from the line is taken from the dictionary
  """
  with open(filePath, "a") as file:
    file.write(f'{datetime.now()}-{data["temps"][0]},{data["temps"][1]},{data["temps"][2]},{data["pres"][0]},{data["pres"][1]},{data["gasres"][0]},{data["gasres"][1]}\n')

def onPress(key):
  if key == keyboard.Key.space:
    return False 

listener = keyboard.Listener(on_press=onPress) 
listener.start()


s = serial.Serial(port, timeout=2)
s.set_buffer_size(rx_size=12800, tx_size=12800)

while True:
  dataDict = readLine(s)
  if dataDict:
    writeLine(filePath, dataDict)

  if not listener.is_alive():
    print("\n>>> Space key pressed, exiting program\n")
    s.close()
    break

listener.join()

