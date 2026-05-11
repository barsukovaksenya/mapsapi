import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt



class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Карта")
        self.setFixedSize(600, 600)
        self.setStyleSheet("background-color: #ffe0ec;")

        self.lon = 37.620070
        self.lat = 55.753630
        self.zoom = 10
        self.theme = "light"
        self.marker = None
        self.current_address = ""
        self.current_postal = ""

        self.map_label = QLabel(self)
        self.map_label.setGeometry(0, 0, 600, 450)
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.theme_checkbox = QCheckBox("Тёмная тема", self)
        self.theme_checkbox.setGeometry(10, 460, 150, 30)
        self.theme_checkbox.setStyleSheet("color: #d63384; font-size: 14px;")
        self.theme_checkbox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.theme_checkbox.stateChanged.connect(self.change_theme)

        self.search_input = QLineEdit(self)
        self.search_input.setGeometry(10, 500, 480, 30)
        self.search_input.setPlaceholderText("Введите адрес...")
        self.search_input.setStyleSheet("background: white; border: 2px solid #d63384; border-radius: 5px; padding: 2px;")
        self.search_input.returnPressed.connect(self.search)

        self.search_button = QPushButton("Искать", self)
        self.search_button.setGeometry(500, 500, 90, 30)
        self.search_button.setStyleSheet("background: #d63384; color: white; border: none; border-radius: 5px; font-size: 14px;")
        self.search_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.search_button.clicked.connect(self.search)

        self.reset_button = QPushButton("Сброс", self)
        self.reset_button.setGeometry(170, 460, 90, 30)
        self.reset_button.setStyleSheet("background: #d63384; color: white; border: none; border-radius: 5px; font-size: 14px;")
        self.reset_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.reset_button.clicked.connect(self.reset_search)

        self.address_label = QLabel(self)
        self.address_label.setGeometry(270, 460, 320, 30)
        self.address_label.setStyleSheet("color: #d63384; font-size: 12px;")

        self.search_input.setGeometry(10, 530, 400, 30)
        self.search_button.setGeometry(420, 530, 80, 30)

        self.postal_checkbox = QCheckBox("Почтовый индекс", self)
        self.postal_checkbox.setGeometry(10, 500, 200, 30)
        self.postal_checkbox.setStyleSheet("color: #d63384; font-size: 14px;")
        self.postal_checkbox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.postal_checkbox.stateChanged.connect(self.update_address)

        self.update_map()

    def update_map(self):
        params = {
            "ll": f"{self.lon},{self.lat}",
            "z": str(self.zoom),
            "size": "600,450",
            "apikey": "922bfd59-b49e-4833-b597-11a936859a60",
            "theme": self.theme,
        }
        if self.marker:
            params["pt"] = f"{self.marker},pm2rdl"

        response = requests.get("https://static-maps.yandex.ru/v1", params=params,
                                headers={"Referer": "http://localhost"})
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.map_label.setPixmap(pixmap)
        else:
            self.map_label.setText(f"Ошибка: {response.status_code}")

    def search(self):
        query = self.search_input.text().strip()
        if not query:
            return
        params = {
            "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
            "geocode": query,
            "format": "json",
        }
        response = requests.get("http://geocode-maps.yandex.ru/1.x/", params=params)
        if not response:
            return
        json_response = response.json()
        members = json_response["response"]["GeoObjectCollection"]["featureMember"]
        if not members:
            return
        toponym = members[0]["GeoObject"]
        coords = toponym["Point"]["pos"]
        self.lon, self.lat = [float(x) for x in coords.split(" ")]
        self.marker = f"{self.lon},{self.lat}"
        self.current_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        postal = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"].get("postal_code", "")
        self.current_postal = postal
        self.update_address()
        self.search_input.clearFocus()
        self.update_map()

    def reset_search(self):
        self.marker = None
        self.current_address = ""
        self.current_postal = ""
        self.search_input.clear()
        self.address_label.clear()
        self.update_map()

    def update_address(self):
        if self.current_address:
            text = self.current_address
            if self.postal_checkbox.isChecked() and self.current_postal:
                text += ", " + self.current_postal
            self.address_label.setText(text)

    def change_theme(self):
        if self.theme_checkbox.isChecked():
            self.theme = "dark"
        else:
            self.theme = "light"
        self.update_map()

    def keyPressEvent(self, event):
        if self.search_input.hasFocus():
            return

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