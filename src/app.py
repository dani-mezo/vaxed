import logging
import os
import random
from datetime import datetime

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox, QFileDialog, QWidget

from logger import QTextEditLogger
from message import welcome, comment, fun
from src.excel import ExcelProcessor

no_file_selected = 'Nincs fájl kiválasztva.'


class App(QWidget):
    def __init__(self, config):
        super().__init__()
        self.title = 'Vax'
        self.left = 300
        self.top = 300
        self.width = 550
        self.height = 400
        default_full_label = config['sources']['full'] if config['sources']['full'] else no_file_selected
        default_terv_label = config['sources']['terv'] if config['sources']['terv'] else no_file_selected
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
        comboBox = QComboBox(self)
        years = [str(datetime.today().year), str(datetime.today().year - 1)]
        comboBox.addItems(years)
        self.selected_year = years[0]
        comboBox.setCurrentIndex(0)
        comboBox.move(110, 100)
        comboBox.activated[str].connect(self.select_year)

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
        if not os.path.isfile(self.terv_label.text()) or not os.path.isfile(self.full_label.text()):
            return
        logging.info('Excel táblák összevetése...')
        ExcelProcessor(self, self.terv_label.text(), self.full_label.text(), self.selected_year, self.selected_month, self.months.index(self.selected_month) + 1)

    def write_out(self):
        f = open('../config.yml', 'w')
        f.write("sources:\n")
        f.write("  full: " + self.full_label.text() + "\n")
        f.write("  terv: " + self.terv_label.text() + "\n")
        f.close()

    def logger(self):
        logTextBox = QTextEditLogger(self)
        logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)