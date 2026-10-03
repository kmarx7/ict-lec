APP_STYLESHEET = """
QMainWindow, QWidget#appRoot {
    background: #F6F7F9;
    color: #181A1F;
}
QWidget {
    font-family: "SF Pro Text", "Inter", "Helvetica Neue";
    font-size: 13px;
}
QWidget#sidebar {
    background: #ECEEF2;
    border-right: 1px solid #D9DCE2;
}
QLabel#brandMark {
    background: #15171B;
    color: white;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 700;
}
QLabel#brandName {
    color: #15171B;
    font-size: 14px;
    font-weight: 650;
}
QLabel#brandCaption, QLabel#eyebrow, QLabel#secondaryText, QLabel#panelDescription {
    color: #70747D;
}
QLabel#eyebrow {
    font-size: 11px;
    font-weight: 700;
}
QListWidget#navigation {
    background: transparent;
    border: 0;
    outline: 0;
}
QListWidget#navigation::item {
    color: #4C5059;
    padding: 10px 12px;
    margin: 2px 0;
    border-radius: 7px;
}
QListWidget#navigation::item:hover {
    background: #E1E3E8;
    color: #181A1F;
}
QListWidget#navigation::item:selected {
    background: #D8DBE2;
    color: #111318;
    font-weight: 650;
}
QLabel#pageTitle {
    color: #111318;
    font-size: 27px;
    font-weight: 700;
}
QLabel#pageDescription {
    color: #696E78;
    font-size: 14px;
}
QFrame#panel {
    background: #FFFFFF;
    border: 1px solid #E0E2E7;
    border-radius: 10px;
}
QLabel#panelTitle {
    color: #202228;
    font-size: 14px;
    font-weight: 650;
}
QLabel#fieldLabel {
    color: #34373E;
    font-size: 12px;
    font-weight: 650;
}
QLineEdit {
    min-height: 22px;
    padding: 9px 11px;
    color: #181A1F;
    background: #FFFFFF;
    border: 1px solid #C9CDD5;
    border-radius: 7px;
    selection-background-color: #2F6FEB;
}
QLineEdit:hover { border-color: #9CA2AD; }
QLineEdit:focus { border: 2px solid #3478F6; padding: 8px 10px; }
QPushButton {
    min-height: 22px;
    padding: 8px 14px;
    background: #FFFFFF;
    color: #272A30;
    border: 1px solid #C9CDD5;
    border-radius: 7px;
    font-weight: 600;
}
QPushButton:hover { background: #F2F3F5; border-color: #ADB2BC; }
QPushButton:pressed { background: #E8EAEF; }
QPushButton:disabled { color: #A6AAB2; background: transparent; border-color: transparent; }
QPushButton#primaryButton {
    background: #1F6FEB;
    color: white;
    border-color: #1F6FEB;
}
QPushButton#primaryButton:hover { background: #1763D6; border-color: #1763D6; }
QPushButton#quietButton { background: transparent; border-color: transparent; }
QPushButton#quietButton:hover { background: #E5E7EB; }
QLabel#securityNote {
    color: #555A64;
    background: #F3F6FB;
    border: 1px solid #DCE5F3;
    border-radius: 8px;
    padding: 11px 13px;
}
QLabel#statusBadge {
    color: #17653A;
    background: #E8F6EE;
    border: 1px solid #CBE9D7;
    border-radius: 9px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 650;
}
QLabel#statusBadge[state="running"] { color: #1F5FAE; background: #EAF2FE; border-color: #C9DDF9; }
QLabel#statusBadge[state="error"] { color: #A33A2B; background: #FCEDEA; border-color: #F2CFC7; }
QLabel#statusBadge[state="success"] { color: #17653A; background: #E8F6EE; border-color: #CBE9D7; }
QSplitter::handle { background: transparent; width: 12px; }
QListWidget#timeline {
    background: #FFFFFF;
    border: 1px solid #E0E2E7;
    border-radius: 10px;
    outline: 0;
    padding: 8px;
}
QListWidget#timeline::item {
    color: #34373E;
    padding: 10px 9px;
    border-bottom: 1px solid #ECEEF2;
}
QProgressBar {
    min-height: 5px;
    max-height: 5px;
    background: #E4E7EC;
    border: 0;
    border-radius: 2px;
    text-align: center;
}
QProgressBar::chunk { background: #3478F6; border-radius: 2px; }
QTableWidget {
    background: #FFFFFF;
    alternate-background-color: #FAFAFB;
    border: 1px solid #E0E2E7;
    border-radius: 10px;
    gridline-color: transparent;
    selection-background-color: #E8F0FE;
    selection-color: #181A1F;
    outline: 0;
}
QTableWidget::item { padding: 8px; border-bottom: 1px solid #ECEEF2; }
QHeaderView::section {
    background: #F5F6F8;
    color: #666B74;
    border: 0;
    border-bottom: 1px solid #DEE1E6;
    padding: 9px;
    font-size: 11px;
    font-weight: 700;
}
QScrollBar:vertical { width: 10px; background: transparent; margin: 3px; }
QScrollBar::handle:vertical { background: #C5C8CE; border-radius: 4px; min-height: 28px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""
