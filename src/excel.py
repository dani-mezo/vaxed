import logging
import random

from openpyxl import load_workbook
from message import fun, sad
from task1 import Task1
from taskn import TaskN

hr_sheet_name = 'HR'


class ExcelProcessor:
    def __init__(self, app, terv, full, year, month, month_number):
        self.terv_workbook = load_workbook(filename=terv)
        self.terv_workbook_data_only = load_workbook(filename=terv, data_only=True)
        self.full_workbook = load_workbook(filename=full)
        self.full = full
        self.terv = terv
        self.app = app
        self.year = year
        self.month = month
        self.month_number = month_number
        self.cells_promoted_for_coloring = dict()
        self.SMALL_LINE = "-------------------"
        self.SMALL_ARROW = "---------->"
        self.TASK1 = "------------------ TASK 1 - 100% Színezés ------------------"
        self.TASK1_END = "------------ TASK 1 - 100% Színezés - Befejezve ------------"
        self.TASKN = "------------ TASK {} - {} ------------"
        self.TASKN_END = "------------ TASK {} - {} - Befejezve ------------"
        self.header_month_column_name = str(self.year) + '_' + str(self.month_number)
        self.error_cells = []
        cut_year = year[2:]
        full_workbook_referred_sheet_names = list(filter(lambda sheet_name: cut_year in sheet_name and month in sheet_name,
                                                    self.full_workbook.get_sheet_names()))
        logging.info('Betöltöttem a FULL táblából a következő füleket: ' + str(full_workbook_referred_sheet_names))
        if len(full_workbook_referred_sheet_names) > 1:
            logging.error('Valami nem stimmel, több fül is megfelelt a kiválasztásnak: ' + str(full_workbook_referred_sheet_names))
            return
        if len(full_workbook_referred_sheet_names) < 1:
            logging.error("Valami nem stimmel, nem találok fület ami megfelel az év '" + year + "', hónap '" + month + "' feltételeknek.")
            return
        try:
            self.task1(full_workbook_referred_sheet_names[0])
            self.taskn()
            logging.info(self.SMALL_LINE + self.SMALL_LINE + self.SMALL_LINE + self.SMALL_LINE)
            if len(self.error_cells) == 0:
                self.log_block(random.choice(fun) + random.choice(fun) + ' Sikeresen VÉGEZTÜNK!' + random.choice(fun) + random.choice(fun))
            else:
                self.log_block(random.choice(sad) + ' Végeztünk, de voltak FULL-beli cellák amik nem egyeztek: '
                               + str(list(map(lambda cell: cell.coordinate, self.error_cells))))
            logging.info(self.SMALL_LINE + self.SMALL_LINE + self.SMALL_LINE + self.SMALL_LINE)
        except Exception as e:
            logging.error("Probléma merült fel, a végrehajtást megszakítom.")
            logging.exception(e)
            return

    def task1(self, full_workbook_sheet_name):
        self.full_workbook_sheet_name = full_workbook_sheet_name
        logging.info(self.TASK1)
        logging.info("Forrás fül: '" + full_workbook_sheet_name + "'")
        logging.info("Cél fül: '" + hr_sheet_name + "'")
        self.full_sheet = self.full_workbook.get_sheet_by_name(full_workbook_sheet_name)
        self.hr_sheet = self.terv_workbook.get_sheet_by_name(hr_sheet_name)
        Task1(self)
        self.save()
        logging.info(self.TASK1_END + random.choice(fun))

    def taskn(self):
        TaskN(self)

    def save(self):
        logging.info(self.SMALL_LINE + self.SMALL_LINE)
        logging.info('Mentés: ' + self.full)
        self.full_workbook.save(self.full)
        logging.info('Mentés: ' + self.terv)
        self.terv_workbook.save(self.terv)

    def log_block(self, text):
        for j in range(10):
            logging.info('->')
            if j == 4:
                if len(text) > 20:
                    logging.info('->' + text)
                else:
                    logging.info('->                             ' + text)



