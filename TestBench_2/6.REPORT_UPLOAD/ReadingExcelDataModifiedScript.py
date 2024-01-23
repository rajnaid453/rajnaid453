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

dict = {'UC1':"Reading_Light_Front", 'UC2':"Unbuckled_child_seat", 'UC3':"Predictive_BSM_Warning", 'UC4':"Sunroof_&_Sunblind_Control", 'UC5':"Exterior_Mirror",
              'UC6':"Supporting_Search_Light", 'UC7':"Rear_Window_Sunblind_Support"}

def Logger(key,value):
    print("="*20)
    print(">",key)
    print(value)
    print("="*20)

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
    def Logger(self,key,value):
        print("="*20)
        print(">",key)
        print(value)
        print("="*20)

    def grid_landing_sheet(self, filename):
        wb = LoadExcelUtil(self.mainExcel).get_workbook_instance()
        sheet_landing = wb.sheets()[1]
        number_of_rows = sheet_landing.nrows
        number_of_columns = sheet_landing.ncols
        testcaseid_column = []
        
##        rows = []
        
        for row_number in range(4,number_of_rows):
            
            no = sheet_landing.cell(row_number, 1).value  # [row_number][1]
            # print(no)
            oms_use_case = sheet_landing.cell(row_number, 2).value
            total_use_case_count = sheet_landing.cell(row_number, 3).value
##            print("total_use_case_count",total_use_case_count)
            
##            Result_value = str(sheet_landing.cell(row_number, 7).value)
##            print(Result_value,type(Result_value))
##            if no != "" and type(Result_value) == str:
            if str(total_use_case_count) != "0.0":
                    print("total_use_case_count",total_use_case_count)
##                if (Result_value) in ["PASS","FAIL","NOT EXECUTED"]:
                    myName = dict[no]
                    print("myName",myName)
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



    def get_use_case_mode(self, row_number, sheet_reference,Release_Version,OMS_Type):

        # Is_Usecase=""
        # Module=""
        #
        # if sheet_reference.cell(row, 14).value == "START":
        #     Is_Usecase = 0
        # else:
        #     Is_Usecase = 1
        #
        # if sheet_reference.cell(row, 14).value == "START":
        #     if sheet_reference.cell(row, 13).value in ("TGC_D_HandRt_FctTrigger","TGC_D_HandLt_FctTrigger","TGC_P_HandRt_FctTrigger","TGC_P_HandLt_FctTrigger"):
        #         Module="UC4"
        #     elif sheet_reference.cell(row, 13).value in ("TGC_D_RdLgt_Md_Rq","TGC_P_RdLgt_Md_Rq"):
        #         Module="UC5"
        #     elif sheet_reference.cell(row, 13).value in ("TGC_TSSR_Rq","TGC_TSSR_RB_Rq","TGC_TSSR_RB_R_Rq"):
        #         Module="UC13"
        #     elif sheet_reference.cell(row, 13).value in ("TGC_D_SeatOccClass","TGC_P_SeatOccClass"):
        #         Module="F2"
        #     elif sheet_reference.cell(row, 13).value in ("TGC_D_HdInDrHndlArea","TGC_P_HdInDrHndlArea"):
        #         Module ="UC11"
        #     elif sheet_reference.cell(row, 13).value in ("TGC_RB_R_Ctrl_Rq"):
        #         Module ="UC8"
        #     elif sheet_reference.cell(row, 13).value in ("TGC_D_HandRt_Stat_ROI","TGC_D_HandLt_Stat_ROI","TGC_P_HandRt_Stat_ROI","TGC_P_HandLt_Stat_ROI"):
        #         Module ="F1"
        #     elif sheet_reference.cell(row, 13).value in ("TGC_D_LookAtROI"):
        #         Module ="UC7"
        #     else:
        #         Module = sheet_reference.cell(row, 1).value
        # else:
        #     Module = sheet_reference.cell(row, 1).value

        # Module = sheet_reference.cell(row, 1)
            
        use_case_model = UseCaseModel(
            TestCaseId=sheet_reference.cell(row, 0).value,#>>>>>>>>>>Done
            Module=sheet_reference.cell(row, 1).value,#>>>>>>>>>>Done
            CarId=sheet_reference.cell(row, 2).value,#>>>>>>>>>>Done
            RecordingId=(sheet_reference.cell(row, 3).value),#>>>>>>>>>>Done
            Steeringwheel=sheet_reference.cell(row, 4).value,#>>>>>>>>>>Done
            # TripParts=sheet_reference.cell(row, 5).value,
            TrimParts=sheet_reference.cell(row, 5).value,#>>>>>>>>>>Done
            Interior=sheet_reference.cell(row, 6).value,#>>>>>>>>>>Done
            TestPerformedby=sheet_reference.cell(row, 7).value,#>>>>>>>>>>Done
            OccupiedSeats=sheet_reference.cell(row, 8).value,#>>>>>>>>>>Done
            TestcaseDescription=sheet_reference.cell(row, 9).value,#>>>>>>>>>>Done
            ObjectId=sheet_reference.cell(row, 10).value,#>>>>>>>>>>Done
            Evaluation=sheet_reference.cell(row, 11).value,#>>>>>>>>>>Done
            DATfile=sheet_reference.cell(row, 12).value,#>>>>>>>>>>Done
            # Signal= sheet_reference.cell(row, 13).value,
            # StartTimestamp = sheet_reference.cell(row, 14).value,
            # EndTimestamp = sheet_reference.cell(row, 15).value,
            FalseTriggers=sheet_reference.cell(row, 13).value,#>>>>>>>>>>Done
            
            # PassPercentage=sheet_reference.cell(row, 17).value,
            Tid=sheet_reference.cell(row, 14).value,        #>>>>>>>>>>Done
            DriverID=sheet_reference.cell(row, 15).value,#>>>>>>>>>>Done
            PassengerID=sheet_reference.cell(row, 16).value,#>>>>>>>>>>Done
            TestExecutionComment=sheet_reference.cell(row, 17).value,#>>>>>>>>>>Done
            # TMX_Ticket =sheet_reference.cell(row, 18).value,
            TMX_Ticket ="Test",

            Result=sheet_reference.cell(row, 18).value,#>>>>>>>>>>Done
            Release_Version=Release_Version,#>>>>>>>>>>Done
            OMS_Type=OMS_Type #>>>>>>>>>>Done
            )
            
        return use_case_model


            
    
    @staticmethod
    def get_all_files(fpath):
        listtpathfiles=[]
        for path in os.listdir(fpath):
            full_path = os.path.join(fpath, path)
            if os.path.isfile(full_path):
                #print( full_path)
                listtpathfiles.append(full_path)
        return  listtpathfiles




if __name__ == '__main__':

        basepath =r"C:\TESTFARM_AUTOMATION\Report_output\copy"
        utils = MySQLUtils()
        files = ExcelReaderEntry.get_all_files(basepath)

        
        print("files",files)
        for p in files:
            instance = ExcelReaderEntry(p)
            version= open_workbook(p)
            sheet_names = version.sheet_names()
            Version_Info=version.sheet_by_name(sheet_names[0])
            Release_Version=Version_Info.cell(4,1).value
            OMS_Type=Version_Info.cell(2,1).value
            print(Release_Version)
            print(OMS_Type)
            
            object = []
            testcaseid_column =instance.grid_landing_sheet(p)
            # print(testcaseid_column)
        
            
            for i in testcaseid_column:
##                 sheet=instance.get_use_case_details(i)
                 sheet=version.sheet_by_name(i)
                 print(sheet)
                 for row in range(2,sheet.nrows):
##                    print("inside for")
                    object.append(instance.get_use_case_mode(row,sheet,Release_Version,OMS_Type))

            for row in object:
##                pass
                utils.saveData(row)
                # print(row)




##            for o in object:
##                row=o.__str__()
##                print(row)




#TO_DO
# Keep Test Case Name and Sheet Name same 
# Modify required columns in C:\WorkSpace\Gen20X\artifactory_checkout\TestBench_2\6.REPORT_UPLOAD\ReadingExcelDataModifiedScript.py and C:\WorkSpace\Gen20X\artifactory_checkout\TestBench_2\6.REPORT_UPLOAD\SQLdatabase_Modified.py
# Confirm the query part for non unique TID