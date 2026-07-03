from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from models import Note


class NoteListItemWidget(QWidget):
    def __init__(self, note: Note, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(3)

        title_text = note.title.strip() or "Untitled Note"
        title = QLabel(title_text)
        title.setStyleSheet("font-size: 14px; font-weight: 600;")
        layout.addWidget(title)

        preview_text = note.preview() or "No additional text"
        preview = QLabel(preview_text)
        preview.setObjectName("metaLabel")
        layout.addWidget(preview)

        date = QLabel(note.updated_at)
        date.setObjectName("metaLabel")
        date.setStyleSheet("color: #6f7180; font-size: 10px;")
        layout.addWidget(date)

    def sizeHint(self):
        from PySide6.QtCore import QSize
        return QSize(220, 70)
