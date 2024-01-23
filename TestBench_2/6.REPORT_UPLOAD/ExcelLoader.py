from xlrd import open_workbook


class LoadExcelUtil:
    def __init__(self, filename):
        self.wb = open_workbook(filename)

    def get_workbook_instance(self):
        return self.wb
