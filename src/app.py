import logging
import os
import random
from datetime import datetime

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox, QFileDialog, QWidget, QMainWindow

from logger import QTextEditLogger
from message import welcome, comment, fun, sad, LONG_LINE, Message
from excel import ExcelProcessor
from time_utils import Time

no_file_selected = 'Nincs fájl kiválasztva.'


class App(QMainWindow):
    def __init__(self, config):
        super(App, self).__init__()
        super().__init__()
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
        self.full_label = QLabel(default_full_label, self)
        self.terv_label = QLabel(default_terv_label, self)
        self.init_ui()
        logging.info(random.choice(welcome))
        logging.info(random.choice(comment) + ' ' + random.choice(fun))

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.full_button()
        self.terv_button()
        self.month_dropdown()
        self.year_dropdown()
        self.match_button()
        self.logger()
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
        match_button.move(20, 140)
        match_button.resize(100,32)
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

    def select_month(self, month):
        self.selected_month = month
        logging.info("Kiválasztott hónap: " + month)

    def select_year(self, year):
        self.selected_year = year
        logging.info("Kiválasztott év: " + year)

    @pyqtSlot()
    def load_full(self):
        full_file = QFileDialog.getOpenFileName()[0]
        if not full_file:
            return
        logging.info('FULL fájl kiválasztva: ' + full_file)
        file_name = full_file if os.path.isfile(full_file) else no_file_selected
        self.full_label.setText(file_name)
        self.full_label.adjustSize()
        self.write_out()

    @pyqtSlot()
    def load_terv(self):
        terv_file = QFileDialog.getOpenFileName()[0]
        if not terv_file:
            return
        logging.info('HR terv fájl kiválasztva: ' + terv_file)
        file_name = terv_file if os.path.isfile(terv_file) else no_file_selected
        self.terv_label.setText(file_name)
        self.terv_label.adjustSize()
        self.write_out()

    @pyqtSlot()
    def match(self):
        if not os.path.isfile(self.terv_label.text()):
            logging.info("Nem sikerült betölteni a terv fájlt: '" + self.terv_label.text() + "'")
            return
        if not os.path.isfile(self.full_label.text()):
            logging.info("Nem sikerült betölteni a FULL fájlt: '" + self.terv_label.text() + "'")
            return
        logging.info('Excel táblák összevetése...')
        started_at = datetime.now()
        self.excel_processor = ExcelProcessor(self, self.terv_label.text(), self.full_label.text(), self.selected_year, self.selected_month,
                       self.months.index(self.selected_month) + 1, self.mean)
        finished_at = datetime.now()
        self.took_seconds = str((finished_at - started_at).total_seconds())
        logging.info('Ennyi másodpercig tartott a teljes feldolgozás: ' + str(format(float(self.took_seconds), '.2f')))
        self.calculate_new_mean()
        self.write_out()
        self.app_log_outro(self.excel_processor.error_cells)
        self.excel_processor = None

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
        f.close()

    def logger(self):
        self.logTextBox = QTextEditLogger(self, self.width, self.height)
        self.logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self.logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)

    def calculate_new_mean(self):
        try:
            self.mean = str((float(self.mean) * float(self.sample_size) + float(self.took_seconds)) /
                            (float(self.sample_size) + 1))
            self.sample_size = str(float(self.sample_size) + 1)
        except:
            return

    def app_log_outro(self, failed_verification_cells):
        logging.info(LONG_LINE)
        logging.info(LONG_LINE)
        logging.info(LONG_LINE)
        if len(failed_verification_cells) == 0:
            Message.log_block(
                random.choice(fun) + random.choice(fun) + ' A teljes végrehajtással sikeresen végeztünk!' + random.choice(fun)
                + random.choice(fun), "Ennyi másodpercig tartott: " + Time.format_seconds(self.took_seconds))
        else:
            Message.log_block(random.choice(sad) + ' Végeztünk mindennel, de voltak FULL-beli cellák amik nem egyeztek: '
                           + str(failed_verification_cells), "Ennyi másodpercig tartott: " + Time.format_seconds(self.took_seconds))
        logging.info(LONG_LINE)
        logging.info(LONG_LINE)

    def closeEvent(self, event):
        if self.excel_processor is not None:
            self.excel_processor.close()