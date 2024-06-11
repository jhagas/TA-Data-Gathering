import serial.tools.list_ports
import time
import os

# This script located at?
# Required for making absolute path of this script
script_dir = os.path.dirname(__file__)

# Make "data" folder to contain audio recording
if not os.path.exists("data"): 
	os.makedirs("data") 

######################################################
# Arduino Preparation and opening serial port
ports = serial.tools.list_ports.comports()
arduino = serial.Serial()

portList = []
portVar = ""

for onePort in ports:
	portList.append(str(onePort))
	print(str(onePort))

print("-----------------------")
val = input("Select Arduino Port: COM")

for x in range(len(portList)):
	if portList[x].startswith("COM" + val):
		portVar = "COM" + str(val)
		print("Selected ", portList[x])

arduino.baudrate = 115200
arduino.port = portVar
arduino.open()
time.sleep(2)
######################################################

# Loop for gathering a lot of data
for i in range(500):
	print("-----------------------")
	print("Loop ke-" + str(i + 1))
	print("-----------------------")

	# Send "RECORD" command via serial
	arduino.write(bytes("RECORD", 'utf-8')) 
	time.sleep(0.05)

	num = 0
	timeStr = ""

	# Receiving messages and files from Arduino
	while True:
		if arduino.in_waiting:
			# Readline for splitting serial communication with \n (0a) per packet
			packet = arduino.readline() 
			msg = packet.decode('utf8', "ignore") # "ignore" means non-UTF byte goes through without decoding

			# If there is "ERROR" or "EVENT" in serial message, print it
			if (msg.find("ERROR", 0, 5) != -1 or msg.find("EVENT", 0, 5) != -1):
				print(msg, end="")

				# If there is "wav" in serial message, increase num by 1, and get NOW time unix epoch
				# Also opening file for writing
				if (msg.find("wav") != -1):
					if (num != 0):
						file.close()
					num = num + 1
					timeStr = str(int(time.time()))
					abs_file_path = os.path.join(script_dir, "data/Mic " + str(num) + "-" + timeStr + ".wav")
					file = open(abs_file_path, "wb") 

				# If there is "Done Sending Data to PC", break the while loop
				if (msg.find("Done Sending Data to PC") != -1):
					break
			# Else, write the file
			else:
				file.write(packet)

	# Truncate 0a (\n , newline) byte from the file
	for i in range(1,4):
		abs_file_path = os.path.join(script_dir, "data/Mic " + str(num) + "-" + timeStr + ".wav")
		with open(abs_file_path, "r+b") as f:
			# Move the file pointer to the end of the file.
			f.seek(0, 2)
			# Truncate the file to the previous byte.
			f.truncate(f.tell() - 1)
