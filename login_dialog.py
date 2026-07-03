"""The master-password dialog shown on startup and when locking the vault.

Handles two flows in one widget:
  * First run: no vault exists yet -> ask the user to choose a password.
  * Returning user: vault exists -> ask for the existing password.
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from note_storage import NoteStorage


class LoginDialog(QDialog):
    def __init__(self, storage: NoteStorage, parent=None):
        super().__init__(parent)
        self.storage = storage
        self.is_new_vault = not storage.has_existing_vault()

        self.setWindowTitle("Encrypted Notes")
        self.setFixedSize(360, 300 if self.is_new_vault else 250)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(10)

        icon = QLabel("🔒")
        icon.setStyleSheet("font-size: 34px;")
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        title = QLabel(
            "Create your master password" if self.is_new_vault else "Welcome back"
        )
        title.setStyleSheet("font-size: 17px; font-weight: 600;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            "This password encrypts every note.\nThere is no way to recover it if lost."
            if self.is_new_vault
            else "Enter your master password to unlock your notes."
        )
        subtitle.setObjectName("metaLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        layout.addSpacing(6)

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Master password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setObjectName("searchBox")
        layout.addWidget(self.password_edit)

        if self.is_new_vault:
            self.confirm_edit = QLineEdit()
            self.confirm_edit.setPlaceholderText("Confirm password")
            self.confirm_edit.setEchoMode(QLineEdit.Password)
            self.confirm_edit.setObjectName("searchBox")
            layout.addWidget(self.confirm_edit)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #f28b82; font-size: 12px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        layout.addWidget(self.error_label)

        layout.addSpacing(4)

        self.submit_button = QPushButton(
            "Create vault" if self.is_new_vault else "Unlock"
        )
        self.submit_button.setObjectName("primaryButton")
        self.submit_button.clicked.connect(self._on_submit)
        layout.addWidget(self.submit_button)

        self.password_edit.returnPressed.connect(self._on_submit)
        if self.is_new_vault:
            self.confirm_edit.returnPressed.connect(self._on_submit)

    def _on_submit(self):
        password = self.password_edit.text()

        if not password:
            self.error_label.setText("Please enter a password.")
            return

        if self.is_new_vault:
            if len(password) < 4:
                self.error_label.setText(
                    "Use at least 4 characters for your password."
                )
                return
            if password != self.confirm_edit.text():
                self.error_label.setText("Passwords do not match.")
                return
            self.storage.create_vault(password)
            self.accept()
        else:
            if self.storage.unlock(password):
                self.accept()
            else:
                self.error_label.setText("Incorrect password. Try again.")
                self.password_edit.clear()
                self.password_edit.setFocus()

    @staticmethod
    def confirm_unlock(storage: NoteStorage, parent=None) -> bool:
        """Convenience: run the dialog, return True if the vault was opened."""
        dialog = LoginDialog(storage, parent)
        return dialog.exec() == QDialog.Accepted
