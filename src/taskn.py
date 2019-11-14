import logging
import random

from message import fun
from worksheet_utils import WorksheetUtils


class TaskN:
    def __init__(self, excel):
        self.excel = excel
        self.task_counter = 0
        self.column_map = {
            "Bruttó bér/ illetmény/ megbízási díj/ céljuttatás": "Bruttó bér",
            "Bruttó bér projektre elszámolva": "PRogramban elsz bér (54)",
            "Járulékok és adók": "Kapcsolódó járulék (56)"
        }
        for i, full_column_name in zip(range(2, 5), self.column_map):
            self.process(full_column_name, self.column_map[full_column_name], i)

    def process(self, full_column_name, terv_worksheet_name, i):
        for j in range(10):
            logging.info('->')
            if j == 4:
                logging.info('->                             TASK ' + str(i))
        logging.info(self.excel.TASKN.format(i, full_column_name))
        logging.info("Forrás fül: '" + self.excel.full_workbook_sheet_name + "'")
        logging.info("Forrás oszlop: '" + full_column_name + "'")
        logging.info("Cél fül: '" + terv_worksheet_name + "'")
        terv_worksheet = self.excel.terv_workbook.get_sheet_by_name(terv_worksheet_name)
        header_month_cell = WorksheetUtils.find_first_cell_by_value(self.excel.terv_workbook, terv_worksheet, self.excel.header_month_column_name)
        header_month_cell_full = WorksheetUtils.find_first_cell_by_value(None, self.excel.full_sheet, full_column_name)
        cells_to_process = self.use_case(header_month_cell, terv_worksheet, header_month_cell_full, terv_worksheet_name)
        self.process_use_case_result(self.excel.terv_workbook, cells_to_process, terv_worksheet_name, terv_worksheet, i)
        self.excel.save()
        logging.info(self.excel.TASKN_END.format(i, full_column_name) + random.choice(fun))

    def use_case(self, header_month_cell, terv_worksheet, header_month_cell_full, terv_worksheet_name):
        cells_to_process = []
        for row in self.excel.full_sheet.iter_rows():
            if 'neve' in row[0].value:
                continue
            target_name = row[0].value.splitlines()[0]
            logging.info(self.excel.SMALL_LINE)
            logging.info('Célszemély: ' + target_name)
            logging.info('Keresem a célszemélyhez tartozó cellákat...')
            found_cells = WorksheetUtils.find_cells_by_value_coordinates(self.excel.terv_workbook, terv_worksheet,
                                                                         header_month_cell.value, target_name)
            logging.info('Megtaláltam a cellákat: ' + str(list(map(lambda x: x.coordinate, found_cells))))
            found_cells_with_value = WorksheetUtils.only_cells_with_value(self.excel.terv_workbook, found_cells, terv_worksheet)
            logging.info('Ezek közül cellák nem nulla értékkel: ' + str(list(map(lambda x: x.coordinate, found_cells_with_value))))
            if len(found_cells_with_value) > 1:
                raise Exception("Túl sok sort találtam értékkel a célszemélyhez: " + target_name + "\ntalált cellák: "
                                + str(found_cells_with_value))
            if len(found_cells_with_value) == 0:
                raise Exception("Nem találtam egyetlen cellát sem értékkel a célszemélyhez: " + target_name)
            logging.info('Összevetendő cella megtalálva: ' + found_cells_with_value[0].coordinate)
            value_to_verify = WorksheetUtils.simple_resolve_in_sheet(self.excel.full_sheet, row[header_month_cell_full.column - 1].value)
            value_to_verify_against = WorksheetUtils.resolve_reference(self.excel.terv_workbook, found_cells_with_value[0].value, terv_worksheet)
            logging.info("Összevetem az értékeket.")
            logging.info("FULL tábla - érték: '" + str(value_to_verify) + "'")
            logging.info("Terv tábla - natív érték: '" + str(found_cells_with_value[0].value) + "'")
            logging.info("Terv tábla - feloldott érték: '" + str(value_to_verify_against) + "'")
            if str(value_to_verify) != str(value_to_verify_against):
                raise Exception("Nem egyezik meg a két összevetett érték.\nFül: " + terv_worksheet_name
                                + "\nNév: " + target_name + "\nFULL érték: " + str(value_to_verify) + "\nTerv érték: " +
                                str(value_to_verify_against))
            logging.info("Az értékek egyeznek!")
            logging.info("Cella '" + str(found_cells_with_value[0].coordinate) + "' eltárolása későbbi feldolgozásra...")
            cells_to_process.append(found_cells_with_value[0])
        return cells_to_process

    def process_use_case_result(self, workbook, result_cells, terv_worksheet_name, current_sheet, i):
        logging.info(self.excel.SMALL_LINE + self.excel.SMALL_LINE)
        logging.info("A keresés és ellenőrzés befejeződött - TASK " + str(i))
        logging.info("A következő cellák kerülnek feldolgozásra a '" + terv_worksheet_name + "' célfülön: "
                     + str(sorted(list(map(lambda cell: cell.coordinate, result_cells)))))
        for cell in result_cells:
            cell.value = WorksheetUtils.resolve_reference(workbook, cell.value, current_sheet)
            WorksheetUtils.color_cell(cell, "FF99FF")
        logging.info("A színezés és képleteltüntetés sikeresen befejeződött!")






