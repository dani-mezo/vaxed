import logging
import random

from message import fun


class Task2:
    def __init__(self, excel):
        self.excel = excel
        self.task_counter = 0
        self.column_map = { "Bruttó bér": "Bruttó bér", "Bruttó bér projektre elszámolva": "PRogramban elsz bér (54)", "Járulékok és adók": "Kapcsolódó járulék (56)" }
        for i, full_column_name in zip(range(2, 5), self.column_map):
            self.process(full_column_name, self.column_map[full_column_name], i)

    def process(self, full_column_name, terv_worksheet_name, i):
        logging.info(self.excel.TASKN.format(i, full_column_name))
        logging.info("Forrás fül: '" + self.excel.full_workbook_sheet_name + "'")
        logging.info("Forrás oszlop: '" + full_column_name + "'")
        logging.info("Cél fül: '" + terv_worksheet_name + "'")
        self.excel.terv_workbook.get_sheet_by_name(terv_worksheet_name)
        self.check_use_case(full_column_name, terv_worksheet_name)
        logging.info(self.excel.TASKN_END.format(i, full_column_name) + random.choice(fun))

    def check_use_case(self, full_column_name, terv_worksheet_name):
        pass



