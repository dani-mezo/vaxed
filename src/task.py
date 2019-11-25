import logging
import random
from datetime import datetime, timedelta

from message import DOUBLE_LINE, fun, TASK_END, TASK, Message, LONG_LINE, sad
from sheet_data import SheetData
from time_utils import Time
from worksheet_utils import WorksheetUtils, YELLOW, PINK


class Task:
    i = 0

    def __init__(self, terv_workbook, full_data, full_sheet, full_task_value, terv_workbook_name, terv_task_value, just_verify_presence):
        Task.i = Task.i + 1
        self.started_at = datetime.now()
        Task.log_init(full_task_value, terv_task_value)
        self.terv_sheet = terv_workbook.get_sheet_by_name(terv_workbook_name)
        self.terv_data = SheetData(terv_workbook, self.terv_sheet, 'Terv - ' + terv_workbook_name, just_verify_presence)
        self.full_data = full_data
        self.full_sheet = full_sheet
        self.just_verify_presence = just_verify_presence
        self.verified_cells = dict()
        self.verified_presence_cells = []
        self.failed_verification_cells = []
        self.terv_month_column = self.terv_data.column_by_value(terv_task_value)
        self.full_task_column = full_data.column_by_value(full_task_value)
        self.process()
        self.finish()
        logging.info(TASK_END.format(Task.i, full_task_value.replace('\n', '')) + random.choice(fun))
        self.finished_at = datetime.now()
        self.took_seconds = (self.finished_at - self.started_at).total_seconds()
        self.log_outro()

    def process(self):
        for full_coordinate, full_value in self.full_data.cells.items():
            if self.full_data.name_column in full_coordinate and full_coordinate != self.full_data.name_column + '1':
                rownum = full_coordinate[1:]
                name = full_value.splitlines()[0]
                target_task_coordinate = self.full_task_column + rownum
                target_value = self.full_data.cells[target_task_coordinate]
                try:
                    self.verify_user(name, target_value)
                except Exception as e:
                    logging.error(e)
                    self.failed_verification_cells.append(target_task_coordinate)

    def verify_user(self, name, target_value):
        logging.info(DOUBLE_LINE)
        logging.info('Célszemély: ' + name)
        cached_rows = self.terv_data.cached_name_rows[name]
        if cached_rows:
            logging.info('Megtalált sorok: ' + str(cached_rows))
            verify_coordinates = list(map(lambda row: self.terv_month_column + row, cached_rows))
            for verify_coordinate in verify_coordinates:
                terv_value_to_verify = self.terv_data.cells[verify_coordinate]
                if self.just_verify_presence:
                    if terv_value_to_verify == 1:
                        self.verified_presence_cells.append(verify_coordinate)
                        logging.info("Megtaláltam és igazoltam a '100%' értéket a '" + verify_coordinate + "' cellában.")
                        return
                else:
                    if target_value == terv_value_to_verify:
                        self.verified_cells[verify_coordinate] = terv_value_to_verify
                        logging.info("Megtaláltam és igazoltam az értéket a '" + verify_coordinate + "' cellában.")
                        return
            raise Exception("Nem találtam cellát ami megfelelne a full táblabeli '" + str(target_value)
                            + "' értékhez a felhasználóhoz '" + name + "'. Vizsgált cellák: " + str(verify_coordinates))
        raise Exception("Nem találtam egyáltalán cellát a felhasználóhoz '" + name)

    @staticmethod
    def log_init(full_task_value, terv_task_value):
        Message.log_block('TASK ' + str(Task.i), None)
        logging.info(TASK.format(Task.i, full_task_value.replace('\n', '')))
        logging.info("FULL forrás oszlop: '" + full_task_value.replace('\n', '') + "'")
        logging.info("Terv cél oszlop: '" + terv_task_value + "'")

    def finish(self):
        for coordinate in self.failed_verification_cells:
            full_cell_failed_verification = self.full_sheet[coordinate]
            WorksheetUtils.color_cell(full_cell_failed_verification, YELLOW)
        for coordinate, value in self.verified_cells.items():
            verified_cell = self.terv_sheet[coordinate]
            verified_cell.value = value
            WorksheetUtils.color_cell(verified_cell, PINK)
        for coordinate in self.verified_presence_cells:
            verified_cell = self.terv_sheet[coordinate]
            WorksheetUtils.color_cell(verified_cell, PINK)

    def log_outro(self):
        logging.info(LONG_LINE)
        if len(self.failed_verification_cells) == 0:
            Message.log_block(
                random.choice(fun) + ' Sikeresen befejeződött TASK ' + str(Task.i) + '!' + random.choice(fun),
                "A task ennyi másodpercig tartott: " + Time.format_seconds(self.took_seconds))
        else:
            Message.log_block(random.choice(sad) + ' Végeztünk, de voltak FULL-beli cellák amik nem egyeztek: '
                           + str(self.failed_verification_cells), "A task ennyi másodpercig tartott: "
                              + Time.format_seconds(self.took_seconds))
        logging.info(LONG_LINE)
