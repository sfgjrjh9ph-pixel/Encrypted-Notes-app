"""The main window: sidebar with search + note list, and an editor pane."""
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from models import Note
from note_list_item import NoteListItemWidget
from note_storage import NoteStorage

AUTOSAVE_DELAY_MS = 600


class MainWindow(QMainWindow):
    # Emitted when the user clicks "Lock", after the vault has been
    # re-encrypted and the in-memory key discarded.
    locked = Signal()

    def __init__(self, storage: NoteStorage):
        super().__init__()
        self.storage = storage
        self.notes: list[Note] = storage.load_notes()
        self.current_note: Note | None = None
        self._is_locking = False

        self.setWindowTitle("Encrypted Notes")
        self.resize(980, 620)

        # Debounce timer so we don't hit the disk on every keystroke.
        self.autosave_timer = QTimer(self)
        self.autosave_timer.setSingleShot(True)
        self.autosave_timer.setInterval(AUTOSAVE_DELAY_MS)
        self.autosave_timer.timeout.connect(self._save_current_note)

        self._build_ui()
        self._refresh_note_list()
        self.statusBar().showMessage(f"Vault unlocked — {len(self.notes)} notes")

    # ------------------------------------------------------------------ UI

    def _build_ui(self):
        central = QWidget()
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_sidebar(), 0)
        root.addWidget(self._build_editor(), 1)

        self.setCentralWidget(central)
        self.setStatusBar(self.statusBar())

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(300)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        header = QHBoxLayout()
        app_label = QLabel("🔒 My Notes")
        app_label.setStyleSheet("font-size: 16px; font-weight: 700;")
        header.addWidget(app_label)
        header.addStretch()
        lock_btn = QPushButton("Lock")
        lock_btn.setObjectName("iconButton")
        lock_btn.setToolTip("Lock the vault")
        lock_btn.clicked.connect(self._lock_vault)
        header.addWidget(lock_btn)
        layout.addLayout(header)

        self.search_box = QLineEdit()
        self.search_box.setObjectName("searchBox")
        self.search_box.setPlaceholderText("Search notes...")
        self.search_box.textChanged.connect(self._refresh_note_list)
        layout.addWidget(self.search_box)

        new_btn = QPushButton("+ New Note")
        new_btn.setObjectName("primaryButton")
        new_btn.clicked.connect(self._create_note)
        layout.addWidget(new_btn)

        self.note_list = QListWidget()
        self.note_list.setObjectName("noteList")
        self.note_list.currentItemChanged.connect(self._on_selection_changed)
        layout.addWidget(self.note_list, 1)

        return sidebar

    def _build_editor(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("editorPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(6)

        top_row = QHBoxLayout()
        self.meta_label = QLabel("")
        self.meta_label.setObjectName("metaLabel")
        top_row.addWidget(self.meta_label)
        top_row.addStretch()

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setObjectName("dangerButton")
        self.delete_btn.clicked.connect(self._delete_current_note)
        top_row.addWidget(self.delete_btn)
        layout.addLayout(top_row)

        self.title_edit = QLineEdit()
        self.title_edit.setObjectName("titleEdit")
        self.title_edit.setPlaceholderText("Title")
        self.title_edit.textChanged.connect(self._on_edited)
        layout.addWidget(self.title_edit)

        self.content_edit = QTextEdit()
        self.content_edit.setObjectName("contentEdit")
        self.content_edit.setPlaceholderText("Start writing...")
        self.content_edit.textChanged.connect(self._on_edited)
        layout.addWidget(self.content_edit, 1)

        self.empty_state = QLabel("Select a note or create a new one to get started.")
        self.empty_state.setObjectName("emptyStateLabel")
        self.empty_state.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.empty_state)

        self.editor_widgets = [self.title_edit, self.content_edit, self.delete_btn]
        self._set_editor_visible(False)

        return panel

    def _set_editor_visible(self, visible: bool):
        for widget in self.editor_widgets:
            widget.setVisible(visible)
        self.meta_label.setVisible(visible)
        self.empty_state.setVisible(not visible)

    # ------------------------------------------------------------- helpers

    def _visible_notes(self) -> list[Note]:
        query = self.search_box.text()
        notes = [n for n in self.notes if n.matches(query)]
        notes.sort(key=lambda n: n.updated_at, reverse=True)
        return notes

    def _refresh_note_list(self):
        selected_id = self.current_note.id if self.current_note else None

        self.note_list.blockSignals(True)
        self.note_list.clear()

        row_to_select = -1
        for row, note in enumerate(self._visible_notes()):
            item = QListWidgetItem()
            item.setData(Qt.UserRole, note.id)
            widget = NoteListItemWidget(note)
            item.setSizeHint(widget.sizeHint())
            self.note_list.addItem(item)
            self.note_list.setItemWidget(item, widget)
            if note.id == selected_id:
                row_to_select = row

        self.note_list.blockSignals(False)

        if row_to_select >= 0:
            self.note_list.setCurrentRow(row_to_select)
        elif self.note_list.count() > 0 and self.search_box.text():
            self.note_list.setCurrentRow(0)
        else:
            self._load_note(None)

    def _find_note(self, note_id: str) -> Note | None:
        return next((n for n in self.notes if n.id == note_id), None)

    # -------------------------------------------------------------- events

    def _create_note(self):
        note = Note(title="", content="")
        self.notes.insert(0, note)
        self.storage.save_notes(self.notes)
        self.search_box.clear()
        self._refresh_note_list()
        for row in range(self.note_list.count()):
            if self.note_list.item(row).data(Qt.UserRole) == note.id:
                self.note_list.setCurrentRow(row)
                break
        self.title_edit.setFocus()
        self.statusBar().showMessage("New note created")

    def _on_selection_changed(self, current: QListWidgetItem, _previous):
        self._save_current_note(force=True)
        if current is None:
            self._load_note(None)
            return
        note_id = current.data(Qt.UserRole)
        self._load_note(self._find_note(note_id))

    def _load_note(self, note: Note | None):
        self.current_note = note
        self._set_editor_visible(note is not None)
        if note is None:
            return

        for widget in (self.title_edit, self.content_edit):
            widget.blockSignals(True)
        self.title_edit.setText(note.title)
        self.content_edit.setPlainText(note.content)
        for widget in (self.title_edit, self.content_edit):
            widget.blockSignals(False)

        self.meta_label.setText(f"Last edited {note.updated_at}")

    def _on_edited(self):
        if self.current_note is None:
            return
        self.autosave_timer.start()

    def _save_current_note(self, force: bool = False):
        if force:
            self.autosave_timer.stop()
        if self.current_note is None:
            return
        self.current_note.title = self.title_edit.text().strip() or "Untitled Note"
        self.current_note.content = self.content_edit.toPlainText()
        self.current_note.touch()
        self.storage.save_notes(self.notes)
        self.meta_label.setText(f"Last edited {self.current_note.updated_at}")
        self.statusBar().showMessage("Saved", 1500)
        self._refresh_list_item_only()

    def _refresh_list_item_only(self):
        """Update the currently selected row's preview text without losing selection."""
        row = self.note_list.currentRow()
        if row < 0 or self.current_note is None:
            return
        item = self.note_list.item(row)
        widget = NoteListItemWidget(self.current_note)
        item.setSizeHint(widget.sizeHint())
        self.note_list.setItemWidget(item, widget)

    def _delete_current_note(self):
        if self.current_note is None:
            return
        reply = QMessageBox.question(
            self,
            "Delete note",
            f'Delete "{self.current_note.title}"? This cannot be undone.',
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return
        self.notes = [n for n in self.notes if n.id != self.current_note.id]
        self.storage.save_notes(self.notes)
        self.current_note = None
        self._refresh_note_list()
        self.statusBar().showMessage("Note deleted", 1500)

    def _lock_vault(self):
        self._is_locking = True
        self._save_current_note(force=True)

        self.title_edit.clear()
        self.content_edit.clear()
        self.current_note = None
        self.hide()

        self.locked.emit()
        self.close()

    def closeEvent(self, event):
        if not self._is_locking:
            self._save_current_note(force=True)
        super().closeEvent(event)