import serial
import struct


port = "\\\\.\\CNCA0" # port to read from

def readLine(port):
  """
  reads 16 bytes from port
   - if less than 16 bytes are read, returns a tuple with 1 element, False

  
  """
  with serial.Serial(port, timeout=2) as s:
    print("\n>>> receiving from ", port, " ...")
    dataBin = s.read(16)
    print("received: ", dataBin)

  if len(dataBin) != 16:
    return (False,)
  
  data = struct.unpack("<bbbHHIIx", dataBin)

  dataDict = {
    "temps": [data[0], data[1], data[2]],
    "pres": [data[3], data[4]],
    "gasres": [data[5], data[6]]
  }

  print("unpacked to: ", dataDict)
  return dataDict

while True:
  readLine(port)

