import serial
import struct
from pynput import keyboard
from sys import exit


port = "\\\\.\\CNCA0" # port to read from
stopProgram = False

def readLine(port):
  """
  reads 16 bytes from port
   - if less than 16 bytes are read, returns False
  """
  with serial.Serial(port, timeout=2) as s:
    print("\n>>> receiving from ", port, " ...")
    dataBin = s.read(16)
    print("received: ", dataBin)

  if len(dataBin) != 16:
    return False
  
  data = struct.unpack("<bbbHHIIx", dataBin)

  dataDict = {
    "temps": [data[0], data[1], data[2]],
    "pres": [data[3], data[4]],
    "gasres": [data[5], data[6]]
  }

  print("unpacked to: ", dataDict)
  return dataDict

def onPress(key):
  if key == keyboard.Key.space:
    return False 

listener = keyboard.Listener(on_press=onPress) 
listener.start()

while True:
  readLine(port)
  if not listener.is_alive():
    print("\n>>> Space key pressed, exiting program\n")
    break

listener.join()

