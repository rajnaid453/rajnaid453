##import MySQLdb
import pyodbc
class MySQLUtils:
    # def __init__(self, user='root', password='Ilovmom@1', host='localhost', database='database1'):
    #     # self.connection = MySQLdb.connect(user=user, password=password, host=host, database=database)
    def __init__(self):
        pass
    def saveData(self,row):
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=53.127.139.67;DATABASE=TestingTeam_DB;uid=TestTeamL;pwd=Gesture@2020;')
        cursor = connection.cursor()

        try:
            #print(type(row))
            query = """INSERT INTO  TestCase_Info_Gen2(  Tid,             
                                                    TestCaseId,
                                                    Module,                         
                                                    CarId,
                                                    RecordingId,     
                                                    SteeringWheel,
                                                    TrimParts,     
                                                    Interior,
                                                    TestPerformedBy,     
                                                    OccupiedSeats,
                                                    TestCaseDescription,     
                                                    ObjectId,
                                                    Evaluation,     
                                                    DATFile,
                                                    FalseTriggers,
                                                    Result,
                                                    Release_Version,
                                                    DriverId,
                                                    PassengerId,
                                                    TestExecutionComment,
                                                    OMS_Type,
                                                    TMX_Ticket
                                                    )
                                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

            


            
            recordTup = ( str(row.Tid),
                         str(row.TestCaseId),
                         str(row.Module),
                         str(row.CarId),
                         str(row.RecordingId),
                         str(row.Steeringwheel),
                         str(row.TrimParts),
                         str(row.Interior),
                         str(row.TestPerformedby),
                         str(row.OccupiedSeats),
                         str(row.TestcaseDescription),
                         str(row.ObjectId),
                         str(row.Evaluation),
                         str(row.DATfile),
                         str(row.FalseTriggers),
                         str(row.Result),
                         str(row.Release_Version),
                         str(int(row.DriverID)),
                         str(int(row.PassengerID)),
                         str(row.TestExecutionComment),
                         str(row.OMS_Type),
                         str(row.TMX_Ticket)
                         )
                        

            a = cursor.execute(query,recordTup)
            connection.commit()
            
            print("Saved Successflly ", a)
        except Exception as error:
            print(error)
        finally:
           cursor.close()
           connection.close()



##    def get_version_info(self):
##        try:
##            connection=pyodbc.connect('DRIVER={SQL Server};SERVER=53.88.131.214;DATABASE=TestingTeam_DB;uid=TestTeamL;pwd=Gesture@2020;')
##            
##
##            query='SELECT Release_Version FROM TestCase_Info;'
##            cursor = connection.cursor()
##            cursor.execute(query)
##            version_number=cursor.fetchone()
##            print(version_number)
##            return version_number
##        except Exception as e:
##            print(e)
##            return None
##
