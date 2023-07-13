
import sys

from qtpy import QtWidgets

from app import MainWindow


def main():

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("FreeLabel")
    # app.setWindowIcon(newIcon("icon"))
    # app.installTranslator(translator)
    win = MainWindow()
    win.show()
    win.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
