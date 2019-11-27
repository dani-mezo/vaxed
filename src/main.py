import sys
from PyQt5.QtWidgets import QApplication

from app import App
from config import Config

if __name__ == '__main__':
    try:
        loaded_config = Config()
        app = QApplication(sys.argv)
        ex = App(loaded_config.config)
        sys.exit(app.exec_())
    except Exception as e:
        error_file = open('error.log', 'w')
        error_file.write(str(e))
        error_file.close()

