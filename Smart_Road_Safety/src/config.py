import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_KEY = os.getenv("WEATHER_API_KEY")
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = 8883
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")