import os
import time


def load_data_from_configfile():
    """
    This method fetches the data from config.txt and return it in list format.
    """
    loadval = []
    f = open('config.txt', 'r')
    for line in f:
        loadval.append((line.partition('#')[0]).rstrip())                                                               # Read data from config.txt
    return loadval


def flash_vcpu():
    timeout = 900
    loadval = load_data_from_configfile()
    flashgui = loadval[0].replace("\n", "")
    vcpu_file_path = loadval[1].replace("\n", "")
    kds_file_path = loadval[2].replace("\n", "")
    flash_gui_path = os.path.join(flashgui, "FlashGUI.exe /h")
    result_file = os.path.join(flashgui, "Result.txt")
    log_file = os.path.join(flashgui, "logfile.txt")
    if os.path.exists(result_file):
        os.remove(result_file)
    if os.path.exists(log_file):
        os.remove(log_file)
    cmd = "{} /f{} /KDS{} /iQuad-G3G-RS232-DebugAdapter C - FT4ZNWF1,3000000,even,8,1 /KDSSAVE /av".format(
        flash_gui_path, vcpu_file_path, kds_file_path)

    os.system(cmd)
    tasklist = os.popen("tasklist").read()
    count = 0

    while ("FlashGUI.exe" in tasklist):
        if count < timeout:
            count += 1
            time.sleep(1)
        else:
            print("VCPU flashing did not complete within {} seconds. Hence failing".format(timeout))
            exit(0)
        tasklist = os.popen("tasklist").read()
    if os.path.exists(result_file):
        with open(result_file) as f:
            logFile = open(log_file,'r')
            data = logFile.readlines()
            for line in data:
                print(line)
            logFile.close()
            res = f.read()
            if "0x00000000" in res:
                print("VCPU flashing was successful")
            else:
                print("VCPU flashing Failed")
        
    else:
        print("Result file is not generated.")

flash_vcpu()
