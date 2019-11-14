import logging

from PyQt5 import QtWidgets


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QTextEdit(parent)
        self.widget.setReadOnly(True)
        self.widget.move(20, 190)
        self.widget.setMinimumWidth(610)

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)