import serial
import struct
from pynput import keyboard
from datetime import datetime
from mysql.connector import connect, Error

# don't use pynput? we may want to switch to the keyboard package, apparently this one only detects spaces if the correct terminal window is in focus

port = "\\\\.\\CNCA0"       # port to read from
filePath = "dataRecord.txt" # file to write to

password = "" # the mysql database password
with open("password.txt", "r") as f:
  password = f.readline().strip()

def readLine(port):
  """
  reads 16 bytes from port (which is a pySerial object)
   - if less than 16 bytes are read, returns False
   - otherwise returns dictionary of the data
  """

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

def readDataFile(filePath):
  """
  reads the data file and generates a list of lists where each internal list stores a line of data
   - elements in order: date, temps, pressures, gas resistances
  this is the perfect form to pass straight into a executemany command
  """
  data = []
  with open(filePath, "r") as f:
    for line in f:
      line = line.strip() # get rid of ending newline
      if line: # if line not empty
        entry = [line[:26]]
        entry.extend(line[27:].split(","))
      data.append(entry)
  return data

def onPress(key):
  if key == keyboard.Key.space:
    return False 


listener = keyboard.Listener(on_press=onPress) 
listener.start()

s = serial.Serial(port, timeout=2)
s.set_buffer_size(rx_size=12800, tx_size=12800)

with open(filePath, "w") as f: # delete existing contents of the record file
  f.truncate(0)

while True:
  dataDict = readLine(s)
  if dataDict:
    writeLine(filePath, dataDict)

  if not listener.is_alive():
    print("\n>>> Space key pressed, writing to database...\n")

    query = """
      INSERT INTO vcycene_test.data_test 
      (record_date, temperature_1, temperature_2, temperature_3, pressure_1, pressure_2, gas_resistance_1, gas_resistance_2)
      VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
      connection = connect(host="localhost", user="bryan", password=password, database="vcycene_test") 
      with connection.cursor() as c:
        c.executemany(query, readDataFile(filePath))
        connection.commit()
      connection.close()
    except Error as e:
      print(e)

    print("\n>>> Now ending program...")
    s.close()
    break

listener.join()

