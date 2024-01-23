import time, sys, os, re
import adtf
import xlrd
import requests
import REST_URI as URI
import shutil

# Logging
log = adtf.Log()
session = adtf.Session()    
sys.stderr = log

def triggerETFW(state, uri):
    log_wait_info("state " + state)
    res = requests.get(uri)
    # log_wait_info(res.status_code + str(res.json()))
    # return res

def log_wait_info(text):
    global log
    log.info(text)
    time.sleep(2)

# # Reading Light
def uc1_signal():
    triggerETFW("UC1 Reading Light Signals", URI.uc1_signal1_URI)
    print("uc1_signal1_URI added successfully")

# # Unbuckled child seat
def uc2_signal():
    triggerETFW("UC2 Unbuckled Child Seat Signals", URI.uc2_signal1_URI)

# # BSM
def uc3_signal():
    triggerETFW("UC3 BSM Signals", URI.uc3_signal1_URI)

# Sunblind Front Open
def uc4_signal1():
    triggerETFW("UC4_SB Sunroof Sunblind Front Signals", URI.uc4_signal1_URI)

# Sunblind Front Opening
def uc4_signal11():
    triggerETFW("UC4_SB Sunroof Sunblind Front Signals", URI.uc4_signal11_URI)

# # Sunroof  Front Open   
def uc4_signal2():
    triggerETFW("UC4_SR Sunroof Sunblind Front Signals", URI.uc4_signal2_URI)

# # Sunroof  Front Open   
def uc4_signal22():
    triggerETFW("UC4_SR Sunroof Sunblind Front Signals", URI.uc4_signal22_URI)

# # Sunroof  Front Open   
def uc4_signal3():
    triggerETFW("UC4_SR Sunroof Sunblind Front Signals", URI.uc4_signal3_URI)
    
# # Sunroof  Front Open   
def uc4_signal33():
    triggerETFW("UC4_SR Sunroof Sunblind Front Signals", URI.uc4_signal33_URI)

# # Sunblind Front Open
def uc4_signal4():
    triggerETFW("UC4_SB Sunroof Sunblind Front Signals", URI.uc4_signal4_URI)

# # Sunblind Front Open
def uc4_signal44():
    triggerETFW("UC4_SB Sunroof Sunblind Front Signals", URI.uc4_signal44_URI)

# # Mirror Preselection
def uc5_signal():
    triggerETFW("UC5 Mirror Preselection Signals", URI.uc5_signal1_URI)

# # Search Light Front
def uc6_signal():
    triggerETFW("UC6 Search Light Front Signals", URI.uc6_signal1_URI)

# # Rear Window Rollerblind
def uc7_signal():
    triggerETFW("UC7 Rear Window Rollerblind Signals",
                URI.uc7_signal1_URI)
    
signalDict = {'UC1': uc1_signal, 'UC2': uc2_signal, 'UC3': uc3_signal, 'UC4': uc4_signal1, 'UC5': uc5_signal, 'UC6': uc6_signal, 'UC7': uc7_signal}

config_path = r"C:\Gen20_Automation\IVTS\IVTS_QT_V1.78_220922_test_version\HILS\config\system.xml"
csv_Dump=r"C:\\testteam_IVTS"

log_wait_info("Unloading current configuration")
session.unload_configuration()
log_wait_info("Loading configuration")
session.load_configuration(config_path)

excel_file = xlrd.open_workbook(filename=sys.argv[2])
excel_sheet = excel_file.sheet_by_index(0)
column_names=excel_sheet.row(0)
col_values = excel_sheet.col_values(13)
log_wait_info(str(col_values))

def replay_dats(dat_location,dat_name):
    # Playing DAts(Playing COnfig)
        session.set_active_configuration("PlaybackGen2_Common")
        log_wait_info(str(dat_location+"\\"+ dat_name))
        session.filter_set_property("Harddisk_Player", "filename", dat_location+ "\\" + dat_name)
        #HILS Config(Replay)
        session.set_active_configuration("Playback_Gen2_REC")
        session.filter_set_property("Harddisk_Recorder", "filename", "C:\\testteam_IVTS" + "\\" + dat_name)
        
        log_wait_info("Initializing the configuration.")
        session.set_runlevel(4)
        session.set_current_file_pos(0)
        session.set_runlevel(5)
        session.start()
        while 5 == session.get_runlevel():
            log.info("Current file pos is " + str(session.get_current_file_pos()))
            time.sleep(0.5)
        log_wait_info("Shutdown the configuration.")
        session.set_runlevel(3)
        time.sleep(10)
       
for i in column_names:
    if "DAT File" in str(i):
        log_wait_info(str(i))
        index = column_names.index(i)

    if "Module" in str(i):
        mod_index = column_names.index(i)

col_values = excel_sheet.col_values(index)
module = excel_sheet.col_values(mod_index)

dict1 = {}
for i in range(1,excel_sheet.nrows):
    row = excel_sheet.row_values(i)
    dict1 [row[index]] = row[mod_index]
log_wait_info(str(dict1))

datfile_names = list(map(str,col_values))
log_wait_info(str(datfile_names))
print("....datfile_names....", str(datfile_names))

for x in os.listdir(sys.argv[1]):
    log_wait_info(str(x))
    if str(x.split(".dat")[0]) in datfile_names:
        if (dict1.get(str(x.split(".dat")[0]))) == "UC1":
            log_wait_info(str("UC1/Reading Light ETH RESTAPI Signals"))
            res_readlight_signal= uc1_signal()
            log_wait_info(str(res_readlight_signal))

        elif (dict1.get(str(x.split(".dat")[0]))) == "UC2":
            log_wait_info(str("UC2/Unbuckled child seat ETH RESTAPI Signals"))
            res_UnBuckled_ChildSeat_signal = uc2_signal()
            log_wait_info(str(res_UnBuckled_ChildSeat_signal))
        
        elif (dict1.get(str(x.split(".dat")[0]))) == "UC3":
            log_wait_info(str("UC3/BSM ETH RESTAPI Signals"))
            res_BSM_Warning_signal = uc3_signal()
            log_wait_info(str(res_BSM_Warning_signal))    

        elif (dict1.get(str(x.split(".dat")[0]))) == "UC5":
            log_wait_info(str("UC1/Mirror Preselection ETH RESTAPI Signals"))
            res_Ext_Mirror_Preselect_signal= uc5_signal()
            log_wait_info(str(res_Ext_Mirror_Preselect_signal))

        elif (dict1.get(str(x.split(".dat")[0]))) == "UC6":
            log_wait_info(str("UC2/Search Light Front ETH RESTAPI Signals"))
            res_Search_Light_signal = uc6_signal()
            log_wait_info(str(res_readlight_signal))
        
        elif (dict1.get(str(x.split(".dat")[0]))) == "UC7":
            log_wait_info(str("UC2/Rear Window Rollerblind ETH RESTAPI Signals"))
            res_Rear_Window_Sunblind_signal = uc7_signal()
            log_wait_info(str(res_Rear_Window_Sunblind_signal))

        elif (dict1.get(str(x.split(".dat")[0]))) == "UC4":
            if str(x.split(".dat")[0]) == "223_1227_7524549642_2022_04_05_11_56_09" or str(x.split(".dat")[0]) == "223_1227_9617270392_2022_04_05_11_20_33":
                log_wait_info(str("UC4/Sunblind Front ETH RESTAPI Signals"))
                res_SunRoof_SunBlind_Ctrl_signal = uc4_signal1()
                log_wait_info(str(res_SunRoof_SunBlind_Ctrl_signal ))         

            elif str(x.split(".dat")[0]) == "223_1227_8387427587_2022_04_05_11_13_23" or str(x.split(".dat")[0]) == "223_1227_9961327356_2022_03_01_15_12_49":
                log_wait_info(str("UC4/Sunblind Front ETH RESTAPI Signals"))
                res_SunRoof_SunBlind_Ctrl_signal = uc4_signal2()
                log_wait_info(str(res_SunRoof_SunBlind_Ctrl_signal))

        
            elif str(x.split(".dat")[0]) == "223_1227_5911580432_2022_04_05_11_23_59" or str(x.split(".dat")[0]) == "223_1227_8877669960_2022_04_05_11_57_56":
                log_wait_info(str("UC4/Sunblind Front ETH RESTAPI Signals"))
                res_SunRoof_SunBlind_Ctrl_signal = uc4_signal3()
                log_wait_info(str(res_SunRoof_SunBlind_Ctrl_signal))

            elif str(x.split(".dat")[0]) == "223_1227_7736448032_2022_04_05_11_44_30" or str(x.split(".dat")[0]) == "223_1227_9864261804_2022_04_05_11_42_17":
                log_wait_info(str("UC4/Sunblind Front ETH RESTAPI Signals"))
                res_SunRoof_SunBlind_Ctrl_signal = uc4_signal4()
                log_wait_info(str(res_SunRoof_SunBlind_Ctrl_signal))

        else:
           continue
        replay_dats(sys.argv[1],x)
       
    else:
        continue

log.info("ADTF replay finished.")


        

    




