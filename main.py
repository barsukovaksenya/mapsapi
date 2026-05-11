import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Карта")
        self.setFixedSize(600, 450)
        self.setStyleSheet("background-color: #ffe0ec;")

        self.lon = 37.620070
        self.lat = 55.753630
        self.zoom = 10

        self.map_label = QLabel(self)
        self.map_label.setGeometry(0, 0, 600, 450)
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.update_map()

    def update_map(self):
        params = {
            "ll": f"{self.lon},{self.lat}",
            "z": str(self.zoom),
            "size": "600,450",
            "l": "map",
        }

        response = requests.get("https://static-maps.yandex.ru/1.x/", params=params)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.map_label.setPixmap(pixmap)
        else:
            self.map_label.setText(f"Ошибка: {response.status_code}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapApp()
    window.show()
    sys.exit(app.exec())