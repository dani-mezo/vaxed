import logging
import math

from openpyxl.styles import PatternFill

LIGHT_RED = 'ff726f'
PINK = 'ff99ff'


class WorksheetUtils:

    @staticmethod
    def resolve_reference(workbook, reference, current_sheet):
        if not WorksheetUtils.is_meaningful(reference):
            return reference
        if 'SUMIF' in reference or 'DATEDIF' in reference:
            return reference
        if 'IF' in reference:
            return WorksheetUtils.resolve_if_reference(workbook, reference, current_sheet)
        if 'ROUND' in reference:
            return WorksheetUtils.resolve_round_reference(workbook, reference, current_sheet)
        if '-' in reference:
            return WorksheetUtils.resolve_minus(workbook, reference, current_sheet)
        if '*' in reference:
            return WorksheetUtils.resolve_multiplication(workbook, reference, current_sheet)
        return WorksheetUtils.resolve_simple_reference_recursively(workbook, reference, current_sheet)

    @staticmethod
    def resolve_if_reference(workbook, reference, current_sheet):
        no_overhead = WorksheetUtils.remove_overhead_from_reference(reference).replace('IF', '')
        condition, true, false = no_overhead.split(',')
        cond_left, cond_right = condition.split('=')
        cond_left_value = cond_left
        cond_right_value = cond_right
        if '!' in cond_left:
            cond_left_value = WorksheetUtils.resolve_reference(workbook, cond_left, current_sheet)
        if '!' in cond_right:
            cond_right_value = WorksheetUtils.resolve_reference(workbook, cond_right, current_sheet)
        if cond_right_value == cond_left_value or not cond_right_value and not cond_left_value:
            return true
        return WorksheetUtils.resolve_reference(workbook, false, current_sheet)

    @staticmethod
    def resolve_round_reference(workbook, reference, current_sheet):
        no_overhead = WorksheetUtils.remove_overhead_from_reference(reference).replace('ROUND', '')
        multiplication, rounded_by = no_overhead.split(',')
        left_multiplication, right_multiplication = multiplication.split('*')
        left_resolved = WorksheetUtils.resolve_reference(workbook, left_multiplication, current_sheet)
        right_resolved = WorksheetUtils.resolve_reference(workbook, right_multiplication, current_sheet)
        try:
            return WorksheetUtils.ceil_up(left_resolved, right_resolved)
        except:
            return reference

    @staticmethod
    def resolve_simple_reference_recursively(workbook, reference, current_sheet):
        if WorksheetUtils.simple_local_reference(reference):
            try:
                return WorksheetUtils.resolve_reference(workbook, current_sheet[reference[1:]].value, current_sheet)
            except:
                return reference
        if WorksheetUtils.simple_reference(reference):
            no_overhead_reference = WorksheetUtils.remove_overhead_from_reference(reference)
            try:
                sheet, cell = no_overhead_reference.split('!')
                new_current_sheet = workbook.get_sheet_by_name(sheet)
                sheet_referred_cell = new_current_sheet[cell]
            except:
                logging.debug('Nem sikerült feloldani a referenciát, a fül vagy a cella nem létezik: ' + reference)
                return reference
            return WorksheetUtils.resolve_reference(workbook, sheet_referred_cell.value, new_current_sheet)
        try:
            return WorksheetUtils.resolve_reference(workbook, current_sheet[reference].value, current_sheet)
        except:
            return reference

    @staticmethod
    def resolve_multiplication(workbook, reference, current_sheet):
        if '=' in reference:
            no_overhead = reference[1:]
        else:
            no_overhead = reference
        try:
            left, right = no_overhead.split('*')
        except:
            return reference
        resolved_left = WorksheetUtils.resolve_reference(workbook, left, current_sheet)
        resolved_right = WorksheetUtils.resolve_reference(workbook, right, current_sheet)
        try:
            return WorksheetUtils.ceil_up(resolved_left, resolved_right)
        except:
            return reference

    @staticmethod
    def resolve_minus(workbook, reference, current_sheet):
        if reference.count("-") > 1:
            return reference
        no_overhead_reference = WorksheetUtils.remove_overhead_from_reference(reference)
        left_minus, right_minus = no_overhead_reference.split('-')
        left_minus_resolved = WorksheetUtils.resolve_reference(workbook, left_minus, current_sheet)
        right_minus_resolved = WorksheetUtils.resolve_reference(workbook, right_minus, current_sheet)
        try:
            return round(float(left_minus_resolved) - float(right_minus_resolved))
        except:
            return reference

    @staticmethod
    def simple_reference(reference):
        if not reference or not isinstance(reference, str):
            return False
        return not "#REF" in reference and "!" in reference and reference[-1] != '!' and ('(54)' in reference or not '(' in reference) \
               and not '!!' in reference and len(reference) < 40 and not 'ÚJ' in reference

    @staticmethod
    def is_meaningful(reference):
        if not reference or not isinstance(reference, str):
            return False
        return True

    @staticmethod
    def remove_overhead_from_reference(reference):
        no_overhead = reference.replace('\'', '').replace('$', '').replace('"', '').replace('\\',  '').replace('(', '').replace(')', '')
        if 'Programban' in reference and '54' in reference:
            no_overhead = no_overhead[:no_overhead.find('54')] + '(54)' + no_overhead[no_overhead.find('54') + 2:]
        if reference.startswith('=+'):
            return no_overhead[2:]
        if reference.startswith('='):
            return no_overhead[1:]
        return no_overhead

    @staticmethod
    def color_cell(cell, color):
        if not cell or not color:
            raise Exception("Nem sikerült színezni, nem létezik a cella vagy hiányzik a szín.")
        color_fill = PatternFill(start_color=color, fill_type="solid")
        cell.fill = color_fill

    @staticmethod
    def simple_local_reference(reference):
        if not reference or not isinstance(reference, str):
            return False
        return not "#REF" in reference and not '!' in reference and "=" in reference and not '*' in reference and len(reference) < 8

    @staticmethod
    def ceil_up(left, right):
        multiplied = float(left) * float(right)
        if (float(multiplied) % 1) >= 0.499:
            return math.ceil(multiplied)
        else:
            return round(multiplied)