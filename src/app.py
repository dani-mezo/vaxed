import logging
import os
import random
from datetime import datetime

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox, QFileDialog, QWidget, QMainWindow, QColorDialog, QCheckBox

from logger import QTextEditLogger
from message import welcome, comment, fun, sad, LONG_LINE, Message
from excel import ExcelProcessor
from src.worksheet_utils import PINK
from time_utils import Time

no_file_selected = 'Nincs fájl kiválasztva.'

log_level_map = {
    'CRITICAL': 50,
    'ERROR' : 40,
    'WARNING' : 30,
    'INFO' : 20,
    'DEBUG' : 10
}

class App(QMainWindow):
    def __init__(self, config):
        super(App, self).__init__()
        super().__init__()
        self.tasks = [
            {"Munkavállaló,\nmegbízottszemély neve/\nbeosztása": "HR"},
            {"Bruttó bér/ illetmény/ megbízási díj/ céljuttatás": "Bruttó bér"},
            {"Bruttó bér projektre elszámolva": "Programban elsz bér (54)"},
            {"Járulékok és adók": "Kapcsolódó járulék (56)"}
        ]
        self.task1_checkbox = QCheckBox("Task1: " + next(iter(self.tasks[0].keys())).replace('\n', '') + ' -> ' + next(iter(self.tasks[0].values())), self)
        self.task2_checkbox = QCheckBox("Task2: " + next(iter(self.tasks[1].keys())).replace('\n', '') + ' -> ' + next(iter(self.tasks[1].values())), self)
        self.task3_checkbox = QCheckBox("Task3: " + next(iter(self.tasks[2].keys())).replace('\n', '') + ' -> ' + next(iter(self.tasks[2].values())), self)
        self.task4_checkbox = QCheckBox("Task4: " + next(iter(self.tasks[3].keys())).replace('\n', '') + ' -> ' + next(iter(self.tasks[3].values())), self)
        self.task_checks = [ True, True, True, True ]
        self.title = 'Vax'
        self.left = 300
        self.top = 300
        self.width = 700
        self.height = 600
        self.logTextBox = None
        self.excel_processor = None
        try:
            self.mean = str(config['measurements']['mean'])
        except:
            self.mean = '0'
        try:
            self.sample_size = str(config['measurements']['sample-size'])
        except:
            self.sample_size = '0'
        try:
            default_full_label = config['sources']['full']
        except:
            default_full_label = no_file_selected
        try:
            default_terv_label = config['sources']['terv']
        except:
            default_terv_label = no_file_selected
        try:
            default_target_color_label = config['color']
        except:
            default_target_color_label = PINK
        self.full_label = QLabel(default_full_label, self)
        self.terv_label = QLabel(default_terv_label, self)
        self.target_color_label = QLabel(default_target_color_label, self)
        self.init_ui()
        logging.info(random.choice(welcome))
        logging.info(random.choice(comment) + ' ' + random.choice(fun))

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.full_button()
        self.terv_button()
        self.color_button()
        self.month_dropdown()
        self.year_dropdown()
        self.match_button()
        self.task_checkboxes()
        self.logger()
        self.log_cleaner()
        self.show()

    def full_button(self):
        full_button = QPushButton('Full', self)
        full_button.move(20, 20)
        full_button.resize(80, 20)
        full_button.clicked.connect(self.load_full)
        self.full_label.move(120, 25)

    def terv_button(self):
        terv_button = QPushButton('HR terv', self)
        terv_button.move(20, 60)
        terv_button.resize(80, 20)
        terv_button.clicked.connect(self.load_terv)
        self.terv_label.move(120, 65)

    def match_button(self):
        match_button = QPushButton('Összevet', self)
        match_button.move(20, 130)
        match_button.resize(100, 80)
        match_button.clicked.connect(self.match)

    def month_dropdown(self):
        comboBox = QComboBox(self)
        comboBox.resize(80, 20)
        self.months = ["Január", "Február", "Március", "Április", "Május", "Június", "Július", "Augusztus", "Szeptember", "Október", "November", "December"]
        comboBox.addItems(self.months)
        month_index = datetime.today().month - 2 if datetime.today().month >= 2 else 11
        self.selected_month = self.months[month_index]
        comboBox.setCurrentIndex(month_index)
        comboBox.move(21, 100)
        comboBox.activated[str].connect(self.select_month)

    def year_dropdown(self):
        self.year_combo = QComboBox(self)
        years = [str(datetime.today().year), str(datetime.today().year - 1)]
        self.year_combo.addItems(years)
        self.selected_year = years[0]
        self.year_combo.setCurrentIndex(0)
        self.year_combo.move(110, 100)
        self.year_combo.activated[str].connect(self.select_year)

    def color_button(self):
        color_button = QPushButton('Szín', self)
        color_button.move(180, 100)
        color_button.resize(80, 20)
        color_button.clicked.connect(self.load_color)
        self.target_color_label.move(270, 95)
        self.target_color_label.setStyleSheet('QLabel {color: #' + self.target_color_label.text() + ';}')

    def select_month(self, month):
        self.selected_month = month
        logging.debug("Kiválasztott hónap: " + month)

    def select_year(self, year):
        self.selected_year = year
        logging.debug("Kiválasztott év: " + year)

    def task_checkboxes(self):
        self.task1_checkbox.move(140, 130)
        self.task1_checkbox.stateChanged.connect(self.task1_update_state)
        self.task1_checkbox.resize(400, 20)
        self.task1_checkbox.setChecked(True)

        self.task2_checkbox.move(140, 150)
        self.task2_checkbox.stateChanged.connect(self.task2_update_state)
        self.task2_checkbox.resize(400, 20)
        self.task2_checkbox.setChecked(True)

        self.task3_checkbox.move(140, 170)
        self.task3_checkbox.stateChanged.connect(self.task3_update_state)
        self.task3_checkbox.resize(400, 20)
        self.task3_checkbox.setChecked(True)

        self.task4_checkbox.move(140, 190)
        self.task4_checkbox.stateChanged.connect(self.task4_update_state)
        self.task4_checkbox.resize(400, 20)
        self.task4_checkbox.setChecked(True)

    def task1_update_state(self):
        self.task1_check_state = self.task1_checkbox.isChecked()
        self.task_checks[0] = self.task1_checkbox.isChecked()
        if self.task1_checkbox.isChecked():
            logging.debug('Task 1 végrehajtása bekapcsolva.')
        else:
            logging.debug('Task 1 végrehajtása kikapcsolva.')

    def task2_update_state(self):
        self.task2_check_state = self.task2_checkbox.isChecked()
        self.task_checks[1] = self.task2_checkbox.isChecked()
        if self.task2_checkbox.isChecked():
            logging.debug('Task 2 végrehajtása bekapcsolva.')
        else:
            logging.debug('Task 2 végrehajtása kikapcsolva.')

    def task3_update_state(self):
        self.task3_check_state = self.task3_checkbox.isChecked()
        self.task_checks[2] = self.task3_checkbox.isChecked()
        if self.task3_checkbox.isChecked():
            logging.debug('Task 3 végrehajtása bekapcsolva.')
        else:
            logging.debug('Task 3 végrehajtása kikapcsolva.')

    def task4_update_state(self):
        self.task4_check_state = self.task4_checkbox.isChecked()
        self.task_checks[3] = self.task4_checkbox.isChecked()
        if self.task4_checkbox.isChecked():
            logging.debug('Task 4 végrehajtása bekapcsolva.')
        else:
            logging.debug('Task 4 végrehajtása kikapcsolva.')

    @pyqtSlot()
    def load_color(self):
        color = QColorDialog.getColor()
        if color.name() == '#000000':
            return
        logging.debug('Szín kiválasztva: ' + color.name()[1:])
        self.target_color_label.setText(color.name()[1:])
        self.target_color_label.setStyleSheet('QLabel {color: #' + self.target_color_label.text() + ';}')
        self.write_out()

    @pyqtSlot()
    def load_full(self):
        full_file = QFileDialog.getOpenFileName()[0]
        if not full_file:
            return
        logging.debug('FULL fájl kiválasztva: ' + full_file)
        file_name = full_file if os.path.isfile(full_file) else no_file_selected
        self.full_label.setText(file_name)
        self.full_label.adjustSize()
        self.write_out()

    @pyqtSlot()
    def load_terv(self):
        terv_file = QFileDialog.getOpenFileName()[0]
        if not terv_file:
            return
        logging.debug('HR terv fájl kiválasztva: ' + terv_file)
        file_name = terv_file if os.path.isfile(terv_file) else no_file_selected
        self.terv_label.setText(file_name)
        self.terv_label.adjustSize()
        self.write_out()

    @pyqtSlot()
    def match(self):
        if not os.path.isfile(self.terv_label.text()):
            logging.error("Nem sikerült betölteni a terv fájlt: '" + self.terv_label.text() + "'")
            return
        if not os.path.isfile(self.full_label.text()):
            logging.error("Nem sikerült betölteni a FULL fájlt: '" + self.terv_label.text() + "'")
            return
        logging.info('Excel táblák összevetése...')
        started_at = datetime.now()
        self.excel_processor = ExcelProcessor(self, self.terv_label.text(), self.full_label.text(), self.selected_year, self.selected_month,
                       self.months.index(self.selected_month) + 1, self.mean, self.target_color_label.text(), self.checked_tasks())
        finished_at = datetime.now()
        self.took_seconds = str((finished_at - started_at).total_seconds())
        logging.info('Ennyi másodpercig tartott a teljes feldolgozás: ' + str(format(float(self.took_seconds), '.2f')))
        self.calculate_new_mean()
        self.write_out()
        self.app_log_outro(self.excel_processor.error_cells)
        self.excel_processor = None

    @pyqtSlot()
    def clean_logs(self):
        self.logTextBox.clear()

    def resizeEvent(self, event):
        if self.logTextBox:
            self.logTextBox.resize(event.size().width(), event.size().height())
        self.full_label.adjustSize()
        self.terv_label.adjustSize()
        self.year_combo.adjustSize()
        return super(App, self).resizeEvent(event)

    def write_out(self):
        f = open('config.yml', 'w')
        f.write("sources:\n")
        f.write("  full: " + self.full_label.text() + "\n")
        f.write("  terv: " + self.terv_label.text() + "\n")
        f.write("measurements:\n")
        f.write("  sample-size: " + self.sample_size + "\n")
        f.write("  mean: " + self.mean + "\n")
        f.write("color: " + self.target_color_label.text() + "\n")
        f.close()

    def log_cleaner(self):
        log_cleaner_button = QPushButton('Log ürítése', self)
        log_cleaner_button.move(611, 170)
        log_cleaner_button.resize(70, 22)
        log_cleaner_button.clicked.connect(self.clean_logs)

    def logger(self):
        combo_box = QComboBox(self)
        combo_box.resize(60, 20)
        self.log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        combo_box.addItems(self.log_levels)
        combo_box.setCurrentIndex(1)
        combo_box.move(620, 195)
        combo_box.activated[str].connect(self.set_log_level)
        log_label = QLabel('Logolási szint: ', self)
        log_label.resize(80, 20)
        log_label.move(550, 195)

        self.logTextBox = QTextEditLogger(self, self.width, self.height, 220)
        self.logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self.logTextBox)
        logging.getLogger().setLevel(logging.INFO)

    def set_log_level(self, log_level):
        logging.debug('Új log szint került beállításra: ' + log_level)
        logging.getLogger().setLevel(log_level_map.get(log_level))

    def calculate_new_mean(self):
        try:
            self.mean = str((float(self.mean) * float(self.sample_size) + float(self.took_seconds)) /
                            (float(self.sample_size) + 1))
            self.sample_size = str(float(self.sample_size) + 1)
        except:
            return

    def app_log_outro(self, failed_verification_cells):
        if len(failed_verification_cells) == 0:
            Message.log_block(
                random.choice(fun) + random.choice(fun) + ' A teljes végrehajtással sikeresen végeztünk!' + random.choice(fun)
                + random.choice(fun), "Ennyi másodpercig tartott: " + Time.format_seconds(self.took_seconds), logging.critical)
        else:
            Message.log_block(random.choice(sad) + ' Végeztünk mindennel, de voltak FULL-beli cellák amik nem egyeztek: '
                           + str(failed_verification_cells), "Ennyi másodpercig tartott: " + Time.format_seconds(self.took_seconds), logging.critical)

    def closeEvent(self, event):
        if self.excel_processor is not None:
            self.excel_processor.close()

    def checked_tasks(self):
        checked_tasks_listed = []
        for i in range(4):
            if self.task_checks[i]:
                checked_tasks_listed.append(self.tasks[i])
            else:
                checked_tasks_listed.append(None)
        return checked_tasks_listed
