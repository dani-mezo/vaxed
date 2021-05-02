import logging
from datetime import datetime

from worksheet_utils import WorksheetUtils


class SheetData:

    def __init__(self, workbook, sheet, name_to_log, skip_resolvation):
        logging.debug('Feloldom a képleteket a fülben: ' + name_to_log)
        self.started_at = datetime.now()
        self.skip_resolvation = skip_resolvation
        self.workbook = workbook
        self.sheet = sheet
        self.cells = dict()
        self.calculate_values()
        self.cached_name_rows = []
        self.name_column = 'A'
        try:
            self.name_column = self.column_by_value('Név')
            self.cached_name_rows = self.generate_name_row_cache()
        except:
            pass
        self.finished_at  = datetime.now()
        self.took_seconds = (self.finished_at - self.started_at).total_seconds()
        logging.debug('A fül teljes képletfeloldása ennyi másodpercig tartott: ' + str(self.took_seconds))


    def calculate_values(self):
        for row in self.sheet.iter_rows():
            for cell in row:
                if self.skip_resolvation:
                    self.cells[cell.coordinate] = cell.value
                else:
                    if cell.value is not None and isinstance(cell.value, str) and cell.value.startswith("="):
                        logging.debug('Elkezdem feloldani a ' + str(cell.coordinate) + ' cella képletét: ' + str(cell.value))
                    if cell.coordinate == "AU3":
                        pass
                    self.cells[cell.coordinate] = WorksheetUtils.resolve_reference(self.workbook, cell.value, self.sheet)
                    if cell.value is not None and isinstance(cell.value, str) and cell.value.startswith("="):
                        logging.debug('Feloldottam a ' + str(cell.coordinate) + ' cella képletét. Eredmény: ' + str(self.cells[cell.coordinate]))


    def generate_name_row_cache(self):
        cache = {}
        for coordinate, value in self.cells.items():
            if SheetData.column(coordinate) == self.name_column:
                cache[value] = cache.get(value, [])
                cache[value].append(SheetData.row(coordinate))
        return cache

    def column_by_value(self, target_value):
        for coordinate, value in self.cells.items():
            if value == target_value:
                return SheetData.column(coordinate)
        raise Exception("Nem találtam meg a keresett értéket: '" + target_value + "' a táblában.")

    @staticmethod
    def column(coordinate):
        if not coordinate:
            return coordinate
        return ''.join(filter(lambda c: not c.isdigit(), coordinate))

    @staticmethod
    def row(coordinate):
        if not coordinate:
            return coordinate
        return ''.join(filter(lambda c: c.isdigit(), coordinate))

