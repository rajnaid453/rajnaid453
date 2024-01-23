import os
import time
import os
import time
from datetime import datetime
import config as CONF


def writeLog(log1, log2=""):
    current_time = datetime.now().strftime("%H_%M_%S")
    current_date = datetime.now().strftime("%d_%m_%y")
    log_file = current_date + '_log.txt'
    message = current_time + ' : ' + str(log1) + ' >> ' + str(log2)
    with open(log_file , 'a') as fo :
        fo.write('\n' + message)
    print(message)


def flash_vcpu():
    writeLog("VCPU flashing Started")
    timeout = 900
    flashgui = CONF.flashgui
    vcpu_file_path = CONF.vcpu_file_path
    kds_file_path = CONF.kds_file_path
    flash_gui_path = os.path.join(flashgui, "FlashGUI.exe /h")
    result_file = os.path.join(flashgui, "Result.txt")
    log_file = os.path.join(flashgui, "logfile.txt")
    if os.path.exists(result_file):
        os.remove(result_file)
    if os.path.exists(log_file):
        os.remove(log_file)
    cmd = "{} /f{} /KDS{} /iQuad-G3G-RS232-DebugAdapter C - FT6RVBE9,3000000,8,1,even /KDSSAVE /av".format(
        flash_gui_path, vcpu_file_path, kds_file_path)

    os.system(cmd)
    tasklist = os.popen("tasklist").read()
    count = 0

    while ("FlashGUI.exe" in tasklist):
        if count < timeout:
            count += 1
            time.sleep(1)
        else:
            writeLog(
                "VCPU flashing did not complete within {} seconds. Hence failing".format(timeout))
            exit(0)
        tasklist = os.popen("tasklist").read()
    if os.path.exists(result_file):
        with open(result_file) as f:
            logFile = open(log_file, 'r')
            data = logFile.readlines()
            for line in data:
                writeLog(line)
            logFile.close()
            res = f.read()
            if "0x00000000" in res:
                writeLog("VCPU flashing was successful")
            else:
                writeLog("VCPU flashing Failed")

    else:
        writeLog("Result file is not generated.")


flash_vcpu()
