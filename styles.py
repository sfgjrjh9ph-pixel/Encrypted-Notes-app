
COLOR_BG = "#1e1f26"
COLOR_PANEL = "#262832"
COLOR_PANEL_ALT = "#2d2f3a"
COLOR_BORDER = "#3a3d4a"
COLOR_TEXT = "#e6e6ec"
COLOR_TEXT_DIM = "#9797a6"
COLOR_ACCENT = "#7c9fff"
COLOR_ACCENT_HOVER = "#6b8cf5"
COLOR_DANGER = "#f28b82"

STYLE_SHEET = f"""
QWidget {{
    background-color: {COLOR_BG};
    color: {COLOR_TEXT};
    font-family: "Segoe UI", "Inter", "Helvetica Neue", sans-serif;
    font-size: 13px;
}}

QMainWindow, QDialog {{
    background-color: {COLOR_BG};
}}

/* --- Sidebar / panels --- */
#sidebar {{
    background-color: {COLOR_PANEL};
    border-right: 1px solid {COLOR_BORDER};
}}

#editorPanel {{
    background-color: {COLOR_BG};
}}

/* --- Search box --- */
QLineEdit#searchBox {{
    background-color: {COLOR_PANEL_ALT};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    padding: 8px 12px;
    color: {COLOR_TEXT};
    font-size: 13px;
}}
QLineEdit#searchBox:focus {{
    border: 1px solid {COLOR_ACCENT};
}}

/* --- Note list --- */
QListWidget#noteList {{
    background-color: transparent;
    border: none;
    outline: none;
    padding: 4px;
}}
QListWidget#noteList::item {{
    border-radius: 8px;
    margin: 2px 4px;
    padding: 0px;
}}
QListWidget#noteList::item:selected {{
    background-color: {COLOR_PANEL_ALT};
}}
QListWidget#noteList::item:hover {{
    background-color: #2a2c37;
}}

/* --- Title / content editors --- */
QLineEdit#titleEdit {{
    background: transparent;
    border: none;
    font-size: 22px;
    font-weight: 600;
    padding: 4px 2px;
    color: {COLOR_TEXT};
}}

QTextEdit#contentEdit {{
    background: transparent;
    border: none;
    font-size: 14px;
    line-height: 1.4;
    padding: 4px 2px;
    color: {COLOR_TEXT};
}}

QLabel#metaLabel {{
    color: {COLOR_TEXT_DIM};
    font-size: 11px;
}}

QLabel#emptyStateLabel {{
    color: {COLOR_TEXT_DIM};
    font-size: 14px;
}}

/* --- Buttons --- */
QPushButton {{
    background-color: {COLOR_PANEL_ALT};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    padding: 7px 14px;
    color: {COLOR_TEXT};
}}
QPushButton:hover {{
    background-color: #34374400;
    border: 1px solid {COLOR_ACCENT};
}}
QPushButton:pressed {{
    background-color: {COLOR_BORDER};
}}

QPushButton#primaryButton {{
    background-color: {COLOR_ACCENT};
    border: 1px solid {COLOR_ACCENT};
    color: #10121a;
    font-weight: 600;
}}
QPushButton#primaryButton:hover {{
    background-color: {COLOR_ACCENT_HOVER};
}}

QPushButton#dangerButton {{
    color: {COLOR_DANGER};
}}
QPushButton#dangerButton:hover {{
    background-color: #3a2626;
    border: 1px solid {COLOR_DANGER};
}}

QPushButton#iconButton {{
    background: transparent;
    border: none;
    padding: 6px;
    border-radius: 8px;
}}
QPushButton#iconButton:hover {{
    background-color: {COLOR_PANEL_ALT};
}}

/* --- Toolbar --- */
#topBar {{
    background-color: {COLOR_PANEL};
    border-bottom: 1px solid {COLOR_BORDER};
}}

/* --- Scrollbars --- */
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 0px;
}}
QScrollBar::handle:vertical {{
    background: {COLOR_BORDER};
    border-radius: 5px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background: {COLOR_ACCENT};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* --- Status bar --- */
QStatusBar {{
    background-color: {COLOR_PANEL};
    color: {COLOR_TEXT_DIM};
    border-top: 1px solid {COLOR_BORDER};
}}

/* --- Message boxes --- */
QMessageBox {{
    background-color: {COLOR_PANEL};
}}
"""
