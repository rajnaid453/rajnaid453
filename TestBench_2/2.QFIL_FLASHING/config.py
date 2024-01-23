flashgui = r"C:\Tools\v7.33\bin"                                       
vcpu_file_path = r"C:\WorkSpace\Gen20X\builds\73\vcpu\output_release\bin\TRICORE_TC39XX_VCPU_FULL_IMAGE_Production.dnl"		
kds_file_path = r"C:\WorkSpace\Gen20X\builds\73\7513700051.KDS" 


startBaseURI = "http://localhost:9006/etfapi/v1"
triggeBaseURI = "http://localhost:9002/etfapi/v1"
accessToken = "xyzabcxyz"
ecuName = "CIVIC206"

activeComfort = ("Active_Comfort",
                 "FF,40,00,53,03,60,A0,3F,00,00,00,00,7A,34,55,2E")
VideoHandling = ("Video_Handling", "A0,60,00,00,00")
VehicleFunctions = ("Vehicle_Functions", "00,00,00,00,00,14,03,00,00,00,00,00,00,00,00,00,00,00,00,4A,00,00,00,00,00,66,00,00,00,50,1A,00,00,5A,05,02,04,00,40,00,00,00,00,00,00,00,00,00,00,04,00,00,00,00")


simulateSignal = triggeBaseURI + "/EthernetService/Ethernet/ChangeEthernetSignal?accessToken=" + \
    accessToken + "&signalName="
simulateSignals = triggeBaseURI + \
    "/EthernetService/Ethernet/ChangeEthernetSignals?accessToken=" + \
    accessToken + "&signals="


varientCodingGet = triggeBaseURI + "/DiagnosticsService/Ethernet/GetVariantCodingFromDomain?accessToken=" + \
    accessToken + "&ecuName=" + ecuName + "&domainIdentifier={0}"
varientCodingWrite = triggeBaseURI + "/DiagnosticsService/Ethernet/WriteVariantCodingFromDomain?accessToken=" + \
    accessToken + "&ecuName=" + ecuName + \
    "&domainIdentifier={0}&codingData={1}"
    

# ETFW START
etfStart = startBaseURI + "/Start?accessToken=" + accessToken
etfStartProfile = startBaseURI + "/Start/" + accessToken + \
    "?profileName=Gen20X_i2_OFN_Simulation"

# ETFW ONLINE
etfGoOnline = triggeBaseURI + "/GoOnline?accessToken=" + accessToken

# VEHICLE LINE SIGNAL SIMULATION
vehLine = simulateSignal + "EVC_List02_VehLine_ST3&signalValue=BR223"
vehStyle = simulateSignal + "EVC_List03_StStyle_ST3&signalValue=LHD"

# IGNITION
accessoryOn = triggeBaseURI + "/SwitchIgnition?accessToken=" + \
    accessToken + "&switchState=Accessory"
accessoryStart = triggeBaseURI + "/SwitchIgnition?accessToken=" + \
    accessToken + "&switchState=Start"
ignitionOn = triggeBaseURI + "/SwitchIgnition?accessToken=" + \
    accessToken + "&switchState=On"
ignitionOff = triggeBaseURI + "/SwitchIgnition?accessToken=" + \
    accessToken + "&switchState=Off"
ignitionLock = triggeBaseURI + "/SwitchIgnition?accessToken=" + \
    accessToken + "&switchState=Lock"
    
# VARIENT CODING GET
getActiveComfort = varientCodingGet.format("Active_Comfort")
getVideoHandling = varientCodingGet.format("Video_Handling")
getVehicleFunctions = varientCodingGet.format("Vehicle_Functions")

# VARIENT CODING PUT
writeActiveComfort = varientCodingWrite.format(
    activeComfort[0], activeComfort[1])
writeVideoHandling = varientCodingWrite.format(
    VideoHandling[0], VideoHandling[1])
writeVehicleFunctions = varientCodingWrite.format(
    VehicleFunctions[0], VehicleFunctions[1])