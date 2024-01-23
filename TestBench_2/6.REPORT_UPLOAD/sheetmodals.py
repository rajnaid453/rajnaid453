class LandingSheet(object):
    def __init__(self, No, OMSUseCase, TotalUsecaseCount, UsecasePass, UsecaseFail, FalseTriggerTestcasesCount,
                 FalseTriggerPassCount, FalseTriggerFailcount, TotalTestcase, TotalPass, TotalFail):
        self.No = No
        self.OMSUseCase = OMSUseCase
        self.TotalUsecaseCount = TotalUsecaseCount
        self.UsecasePass = UsecasePass
        self.UsecaseFail = UsecaseFail
        self.FalseTriggerTestcasesCount = FalseTriggerTestcasesCount
        self.FalseTriggerPassCount = FalseTriggerPassCount
        self.FalseTriggerFailcount = FalseTriggerFailcount
        self.TotalTestcase = TotalTestcase
        self.TotalPass = TotalPass
        self.TotalFail = TotalFail

    @property
    def __str__(self):
        return ("Excel object:\n"
                "No = {0}\n"
                "OMSUseCase = {1}\n"
                "TotalUsecaseCount = {2}\n"
                "UsecasePass = {3}\n"
                "UsecaseFail = {4}\n"
                "FalseTriggerTestcasesCount = {5}\n"
                "FalseTrigger(PassCount) = {6}\n"
                "FalseTrigger(FailCount) = {7}\n"
                "TotalTestcase = {8}\n"
                "TotalPass = {9}\n"
                "TotalFail = {10}\n"
                .format(self.No, self.OMSUseCase,
                        self.TotalUsecaseCount,
                        self.UsecasePass,
                        self.UsecaseFail,
                        self.FalseTriggerTestcasesCount,
                        self.FalseTriggerPassCount,
                        self.FalseTriggerFailcount,
                        self.TotalTestcase,
                        self.TotalPass,
                        self.TotalFail))


class UseCaseModel(object):
    def __init__(self,TestCaseId,Module,CarId,RecordingId,Steeringwheel,TrimParts,Interior,TestPerformedby,OccupiedSeats,TestcaseDescription,ObjectId,Evaluation,DATfile,
                 FalseTriggers,Result,Tid,DriverID,PassengerID,
                 TestExecutionComment,Release_Version,OMS_Type,TMX_Ticket):
        
        self.TestCaseId = TestCaseId
        self.Module = Module
        self.CarId = CarId
        self.RecordingId = RecordingId
        self.Steeringwheel = Steeringwheel
        self.TrimParts = TrimParts
        self.Interior = Interior
        self.TestPerformedby = TestPerformedby
        self.OccupiedSeats = OccupiedSeats
        self.TestcaseDescription = TestcaseDescription
        self.ObjectId = ObjectId
        self.Evaluation = Evaluation
        self.DATfile = DATfile
        self.FalseTriggers = FalseTriggers
        self.Result = Result
        self.Tid=Tid
        self.DriverID = DriverID
        self.PassengerID=PassengerID
        self.TestExecutionComment=TestExecutionComment       
        self.Release_Version=Release_Version
        self.OMS_Type=OMS_Type
        self.TMX_Ticket=TMX_Ticket

##        print(TestCaseId,Module,CarId,RecordingId,Steeringwheel,TripParts,Interior,TestPerformedby,OccupiedSeats,TestcaseDescription,ObjectId,Evaluation,DATfile,Signal,StartTimestamp,EndTimestamp,FalseTriggers,PassPercentage,Result,Is_Usecase)


    def __str__(self):
        return "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(self.TestCaseId,self.Module,self.CarId,self.RecordingId,self.Steeringwheel,self.TrimParts,self.Interior,self.TestPerformedby,self.OccupiedSeats,
                                                        self.TestcaseDescription,self.ObjectId,self.Evaluation,self.DATfile,self.FalseTriggers,
                                                                     self.Result,self.Tid,self.DriverID,self.PassengerID,self.TestExecutionComment,self.Release_Version,self.OMS_Type,self.TMX_Ticket)                                                                   

