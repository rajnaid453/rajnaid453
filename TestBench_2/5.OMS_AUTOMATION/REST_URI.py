baseURI = "http://localhost:9006/etfapi/v1"
subURI = "http://localhost:9002/etfapi/v1"
accessToken = "xyzabcxyz"
# ecuName = "CIVIC206"
# activeComfort = ("Active_Comfort",
#                  "FF,40,00,53,03,60,A0,3F,00,00,00,00,7A,34,55,2E")
# VideoHandling = ("Video_Handling", "A0,60,00,00,00")
# VehicleFunctions = ("Vehicle_Functions", "00,00,00,00,00,14,03,00,00,00,00,00,00,00,00,00,00,00,00,4A,00,00,00,00,00,66,00,00,00,50,1A,00,00,5A,05,02,04,00,40,00,00,00,00,00,00,00,00,00,00,04,00,00,00,00")

simulateSignal = subURI + "/EthernetService/Ethernet/ChangeEthernetSignal?accessToken=" + \
     accessToken + "&signalName="
simulateSignals = subURI + \
     "/EthernetService/Ethernet/ChangeEthernetSignals?accessToken=" + accessToken + "&signals="
# varientCodingGet = baseURI + "/DiagnosticsService/Ethernet/GetVariantCodingFromDomain?accessToken=" + \
#     accessToken + "&ecuName=" + ecuName + "&domainIdentifier={0}"
# varientCodingWrite = baseURI + "/DiagnosticsService/Ethernet/WriteVariantCodingFromDomain?accessToken=" + \
#     accessToken + "&ecuName=" + ecuName + \
#     "&domainIdentifier={0}&codingData={1}"

# ETFW START
etfStart = baseURI + "/Start?accessToken=" + accessToken
etfStartProfile = baseURI + "/Start/" + accessToken + \
    "?profileName=Gen20X_i2_OFN_Simulation"

# ETFW ONLINE
etfGoOnline = subURI + "/GoOnline?accessToken=" + accessToken

# VEHICLE LINE SIGNAL SIMULATION
vehLine = simulateSignal + "EVC_List02_VehLine_ST3&signalValue=BR214"
vehStyle = simulateSignal + "EVC_List03_StStyle_ST3&signalValue=LHD"
vehBstyle = simulateSignal + "EVC_List01_BodyStyle_ST3&signalValue=FV"

# IGNITION
accessoryOn = subURI + "/SwitchIgnition?accessToken=" + \
    accessToken + "&switchState=Accessory"
accessoryStart = subURI + "/SwitchIgnition?accessToken=" + \
    accessToken + "&switchState=Start"
ignitionOn = subURI + "/SwitchIgnition?accessToken=" + \
    accessToken + "&switchState=On"
ignitionOff = subURI + "/SwitchIgnition?accessToken=" + \
    accessToken + "&switchState=Off"
ignitionLock = subURI + "/SwitchIgnition?accessToken=" + \
    accessToken + "&switchState=Lock"

# VARIENT CODING GET
# getActiveComfort = varientCodingGet.format("Active_Comfort")
# getVideoHandling = varientCodingGet.format("Video_Handling")
# getVehicleFunctions = varientCodingGet.format("Vehicle_Functions")

# # VARIENT CODING PUT
# writeActiveComfort = varientCodingWrite.format(
#     activeComfort[0], activeComfort[1])
# writeVideoHandling = varientCodingWrite.format(
#     VideoHandling[0], VideoHandling[1])
# writeVehicleFunctions = varientCodingWrite.format(
#     VehicleFunctions[0], VehicleFunctions[1])

# ETFW OFFLINE
etfOffline = subURI + "/GoOffline?accessToken=" + accessToken

# ETFW STOP
etfStop = subURI + "/Stop?accessToken=" + accessToken

# UC1    #Reading Light
uc1_signal1 = [{"Name": " LgtSens_Night_ST3", "Value": "1"}]
            #    {"Name":"UI_ReadingLight_FR_Stat_ST3 EH_2969_InteriorLight_Stat", "Name": "State","Value":"1"},
            #    {"Name":"UI_ReadingLight_FR_Stat_ST3 EH_2969_InteriorLight_Stat", "Name":"ErrorStatus","Value":"No_Error"},
            #    {"Name":"UI_ReadingLight_FR_Stat_ST3 EH_2969_InteriorLight_Stat", "Name":"ActualClientID","Value":"2584"},
            #    {"Name":"UI_ReadingLight_FL_Stat_ST3 EH_2969_InteriorLight_Stat", "Name":"State","Value":"1"},
            #    {"Name":"UI_ReadingLight_FL_Stat_ST3 EH_2969_InteriorLight_Stat", "Name":"ErrorStatus","Value":"No_Error"},
            #    {"Name":"UI_ReadingLight_FL_Stat_ST3 EH_2969_InteriorLight_Stat", "Name":"ActualClientID","Value":"2584"}
            # ]
uc1_signal1_URI = simulateSignals + str(uc1_signal1)


# UC2    #Unbuckled child seat
uc2_signal1 = [{"Name": "Bckl_Sw_FP_Stat_ST3", "Value": "NOT"},
               {"Name": "VehDrvDir_Stat_ST3", "Value": "FORWARD"},
               {"Name": "DrRLtch_RL_Stat_ST3", "Value": "CLS"},
               {"Name": "DrRLtch_RR_Stat_ST3", "Value": "CLS"},
               {"Name": "TGC_P_MemPosn_Stat_ST3", "Value": "TGC_POS4"},
               {"Name": "PT4_PTCoor_DrvPosn_Stat_ST3", "Value": "D"},
               {"Name": "VehSpd_X_ST3", "Value": "30 km/h"},
               {"Name": "OC_P_ORC_ST3", "Value": "CLASS2"}]
uc2_signal1_URI = simulateSignals + str(uc2_signal1)


# UC3    #BSM
uc3_signal1 = [{"Name": "EVC_49_540_Avl_ST3", "Value": "TRUE"},
               {"Name": "Bckl_Sw_FP_Stat_ST3", "Value": "OK"},
               {"Name": "DrRLtch_FL_Stat_ST3", "Value": "CLS"},
               {"Name": "DrRLtch_FR_Stat_ST3", "Value": "CLS"},
               {"Name": "VehSpd_X_ST3", "Value": "0Km/h"}]
uc3_signal1_URI = simulateSignals + str(uc3_signal1)

# UC4_1   # Sunblind Front Open
uc4_signal1 = [{"Name": "EVC_List06_Country_ST3", "Value": "OTHER"},
               {"Name": "UI_TSSR_Pnl_Stat_ST3", "Value": "SR_CLOSED"},
               {"Name": "UI_TSSR_RB_Stat_ST3", "Value": "CLS"},
               {"Name": "DrRLtch_FL_Stat_ST3", "Value": "CLS"},
               {"Name": "DrRLtch_FR_Stat_ST3", "Value": "CLS"},
               {"Name": "ISw_Stat_ST3", "Value": "ON"},
               {"Name": "EVC_6F_413_Avl_ST3", "Value": "TRUE"}]
uc4_signal1_URI = simulateSignals + str(uc4_signal1)

# UC4_1   # Sunblind Front Opening
uc4_signal11 = [{"Name": "EVC_List06_Country_ST3", "Value": "OTHER"},
               {"Name": "UI_TSSR_Pnl_Stat_ST3", "Value": "SR_CLOSED"},
               {"Name": "UI_TSSR_RB_Stat_ST3", "Value": "OPENING"},
               {"Name": "DrRLtch_FL_Stat_ST3", "Value": "CLS"},
               {"Name": "DrRLtch_FR_Stat_ST3", "Value": "CLS"},
               {"Name": "ISw_Stat_ST3", "Value": "ON"},
               {"Name": "EVC_6F_413_Avl_ST3", "Value": "TRUE"}]
uc4_signal11_URI = simulateSignals + str(uc4_signal11)

# UC4_2    # Sunroof  Front Open
uc4_signal2 = [{"Name": "EVC_List06_Country_ST3", "Value": "OTHER"},
               {"Name": "UI_TSSR_Pnl_Stat_ST3", "Value": "SR_CLOSED"},
               {"Name": "UI_TSSR_RB_Stat_ST3", "Value": "OPN"},
               {"Name": "DrRLtch_FL_Stat_ST3", "Value": "CLS"},
               {"Name": "DrRLtch_FR_Stat_ST3", "Value": "CLS"},
               {"Name": "ISw_Stat_ST3", "Value": "ON"},
               {"Name": "EVC_6F_413_Avl_ST3", "Value": "TRUE"}]
uc4_signal2_URI = simulateSignals + str(uc4_signal2)

# UC4_2    # Sunroof  Front Opening
uc4_signal22 = [{"Name": "EVC_List06_Country_ST3", "Value": "OTHER"},
               {"Name": "UI_TSSR_Pnl_Stat_ST3", "Value": "SR_OPENING"},
               {"Name": "UI_TSSR_RB_Stat_ST3", "Value": "OPN"},
               {"Name": "DrRLtch_FL_Stat_ST3", "Value": "CLS"},
               {"Name": "DrRLtch_FR_Stat_ST3", "Value": "CLS"},
               {"Name": "ISw_Stat_ST3", "Value": "ON"},
               {"Name": "EVC_6F_413_Avl_ST3", "Value": "TRUE"}]
uc4_signal22_URI = simulateSignals + str(uc4_signal22)

# UC4_3    # Sunroof Front Close
uc4_signal3 = [{"Name": "EVC_List06_Country_ST3", "Value": "OTHER"},
               {"Name": "UI_TSSR_Pnl_Stat_ST3", "Value": "SR_OPENING"},
               {"Name": "UI_TSSR_RB_Stat_ST3", "Value": "OPN"},
               {"Name": "DrRLtch_FL_Stat_ST3", "Value": "CLS"},
               {"Name": "DrRLtch_FR_Stat_ST3", "Value": "CLS"},
               {"Name": "ISw_Stat_ST3", "Value": "ON"},
               {"Name": "EVC_6F_413_Avl_ST3", "Value": "TRUE"}]
uc4_signal3_URI = simulateSignals + str(uc4_signal3)

# UC4_33    # Sunroof Front Closing
uc4_signal33 = [{"Name": "EVC_List06_Country_ST3", "Value": "OTHER"},
               {"Name": "UI_TSSR_Pnl_Stat_ST3", "Value": "SR_OPEN"},
               {"Name": "UI_TSSR_RB_Stat_ST3", "Value": "OPN"},
               {"Name": "DrRLtch_FL_Stat_ST3", "Value": "CLS"},
               {"Name": "DrRLtch_FR_Stat_ST3", "Value": "CLS"},
               {"Name": "ISw_Stat_ST3", "Value": "ON"},
               {"Name": "EVC_6F_413_Avl_ST3", "Value": "TRUE"}]
uc4_signal33_URI = simulateSignals + str(uc4_signal33)

# UC4_4   # Sunblind Front Closed
uc4_signal4 = [{"Name": "EVC_List06_Country_ST3", "Value": "OTHER"},
               {"Name": "UI_TSSR_Pnl_Stat_ST3", "Value": "SR_CLOSED"},
               {"Name": "UI_TSSR_RB_Stat_ST3", "Value": "OPN"},
               {"Name": "DrRLtch_FL_Stat_ST3", "Value": "CLS"},
               {"Name": "DrRLtch_FR_Stat_ST3", "Value": "CLS"},
               {"Name": "ISw_Stat_ST3", "Value": "ON"},
               {"Name": "EVC_6F_413_Avl_ST3", "Value": "TRUE"}]
uc4_signal4_URI = simulateSignals + str(uc4_signal4)

# UC4_44   # Sunblind Front Closing
uc4_signal44 = [{"Name": "EVC_List06_Country_ST3", "Value": "OTHER"},
               {"Name": "UI_TSSR_Pnl_Stat_ST3", "Value": "SR_CLOSED"},
               {"Name": "UI_TSSR_RB_Stat_ST3", "Value": "CLOSING"},
               {"Name": "DrRLtch_FL_Stat_ST3", "Value": "CLS"},
               {"Name": "DrRLtch_FR_Stat_ST3", "Value": "CLS"},
               {"Name": "ISw_Stat_ST3", "Value": "ON"},
               {"Name": "EVC_6F_413_Avl_ST3", "Value": "TRUE"}]
uc4_signal44_URI = simulateSignals + str(uc4_signal44)

# UC5    #Mirror Preselection
uc5_signal1 = [{"Name": "EVC_List03_StStyle_ST3", "Value": "LHD"}]
uc5_signal1_URI = simulateSignal + str(uc5_signal1)

# UC6    #Search Light Front
uc6_signal1 = [{"Name": " LgtSens_Night_ST3", "Value": "1"}]
            #    {"Name":"UI_ReadingLight_FR_Stat_ST3 EH_2969_InteriorLight_Stat", "Name": "State","Value":"1"},
            #    {"Name":"UI_ReadingLight_FR_Stat_ST3 EH_2969_InteriorLight_Stat", "Name":"ErrorStatus","Value":"No_Error"},
            #    {"Name":"UI_ReadingLight_FR_Stat_ST3 EH_2969_InteriorLight_Stat", "Name":"ActualClientID","Value":"2584"},
            #    {"Name":"UI_ReadingLight_FL_Stat_ST3 EH_2969_InteriorLight_Stat", "Name":"State","Value":"1"},
            #    {"Name":"UI_ReadingLight_FL_Stat_ST3 EH_2969_InteriorLight_Stat", "Name":"ErrorStatus","Value":"No_Error"},
            #    {"Name":"UI_ReadingLight_FL_Stat_ST3 EH_2969_InteriorLight_Stat", "Name":"ActualClientID","Value":"2584"}
            # ]
uc6_signal1_URI = simulateSignals + str(uc6_signal1)

# UC7    #Rear Window Rollerblind
uc7_signal1 = [{"Name": "PT4_PTCoor_DrvPosn_Stat_ST3", "Value": "R"},
               {"Name": "VehDrvDir_Stat_ST3", "Value": "2"},
               {"Name": "VehSpd_X_ST3", "Value": "0"},
               {"Name": "RB_R_Stat_ST3", "Value": "RB_EXT"},
               {"Name": "EVC_49_540_Avl_ST3", "Value": "TRUE"}]
uc7_signal1_URI = simulateSignals + str(uc7_signal1)



# api = {"baseURI": baseURI, "etfStart": etfStart, "etfStartProfile": etfStartProfile, "etfGoOnline": etfGoOnline, "vehLine": vehLine, "vehStyle": vehStyle, "accessoryOn": accessoryOn, "accessoryStart": accessoryStart, "ignitionOn": ignitionOn,"ignitionOff": ignitionOff,"ignitionLock": ignitionLock, "getActiveComfort": getActiveComfort, "getVideoHandling": getVideoHandling, "getVehicleFunctions": getVehicleFunctions,"writeActiveComfort": writeActiveComfort,"writeVideoHandling": writeVideoHandling,"writeVehicleFunctions": writeVehicleFunctions, "etfOffline": etfOffline, "etfStop": etfStop,
#        "uc1_signal1_URI": uc1_signal1_URI, "uc2_signal1_URI": uc2_signal1_URI, "uc3_signal1_URI": uc3_signal1_URI, "uc4_signal1_URI": uc4_signal1_URI, "uc5_signal1_URI": uc5_signal1_URI, "uc6_signal1_URI": uc6_signal1_URI, "uc7_signal1_URI": uc7_signal1_URI}
# for k, v in api.items():
#     print("########"*3)
#     print(k)
#     print(v)

'''########################
baseURI
http://localhost:9006/etfapi/v1
########################
etfStart
http://localhost:9006/etfapi/v1/Start?accessToken=xyzabcxyz
########################
etfStartProfile
http://localhost:9006/etfapi/v1/Start/xyzabcxyz?profileName=Gen20X_i2_OFN_Simulation
########################
etfGoOnline
http://localhost:9006/etfapi/v1/GoOnline?accessToken=xyzabcxyz
########################
vehLine
http://localhost:9002/etfapi/v1/EthernetService/Ethernet/ChangeEthernetSignal?accessToken=xyzabcxyz&signalName=EVC_List02_VehLine_ST3&signalValue=BR223
########################
vehStyle
http://localhost:9006/etfapi/v1/EthernetService/Ethernet/ChangeEthernetSignal?accessToken=xyzabcxyz&signalName=EVC_List03_StStyle_ST3&signalValue=LHD  
########################
accessoryOn
http://localhost:9006/etfapi/v1/SwitchIgnition?accessToken=xyzabcxyz&switchState=Accessory
########################
accessoryStart
http://localhost:9006/etfapi/v1/SwitchIgnition?accessToken=xyzabcxyz&switchState=Start
########################
ignitionOn
http://localhost:9006/etfapi/v1/SwitchIgnition?accessToken=xyzabcxyz&switchState=On
########################
ignitionOff
http://localhost:9006/etfapi/v1/SwitchIgnition?accessToken=xyzabcxyz&switchState=Off
########################
ignitionLock
http://localhost:9006/etfapi/v1/SwitchIgnition?accessToken=xyzabcxyz&switchState=Lock
########################
getActiveComfort
http://localhost:9006/etfapi/v1/DiagnosticsService/Ethernet/GetVariantCodingFromDomain?accessToken=xyzabcxyz&ecuName=CIVIC206&domainIdentifier=Active_Comfort     
########################
getVideoHandling
http://localhost:9006/etfapi/v1/DiagnosticsService/Ethernet/GetVariantCodingFromDomain?accessToken=xyzabcxyz&ecuName=CIVIC206&domainIdentifier=Video_Handling     
########################
getVehicleFunctions
http://localhost:9006/etfapi/v1/DiagnosticsService/Ethernet/GetVariantCodingFromDomain?accessToken=xyzabcxyz&ecuName=CIVIC206&domainIdentifier=Vehicle_Functions  
########################
writeActiveComfort
http://localhost:9006/etfapi/v1/DiagnosticsService/Ethernet/WriteVariantCodingFromDomain?accessToken=xyzabcxyz&ecuName=CIVIC206&domainIdentifier=Active_Comfort&codingData=FF,40,00,53,03,60,A0,3F,00,00,00,00,7A,34,55,2E
########################
writeVideoHandling
http://localhost:9006/etfapi/v1/DiagnosticsService/Ethernet/WriteVariantCodingFromDomain?accessToken=xyzabcxyz&ecuName=CIVIC206&domainIdentifier=Video_Handling&codingData=A0,60,00,00,00
########################
writeVehicleFunctions
http://localhost:9006/etfapi/v1/DiagnosticsService/Ethernet/WriteVariantCodingFromDomain?accessToken=xyzabcxyz&ecuName=CIVIC206&domainIdentifier=Vehicle_Functions&codingData=00,00,00,00,00,14,03,00,00,00,00,00,00,00,00,00,00,00,00,4A,00,00,00,00,00,66,00,00,00,50,1A,00,00,5A,05,02,04,00,40,00,00,00,00,00,00,00,00,00,00,04,00,00,00,00
########################
etfOffline
http://localhost:9006/etfapi/v1/GoOffline?accessToken=xyzabcxyz
########################
etfStop
http://localhost:9006/etfapi/v1/Stop?accessToken=xyzabcxyz
########################
uc1_signal1_URI
http://localhost:9006/etfapi/v1/EthernetService/Ethernet/ChangeEthernetSignals?accessToken=xyzabcxyz&signals=[{'Name': 'EVC_List03_StStyle_ST3', 'Value': '01'}, {'Name': 'LgtSens_Night_ST3', 'Value': '01'}, {'Name': 'UI_ReadingLight_FR_Stat_ST3 EH_2969_InteriorLight_Stat.State.2969.0.10', 'Value': '2'}]
########################
uc2_signal1_URI
http://localhost:9006/etfapi/v1/EthernetService/Ethernet/ChangeEthernetSignals?accessToken=xyzabcxyz&signals=[{'Name': 'EVC_List03_StStyle_ST3', 'Value': 'LHD'}, 
{'Name': 'Bckl_Sw_FP_Stat_ST3', 'Value': 'NOT'}, {'Name': 'VehDrvDir_Stat_ST3', 'Value': 'FORWARD'}, {'Name': 'DrRLtch_RL_Stat_ST3', 'Value': 'CLS'}, {'Name': 'DrRLtch_RR_Stat_ST3', 'Value': 'CLS'}, {'Name': 'TGC_P_MemPosn_Stat_ST3', 'Value': 'TGC_POS4'}, {'Name': 'PT4_PTCoor_DrvPosn_Stat_ST3', 'Value': 'D'}, {'Name': 'VehSpd_X_ST3', 'Value': '30 km/h'}, {'Name': 'OC_P_ORC_ST3', 'Value': 'CLASS2'}]
########################
uc3_signal1_URI
http://localhost:9006/etfapi/v1/EthernetService/Ethernet/ChangeEthernetSignals?accessToken=xyzabcxyz&signals=[{'Name': 'EVC_List03_StStyle_ST3', 'Value': 'LHD'}, 
{'Name': 'EVC_49_540_Avl_ST3', 'Value': 'TRUE'}, {'Name': 'Bckl_Sw_FP_Stat_ST3', 'Value': 'OK'}, {'Name': 'DrRLtch_FL_Stat_ST3', 'Value': 'CLS'}, {'Name': 'DrRLtch_FR_Stat_ST3', 'Value': 'CLS'}, {'Name': 'VehSpd_X_ST3', 'Value': '0Km/h'}]
########################
uc4_signal1_URI
http://localhost:9006/etfapi/v1/EthernetService/Ethernet/ChangeEthernetSignals?accessToken=xyzabcxyz&signals=[{'Name': 'EVC_List03_StStyle_ST3', 'Value': 'LHD'}, 
{'Name': 'EVC_List02_VehLine_ST3', 'Value': 'BR223'}, {'Name': 'EVC_List06_Country_ST3', 'Value': 'OTHER'}, {'Name': 'UI_TSSR_Pnl_Stat_ST3', 'Value': 'SR_CLOSED'}, {'Name': 'UI_TSSR_RB_Stat_ST3', 'Value': 'CLS'}, {'Name': 'DrRLtch_FL_Stat_ST3', 'Value': 'CLS'}, {'Name': 'DrRLtch_FR_Stat_ST3', 'Value': 'CLS'}, {'Name': 'ISw_Stat_ST3', 'Value': 'ON'}, {'Name': 'EVC_6F_413_Avl_ST3', 'Value': 'TRUE'}]
########################
uc5_signal1_URI
http://localhost:9006/etfapi/v1/EthernetService/Ethernet/ChangeEthernetSignal?accessToken=xyzabcxyz&signalName=EVC_List03_StStyle_ST3&signalValue=LHD
########################
uc6_signal1_URI
http://localhost:9006/etfapi/v1/EthernetService/Ethernet/ChangeEthernetSignals?accessToken=xyzabcxyz&signals=[{'Name': 'EVC_List03_StStyle_ST3', 'Value': 'LHD'}, 
{'Name': 'LgtSens_Night_ST3', 'Value': '1'}]
########################
uc7_signal1_URI
http://localhost:9006/etfapi/v1/EthernetService/Ethernet/ChangeEthernetSignals?accessToken=xyzabcxyz&signals=[{'Name': 'EVC_List03_StStyle_ST3', 'Value': 'LHD'}, 
{'Name': 'PT4_PTCoor_DrvPosn_Stat_ST3', 'Value': 'R'}, {'Name': 'VehDrvDir_Stat_ST3', 'Value': '2'}, {'Name': 'VehSpd_X_ST3', 'Value': '0'}, {'Name': 'RB_R_Stat_ST3', 'Value': 'RT_EXT'}, {'Name': 'ISw_Stat_ST3', 'Value': 'IGN_START'}, {'Name': 'EVC_49_540_Avl_ST3', 'Value': 'TRUE'}]
'''
