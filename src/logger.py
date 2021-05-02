import logging

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QSizePolicy


class QTextEditLogger(logging.Handler):
    def __init__(self, parent, width, height, y):
        super().__init__()
        self.widget = QtWidgets.QTextEdit(parent)
        self.widget.setReadOnly(True)
        self.widget.move(20, y)
        self.resize(width, height)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.widget.setSizePolicy(size_policy)

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)
        QtWidgets.QApplication.processEvents()

    def resize(self, width, height):
        self.widget.resize(width - 40, height - 230)

    def clear(self):
        self.widget.clear()