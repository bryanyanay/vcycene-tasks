import struct
import serial

port = "\\\\.\\CNCB0" # port to write to

def sendLine(temps, pres, gasres, port):
  """
  temps is a list of 3 temperatures, -30 to 80
  pres is a list of 2 pressures, 0 to 60000
  gasres is a last of gas resistances, 0 to 3000000
  port is the COM port to send the data out to

  temperatures stored signed, 1 byte
  pressures stored unsigned, 2 bytes, little-endian
  gas resistances stored unsigned, 4 bytes, little-endian
  """
  tempBin = struct.pack("<bbb", temps[0], temps[1], temps[2])
  presBin = struct.pack("<HH", pres[0], pres[1])
  gasresBin = struct.pack("<II", gasres[0], gasres[1])
  
  print("\n>>> sending data to " + port + " ...")
  print("temperatures: \t", temps, " -> ", tempBin)
  print("pressures: \t", pres, " -> ", presBin)
  print("gas resistances:", gasres, " -> ", gasresBin)

  data = tempBin + presBin + gasresBin + b'\00'
  with serial.Serial(port) as s:
    s.set_buffer_size(rx_size=12800, tx_size=12800)
    s.write(data)

  print("sent: \t\t", data)

sendLine([127, 1, 1], [1, 2**16 - 1], [2**32 -1, 16 + 8 + 256], port)
sendLine([-30, 0, 100], [0, 2**16 - 1], [2**32 -1, 0], port)
