import time
import os
import requests
import serial
from datetime import datetime
from serial.tools import list_ports
import config as CONF
#import arduinoController as controller
import paramiko
import subprocess
import sys

doPowerCycle = False


buildNumber = int(sys.argv[1])
buildType = str(sys.argv[2])
richosBuild = int(sys.argv[3])
outputPath = ""

if buildType == "richos":
    outputPath = os.path.abspath(os.path.join(r"C:\Workspace\Gen20x\builds", "rs" + "_" + str(richosBuild)))
elif buildType == "richosWithSystemBundle":
    outputPath = os.path.abspath(os.path.join(r"C:\Workspace\Gen20x\builds","sb" + "_" + str(buildNumber) + "_" + "rs" + "_" + str(richosBuild)))
elif buildType == "systemBundle":
    outputPath = os.path.abspath(os.path.join(r"C:\Workspace\Gen20x\builds","sb" + "_" + str(buildNumber)))
    
def writeLog(log1, log2=""):
    current_time = datetime.now().strftime("%H_%M_%S")
    current_date = datetime.now().strftime("%d_%m_%y")
    log_file = current_date + '_log.txt'
    message = current_time + ' : ' + str(log1) + ' >> ' + str(log2)
    with open(log_file , 'a') as fo :
        fo.write('\n' + message)
    print(message)


# def comPorts(portType):
#     dictOfComPorts = {}
#     # Key = COM3,COM6,etc.
#     # Value = "Qualcomm HS-USB","Arduino Uno",etc.
#     key = ''
#     value = ''
#     ports = list_ports.comports()
#     for dvc, desc, hwid in sorted(ports):
#         dictOfComPorts[dvc] = desc

#     if dictOfComPorts != {}:
#         for key in dictOfComPorts:
#             if portType in dictOfComPorts[key]:
#                 value = dictOfComPorts[key]
#                 return dictOfComPorts, key, value
#             else:
#                 key = ''
#                 value = ''
#     return dictOfComPorts, key, value


# def powerCycle():
#     dict, key, value = comPorts("Arduino")
#     arduinoPort = key
#     baud = 9600
#     arduino = serial.Serial(port=arduinoPort, baudrate=baud, timeout=.1)
#     arduino.write("1".encode('utf-8'))  # Power OFF
#     writeLog("Power Cycle", "OFF")
#     time.sleep(2)
#     arduino.write("2".encode('utf-8'))  # Power ON
#     writeLog("Power Cycle", "ON")


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
    password='oelinux123'

    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password, timeout=200)

    #ssh.connect(ip, port, username, password, timeout=200)
    print('Retriving Version details from Head Unit')
    time.sleep(1)
    if buildType == "richosWithSystemBundle":
        stdin,stdout2,stderr=ssh.exec_command('cat /etc/build')
    elif buildType == "richos":
        stdin,stdout2,stderr=ssh.exec_command('cat /etc/build')  
    elif buildType == "systemBundle":
        stdin,stdout2,stderr=ssh.exec_command('cat /mnt/vcdata/system-version.txt')
    
    buildInfo = [i.replace('\n','') for i in stdout2]
    print("buildInfo----->>>",buildInfo)
    ssh.close()

    # filePath = os.path.join(outputPath, "versionInfo.txt")
    # with open(filePath, 'w') as f:
    #   for i in buildInfo:
    #       f.write(i+"\n")
    #       print(i)



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
            #controller.powerCycle()
            time.sleep(5)
            
#controller.debugBreaker("normal")
#controller.powerCycle()
triggerETFW("ET Framework", CONF.etfStart)
time.sleep(2)
triggerETFW("ET Online", CONF.etfGoOnline)
triggerIgnitionOn()


#Logging enablement code implementation
def edit_logger_json(sftp):
    new_json_list = []
    with sftp.open('logger.json','r') as fr:
        data = fr.readlines() # returns list of lines
        for line in data:
            if line.strip() == '"log4cplus_enable":"false",':
                line = '    "log4cplus_enable":"true",\n'
                new_json_list.append(line)
            elif line.strip() == '"property_omss_filepath":"/usr/share/omslogger/logger_omss_rel.properties",':
                line = '    "property_omss_filepath":"/usr/share/omslogger/logger_omss_deb.properties",\n'
                new_json_list.append(line)
            elif line.strip() == '"property_omsa_filepath":"/usr/share/omslogger/logger_omsa_rel.properties",':
                line = '    "property_omsa_filepath":"/usr/share/omslogger/logger_omsa_deb.properties",\n'
                new_json_list.append(line)
            elif line.strip() == '"libalgo_tapout": "false",':
                line = '    "libalgo_tapout": "true",\n'
                new_json_list.append(line)
            elif line.strip() == '"libtgc_tapout": "false",':
                line = '    "libtgc_tapout": "true",\n'
                new_json_list.append(line)
            elif line.strip() == '"omsservice_tapout": "false",':
                line = '    "omsservice_tapout": "true",\n'
                new_json_list.append(line)
            elif line.strip() == '"omsapp_tapout": "false",':
                line = '    "omsapp_tapout": "true",\n'
                new_json_list.append(line)
            elif line.strip() == '"time_stamp": "false",':
                line = '    "time_stamp": "true",\n'
                new_json_list.append(line)
            else:
                new_json_list.append(line)
    
    with sftp.open('logger.json','w+') as fw:
        for line in new_json_list:
            fw.write(line)
    
    return "logger_json File Updated Successfully!!!"

def edit_logger_deb_properties(sftp):
    new_json_list = []
    with sftp.open('logger_omsa_deb.properties','r') as fr:
        data = fr.readlines() # returns list of lines
        for line in data:
            if line.strip() == 'log4cplus.rootLogger=OFF':
                line = 'log4cplus.rootLogger=ALL\n'
                new_json_list.append(line)
            elif line.strip() == 'log4cplus.logger.OMSAPP = OFF, SocketAppender,ConsoleAppender,OMSAppDltAppender':
                line = 'log4cplus.logger.OMSAPP = ALL, SocketAppender,ConsoleAppender,OMSAppDltAppender\n'
                new_json_list.append(line)
            else:
                new_json_list.append(line)

    new_json_list1 = []
    with sftp.open('logger_omss_deb.properties','r') as fr:
        data = fr.readlines() # returns list of lines
        for line1 in data:
            if line1.strip() == 'log4cplus.rootLogger=OFF':
                line1 = 'log4cplus.rootLogger=ALL\n'
                new_json_list1.append(line1)
            elif line1.strip() == 'log4cplus.logger.OMSSERVICE = OFF, SocketAppender,ConsoleAppender,OMSServiceDltAppender':
                line1 = 'log4cplus.logger.OMSSERVICE = ALL, SocketAppender,ConsoleAppender,OMSServiceDltAppender\n'
                new_json_list1.append(line1)
            elif line1.strip() == 'log4cplus.logger.LIBTGC = OFF, SocketAppender,ConsoleAppender,LibTgcDltAppender':
                line1 = 'log4cplus.logger.LIBTGC = ALL, SocketAppender,ConsoleAppender,LibTgcDltAppender\n'
                new_json_list1.append(line1)
            elif line1.strip() == 'log4cplus.logger.LIBOMSALGO = OFF, SocketAppender,ConsoleAppender,LibAlgoDltAppender':
                line1 = 'log4cplus.logger.LIBOMSALGO = ALL, SocketAppender,ConsoleAppender,LibAlgoDltAppender\n'
                new_json_list1.append(line1)
            # elif line.strip() == 'log4cplus.logger.OMSAPP = OFF, SocketAppender,ConsoleAppender,OMSAppDltAppender':
            #     line = 'log4cplus.logger.OMSAPP = ALL, SocketAppender,ConsoleAppender,OMSAppDltAppender\n'
                # new_json_list1.append(line1)
            else:
                new_json_list1.append(line1)
        
    
    with sftp.open('logger_omsa_deb.properties','w+') as fw:
        for line in new_json_list:
            fw.write(line)

    with sftp.open('logger_omss_deb.properties','w+') as fw:
        for line in new_json_list1:
            fw.write(line)
    
    return "logger_deb.properties File Updated Successfully!!!"

def edit_run_oms_camera(sftp):
    edit_line = ""
    with sftp.open('run_oms-camera.sh','r') as fw:
        data = fw.readlines()
        for line in data:
            if line.strip() != 'oms-camera /app /etc/oms-camera/config/app_config.xml /etc/oms-camera/config /time /application /another /Capture /Externalcomm /OEC /QoS /dataTransfer':
                edit_line = 'oms-camera /app /etc/oms-camera/config/app_config.xml /etc/oms-camera/config /time /application /another /Capture /Externalcomm /OEC /QoS /dataTransfer'
            elif line.strip() == 'oms-camera /app /etc/oms-camera/config/app_config.xml /etc/oms-camera/config /time /application /another /Capture /Externalcomm /OEC /QoS /dataTransfer':
                edit_line = 'oms-camera /app /etc/oms-camera/config/app_config.xml /etc/oms-camera/config /time /application /another /Capture /Externalcomm /OEC /QoS /dataTransfer'
    with sftp.open('run_oms-camera.sh','w') as fw:
        if len(edit_line) > 0:
            fw.write(edit_line)
    
    return "run_oms-camera.sh File Updated Successfully!!!"

def edit_dataTransfer(sftp):
    new_json_list = []
    with sftp.open('dataTransfer.xml','r') as fr:
        data = fr.readlines() # returns list of lines
        for line in data:
            if line.strip() == '<parameter name="ClientIP" value="10.120.1.101" />':
                line = '                <parameter name="ClientIP" value="169.254.17.12" />\n'
                new_json_list.append(line)
            elif line.strip() == '<parameter name="BindIPToSend" value="10.120.1.91" />':
                line = '                <parameter name="BindIPToSend" value="169.254.17.99" />\n'
                new_json_list.append(line)
            elif line.strip() == '<parameter name="BindIPToRecv" value="10.120.1.91" />':
                line = '                <parameter name="BindIPToRecv" value="169.254.17.99" />\n'
                new_json_list.append(line)
            elif line.strip() == '<parameter name="InterfaceToSend" value="eth1.120" />':
                line = '                <parameter name="InterfaceToSend" value="eth1.1" />\n'
                new_json_list.append(line)
            elif line.strip() == '<parameter name="InterfaceToRecv" value="eth1.120" />':
                line = '                <parameter name="InterfaceToRecv" value="eth1.1" />\n'
                new_json_list.append(line)
            elif line.strip() == '<channel name="CameraChannel0" number="0" send="1" sampling_bitshift="0" InstanceName="CameraImage0" CRCInstanceName="ImageCRC0" />':
                line = '                <channel name="CameraChannel0" number="0" send="0" sampling_bitshift="0" InstanceName="CameraImage0" CRCInstanceName="ImageCRC0" />\n'
                new_json_list.append(line)
            elif line.strip() == '<channel name="CameraChannel1" number="1" send="1" sampling_bitshift="0" InstanceName="CameraImage1" CRCInstanceName="ImageCRC1" />':
                line = '                <channel name="CameraChannel1" number="1" send="0" sampling_bitshift="0" InstanceName="CameraImage1" CRCInstanceName="ImageCRC1" />\n'
                new_json_list.append(line)
            elif line.strip() == '<channel name="CameraChannel2" number="2" send="1" sampling_bitshift="0" InstanceName="CameraImage2" CRCInstanceName="ImageCRC2" />':
                line = '                <channel name="CameraChannel2" number="2" send="0" sampling_bitshift="0" InstanceName="CameraImage2" CRCInstanceName="ImageCRC2" />\n'
                new_json_list.append(line)
            elif line.strip() == '<channel name="CameraChannel3" number="3" send="1" sampling_bitshift="0" InstanceName="CameraImage3" CRCInstanceName="ImageCRC3" />':
                line = '                <channel name="CameraChannel3" number="3" send="0" sampling_bitshift="0" InstanceName="CameraImage3" CRCInstanceName="ImageCRC3" />\n'
                new_json_list.append(line)
            else:
                new_json_list.append(line)
    
    with sftp.open('dataTransfer.xml','w+') as fw:
        for line in new_json_list:
            fw.write(line)
    
    return "dataTransfer.xml File Updated Successfully!!!"
 
def connect_richos_edit_logger_files():
    port=22
    cmd="mount -o remount,rw /"
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(CONF.richos_ip, port, CONF.richos_username,CONF.richos_password, timeout=200)

    time.sleep(2)
    ssh.exec_command(cmd)

    time.sleep(2)
    sftp=ssh.open_sftp()
    sftp.chdir("/usr/share/omslogger")

    msg1 = edit_logger_json(sftp)
    msg2 = edit_logger_deb_properties(sftp)

    print(msg1)
    print(msg2)

    sftp.chdir("/etc/oms-camera/config")
    msg3 = edit_run_oms_camera(sftp)
    msg4 = edit_dataTransfer(sftp)

    print(msg3)
    print(msg4)
    
    ssh.close()

def logging_enable():
    os.chdir('C:\Tools\MobaXterm_Portable_v21.1')
    print("Connecting to RichOS and QNX!!")
    os.system("TASKKILL /F /IM MobaXterm_Personal_21.1.exe")
    run_macro1 = 'MobaXterm_Personal_21.1.exe -runmacro connect_richos_qnx -exitwhendone'
    os.system(run_macro1)

    time.sleep(10)
    print("ADB Disable started!!")
    #subprocess.Popen('adb connect 169.254.17.99;adb disable-verity', shell=True)
    run_macro2 = 'MobaXterm_Personal_21.1.exe -runmacro adb_disable -exitwhendone'
    os.system(run_macro2)
    time.sleep(20)
    run_macro3 = 'MobaXterm_Personal_21.1.exe -runmacro soft_reset -exitwhendone'
    os.system(run_macro3)

    time.sleep(20)
    print("Started Password Reset!!")
    run_macro4 = 'MobaXterm_Personal_21.1.exe -runmacro password_reset -exitwhendone'
    os.system(run_macro4)

    time.sleep(20)
    print("File Edit started")
    connect_richos_edit_logger_files()

    time.sleep(20)
    print("Started Soft Reset!!")
    # run_macro3 = 'MobaXterm_Personal_21.1.exe -runmacro soft_reset -exitwhendone'
    os.system(run_macro3)

    time.sleep(10)
    # print("Connect RichOS!!")
    # run_macro4 = 'MobaXterm_Personal_21.1.exe -runmacro connect_richos'
    # os.system(run_macro4)
    return "Logging enabled"

#vcCoding()
#controller.powerCycle()
#time.sleep(30)
logging_enable()

