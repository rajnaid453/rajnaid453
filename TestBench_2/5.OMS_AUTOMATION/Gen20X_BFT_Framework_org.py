import xlsxwriter
import os
import re
import threading
import time
import requests
import pandas as pd
import numpy as np
import serial
import REST_URI as URI
from collections import OrderedDict
from datetime import datetime
from time import strftime
from serial.tools import list_ports

doCoding = False
executionLogs = []

UC_dict = {'UC1': 'Readling Light Front',
           'UC2': 'Unbuckled child seat',
           'UC3': 'Predictive BSM Warning',
           'UC4': 'Sunroof Sunblind Front',
           'UC5': 'Exterior Mirror',
           'UC6': 'Search Light Front',
           'UC7': 'Rear Window Rollerblind'
           }

signal_name = {
            'UC1_P': 'st_vechif1.Reading_LightRq_FR',
            'UC1_D': 'st_vechif1.Reading_LightRq_FL',
            'UC3_P': 'st_someip.Out_P_HdInDrHndlArea',
            'UC3_D': 'st_someip.Out_D_HdInDrHndlArea',
            'UC4_SR': 'st_vechif1.SunRoofPosition_Rq',
            'UC4_SB': 'st_vechif1.SunblindPosition_BLIND_ROOF',
            'UC5': 'st_someip.Out_ExtMirrorDriverFocus',
            'UC6': 'st_vechif1.Reading_LightRq_FR',
            'UC7': 'st_vechif1.SunblindPosition_BLIND_BACKLITE'
            }

hand_dict = {'right hand': 'R', 'left hand': 'L'}
gestureby_dict = {'Driver': 'D', 'Passenger': 'P'}


reportData_dict = OrderedDict({'TestSummary': {'Tester': 'TestingtTeam', 'Version No': 'E43.1',
                                               'Variant Coding': '206',
                                               'ECU Serial No': '#1', 'OMS Type': 'Gen20X_Front'},
                                'SummarySheetURL': {'UseCase_Summary': 'UseCase_Summary'},
                                'UseCaseList': ['UC1', 'UC2', 'UC3', 'UC4', 'UC5', 'UC6', 'UC7',],
                                
                                'SummarySheetUseCaseURL_key': [
                                   'Reading_Light_Front',
                                   'Unbuckled_child_seat',
                                   'Predictive_BSM_Warning',
                                   'Sunroof_&_Sunblind_Control',
                                   'Exterior_Mirror',
                                   'Supporting_Search_Light',
                                   'Rear_Window_Sunblind_Support'
],
'SummarySheetUseCaseURL_value': [
                                   'Reading_Light_Front',
                                   'Unbuckled_child_seat',
                                   'Predictive_BSM_Warning',
                                   'Sunroof_&_Sunblind_Control',
                                   'Exterior_Mirror',
                                   'Supporting_Search_Light',
                                   'Rear_Window_Sunblind_Support'
],
    'OMSUseCase': {
                                   'UC1': 'Reading_Light_Front',
                                   'UC2': 'Unbuckled_child_seat',
                                   'UC3': 'Predictive_BSM_Warning',
                                   'UC4': 'Sunroof_&_Sunblind_Control',
                                   'UC5': 'Exterior_Mirror',
                                   'UC6': 'Supporting_Search_Light',
                                   'UC7': 'Rear_Window_Sunblind_Support'
},
    'UseCaseSheetHeader': ['Test ID', 'Module', 'Car ID', 'Recording ID', 'Steering Wheel',
                           'Trim parts', 'Interior', 'Test Performed By', 'Occupied Seats',
                           'Test Description', 'Object Id', 'Evaluation', 'DAT File',
                           'FalseTriggers', 'Tid', 'Driver ID', 'Passenger ID',
                           'Test Execution Comment', 'Result', 'TMX-Ticket'],
    'resultMatrix': {'PASS': (1, 0), 'FAIL': (0, 1)}})


def writeLog(operation, log=""):
    current_time = datetime.now().strftime("%H_%M_%S")
    message = current_time + ' : ' + str(operation) + ' >> ' + str(log)
    executionLogs.append(message)
    print(message)


def load_data_from_configfile():
    """
    This method fetches the data from config.txt and return it in list format.
    """
    loadval = []
    f = open('config.txt', 'r')
    for line in f:
        # Read data from config.txt
        loadval.append((line.partition('#')[0]).rstrip())
    return loadval

loadval = load_data_from_configfile()
#print('loadval',loadval)
csv_folder = loadval[0].replace("\n", "")

referance_file = loadval[1].replace("\n", "")
imageextracter = loadval[2].replace("\n", "")
excelresult = pd.read_excel(referance_file)
datfilelist = os.listdir(csv_folder)

new_dat_loc = loadval[3].replace("\n", "")

print("csv_folder = ", csv_folder)

def triggerETFW(state, URI):
    writeLog("state " + state)
    res = requests.get(URI)
    writeLog(res.status_code, res.json())
    print(res)

################
# ETFW Ignition #
################
def triggerIgnitionOn():
    writeLog("Started Ignition Procedure")
    ignitionProcedure = [URI.vehLine, URI.vehStyle,
                         URI.accessoryOn, URI.accessoryStart, URI.ignitionOn]
    # ignition = [URI.etfStop]
    for ignition in ignitionProcedure:
        res = requests.get(ignition)
        writeLog(res.status_code, res.json())
        time.sleep(5)

###################
# Image Extractor #
###################
def image_extractor(imageextracter, dat_folder, referance_file, referencefile_data):
    imgextractor_path = os.path.join(imageextracter, "ImageExtractor.exe")
    dat_folder = csv_folder
    # dat_folder = r"C:\\testteam_IVTS"
    print("dat_folder.....", dat_folder)
    dat_files = os.listdir(dat_folder)
    reference_data = referencefile_data["Recording ID"].tolist()
    recording_list = list(map(str, reference_data))
    filepath_dict = {}

    for dat in dat_files:
        if dat.endswith(".dat"):
            datid = re.search(r'\d{10}', dat).group()
            if datid in recording_list:
                ind = recording_list.index(datid)
                if str(referencefile_data.at[ind, 'CSV Enable']) == "1":
                    dat_filepath = os.path.join(dat_folder, dat)
                    csv_path = os.path.join(dat_folder, datid, "CSVFolder")


                    referencefile_data['Filepath'] = referencefile_data['Filepath'].astype(
                        str)
                    filepath_dict[datid] = csv_path
                    referencefile_data.at[ind, 'Filepath'] = csv_path
                    imgextractor_cmd = imgextractor_path + " -i " + dat_filepath + " -o " + dat_folder
                    res = os.system(imgextractor_cmd)
                    if not res:
                        continue
                    else:
                       print ("Extracting {}... with return code {}...".format(dat_filepath, res))
    referencefile_data.to_excel(referance_file, index=False)
    return filepath_dict


def reference_file_data():

    referance_dict = {}
    for i in range(excelresult.shape[0]):
        recording_id = str(excelresult['Recording ID'].loc[i])
        referance_dict[recording_id] = {}
        referance_dict[recording_id]["filepath"] = str(excelresult['Filepath'].loc[i])
        referance_dict[recording_id]["testid"] = str(excelresult['Test ID'].loc[i])
        referance_dict[recording_id]["module"] = str(excelresult['Module'].loc[i])
        referance_dict[recording_id]["carid"] = str(excelresult['Car ID'].loc[i])
        referance_dict[recording_id]["signal"] = str(excelresult['Signal'].loc[i])
        referance_dict[recording_id]["value"] = int(excelresult['Value'].loc[i])
        referance_dict[recording_id]["starttime"] = str(excelresult['Start Time'].loc[i])
        referance_dict[recording_id]["endtime"] = str(excelresult['End Time'].loc[i])
        referance_dict[recording_id]["datfile"] = str(excelresult['DAT File'].loc[i])
        referance_dict[recording_id]["csvenable"] = str(excelresult['CSV Enable'].loc[i])
        if referance_dict[recording_id]["csvenable"] != "1":
            del referance_dict[recording_id]
    filepath_dict = image_extractor(imageextracter, new_dat_loc, referance_file, excelresult)
    for dat_id in filepath_dict.keys():
        referance_dict[dat_id]["filepath"] = filepath_dict[dat_id]
        print("""referance_dict[dat_id]["filepath"]------------->""",referance_dict[dat_id]["filepath"])
    return referance_dict


modlue_list = ["UC1", "UC2", "UC3", "UC4", "UC5", "UC6", "UC7"]


def comparison():
    data_dict = reference_file_data()
    comparison_dict = {}
    result_dict = {}
    for dat in data_dict.keys():
        if os.path.exists(data_dict[dat]['filepath']):
            # if data_dict[dat]['module'] == "UC5":
            if data_dict[dat]['module'] in modlue_list:
                csv_files = os.listdir(data_dict[dat]['filepath'])
                for file in csv_files:
                    if file.endswith("OMSPayload_OMSApp.csv"):
                        comparison_dict[dat] = []
                        signal = data_dict[dat]['signal']
                        df = pd.read_csv(os.path.join(
                            data_dict[dat]['filepath'], file))
                        value_list = df[signal].tolist()
                        comparison_dict[dat] = list(map(str, value_list))
            else:
                print("Implementation for {} is pending".format(
                    data_dict[dat]['module']))
    comparison_result = {}
    # UC2 UI
    # UC5 Ext
    # UC7 SR
    positiveValues = {'UC1': [1, 2], 'UC2': [1], 'UC3': [1, 3], 'UC4': [1, 2], 'UC5': [1, 2], 'UC6': [1, 2], 'UC7': [1, 4]}
    for dat in comparison_dict.keys():
        if str(data_dict[dat]["value"]) == "0":

            if len(comparison_dict[dat]) == comparison_dict[dat].count("0"):
                result_dict[dat] = ("Pass", data_dict[dat]["value"])
                comparison_result[data_dict[dat]["testid"]] = "PASS"
            else:
                for val in positiveValues[data_dict[dat]['module']]:
                    if comparison_dict[dat].count(str(val)) == 0:
                        continue
                    else:
                        result_dict[dat] = ("Fail", "1")
                        comparison_result[data_dict[dat]["testid"]] = "FAIL"
                        break
                result_dict[dat] = ("Pass", data_dict[dat]["value"])
                comparison_result[data_dict[dat]["testid"]] = "PASS"
        else:
            if str(data_dict[dat]["value"]) in comparison_dict[dat]:
                result_dict[dat] = ("Pass", data_dict[dat]["value"])
                comparison_result[data_dict[dat]["testid"]] = "PASS"
            else:
                result_dict[dat] = ("Fail", "0")
                comparison_result[data_dict[dat]["testid"]] = "FAIL"
    return comparison_result


def playing_dat():

    recording_data = excelresult["Recording ID"].tolist()
    recording_list = list(map(str, recording_data))
    print(recording_list)

    # Modify command
    # inputfilename = r"C:\Gen20_Automation\Dat_Files\MBRDI_223_1227_Carline\OMS_Gen20x_reference_223_original.xlsx"
    # dirname = r"C:\Gen20_Automation\Dat_Files\MBRDI_223_1227_Carline"
   
    cmd1 = "adtf_devenv.exe -script" + "=" + "C:\Gen20_Automation\Gen20X+ETFW_API_v2\Demo_Gen_old.py" + \
          "" + " -argv" + "=" + '"' + csv_folder + " " + referance_file + '"'+" -quit"
    
    # cmd1 = "adtf_devenv.exe -script" + "=" + "C:\Gen20_Automation\Automation_BFT\Demo_Gen1.py" + \
    #      "" + " argv" + -"=" + '"' + csv_folder + " " + referance_file + " "+new_dat_loc+ '"' +" -quit"

    print("ADTF_Command = ", cmd1)
    home_dir = os.getcwd()
    print("Home Directory = ", home_dir)
    os.chdir("C:\\ITM\\2.13.2\\bin")
    print(os.getcwd())
    t = threading.Timer(1800.0, ADTFHang)
    t.start()
    os.system(cmd1)
    os.chdir(home_dir)


def ADTFHang():
    os.system("TASKKILL /F /IM adtf_devenv.exe")


# playing_dat()
# comparison_result = comparison()

####################
# REPORT GENERATION
####################
def generateReport(testResult):
    current_time = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    reportExcelName = "OMS_Testing_Report{}.xlsx".format(current_time)

    print("Report Generation Started.....")
    print("Report Name:", reportExcelName)

    referenceFileData = excelresult

    executedUseCases = referenceFileData['Module'].unique()
    totalUseCase = [0 for i in range(
        len(reportData_dict['UseCaseList']))]
    totalSuccess = [0 for i in range(
        len(reportData_dict['UseCaseList']))]
    toatlFailure = [0 for i in range(
        len(reportData_dict['UseCaseList']))]
    failurePercent = [0 for i in range(
        len(reportData_dict['UseCaseList']))]

    workbook = xlsxwriter.Workbook(reportExcelName)

    # Header Row
    cell_format1 = workbook.add_format()
    cell_format1.set_align('center')
    cell_format1.set_bold(12)
    cell_format1.set_bg_color('gray')

    # Bold Cells
    cell_format2 = workbook.add_format()
    cell_format2.set_align('center')
    cell_format2.set_bold(12)

    # Normal Cell Data
    cell_format3 = workbook.add_format()
    cell_format3.set_align('center')

    # Normal Cell Data with word wrap
    cell_format4 = workbook.add_format()
    cell_format4.set_align('center')
    cell_format4.set_text_wrap()

    # Hyperlinks
    cell_format5 = workbook.add_format()
    cell_format5.set_align('center')
    cell_format5.set_bold(18)
    cell_format5.set_underline()
    cell_format5.set_font_color('Orange')
    cell_format5.set_text_wrap()

    # Result Pass
    cell_format6 = workbook.add_format()
    cell_format6.set_align('center')
    cell_format6.set_bold(12)
    cell_format6.set_bg_color('green')

    # Result Fail
    cell_format7 = workbook.add_format()
    cell_format7.set_align('center')
    cell_format7.set_bold(12)
    cell_format7.set_bg_color('red')

    def writeData(sheet, row, col, cellData, writeType='vertical', valueFormat=cell_format3, keyFormat=cell_format2):
        '''
        writeType can be vertical or v , horizonal or h
        '''
        writeType = writeType.lower()
        if type(cellData) == list:
            for data in cellData:
                sheet.write(row, col, data, valueFormat)
                if writeType == 'vertical' or writeType == 'v':
                    col += 1
                elif writeType == 'horizontal' or writeType == 'h':
                    row += 1
        elif type(cellData) in [OrderedDict, dict]:
            for k, v in cellData.items():
                sheet.write(row, col, k, keyFormat)
                sheet.write(row, col + 1, v, valueFormat)
                row += 1
        else:
            sheet.write(row, col, cellData, valueFormat)

    def writeURL(sheet, row, col, cellData, writeType='vertical', valueFormat=cell_format5):
        writeType = writeType.lower()
        if type(cellData) in [OrderedDict, dict]:
            for link, data in cellData.items():
                url = 'internal:' + link + '!A1'
                sheet.write_url(row, col, url, string=data,
                                cell_format=valueFormat)
                if writeType == 'vertical' or writeType == 'v':
                    col += 1
                elif writeType == 'horizontal' or writeType == 'h':
                    row += 1

    def calculateStats(uc, rMat):

        testPass, testFail = rMat
        total = testPass + testFail
        totalUseCase[reportData_dict['UseCaseList'].index(uc)] = total
        totalSuccess[reportData_dict['UseCaseList'].index(
            uc)] = testPass
        toatlFailure[reportData_dict['UseCaseList'].index(
            uc)] = testFail
        if total != 0:
            failurePercent[reportData_dict['UseCaseList'].index(uc)] = (
                round(((float(testFail) / total) * 100), 2))
        else:
            failurePercent[reportData_dict['UseCaseList'].index(
                uc)] = 0

    #################################
    # Tester Information
    #################################
    worksheet1 = workbook.add_worksheet("Tester Information")
    worksheet1.set_column('A:A', 25)
    worksheet1.set_column('B:B', 50)

    writeURL(worksheet1, 0, 0, {"UseCase_Summary": "TestSummary"})
    writeData(worksheet1, 2, 0, reportData_dict['TestSummary'])
    #################################
    # UseCase_Summary
    #################################

    worksheet2 = workbook.add_worksheet("UseCase_Summary")
    worksheet2.set_column('B:B', 15)
    worksheet2.set_column('C:C', 36)
    worksheet2.set_column('D:O', 15)

    worksheet2.write(
        1, 3, "OMS Test Summary Report", cell_format2)

    sheetHeader2 = ['No', 'OMS UseCase', 'TC',
                    'P(TP+TN)', 'F(FP+FN)', 'Fail %']
    writeData(worksheet2, 3, 1, sheetHeader2, valueFormat=cell_format1)

    writeData(worksheet2, 4, 1,
              reportData_dict["UseCaseList"], 'horizontal', cell_format4)

    sheet2Row = 4
    for (k, v) in zip(reportData_dict["SummarySheetUseCaseURL_key"], reportData_dict["SummarySheetUseCaseURL_value"]):
        # for k, v in reportData_dict["SummarySheetUseCaseURL"].items():
        if k in list([reportData_dict["OMSUseCase"][i] for i in executedUseCases]):
            writeURL(worksheet2, sheet2Row, 2, {k: v})
        else:
            writeData(worksheet2, sheet2Row, 2, v)
        sheet2Row += 1

    #################################
    # Logic to map df with result and formatting
    #################################
    compResult = testResult
    resultDataFrame = pd.DataFrame(
        compResult.items(), columns=['Test ID', 'Result'])
    completeResData = pd.merge(
        referenceFileData, resultDataFrame, how='outer', on='Test ID')
    completeResData = completeResData.replace(
        np.nan, 'Information Not Available')

    rearrangedData = pd.DataFrame()
    for col in reportData_dict["UseCaseSheetHeader"]:
        if col in completeResData.columns:
            rearrangedData[col] = completeResData[col]
        else:
            rearrangedData[col] = 'Information Not Available'

    #################################
    # UseCase Sheet Creations
    #################################

    groupedData = rearrangedData.groupby(['Module'])

    for ucID, ucText in reportData_dict["OMSUseCase"].items():
        if ucID in executedUseCases:
            resultCount = (0, 0)
            useCaseSheet = workbook.add_worksheet(ucText)
            useCaseSheet.set_column('A:Z', 18)
            writeURL(useCaseSheet, 0, 0, reportData_dict["SummarySheetURL"])
            writeData(useCaseSheet, 1, 0,
                      reportData_dict["UseCaseSheetHeader"], 'vertical', cell_format1)
            usecaseDataFrame = groupedData.get_group(ucID)
            usecaseDataFrame = usecaseDataFrame.reset_index()
            for index, row in usecaseDataFrame.iterrows():

                if row['Test ID'] == 'Information Not Available':
                    print("Test ID Information Not Available for the below test")
                    print(row)
                    continue

                if row["Result"] in ['PASS', 'FAIL']:
                    testPass, testFail = reportData_dict["resultMatrix"][row["Result"]]
                    resultCount = tuple(
                        map(sum, zip(resultCount, (testPass, testFail))))
                else:
                    print("{} has no Test Result".format(row["Test ID"]))
                    continue

                if row['Result'] == 'PASS':
                    resultColour = cell_format6
                # elif row['Result'] == 'FAIL':
                else:
                    resultColour = cell_format7

                ucRowIndex = index + 2
                rowData = list([row[col]
                                for col in reportData_dict["UseCaseSheetHeader"][1:-1]])
                writeURL(useCaseSheet, ucRowIndex, 0, {
                    row['Test ID']: row['Test ID']})
                writeData(useCaseSheet, ucRowIndex, 1,
                          rowData, 'vertical', cell_format4)
                writeData(useCaseSheet, ucRowIndex, len(
                    reportData_dict["UseCaseSheetHeader"]) - 2, row['Result'], 'vertical', resultColour)

                testSheet = workbook.add_worksheet(row['Test ID'])
                writeURL(testSheet, 0, 0, {ucText: ucText})
                testSheet.set_column('A:Z', 18)

                writeData(testSheet, 1, 0,
                          reportData_dict["UseCaseSheetHeader"], 'vertical', cell_format1)
                writeURL(testSheet, 2, 0, {row['Test ID']: row['Test ID']})
                writeData(testSheet, 2, 1, rowData, 'vertical', cell_format4)
                writeData(testSheet, 2, len(
                    reportData_dict["UseCaseSheetHeader"]) - 2, row['Result'], 'vertical', resultColour)

        else:
            resultCount = (0, 0)

        calculateStats(ucID, resultCount)

    #################################
    # UseCase_Summary Update
    #################################

    writeData(worksheet2, 4, 3, totalUseCase, 'horizontal', cell_format4)
    writeData(worksheet2, 4, 4, totalSuccess, 'horizontal', cell_format4)
    writeData(worksheet2, 4, 5, toatlFailure, 'horizontal', cell_format4)
    writeData(worksheet2, 4, 6, failurePercent, 'horizontal', cell_format4)
    workbook.close()


triggerETFW("ET Framework", URI.etfStart)
triggerETFW("ET Online", URI.etfGoOnline)
triggerIgnitionOn()
# if doCoding:
#    vcCoding()
playing_dat()
comparison_result = comparison()
generateReport(comparison_result)
