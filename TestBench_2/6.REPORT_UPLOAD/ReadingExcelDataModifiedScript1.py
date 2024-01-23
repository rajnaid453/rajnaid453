import pathlib
##import ExcelLoader
##import sheetmodals
##import SQLdatabase_Modified
from sheetmodals import UseCaseModel
from ExcelLoader import LoadExcelUtil
from SQLdatabase_Modified import MySQLUtils
import os, fnmatch
from xlrd import open_workbook

## For MIN ##

# dict = {'OMS_UC1 & OMS_UC2 &OMS_UC3': "OMS_UC1_UC2_UC3", 'OMS_UC2': "OMS_UC2_Reactive_Home_Screen",
#         'OMS_UC3': "OMS_UC3_Dist_Seat_Settings", 'OMS_UC4': "OMS_UC4_Favorite_Pose",
#         'OMS_UC5': "OMS_UC5_Reading_Light", 'OMS_UC6': "OMS_UC6_Search_Light",
#         'OMS_UC7': "OMS_UC7_Ext_Mirror_Preselect", 'OMS_UC8': "OMS_UC8_Rear_Window_Sunblind",
#         'OMS_UC9': "OMS_UC9_E_Call_NoOfPassengers", 'OMS_UC10': "OMS_UC10_UnBuckled_ChildSeat",
#         'OMS_UC11': "OMS_UC11_BSM_Warning", 'OMS_UC12': "OMS_UC12_Seat_PreAdjusmnt",
#         'OMS_UC13': "OMS_UC13_SunRoof_SunBlind_Ctrl", 'OMS_F1': "OMS_F1_Localization",
#         'OMS_F2': "OMS_F2_Occupancy_Detectn"}


# For MAx ##

dict = {'OMS_MAX_UC1':'OMS_MAX_UC1', 'OMS_MAX_UC2':'OMS_MAX_UC2','OMS_MAX_UC3':'OMS_MAX_UC3',
       'OMS_MAX_UC4':'OMS_MAX_UC4','OMS_MAX_UC5':'OMS_MAX_UC5','OMS_MAX_UC6':'OMS_MAX_UC6',
             'OMS_MAX_UC7':'OMS_MAX_UC7','OMS_MAX_UC8':'OMS_MAX_UC8','OMS_MAX_UC9':'OMS_MAX_UC9' }


class ExcelReaderEntry:
    def __init__(self, mainExcel):
        self.mainExcel = mainExcel

    ##    def get_use_case_details(self, sheet_ref):
    ##        wb = LoadExcelUtil(self.mainExcel).get_workbook_instance()
    ##        sheet_names = wb.sheet_names()
    ##        ctr = 0
    ##        for sheet_name in sheet_names:
    ##            if sheet_name == sheet_ref:
    ##                return wb.sheets()[ctr]
    ##            ctr = ctr + 1

    def grid_landing_sheet(self, filename):
        wb = LoadExcelUtil(self.mainExcel).get_workbook_instance()
        sheet_landing = wb.sheets()[1]
        number_of_rows = sheet_landing.nrows
        number_of_columns = sheet_landing.ncols
        testcaseid_column = []

        ##        rows = []

        for row_number in range(7, number_of_rows):

            no = sheet_landing.cell(row_number, 1).value  # [row_number][1]
            print(no)
            oms_use_case = sheet_landing.cell(row_number, 2).value
            total_use_case_count = sheet_landing.cell(row_number, 3).value
            ##            print("total_use_case_count",total_use_case_count)

            ##            Result_value = str(sheet_landing.cell(row_number, 7).value)
            ##            print(Result_value,type(Result_value))
            ##            if no != "" and type(Result_value) == str:
            if (total_use_case_count) != "":
                print("total_use_case_count", total_use_case_count)
                ##                if (Result_value) in ["PASS","FAIL","NOT EXECUTED"]:
                myName = dict[no]
                print("myName", myName)
                sheetNames = wb.sheet_names()

                for shName in sheetNames:
                    if shName == myName:

                        lsheet = wb.sheet_by_name(myName)

                        number_of_rowsl = lsheet.nrows
                        number_of_columnsl = lsheet.ncols

                        for rowl in range(2, number_of_rowsl):
                            localCol = lsheet.cell(rowl, 0).value
                            testcaseid_column.append(localCol)

        return (testcaseid_column)

    def get_use_case_mode(self, row_number, sheet_reference, Release_Version, OMS_Type):
        Is_Usecase = ""
        Module = ""

        if sheet_reference.cell(row, 14).value == "START":
            Is_Usecase = 0
        else:
            Is_Usecase = 1

        if sheet_reference.cell(row, 14).value == "START":
            if sheet_reference.cell(row, 13).value in (
            "TGC_D_HandRt_FctTrigger", "TGC_D_HandLt_FctTrigger", "TGC_P_HandRt_FctTrigger", "TGC_P_HandLt_FctTrigger"):
                Module = "UC4"
            elif sheet_reference.cell(row, 13).value in ("TGC_D_RdLgt_Md_Rq", "TGC_P_RdLgt_Md_Rq"):
                Module = "UC5"
            elif sheet_reference.cell(row, 13).value in ("TGC_TSSR_Rq", "TGC_TSSR_RB_Rq", "TGC_TSSR_RB_R_Rq"):
                Module = "UC13"
            elif sheet_reference.cell(row, 13).value in ("TGC_D_SeatOccClass", "TGC_P_SeatOccClass"):
                Module = "F2"
            elif sheet_reference.cell(row, 13).value in ("TGC_D_HdInDrHndlArea", "TGC_P_HdInDrHndlArea"):
                Module = "UC11"
            elif sheet_reference.cell(row, 13).value in ("TGC_RB_R_Ctrl_Rq"):
                Module = "UC8"
            elif sheet_reference.cell(row, 13).value in (
            "TGC_D_HandRt_Stat_ROI", "TGC_D_HandLt_Stat_ROI", "TGC_P_HandRt_Stat_ROI", "TGC_P_HandLt_Stat_ROI"):
                Module = "F1"
            elif sheet_reference.cell(row, 13).value in ("TGC_D_LookAtROI"):
                Module = "UC7"
            else:
                Module = sheet_reference.cell(row, 1).value
        else:
            Module = sheet_reference.cell(row, 1).value

        use_case_model = UseCaseModel(
            TestCaseId=sheet_reference.cell(row, 0).value,
            ##            Module=sheet_reference.cell(row, 1).value,
            Module=Module,
            CarId=sheet_reference.cell(row, 2).value,
            RecordingId=(sheet_reference.cell(row, 3).value),
            Steeringwheel=sheet_reference.cell(row, 4).value,
            TripParts=sheet_reference.cell(row, 5).value,
            Interior=sheet_reference.cell(row, 6).value,
            TestPerformedby=sheet_reference.cell(row, 7).value,
            OccupiedSeats=sheet_reference.cell(row, 8).value,
            TestcaseDescription=sheet_reference.cell(row, 9).value,
            ObjectId=sheet_reference.cell(row, 10).value,
            Evaluation=sheet_reference.cell(row, 11).value,
            DATfile=sheet_reference.cell(row, 12).value,
            Signal=sheet_reference.cell(row, 13).value,
            StartTimestamp=sheet_reference.cell(row, 14).value,
            EndTimestamp=sheet_reference.cell(row, 15).value,
            FalseTriggers=sheet_reference.cell(row, 16).value,
            PassPercentage=sheet_reference.cell(row, 17).value,
            Result=sheet_reference.cell(row, 18).value,
            Tid=sheet_reference.cell(row, 19).value,
            DriverID=sheet_reference.cell(row, 20).value,
            PassengerID=sheet_reference.cell(row, 21).value,
            TestExecutionComment=sheet_reference.cell(row, 22).value,
            Release_Version=Release_Version,
            OMS_Type=OMS_Type,
            Is_Usecase=Is_Usecase
        )

        return use_case_model

    @staticmethod
    def get_all_files(fpath):
        listtpathfiles = []
        for path in os.listdir(fpath):
            full_path = os.path.join(fpath, path)
            if os.path.isfile(full_path):
                # print( full_path)
                listtpathfiles.append(full_path)
        return listtpathfiles


if __name__ == '__main__':

    basepath = r"C:\TESTFARM_AUTOMATION\Report_output\copy"
    utils = MySQLUtils()
    files = ExcelReaderEntry.get_all_files(basepath)

    print("files", files)
    for p in files:

        instance = ExcelReaderEntry(p)
        version = open_workbook(p)
        sheet_names = version.sheet_names()
        Version_Info = version.sheet_by_name(sheet_names[0])
        Release_Version = Version_Info.cell(4, 2).value
        OMS_Type = Version_Info.cell(7, 2).value
        print(Release_Version)
        print(OMS_Type)

        object = []
        testcaseid_column = instance.grid_landing_sheet(p)
        print(testcaseid_column)

        for i in testcaseid_column:
            ##                 sheet=instance.get_use_case_details(i)
            sheet = version.sheet_by_name(i)
            print(sheet)
            for row in range(2, sheet.nrows):
                ##                    print("inside for")
                object.append(instance.get_use_case_mode(row, sheet, Release_Version, OMS_Type))

        for row in object:
            ##                pass
            # utils.saveData(row)
            print(rows)

##            for o in object:
##                row=o.__str__()
##                print(row)
