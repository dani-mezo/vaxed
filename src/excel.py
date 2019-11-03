import logging
import random

from openpyxl import load_workbook
from message import fun
from task1 import Task1
from task2 import Task2

hr_sheet_name = 'HR'


class ExcelProcessor:
    def __init__(self, app, terv, full, year, month, month_number):
        self.terv_workbook = load_workbook(filename=terv)
        self.full_workbook = load_workbook(filename=full)
        self.full = full
        self.terv = terv
        self.app = app
        self.year = year
        self.month = month
        self.month_number = month_number
        self.hr_month_cell = None
        self.cells_promoted_for_coloring = dict()
        self.SMALL_LINE = "-------------------"
        self.SMALL_ARROW = "---------->"
        self.TASK1 = "------------------ TASK 1 - 100% Színezés ------------------"
        self.TASK1_END = "------------ TASK 1 - 100% Színezés - Befejezve ------------"
        self.TASKN = "------------ TASK {} - {} ------------"
        self.TASKN_END = "------------ TASK {} - {} - Befejezve ------------"
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
            self.task2()
        except Exception as e:
            logging.error("Probléma merült fel, a végrehajtást megszakítom.", e)
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

    def task2(self):
        Task2(self)

    def save(self):
        logging.info(self.SMALL_LINE + self.SMALL_LINE)
        logging.info('Mentés: ' + self.full)
        self.full_workbook.save(self.full)
        logging.info('Mentés: ' + self.terv)
        self.terv_workbook.save(self.terv)

