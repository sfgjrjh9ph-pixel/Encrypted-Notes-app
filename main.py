
import sys

from PySide6.QtWidgets import QApplication, QDialog

from login_dialog import LoginDialog
from main_window import MainWindow
from note_storage import NoteStorage
from styles import STYLE_SHEET

_current_window = None


def _open_session(app: QApplication):
    global _current_window

    storage = NoteStorage()
    login = LoginDialog(storage)
    if login.exec() != QDialog.Accepted:
        app.quit()
        return

    window = MainWindow(storage)
    window.locked.connect(lambda: _open_session(app))
    _current_window = window
    window.show()


def run():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    app.setApplicationName("Encrypted Notes")

    _open_session(app)

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
