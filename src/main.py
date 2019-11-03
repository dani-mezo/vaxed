import sys
from PyQt5.QtWidgets import QApplication

from src.app import App
from src.config import Config

if __name__ == '__main__':
    loaded_config = Config()
    app = QApplication(sys.argv)
    ex = App(loaded_config.config)
    sys.exit(app.exec_())
