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


################## --- Inputs ---- ##########################################

listOfFlashItems = ['richos', 'qnx', 'vcpu', 'nonhlos'] #Ex: richos, qnx, vcpu, nonhlos, systemdata
variant = str(sys.argv[1])	# Ex: 8195c, 8295b, 8295c, 8295d
buildType = str(sys.argv[2]) # Ex: systemBundle, richos, richosWithSystemBundle
buildNumber = int(sys.argv[3])	# Ex: 1810, 1752
richosBuild = int(sys.argv[4])	# Ex: 55100,61630
userName = str(sys.argv[5])	 # Ex: smuktha
artifactoryToken = str(sys.argv[6])	 # Ex: APavbsd12Q
if buildType == "richos":
	richosArtifactoryPath = "https://artifact.swf.daimler.com:443/artifactory/apricotbscqal/build/yocto.apricot-manifests.dunfell.downstream"
	richosOutputPath = os.path.abspath(os.path.join(
		r"C:\Workspace\Gen20x\builds", "rs" + "_" + str(richosBuild)))
elif buildType == "richosWithSystemBundle":
	richosArtifactoryPath = "https://artifact.swf.daimler.com:443/artifactory/apricotbscqal/build/yocto.apricot-manifests.dunfell.downstream"
	richosSystemBundleOutputPath = os.path.abspath(os.path.join(r"C:\Workspace\Gen20x\builds",
																"sb" + "_" + str(buildNumber) + "_" + "rs" + "_" + str(
																	richosBuild)))
	richosOutputPath = os.path.abspath(os.path.join(
		richosSystemBundleOutputPath, "rs" + "_" + str(richosBuild)))
	systemBundleOutputPath = os.path.abspath(os.path.join(
		richosSystemBundleOutputPath, "sb" + "_" + str(buildNumber)))
outputPath = os.path.abspath(os.path.join(
	r"C:\Workspace\Gen20x\builds", "sb" + "_" + str(buildNumber)))
inputArtifactoryPath = "https://artifact.swf.daimler.com:443/artifactory/apricotbscqal/build/system.apricot-system-manifests.master.promote"
#inputArtifactoryPath = "https://artifact.swf.daimler.com:443/artifactory/apricotbscqal/build/system.apricot-system-manifests.release_E035.promote"
kdsFileName = "7513700455.KDS" # 8295d2
#kdsFileName = "7513700151.KDS" # 8295d1
#kdsFileName = "7513700148.KDS" # 8295c
#kdsFileName = "7513700051.KDS" # 8195c
# (Add bash to System Variables [C:\Program Files\Git\bin\])
bashPath = r"C:\Program Files\Git\bin\bash.exe"
qFilPath = r"C:\Program Files (x86)\Qualcomm\QPST\bin\QFIL.exe"

#############################################################################

if buildType == "systemBundle":
	if os.path.exists(outputPath):
		print("System bundle Directory Already Exists")
		count = 1
		if os.path.exists(outputPath+"\\qnx\\i2\\dev"):
			print("Qnx Directory Already Exists")
		else:
			os.makedirs(outputPath+"\\qnx\\i2\\dev")
		# shutil.rmtree(outputPath)
	else:
		os.makedirs(outputPath)
		os.makedirs(outputPath+"\\qnx\\i2\\dev")
		count = 0

elif buildType == "richos":
	if os.path.exists(richosOutputPath):
		print("Richos Directory Already Exists")
		richosCount = 1
		# shutil.rmtree(richosOutputPath)
	else:
		os.makedirs(richosOutputPath)
		richosCount = 0

elif buildType == "richosWithSystemBundle":
	call = 0
	richosCall = 0
	systemBundleCall = 0
	qnxcall = 0
	if os.path.exists(richosSystemBundleOutputPath):
		call = call + 1
		if os.path.exists(richosOutputPath):
			richosCall = call + 1
		if os.path.exists(systemBundleOutputPath):
			systemBundleCall = call + 1
			if os.path.exists(systemBundleOutputPath+"\\qnx\\i2\\dev"):
				qnxcall = call+1
		# shutil.rmtree(richosSystemBundleOutputPath)
		if call == 1 and richosCall == 0 and systemBundleCall == 0 and qnxcall == 0:
			print(
				"Parent dirctory already exists, children: system bundle, richos Directories are created")
			print("qnx dirctory is created")
			os.makedirs(richosOutputPath)
			os.makedirs(systemBundleOutputPath)
			os.makedirs(systemBundleOutputPath+"\\qnx\\i2\\dev")
		if call == 1 and richosCall == 2 and systemBundleCall == 0 and qnxcall == 0:
			print(
				"Parent and child Richos Directory Already Exist, system bundle directory is created")
			print("qnx dirctory is created")
			os.makedirs(systemBundleOutputPath)
			os.makedirs(systemBundleOutputPath+"\\qnx\\i2\\dev")
		if call == 1 and richosCall == 0 and systemBundleCall == 2 and qnxcall == 0:
			print(
				"Parent and child System bundle Directory Already Exist, richos directory is created")
			print("qnx dirctory is created")
			os.makedirs(richosOutputPath)
			os.makedirs(systemBundleOutputPath+"\\qnx\\i2\\dev")
		if call == 1 and richosCall == 2 and systemBundleCall == 2 and qnxcall == 0:
			print(
				"Parent and children richos, System bundle Directory Already Exist, qnx directory is created")
			os.makedirs(systemBundleOutputPath+"\\qnx\\i2\\dev")
		if call == 1 and richosCall == 2 and systemBundleCall == 2 and qnxcall == 2:
			print(
				"Parent and children richos,system bundle and qnx Directories Already Exist")

	if call == 0:
		os.makedirs(richosSystemBundleOutputPath)
		os.makedirs(richosOutputPath)
		os.makedirs(systemBundleOutputPath)
		os.makedirs(systemBundleOutputPath+"\\qnx\\i2\\dev")


##################### --- APIs --- #########################################


################# --- Download Artifacts --- ###############################
def downloadArtifacts(bdType, listOfFlashItems, bdNumber, artifactoryPath, otPath, userName, artifactoryToken):
	if bdType == 'systemBundle':
		for item in listOfFlashItems:
			if item == 'richos':
				if variant == '8195c':
					print("Downloading {} Artifacts Started".format(item))
					inp = artifactoryPath + "/" + \
						str(bdNumber) + "/" + item + "/" + "dev" + \
						"/" + "archive_balboa-apricot-image-ui-dev"
					out = os.path.abspath(
						otPath + "\\" + "archive_balboa-apricot-image-ui-dev" + ".zip")
				elif variant == '8295c':
					print("Downloading {} Artifacts Started".format(item))
					inp = artifactoryPath + "/" + \
						str(bdNumber) + "/" + item + "/" + "dev" + \
						"/" + "archive_binz-apricot-image-ui"
					out = os.path.abspath(
						otPath + "\\" + "archive_binz-apricot-image-ui" + ".zip")
				elif variant == '8295b':
					print("Downloading {} Artifacts Started".format(item))
					inp = artifactoryPath + "/" + \
						str(bdNumber) + "/" + item + "/" + "dev" + \
						"/" + "archive_binz-apricot-image-ui-dev"
					out = os.path.abspath(
						otPath + "\\" + "archive_binz-apricot-image-ui-dev" + ".zip")
				elif variant == '8295d':
					print("Downloading {} Artifacts Started".format(item))
					inp = artifactoryPath + "/" + \
						str(bdNumber) + "/" + item + "/" + "dev" + \
						"/" + "archive_binz-apricot-image-ui"
					out = os.path.abspath(
						otPath + "\\" + "archive_binz-apricot-image-ui" + ".zip")

			elif item == "qnx":
				if variant == '8195c':
					print("Downloading {} Artifacts Started".format(item))
					inp = artifactoryPath + "/" + \
						str(bdNumber) + "/" + item + "/" + \
						"i2" + "/" + "dev" + "/" + "SA8195"
					out = os.path.abspath(
						otPath + "\\qnx\\i2\\dev\\" + "SA8195" + ".zip")
				elif variant == '8295c':
					print("Downloading {} Artifacts Started".format(item))
					inp = artifactoryPath + "/" + \
						str(bdNumber) + "/" + item + "/" + \
						"i2" + "/" + "dev" + "/" + "SA8295"
					out = os.path.abspath(
						otPath + "\\qnx\\i2\\dev\\" + "SA8295" + ".zip")
				elif variant == '8295d':
					print("Downloading {} Artifacts Started".format(item))
					inp = artifactoryPath + "/" + \
						str(bdNumber) + "/" + item + "/" + \
						"i2" + "/" + "dev" + "/" + "SA8295"
					out = os.path.abspath(
						otPath + "\\qnx\\i2\\dev\\" + "SA8295" + ".zip")
			else:
				print("Downloading {} Artifacts Started".format(item))
				inp = artifactoryPath + "/" + str(bdNumber) + "/" + item
				out = os.path.abspath(otPath + "\\" + item + ".zip")
			path = ArtifactoryPath(inp, auth=(userName, artifactoryToken))
			path.archive().writeto(out=out, chunk_size=16 * 1024 * 1024)
			print("Downloading {} Artifacts Completed".format(item))
	elif bdType == 'richosWithSystemBundle':

		for item in listOfFlashItems:
			if item == 'richos':

				if variant == '8195c':
					print("Downloading {} Artifacts Started".format(item))
					inp = artifactoryPath[-1] + "/" + \
						str(bdNumber[-1]) + "/" + \
						"archive_balboa-apricot-image-ui-dev"
					out = os.path.abspath(otPath[-1] + "\\" +
										  "archive_balboa-apricot-image-ui-dev" + ".zip")
				elif variant == '8295c':
					print("Downloading {} Artifacts Started".format(item))
					inp = artifactoryPath[-1] + "/" + \
						str(bdNumber[-1]) + "/" + \
						"archive_binz-apricot-image-ui"
					out = os.path.abspath(otPath[-1] + "\\" +
										  "archive_binz-apricot-image-ui" + ".zip")
				elif variant == '8295b':
					print("Downloading {} Artifacts Started".format(item))
					inp = artifactoryPath[-1] + "/" + \
						str(bdNumber[-1]) + "/" + \
						"archive_binz-apricot-image-ui-dev"
					out = os.path.abspath(otPath[-1] + "\\" +
										  "archive_binz-apricot-image-ui-dev" + ".zip")
				elif variant == '8295d':
					print("Downloading {} Artifacts Started".format(item))
					inp = artifactoryPath[-1] + "/" + \
						str(bdNumber[-1]) + "/" + \
						"archive_binz-apricot-image-ui"
					out = os.path.abspath(otPath[-1] + "\\" +
										  "archive_binz-apricot-image-ui" + ".zip")

				path = ArtifactoryPath(inp, auth=(userName, artifactoryToken))
				path.archive().writeto(out=out, chunk_size=16 * 1024 * 1024)
				print("Downloading {} Artifacts Completed".format(item))

			elif item == "qnx":
				if variant == '8195c':
					print("Downloading {} Artifacts Started".format(item))
					inp = inputArtifactoryPath + "/" + \
						str(bdNumber[0]) + "/" + item + "/" + \
						"i2" + "/" + "dev" + "/" + "SA8195"
					out = os.path.abspath(
						systemBundleOutputPath + "\\qnx\\i2\\dev\\" + "SA8195" + ".zip")
				elif variant == '8295c':
					print("Downloading {} Artifacts Started".format(
						item), artifactoryPath[-1], str(bdNumber[0]))
					inp = inputArtifactoryPath + "/" + \
						str(bdNumber[0]) + "/" + item + "/" + \
						"i2" + "/" + "dev" + "/" + "SA8295"
					print(inp)
					out = os.path.abspath(
						systemBundleOutputPath + "\\qnx\\i2\\dev\\" + "SA8295" + ".zip")
				elif variant == '8295d':
					print("Downloading {} Artifacts Started".format(
						item), artifactoryPath[-1], str(bdNumber[0]))
					inp = inputArtifactoryPath + "/" + \
						str(bdNumber[0]) + "/" + item + "/" + \
						"i2" + "/" + "dev" + "/" + "SA8295"
					print(inp)
					out = os.path.abspath(
						systemBundleOutputPath + "\\qnx\\i2\\dev\\" + "SA8295" + ".zip")
				path = ArtifactoryPath(inp, auth=(userName, artifactoryToken))
				path.archive().writeto(out=out, chunk_size=16 * 1024 * 1024)
				print("Downloading {} Artifacts Completed".format(item))

			else:
				print("Downloading {} Artifacts Started".format(item))
				inp = artifactoryPath[0] + "/" + str(bdNumber[0]) + "/" + item
				out = os.path.abspath(otPath[0] + "\\" + item + ".zip")
				path = ArtifactoryPath(inp, auth=(userName, artifactoryToken))
				path.archive().writeto(out=out, chunk_size=16 * 1024 * 1024)
				print("Downloading {} Artifacts Completed".format(item))

	else:
		print("Downloading {} Artifacts Started".format(bdType))
		if variant == '8195c':
			inp = artifactoryPath + "/" + \
				str(bdNumber) + "/" + "archive_balboa-apricot-image-ui-dev"
			out = os.path.abspath(
				otPath + "\\" + "archive_balboa-apricot-image-ui-dev" + ".zip")
		else:
			inp = artifactoryPath + "/" + \
				str(bdNumber) + "/" + "archive_binz-apricot-image-ui"
			out = os.path.abspath(
				otPath + "\\" + "archive_binz-apricot-image-ui" + ".zip")
		path = ArtifactoryPath(inp, auth=(userName, artifactoryToken))
		path.archive().writeto(out=out, chunk_size=16 * 1024 * 1024)
		print("Downloading {} Artifacts Completed".format(bdType))


############### --- Unzip Artifacts --- #################################
def unzipArtifacts(listOfFlashItems, outputPath):
	print("Unzipping Artifacts Started")
	for item in listOfFlashItems:
		if item == 'richos':
			if variant == '8195c':
				zipPath = outputPath + "\\" + "archive_balboa-apricot-image-ui-dev" + '.zip'
				unzipPath = outputPath + "\\" + item + "\\" + \
					"archive_balboa-apricot-image-ui-dev"
			elif variant == '8295d':
				zipPath = outputPath + "\\" + "archive_binz-apricot-image-ui" + '.zip'
				unzipPath = outputPath + "\\" + item + "\\" + "archive_binz-apricot-image-ui"
			elif variant == '8295c':
				zipPath = outputPath + "\\" + "archive_binz-apricot-image-ui" + '.zip'
				unzipPath = outputPath + "\\" + item + "\\" + "archive_binz-apricot-image-ui"
			elif variant == '8295b':
				zipPath = outputPath + "\\" + "archive_binz-apricot-image-ui-dev" + '.zip'
				unzipPath = outputPath + "\\" + item + "\\" + "archive_binz-apricot-image-ui-dev"
		elif item == 'qnx':
			if variant == '8195c':
				zipPath = outputPath + "\\qnx\\i2\\dev\\" + "SA8195" + '.zip'
				unzipPath = outputPath + "\\" + item + "\\i2\\dev\\" + "SA8195"
			elif variant == '8295c':
				zipPath = outputPath + "\\qnx\\i2\\dev\\" + "SA8295" + '.zip'
				unzipPath = outputPath + "\\" + item + "\\i2\\dev\\" + "SA8295"
			elif variant == '8295d':
				zipPath = outputPath + "\\qnx\\i2\\dev\\" + "SA8295" + '.zip'
				unzipPath = outputPath + "\\" + item + "\\i2\\dev\\" + "SA8295"
		else:
			zipPath = outputPath + "\\" + item + '.zip'
			unzipPath = outputPath + "\\" + item
		shutil.unpack_archive(zipPath, unzipPath)
		print("Unzipping {} Artifacts Completed".format(item))
		# if item=='vcpu':
		#	 for root,dir,files in os.walk(unzipPath):
		#		 for file in files:
		#			 if file == 'output_release.zip':
		#				 rlsZipPath = os.path.join(root,file)
		#				 rlsUnzipPath = os.path.join(root,"output_release")
		#				 shutil.unpack_archive(rlsZipPath, rlsUnzipPath)
		#				 print("Unzipping {} Artifacts in {} Completed".format(file,item))


############ --- Move QNX Package --- ######################################


def moveqnx():
	if buildType == "richosWithSystemBundle":
		source = os.path.abspath(os.path.join(
			systemBundleOutputPath, "qnx\i2\dev\\"))
		destination = os.path.abspath(
			os.path.join(systemBundleOutputPath, "qnx\\"))
	else:
		source = os.path.abspath(os.path.join(outputPath, "qnx\i2\dev\\"))
		destination = os.path.abspath(os.path.join(outputPath, "qnx\\"))
	print("Move from  qnx\i2\dev to qnx Started")
	for i in os.listdir(source):
		shutil.move(source + "\\" + i, destination)
	print("Move from  qnx\i2\dev to qnx Completed")


############### -- Parsing Shell File --- ######################################
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


################# --- XML Parsing --- ######################################
def xmlParsing(outputPath, kdsFileName):
	for root, dir, files in os.walk(outputPath):
		for file in files:
			if file == 'rawprogram3.xml':
				xmlFilePath = os.path.join(root, file)
				os.chmod(xmlFilePath, stat.S_IWRITE)
				tree = ET.parse(xmlFilePath)
				root = tree.getroot()
				for item in root.iter():
					value = item.get('label')
					if value == 'kds':
						print("{} Parsing Started".format(file))
						text = item.get('fileName')
						item.attrib['filename'] = kdsFileName
						print("{} Parsing Completed".format(file))
				tree.write(xmlFilePath, encoding='utf-8', xml_declaration=True)

			################# -- Flat build Generation ---- #################################


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

############ --- Renaming file in Richos --- ######################################


def rename():
	filename = "richos-prealloc-var-image-dev.ext4"
	if buildType == "richosWithSystemBundle":
		filepath = os.path.abspath(os.path.join(
			systemBundleOutputPath, "nonhlos\\flat"))
	else:
		filepath = os.path.abspath(os.path.join(outputPath, "nonhlos\\flat"))
	splittedname = filename.split("-dev")
	newfilename = splittedname[0]+splittedname[1]
	return os.rename(filepath+"\\"+filename, filepath+"\\"+newfilename)


############ --- copy systemdata --- ######################################

def systemdata():
	if buildType == "richosWithSystemBundle":
		source = r"C:\SOFTWARES\systemdata.zip"
		destination = os.path.abspath(systemBundleOutputPath)
	else:
		source = r"C:\SOFTWARES\systemdata.zip"
		destination = os.path.abspath(outputPath)
	print("Copying systemdata Started")
	#copy_tree(source, destination)
	shutil.unpack_archive(source, destination)
	print("Copying systemdata Completed")


################ --- Copy Patch, RawProgramming files --- #######################
def copyFiles(kdsFileName, outputPath):
	kdsPath = os.path.abspath(os.path.join(r"C:\SOFTWARES", kdsFileName))
	kdsDst = os.path.join(outputPath, "nonhlos", "flat")
	for root, dir, files in os.walk(outputPath):
		for di in dir:
			if di == 'only_factory':
				flatPath = os.path.join(root, di)
				for file in os.listdir(flatPath):
					print("Copy of {} file Started".format(file))
					src = os.path.join(flatPath, file)
					dst = os.path.join(outputPath, "nonhlos", "flat", file)
					if os.path.isdir(src):
						shutil.copytree(src, dst)
					else:
						shutil.copy(src, dst)

				shutil.copy(kdsPath, kdsDst)

				print("Copy of Flat build Patch files Completed")


############# --- Delete Unzipped Packages --- #################################
def delUnzipPackages(outputPath):
	for root, dir, files in os.walk(outputPath):
		for di in dir:
			print("Deleting of Unzipped Package {} Started".format(di))
			pathToDi = os.path.join(root, di)
			shutil.rmtree(pathToDi)

			print("Deleting of Unzipped Package {} Completed".format(di))


############ --- Copy Richos Package --- ######################################
def copyRichosPackage(richosOutputPath, outputPath):
	os.chmod(richosOutputPath, stat.S_IWRITE)
	os.chmod(outputPath, stat.S_IWRITE)
	if variant == '8195c':
		searchfile = "archive_balboa-apricot-image-ui-dev.zip"
	else:
		searchfile = "archive_binz-apricot-image-ui.zip"

	for root, dir, files in os.walk(richosOutputPath):
		for file in files:
			if file == searchfile:
				print("Copying of Richos Image Started")
				imagePath = os.path.join(root, file)
				shutil.copy(imagePath, outputPath)

				print("Copying of Richos Image Completed")


############# --- Flat Build Flashing --- #####################
# def Power_on_off(arduino, x):
#	print(x)
#	arduino.write(x.encode('utf-8'))
#	time.sleep(0.05)
#	data = arduino.readline()
#	return data


# def comPorts(portType):
#	dictOfComPorts = {}
#	key = ''  # key will hold the COM port entry ex: COM3,COM6,etc.
#	value = ''	# value will hold the description of COM port ex: "Qualcomm HS-USB","Arduino Uno",etc.
#	ports = list_ports.comports()
#	for dvc, desc, hwid in sorted(ports):
#		dictOfComPorts[dvc] = desc

#	if dictOfComPorts != {}:
#		for key in dictOfComPorts:
#			if portType in dictOfComPorts[key]:
#				value = dictOfComPorts[key]
#				return dictOfComPorts, key, value
#			else:
#				key = ''
#				value = ''
#	return dictOfComPorts, key, value


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

		dict, key, value = controller.comPorts("Arduino")
		arduinoPort = key  # serial port
		baud = 9600	 # baudrate
		arduino = serial.Serial(port=arduinoPort, baudrate=baud, timeout=.1)
		controller.Power_on_off(arduino, "wakeup")
		time.sleep(2)
		controller.Power_on_off(arduino, "2")  # power on
		print('Powered on')
		time.sleep(7)
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

					print("-----------Console Output of Flatbuild Flashing-------------------")
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
							controller.Power_on_off(arduino, "1")
							time.sleep(2)
							controller.Power_on_off(arduino, "2")  # power on
							time.sleep(2)
							print('Powered on')
							time.sleep(5)
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


############# --- Write Build Information to Text File --- #####################
def writeBuildInformation(outputPath):

	filePath = os.path.join(outputPath, "buildInformation.txt")
	with open(filePath, 'w') as f:
		f.write("User: {}".format(userName))
		f.write("\nDate & Time: {}".format(datetime.datetime.now()))
		f.write("\nBuild Type: {}".format(buildType))
		f.write("\nBuild Number: {}".format(buildNumber))
		if sys.argv[1] == "richos":
			f.write("\nRichOS buildNumber: {}".format(richosBuild))
			f.write("\nRichOS Artifactory Path: {}".format(
				richosArtifactoryPath))
			f.write("\nRichOS Output Path: {}".format(richosOutputPath))
		elif sys.argv[1] == "richosWithSystemBundle":
			f.write("\nRichOS buildNumber: {}".format(richosBuild))
			f.write("\nRichOS Artifactory Path: {}".format(
				richosArtifactoryPath))
			f.write("\nSystem bundle Information: {}".format(
				inputArtifactoryPath))
			f.write("\nOutput Path: {}".format(outputPath))
		else:
			f.write("\nSystem bundle Information: {}".format(
				inputArtifactoryPath))
			f.write("\nOutput Path: {}".format(outputPath))


############### --- Pre Flashing  Setup --- #####################################
def preFlashingSetup():
	if buildType == "richos":
		downloadArtifacts(buildType, listOfFlashItems, richosBuild, richosArtifactoryPath, richosOutputPath, userName,artifactoryToken)
		systemdata()
		#delUnzipPackages(outputPath)
		copyRichosPackage(richosOutputPath, outputPath)
		#unzipArtifacts(listOfFlashItems, outputPath)
		#moveqnx()
		#shFileParsing(outputPath)
		#flatBuildGeneration(outputPath)
		#xmlParsing(outputPath, kdsFileName)
		#copyFiles(kdsFileName, outputPath)
		#rename()
		#flashFlatBuild(outputPath, qFilPath)
		writeBuildInformation(outputPath)
	elif buildType == "richosWithSystemBundle":
		downloadArtifacts(buildType, listOfFlashItems, [buildNumber, richosBuild],[inputArtifactoryPath, richosArtifactoryPath], [systemBundleOutputPath, richosOutputPath],userName, artifactoryToken)
		systemdata()
		#delUnzipPackages(systemBundleOutputPath)
		copyRichosPackage(richosOutputPath, systemBundleOutputPath)
		#unzipArtifacts(listOfFlashItems, systemBundleOutputPath)
		#moveqnx()
		#shFileParsing(systemBundleOutputPath)
		#flatBuildGeneration(systemBundleOutputPath)
		#xmlParsing(systemBundleOutputPath, kdsFileName)
		#copyFiles(kdsFileName, systemBundleOutputPath)
		#rename()
		#flashFlatBuild(systemBundleOutputPath, qFilPath)
		writeBuildInformation(richosSystemBundleOutputPath)
	else:
		downloadArtifacts(buildType, listOfFlashItems, buildNumber, inputArtifactoryPath, outputPath, userName,artifactoryToken)
		systemdata()
		#delUnzipPackages(outputPath)
		#unzipArtifacts(listOfFlashItems, outputPath)
		#moveqnx()
		#shFileParsing(outputPath)
		#flatBuildGeneration(outputPath)
		#xmlParsing(outputPath, kdsFileName)
		#copyFiles(kdsFileName, outputPath)
		#rename()
		flashFlatBuild(outputPath,qFilPath)
		writeBuildInformation(outputPath)


#################################################################################

def main():
	#controller.debugBreaker("debug")
	preFlashingSetup()
	#controller.debugBreaker("normal")
	# controller.powerCycle()
	return


if __name__ == '__main__':
	main()

