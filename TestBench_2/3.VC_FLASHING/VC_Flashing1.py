import time
import os
import requests
import serial
from datetime import datetime
from serial.tools import list_ports
import config as CONF
import arduinoController as controller
import paramiko
import sys

doPowerCycle = False
buildNumber = int(sys.argv[1])
buildType = str(sys.argv[2])
outputPath = ""

if buildType == "richos":
	outputPath = os.path.abspath(os.path.join(r"C:\Workspace\Gen20x\builds", "rs" + "_" + str(richosBuild)))
elif buildType == "richosWithSystemBundle":
	outputPath = os.path.abspath(os.path.join(r"C:\Workspace\Gen20x\builds","sb" + "_" + str(buildNumber) + "_" + "rs" + "_" + str(richosBuild)))
def writeLog(log1, log2=""):
	current_time = datetime.now().strftime("%H_%M_%S")
	current_date = datetime.now().strftime("%d_%m_%y")
	log_file = current_date + '_log.txt'
	message = current_time + ' : ' + str(log1) + ' >> ' + str(log2)
	with open(log_file , 'a') as fo :
		fo.write('\n' + message)
	print(message)

# def comPorts(portType):
#	  dictOfComPorts = {}
#	  # Key = COM3,COM6,etc.
#	  # Value = "Qualcomm HS-USB","Arduino Uno",etc.
#	  key = ''
#	  value = ''
#	  ports = list_ports.comports()
#	  for dvc, desc, hwid in sorted(ports):
#		  dictOfComPorts[dvc] = desc

#	  if dictOfComPorts != {}:
#		  for key in dictOfComPorts:
#			  if portType in dictOfComPorts[key]:
#				  value = dictOfComPorts[key]
#				  return dictOfComPorts, key, value
#			  else:
#				  key = ''
#				  value = ''
#	  return dictOfComPorts, key, value

# def powerCycle():
#	  dict, key, value = comPorts("Arduino")
#	  arduinoPort = key
#	  baud = 9600
#	  arduino = serial.Serial(port=arduinoPort, baudrate=baud, timeout=.1)
#	  arduino.write("1".encode('utf-8'))  # Power OFF
#	  writeLog("Power Cycle", "OFF")
#	  time.sleep(2)
#	  arduino.write("2".encode('utf-8'))  # Power ON
#	  writeLog("Power Cycle", "ON")

def triggerETFW(state, uri):
	writeLog("state " + state)
	res = requests.get(uri)
	writeLog(res.status_code, res.json())
	print(res)

def triggerIgnitionOn():
	writeLog("Started Ignition Procedure")
	ignitionProcedure = [CONF.vehLine, CONF.vehStyle,
						 CONF.accessoryOn, CONF.accessoryStart, CONF.ignitionOn]
	# ignition = [URI.etfStop]
	for ignition in ignitionProcedure:
		res = requests.get(ignition)
		writeLog(res.status_code, res.json())
		time.sleep(5)

def writeVersionInformation(outputPath):
	#ip = "10.120.1.91"
	ip = "169.254.17.99"
	port=22
	username='root'
	password=''

	ssh=paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip, port, username, password, timeout=200)

	ssh.connect(ip, port, username, password, timeout=200)
	print('Retriving Version details from Head Unit')
	time.sleep(1)
	stdin,stdout2,stderr=ssh.exec_command('hostname; cat /etc/build')
	buildInfo = [i.replace('\n','') for i in stdout2]
	ssh.close()

	filePath = os.path.join(outputPath, "versionInfo.txt")
	with open(filePath, 'w') as f:
		for i in buildInfo:
			f.write(i+"\n")
			print(i)

def vcCoding():
	writeLog("VC flashing Started")
	doReset = False
	domainList = [(CONF.activeComfort, CONF.getActiveComfort, CONF.writeActiveComfort), (CONF.VideoHandling, CONF.getVideoHandling,
																						 CONF.writeVideoHandling), (CONF.VehicleFunctions, CONF.getVehicleFunctions, CONF.writeVehicleFunctions)]
	for domainData in domainList:
		domain, getDomain, writeDomain = domainData
		writeLog("Get Coding", domain[0])
		getRes = requests.get(getDomain)
		writeLog(getRes.status_code, getRes.json())
		if getRes.status_code == 200:
			if getRes.json()["Value"] != domain[1].replace(',', ' '):
				writeLog("Do Coding", domain[0])
				res = requests.put(writeDomain)
				doReset = True
				writeLog(res.status_code, res.json())
						
	try:
		time.sleep(15)
		writeVersionInformation(outputPath)
	except:
		print("Version Check : SSH connection Timed out")
		
	if doReset:
		if doPowerCycle:
			writeLog('Perform ECU Rest')
			controller.powerCycle()
			time.sleep(5)
			
#controller.debugBreaker("normal")
#controller.powerCycle()
triggerETFW("ET Framework", CONF.etfStart)
time.sleep(2)
triggerETFW("ET Online", CONF.etfGoOnline)
triggerIgnitionOn()
vcCoding()
