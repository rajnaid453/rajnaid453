import os
import time
from datetime import datetime
from winreg import ConnectRegistry
# import config as CONF
import arduinoController as controller
import sys
from artifactory import ArtifactoryPath
from artifactory import *
from shutil import *
import shutil

################################### --- Inputs ---- ##########################################
buildNumber = str(sys.argv[1])	# Ex: 1810, 1752
kdsNumber = str(sys.argv[2])
userName = str(sys.argv[3])	 # Ex: smuktha
artifactoryToken = str(sys.argv[4])	 # Ex: cmVmdGtuOjAxOjE3MzEwNTY0MDA6Qzl5d0F6b2YwMGhlZTBtRDRlSlFMcVpUM2Zr


inputArtifactoryPath = "https://artifact.swf.i.mercedes-benz.com/artifactory/avocadobscqal-delivery-release/i2"

flashgui = r"C:\Tools\v7.33\bin"
OutputPath = os.path.abspath(os.path.join(
	r"C:\Workspace\Gen20x\builds", "SB" + "_" + str(buildNumber)))                                  
vcpu_file_path = os.path.abspath(OutputPath + 
				"\\" + "vcpu" + "\\" + "output_release" + "\\" + "bin" + "\\" +"TRICORE_TC39XX_VCPU_FULL_IMAGE_Developer.dnl")
kds_file_path = os.path.abspath("C:\\Workspace\\Gen20x\\builds\\KDS"
			 + "\\" + kdsNumber + ".KDS")

if os.path.exists(OutputPath):
	print("System bundle Directory Already Exists")
	count = 1
else:
	os.makedirs(OutputPath)
	count = 0
#########################################################################################

############################ --- Download & Unzip Artifacts --- #########################
def downloadArtifacts(bdNumber,  artiPath, otPath, userName, artifactoryToken):
	print("Downloading VCPU Artifacts Started")
	inp = artiPath + "/" + \
		str(bdNumber) + "/" +"deliverables"+ "/" + "vcpu" + "/" + "dev" + \
			"/" + "output_release.zip"
	outpath = os.path.abspath(
		otPath + "\\" + "output_release.zip")
	path = ArtifactoryPath(inp, auth=(userName, artifactoryToken))
	with open(outpath, "wb") as out:
		path.writeto(out=outpath, chunk_size=256)
	print("Downloading VCPU Artifacts Completed")

def unzipArtifacts(otPath):
	print("Unzipping vcpu Artifacts started")
	os.makedirs(OutputPath+"\\vcpu")
	zipPath = otPath + "\\" + "output_release.zip"
	unzipPath = otPath + "\\" + "vcpu" + "\\" + "output_release"
	shutil.unpack_archive(zipPath, unzipPath)
	print("Unzipping vcpu Artifacts Completed")
#########################################################################################

def writeLog(log1, log2=""):
	current_time = datetime.datetime.now().strftime("%H_%M_%S")
	current_date = datetime.datetime.now().strftime("%d_%m_%y")
	log_file = current_date + '_log.txt'
	message = current_time + ' : ' + str(log1) + ' >> ' + str(log2)
	with open(log_file, 'a') as fo:
		fo.write('\n' + message)
	print(message)

################################## --- VCPU Flashing --- ################################
def flash_vcpu():
	writeLog("VCPU flashing Started")
	timeout = 900
	# flashgui = flashgui
	# vcpu_file_path = CONF.vcpu_file_path
	# kds_file_path = CONF.kds_file_path
	flash_gui_path = os.path.join(flashgui, "FlashGUI.exe /h")
	result_file = os.path.join(flashgui, "Result.txt")
	log_file = os.path.join(flashgui, "logfile.txt")
	if os.path.exists(result_file):
		os.remove(result_file)
	if os.path.exists(log_file):
		os.remove(log_file)
	
	cmd = "{} /f{} /KDS{} /Quad-G3G-RS232-DebugAdapter C - FT6RVBE9,3000000,8,1,even /KDSSAVE /au".format(
		flash_gui_path, vcpu_file_path, kds_file_path)
	
	#cmd = "{} /f{} /KDS{} /Quad-G3G-RS232-DebugAdapter C - FT6A4KS3,3000000,even,8,1 /KDSSAVE /au".format(
	#	 flash_gui_path, vcpu_file_path, kds_file_path)

	os.system(cmd)
	tasklist = os.popen("tasklist").read()
	count = 0

	while ("FlashGUI.exe" in tasklist):
		if count < timeout:
			count += 1
			time.sleep(1)
		else:
			print("VCPU flashing did not complete within {} seconds. Hence failing".format(
				timeout))
			exit(0)
		tasklist = os.popen("tasklist").read()

	log = open(r"C:\Tools\v7.33\bin\logfile.txt", 'r')
	file_contents = log.read()
	print (file_contents)
	log.close()
	if os.path.exists(result_file):
		with open(result_file) as f:
			logFile = open(log_file, 'r')
			data = logFile.readlines()
			for line in data:
				# print(line)
				writeLog(line)
			logFile.close()
			res = f.read()
			if "0x00000000" in res:
				print("VCPU flashing was successful")
			else:
				print("VCPU flashing Failed")
	else:
		print("Result file is not generated.")
#########################################################################################

# controller.debugBreaker("debug")
downloadArtifacts(buildNumber, inputArtifactoryPath, OutputPath, userName, artifactoryToken)
unzipArtifacts(OutputPath)
flash_vcpu()
time.sleep(1)
# controller.debugBreaker("normal")
