import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt



class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Карта")
        self.setFixedSize(600, 500)
        self.setStyleSheet("background-color: #ffe0ec;")

        self.lon = 37.620070
        self.lat = 55.753630
        self.zoom = 10
        self.theme = "light"

        self.map_label = QLabel(self)
        self.map_label.setGeometry(0, 0, 600, 450)
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.theme_checkbox = QCheckBox("Тёмная тема", self)
        self.theme_checkbox.setGeometry(10, 460, 200, 30)
        self.theme_checkbox.setStyleSheet("color: #d63384; font-size: 14px;")
        self.theme_checkbox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.theme_checkbox.stateChanged.connect(self.change_theme)

        self.update_map()

    def update_map(self):
        params = {
            "ll": f"{self.lon},{self.lat}",
            "z": str(self.zoom),
            "size": "600,450",
            "apikey": "922bfd59-b49e-4833-b597-11a936859a60",
            "theme": self.theme,
        }

        response = requests.get("https://static-maps.yandex.ru/v1", params=params)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.map_label.setPixmap(pixmap)
        else:
            self.map_label.setText(f"Ошибка: {response.status_code}")

    def change_theme(self):
        if self.theme_checkbox.isChecked():
            self.theme = "dark"
        else:
            self.theme = "light"
        self.update_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp and self.zoom < 17:
            self.zoom += 1
            self.update_map()
        elif event.key() == Qt.Key.Key_PageDown and self.zoom > 0:
            self.zoom -= 1
            self.update_map()

        step = 360 / (2 ** self.zoom) * 0.1

        if event.key() == Qt.Key.Key_Up:
            self.lat = min(85, self.lat + step)
            self.update_map()
        elif event.key() == Qt.Key.Key_Down:
            self.lat = max(-85, self.lat - step)
            self.update_map()
        elif event.key() == Qt.Key.Key_Right:
            self.lon = min(180, self.lon + step)
            self.update_map()
        elif event.key() == Qt.Key.Key_Left:
            self.lon = max(-180, self.lon - step)
            self.update_map()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapApp()
    window.show()
    sys.exit(app.exec())