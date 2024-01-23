################### --- Gen20x Auto Flashing Setup---- ###########################

# Description: The file automates downloading of software artifacts from Jfrog artifactory;
# unzipping of downloaded artifacts; parsing of xml, shell files; generating flat build for Gen20x Project

# Usecases: 1. Complete System bundle
#			2. Existing system bundle but a different richos version
#			3. Customised download: download of Version X richos and Version Y system bundle (other than Richos)

# Usecase1: Complete System bundle
# User has to provide parameters buildType as systemBundle, buildNumber for system bundle, username and artifactoryToken for artifactory access.
# In this use case richosBuild parameter remains dummy menaing it can be any random integer value.

# Usecase2: Existing system bundle but a different richos version
# User wants to generate a flat build with existing system bundle but a different richos version
# Here we avoid downloading the systembundle again as it is already existing in local computer
# Script will patch the downloaded richos with existing system bundle and generate flat build
# User has to provide parameters buildType as richos, buildNumber for system bundle, richosBuild, username and artifactoryToken for artifactory access.

# Usecase3: Customised download:- Download of Version X richos and Version Y system bundle (other than Richos)
# User wants to download a custom build, version X of richos and version Y of system bundle (avoids downloading richos within system bundle)
# User has to provide parameters buildType as richosWithSystemBundle, buildNumber for system bundle, richosBuild, username and artifactoryToken for artifactory access.

# Flashing Usecase: Flash Flat Buid Using Qfil process
# Flat directory generated from flatbuild is fed as input for flashing Nonhlos,QNX,RICHOS,Systemdata
# Provide list of patch files ex: patch0,patch1.xml etc
# Provide list of rawprogramming files ex: rawprogram0.xml,rawprogram1.xml etc
# In case of SAHARA Com error a power cycle is done to make the communication stable
# Retry count for SAHARA Com error is 3, if the count exceeds more than 3 flashing process will be aborted.

#############################################################################


################### --- Imports ---- ########################################
import os
import stat
from shutil import *
import shutil
from artifactory import ArtifactoryPath
from artifactory import *
import lxml.etree as ET
import subprocess
from subprocess import PIPE
import sys
import datetime
import serial
import pyfirmata
from pyfirmata import Arduino, util
import win32com.client
from serial.tools import list_ports
from distutils.dir_util import copy_tree
import time
import arduinoController as controller
import paramiko

#############################################################################

################################### --- Inputs ---- ##########################################

listOfFlashItems = ['richos', 'qnx', 'nonhlos', 'richosext4', 'systemdata' ] #Ex: richos, qnx, vcpu, nonhlos
variant = str(sys.argv[1])	# Ex: 8195c, 8295b, 8295c, 8295d
buildType = str(sys.argv[2]) # Ex: systemBundle, flatbuild
buildNumber = str(sys.argv[3])	# Ex: 1810, E307.0(Buildno / System Bundleno)
userName = str(sys.argv[4])	 # Ex: smuktha
artifactoryToken = str(sys.argv[5])	 # Ex: cmVmdGtuOjAxOjE3MzEwNTY0MDA6Qzl5d0F6b2YwMGhlZTBtRDRlSlFMcVpUM2Zr
flatbuildVersion = str(sys.argv[6])  # Ex: https://artifact.swf.i.mercedes-benz.com/apricotbscqal/i2_MBRDI/231221_dresden_richOs88174_qnx-105_nonhlos105_systemdata105.zip

OutputPath = os.path.abspath(os.path.join(r"C:\Workspace\Gen20x\builds", "SB" + "_" + str(buildNumber)))
if buildType == "flatbuild":
	flatArtifactoryPath = ArtifactoryPath(flatbuildVersion, auth=("smuktha", "cmVmdGtuOjAxOjE3MzEwNTY0MDA6Qzl5d0F6b2YwMGhlZTBtRDRlSlFMcVpUM2Zr"))
	fbVersion = flatbuildVersion.split("/")[-1]
else:
	inputArtifactoryPath = "https://artifact.swf.i.mercedes-benz.com/artifactory/avocadobscqal-delivery-release/i2"
	fbVersion = inputArtifactoryPath.split("/")[-1]
bashPath = r"C:\Program Files\Git\bin\bash.exe"
qFilPath = r"C:\Program Files (x86)\Qualcomm\QPST\bin\QFIL.exe"

if os.path.exists(OutputPath):
	print("System bundle Directory Already Exists")
	count = 1
else:
	os.makedirs(OutputPath)
	count = 0

############################################################################################################

############################################ --- Download Artifacts --- ####################################

def downloadArtifacts(bdType, listOfFlashItems, bdNumber, artiPath, otPath, bdversion, userName, artifactoryToken):
	if bdType == 'flatbuild':
		print("Downloading {} Artifacts Started".format(bdType))
		# outpath = artiPath
		bpath = os.path.abspath(os.path.join(otPath, bdversion))
		with open(bpath, "wb") as out:
			artiPath.writeto(out, chunk_size =30*1024*1024)
		artiPath.writeto(
			out=bpath,
				progress_func=lambda x, y: print(x, y, custom="test")
			)
	elif bdType == 'systemBundle':
		for item in listOfFlashItems:
			if item == 'richos':
				print("Downloading {} Artifacts Started".format(item))
				inp = artiPath + "/" + \
					str(bdNumber) + "/" +"deliverables"+ "/" + item + "/" + "dev" + \
					"/" + "archive_binz-apricot-image-ui"
				out = os.path.abspath(
					otPath + "\\" + "archive_binz-apricot-image-ui" + ".zip")
				path = ArtifactoryPath(inp, auth=(userName, artifactoryToken))
				path.archive().writeto(out=out, chunk_size=16 * 1024 * 1024)
				print("Downloading {} Artifacts Completed".format(item))

			elif item == "qnx":
				print("Downloading {} Artifacts Started".format(item))
				inp = artiPath + "/" + \
					str(bdNumber) + "/" +"deliverables"+ "/" + item + \
				    "/" + "dev"
				out = os.path.abspath(
					otPath + "\\" + "dev" + ".zip")
				path = ArtifactoryPath(inp, auth=(userName, artifactoryToken))
				path.archive().writeto(out=out, chunk_size=16 * 1024 * 1024)
				print("Downloading {} Artifacts Completed".format(item))

			elif item == "nonhlos":
				print("Downloading {} Artifacts Started".format(item))
				inp = artiPath + "/" + \
					str(bdNumber) + "/" +"deliverables"+ "/" + item
				out = os.path.abspath(
					otPath + "\\" + "nonhlos" + ".zip")
				path = ArtifactoryPath(inp, auth=(userName, artifactoryToken))
				path.archive().writeto(out=out, chunk_size=16 * 1024 * 1024)
				print("Downloading {} Artifacts Completed".format(item))
		
			elif item == "richosext4":
				print("Downloading {} Artifacts Started".format(item))
				inp = artiPath + "/" + \
					str(bdNumber) + "/" +"deliverables"+ "/" + "richos" + "/" + "dev" + \
						"/" + "richos_backup.ext4.gz"
				outpath = os.path.abspath(
					otPath + "\\" + "richos_backup.ext4.gz")
				path = ArtifactoryPath(inp, auth=(userName, artifactoryToken))
				with open(outpath, "wb") as out:
					path.writeto(out=outpath, chunk_size=256)
				print("Downloading {} Artifacts Completed".format(item))

			elif item == "systemdata":
				print("Downloading {} Artifacts Started".format(item))
				inp = artiPath + "/" + \
					str(bdNumber) + "/" +"deliverables"+ "/" + item + "/" + \
						"/" + "systemdata.ext4.gz"
				outpath = os.path.abspath(
					otPath + "\\" + "systemdata.ext4.gz")
				path = ArtifactoryPath(inp, auth=(userName, artifactoryToken))
				with open(outpath, "wb") as out:
					path.writeto(out=outpath, chunk_size=256)
				print("Downloading {} Artifacts Completed".format(item))

####################################### --- Unzip Artifacts --- #####################################

def unzipArtifacts(bdType, listOfFlashItems, outputPath,fversion):
	print("Unzipping Artifacts Started")
	if bdType == 'flatbuild':
		if os.path.exists(outputPath+"\\nonhlos\\flat"):
			print("Flat build Directory Already Exists")
		else:
			os.makedirs(outputPath+"\\nonhlos\\flat")
		zipPath = outputPath + "\\" + fversion
		unzipPath = outputPath + "\\nonhlos\\flat" 
		shutil.unpack_archive(zipPath, unzipPath)
		print("Unzipping Artifacts Completed Successfully")
	else:
		for item in listOfFlashItems:			
			if item == 'richos':
				if os.path.exists(outputPath + "\\" + item):
					print("System bundle Directory Already Exists")
				else:
					os.makedirs(outputPath + "\\" + item)
				zipPath = outputPath + "\\" + "archive_binz-apricot-image-ui" + '.zip'
				unzipPath = outputPath + "\\" + item + "\\" + "archive_binz-apricot-image-ui"
				
			elif item == 'qnx':
				if os.path.exists(outputPath + "\\" + item + "\\" + "i2"):
					print("qnx Directory Already Exists")
				else:
					os.makedirs(outputPath + "\\" + item + "\\" + "i2")
				zipPath = outputPath + "\\" + "dev" + '.zip'
				unzipPath = outputPath + "\\" + item + "\\" + "i2" +"\\" + "dev"

			elif item == 'nonhlos':
				zipPath = outputPath + "\\" + item + '.zip'
				unzipPath = outputPath + "\\" + item
			shutil.unpack_archive(zipPath, unzipPath)
			print("Unzipping {} Artifacts Completed".format(item))
########################################################################################################			
			
####################################### --- copy systemdata --- ########################################
def systemdata(outputPath):
	zipPath = r"C:\Workspace\Gen20X\Builds\systemdata.zip"
	destination = os.path.abspath(outputPath)
	print("Copying systemdata Started")
	if os.path.exists(destination + "\\" + "systemdata"):
		print("systemdata Directory Already Exists")
	else:
		shutil.unpack_archive(zipPath, destination)
	print("Copying systemdata Completed")
########################################################################################################
	
######################################## --- Move files to Package --- ##################################

def movefiles(listOfFlashItems, outputPath):
	for item in listOfFlashItems:			
		if item == 'richosext4':
			print("Move richosext4 to richos Started")
			# source = "C:\\Workspace\\Gen20x\\builds\\SB_E307.0\\richos_backup.ext4.gz"
			source =  os.path.join(outputPath , "richos_backup.ext4.gz")
			destination = os.path.join(outputPath, "richos" + "\\" + "archive_binz-apricot-image-ui")				
			if os.path.exists(os.path.join(destination,"richos_backup.ext4.gz" )):
				print("richos_backup.ext4.gz Already Exists")
			else:
				shutil.move(source, destination)
			print("Move from  richosext4 to richos Completed")

		elif item == 'systemdata':
			print("Move systemdata.ext4.gz to systemdata Started")
			source = os.path.join(outputPath , "systemdata.ext4.gz")
			destination = os.path.join(outputPath , item )
			extfile = os.path.join(destination , "systemdata.ext4.gz")
			if os.path.exists(extfile):
				shutil.rmtree(extfile)
			else:
				shutil.move(source, destination)
			print("Move from systemdata.ext4.gz to systemdata Completed")
#########################################################################################################

######################################## -- Parsing Shell File --- ######################################
def shFileParsing(outputPath):
	text = "python3"
	newText = "py"
	for root, dir, files in os.walk(outputPath):
		for file in files:
			if file == 'flatten.sh':
				path = os.path.join(root, "flatten.sh")
				os.chmod(path, stat.S_IWRITE)
				f = open(path, 'r')
				data = f.readlines()
				f1 = open(path, 'w')
				for line in data:
					i = 0
					if text in line:
						print("Parsing of Shell file text {} Started".format(text))
						line = line.replace(text, newText)
						if text.capitalize() in line:
							print("Parsing of Shell file text {} Started".format(
								text.capitalize()))
							line = line.replace(text.capitalize(), newText)
							print("Parsing of Shell file text {} Completed".format(
								text.capitalize()))
						f1.write(line)
						i = i + 1
						print("Parsing of Shell file text {} Completed".format(text))
					if i == 0:
						f1.write(line)
				f.close()
				f1.close()
##########################################################################################################

##################################### -- Flat build Generation ---- ######################################

def flatBuildGeneration(outputPath):
	flatBuildLog = os.path.abspath(
		outputPath + '\\' + 'nonhlos' + "\\" + 'FlatBuildLog.txt')
	timeoutForFlatBuildGen = 2400
	for root, dir, files in os.walk(outputPath):
		for di in dir:
			if di == 'nonhlos':
				dirPath = os.path.join(root, di)
				os.chdir(dirPath)
				loc = os.getcwd()

				# ./flatten.sh -b  cabrillo -r archive_balboa-apricot-image-ui -P
				try:
					print("Flat Build Generation Started")
					if variant == '8195c':
						p = subprocess.run(
							[bashPath, 'flatten.sh', '-b', 'cabrillo', '-r',
							 'archive_balboa-apricot-image-ui-dev', '-P'],
							stdout=subprocess.PIPE, text=True, timeout=timeoutForFlatBuildGen, cwd=loc, shell=True)
					elif variant == '8295c':
						p = subprocess.run(
							[bashPath, 'flatten.sh', '-b', 'calbe', '-r',
							 'archive_binz-apricot-image-ui',],
							stdout=subprocess.PIPE, text=True, timeout=timeoutForFlatBuildGen, cwd=loc, shell=True)
					elif variant == '8295d':
						p = subprocess.run(
							[bashPath, 'flatten.sh', '-b', 'dresden', '-r',
							 'archive_binz-apricot-image-ui'],
							stdout=subprocess.PIPE, text=True, timeout=timeoutForFlatBuildGen, cwd=loc, shell=True)
					elif variant == '8295b':
						p = subprocess.run(
							[bashPath, 'flatten.sh', '-b', 'binz', '-r',
							 'archive_binz-apricot-image-ui-dev', '-P'],
							stdout=subprocess.PIPE, text=True, timeout=timeoutForFlatBuildGen, cwd=loc, shell=True)

					print(p.stdout)
					with open(flatBuildLog, 'w') as f:
						f.write(p.stdout)
					logfile = open(flatBuildLog, 'r')
					data = logfile.readlines()
					count = 0
					for line in data:
						if 'Validation successful' in line:
							count = 1

					logfile.close()

					if count == 1:
						print("Flat build generation Successful")
					else:
						print("Flat build generation Failed")

				except subprocess.TimeoutExpired:
					print("Timeout: {} seconds Occcured, Flat build generation aborted".format(
						timeoutForFlatBuildGen))
					sys.exit(1)
################################################################################################################
					
###################################### --- Delete Unzipped Packages --- ########################################

def delUnzipPackages(outputPath):
	for root, dir, files in os.walk(outputPath):
		for di in dir:
			print("Deleting of Unzipped Package {} Started".format(di))
			pathToDi = os.path.join(root, di)
			shutil.rmtree(pathToDi)

			print("Deleting of Unzipped Package {} Completed".format(di))
################################################################################################################

######################################### --- Flat Build Flashing --- ##########################################
# def Power_on_off(arduino, x):
#	print(x)
#	arduino.write(x.encode('utf-8'))
#	time.sleep(0.05)
#	data = arduino.readline()
#	return data


def comPorts(portType):
	dictOfComPorts = {}
	key = ''  # key will hold the COM port entry ex: COM3,COM6,etc.
	value = ''	# value will hold the description of COM port ex: "Qualcomm HS-USB","Arduino Uno",etc.
	ports = list_ports.comports()
	for dvc, desc, hwid in sorted(ports):
		dictOfComPorts[dvc] = desc

	if dictOfComPorts != {}:
		for key in dictOfComPorts:
			if portType in dictOfComPorts[key]:
				value = dictOfComPorts[key]
				return dictOfComPorts, key, value
			else:
				key = ''
				value = ''
	return dictOfComPorts, key, value


def flashFlatBuild(outputPath, qFilPath):
	if os.path.exists(os.path.join(outputPath, "nonhlos", "flat")):
		flashPath = os.path.abspath(
			os.path.join(outputPath, "nonhlos", "flat"))
		elfPath = os.path.abspath(flashPath + '\\' + 'prog_firehose_ddr.elf')
		qFilLog = os.path.abspath(outputPath + '\\' + 'QfilFlashLogs.txt')
		timeoutForFlashing = 3000
		if os.path.exists(qFilLog):
			os.remove(qFilLog)
		tasklist = os.popen("tasklist").read()
		if "QFIL.exe" in tasklist:
			os.system("taskkill /f /im	QFIL.exe")
		# dict, key, value = controller.comPorts("Arduino")
		# arduinoPort = key  # serial port
		# baud = 9600	 # baudrate
		# arduino = serial.Serial(port=arduinoPort, baudrate=baud, timeout=.1)
		# controller.Power_on_off(arduino, "wakeup")
		# time.sleep(2)
		# controller.Power_on_off(arduino, "2")  # power on
		# print('Powered on')
		# time.sleep(7)
		saharaCount = 0
		retry = 3

		while (saharaCount < retry):
			# time.sleep(10)
			dict, key, value = controller.comPorts("Qualcomm HS-USB")
			if key != '' and value != '':
				comPortNumber = key.split("COM")[1]
				try:
					print("Flat build Flashing Started in Qfil")
					# Modes 0:Visible, 1:Firehorse, 3: Hidden
					p = subprocess.run([qFilPath, '-COM=' + comPortNumber, '-Mode=3', '-FLATBUILDPATH=' + flashPath,
										'-Programmer=true;' + elfPath,
										'-SEARCHPATH=' + flashPath,
										'-Patch=patch0.xml,patch1.xml,patch2.xml,patch4.xml,patch5.xml,patch6.xml,patch7.xml',
										'-RawProgram=rawprogram0.xml,rawprogram1.xml,rawprogram2.xml,rawprogram4.xml,rawprogram5.xml,rawprogram6.xml,rawprogram7.xml',
										'-DEVICETYPE=ufs', '-VALIDATIONMODE=0', '-ERASEALL=true', '-DOWNLOADFLAT'],
									   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
									   timeout=timeoutForFlashing, text=True)

					print(
						"-----------Console Output of Flatbuild Flashing-------------------")
					print(p.stdout)

					with open(qFilLog, 'w') as f:
						f.write(p.stdout)
					logFile = open(qFilLog, 'r')
					data = logFile.readlines()
					count = 0
					for line in data:
						if "Download Succeed" in line:
							print("Flatbuild Flashing Success")
							saharaCount = retry
						elif "Sahara protocol error" in line:
							print(
								"Flatbuild Flashing Exited becasue of SAHARA Communication Error, Retry After Powercycle")
							count = count + 1
							saharaCount = saharaCount + 1
							# controller.Power_on_off(arduino, "1")
							# time.sleep(2)
							# controller.Power_on_off(arduino, "2")  # power on
							# time.sleep(2)
							# print('Powered on')
							# time.sleep(5)
							if saharaCount == retry:
								print(
									"Sahara Com Retry Count Exceeded, Flashing Aborted, Check for the connections manually")
						elif count == 0 and "Download Fail" in line:
							print("Flatbuild Flashing Failed")
							saharaCount = retry

					logFile.close()
				except subprocess.TimeoutExpired:
					print("Timeout: {} seconds Occcured, Exiting the Flashing".format(
						timeoutForFlashing))
					sys.exit(1)

			else:
				print("COM port not detected, flashing aborted")

	else:
		print("Flat build folder does not exist, flashing aborted")
###############################################################################################################

########################################### --- Pre Flashing  Setup --- #######################################
def preFlashingSetup():
	if buildType == "flatbuild":
		downloadArtifacts(buildType, listOfFlashItems,buildNumber, flatArtifactoryPath, OutputPath, fbVersion, userName,artifactoryToken)
		unzipArtifacts(buildType, listOfFlashItems, OutputPath,fbVersion)
		flashFlatBuild(OutputPath, qFilPath)
		delUnzipPackages(OutputPath)
	
	else:
		# downloadArtifacts(buildType, listOfFlashItems, buildNumber, inputArtifactoryPath, OutputPath, fbVersion, userName,artifactoryToken)
		# systemdata(OutputPath)
		# unzipArtifacts(buildType, listOfFlashItems, OutputPath,fbVersion)
		# movefiles(listOfFlashItems, OutputPath)
		# shFileParsing(OutputPath)
		# flatBuildGeneration(OutputPath)
		flashFlatBuild(OutputPath,qFilPath)
		# delUnzipPackages(OutputPath)
###############################################################################################################

def main():
	# controller.debugBreaker("debug")
	preFlashingSetup()
	# controller.debugBreaker("normal")
	# controller.powerCycle()
	return


if __name__ == '__main__':
	main()

