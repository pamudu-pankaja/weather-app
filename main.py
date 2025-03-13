import sys
import requests
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("Enter a city name: ",self)
        self.city_name=QLineEdit(self)
        self.get_weather_button=QPushButton("Get Weather",self)
        self.temperature_label=QLabel(self)
        self.emoji_label=QLabel(self)
        self.description_label=QLabel(self)
        self.intUI()

    def intUI(self):

        self.setWindowTitle("Weather App")
        self.setGeometry(480,280,40,30)

        vbox=QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_name)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_name.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_name.setObjectName("city_name")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel,QPushButton{
                font-family:calibri;
            }
            QLabel#city_label{
                font-size:40px;
                font-style:italic;
            }

            QLineEdit#city_name{
                font-size:40px;
            }

            QPushButton#get_weather_button{
                font-size:30px;
                font-weight:bold;
            }

            QLabel#temperature_label{
                font-size:75px;
            }

            QLabel#emoji_label{
                font-size:100px;
                font-family:Segoe UI emoji;
            }

            QLabel#description_label{
                font-size:50px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def keyPressEvent(self,event):
        
        if event.key()==16777220:
            self.get_weather()

    def get_weather(self):

        city_name=self.city_name.text()

        api_key="api_key"
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

        try:
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()

            if data["cod"]==200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:

            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nPlease check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self,msg):

        self.description_label.setText("")
        self.emoji_label.setText("")
        self.temperature_label.setStyleSheet("font-size:30px")
        self.temperature_label.setText(msg)

    def display_weather(self,data):

        temp=data["main"]["temp"]
        temp=temp-273.15

        weather_description=data["weather"][0]["description"].capitalize()

        weather_id=data["weather"][0]["id"]

        self.temperature_label.setStyleSheet("font-size:75px;")
        self.temperature_label.setText(f"{temp:.0f}°C")

        self.emoji_label.setText(self.get_emoji(weather_id))

        self.description_label.setText(weather_description)

    @staticmethod

    def get_emoji(weather_id):

        emojis = {
            "thunderstorm": "⛈",
            "drizzle": "🌦",
            "rain": "🌧",
            "snow": "❄",
            "fog": "🌫",
            "volcano": "🌋",
            "wind": "💨",
            "tornado": "🌪",
            "clear": "☀",
            "clouds": "☁",
        }

        if 200 <= weather_id <= 232:
            return emojis["thunderstorm"]
        elif 300 <= weather_id <= 321:
            return emojis["drizzle"]
        elif 500 <= weather_id <= 531:
            return emojis["rain"]
        elif 600 <= weather_id <= 622:
            return emojis["snow"]
        elif 701 <= weather_id <= 741:
            return emojis["fog"]
        elif weather_id == 762:
            return emojis["volcano"]
        elif weather_id == 771:
            return emojis["wind"]
        elif weather_id == 781:
            return emojis["tornado"]
        elif weather_id == 800:
            return emojis["clear"]
        elif 801 <= weather_id <= 804:
            return emojis["clouds"]
        else:
            return ""
    

if __name__=="__main__":
    app=QApplication(sys.argv)
    weather_app=WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
