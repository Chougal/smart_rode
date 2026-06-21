import paho.mqtt.client as mqtt
import requests
import json
import time
import random
import urllib.parse
from datetime import datetime

# ── Credentials ──────────────────────────────────────────────
WEATHER_API_KEY = "1a0614be2518aedd0354ee777eb05469"
MQTT_BROKER     = "e9fb3eab747948d6a0c89cfad05dba79.s1.eu.hivemq.cloud"
MQTT_PORT       = 8883
MQTT_USER       = "Ritesh"
MQTT_PASS       = "Ritesh00@@"
MQTT_TOPIC      = "road/safety"

# ── Testing Scenarios ────────────────────────────────────────
# "Ushuaia" is currently COLD (~2°C). 
# This will trigger the "Slippery Road" smart logic automatically.
CITY = "Ushuaia"   

# ── MongoDB Connection ───────────────────────────────────────
raw_password = os.getenv("MONGO_PASS")
encoded_password = urllib.parse.quote_plus(raw_password)
MONGO_URI = f"mongodb+srv://rcklimble95_db_user:{encoded_password}@cluster0.c3fgi9m.mongodb.net/road_safety?retryWrites=true&w=majority"

try:
    from pymongo import MongoClient
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client["road_safety"]
    logs_collection = db["RoadLogs"]
    MONGO_ENABLED = True
    print("✅ MongoDB: Connection established!")
except Exception as e:
    MONGO_ENABLED = False
    print(f"⚠️  MongoDB: Error {e}. Continuing without logging.")

# ── MQTT Setup (Updated to Version 2 to remove warning) ──────
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ HiveMQ: Connected successfully!")
    else:
        print(f"❌ HiveMQ: Connection failed. Code: {rc}")

def on_publish(client, userdata, mid, reason_code=None, properties=None):
    print(f"📤 MQTT: Data published to cloud.")

# Using CallbackAPIVersion.VERSION2 for the latest library support
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="SmartRoadSign")
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.tls_set()
client.on_connect = on_connect
client.on_publish = on_publish

print(f"🔌 HiveMQ: Connecting to {MQTT_BROKER}...")
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
except Exception as e:
    print(f"❌ HiveMQ: Could not connect. {e}")
    exit()

# ── Weather Fetcher ───────────────────────────────────────────
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get("cod") != 200:
            raise Exception(data.get("message"))
        
        temp        = data["main"]["temp"]
        condition   = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        print(f"🌤️  Weather: {city} is {description} ({temp}°C)")
        return temp, condition
    except Exception as e:
        print(f"⚠️  Weather API error: {e}. Using defaults.")
        return 20.0, "Clear"

# ── Smart Sign Logic ──────────────────────────────────────────
def decide_speed_and_alert(temp, condition):
    # Scenario 1: Icy / Snow (Smart Safety Measure)
    if condition in ["Snow", "Sleet"] or temp < 5:
        return 30, "⚠️ Slippery Road - Drive Slow!"

    # Scenario 2: Heavy Rain / Drizzle
    if condition in ["Thunderstorm", "Drizzle", "Rain"]:
        return 40, "🌧️ Wet Road - Reduce Speed!"

    # Normal conditions
    return 60, "✅ Road Clear - Safe to Drive"

# ── Simulate Random Sensor Events ────────────────────────────
def get_random_events():
    # Scenario 3: Pedestrian crossing (20% chance)
    pedestrian = random.random() < 0.20
    # Scenario 4: Traffic level
    traffic = random.choice(["Low", "Medium", "High"])
    return pedestrian, traffic

# ── Main Project Loop ─────────────────────────────────────────
print("\n🚦 SMART ROAD SAFETY SIGN SYSTEM ACTIVE")
print(f"📍 Monitoring City: {CITY}")
print("─" * 50)

try:
    while True:
        # 1. Gather Data (API + Simulated Sensors)
        temp, condition = get_weather(CITY)
        pedestrian, traffic = get_random_events()

        # 2. Process Data (Decision Making Logic)
        speed_limit, alert = decide_speed_and_alert(temp, condition)

        # Priority Override: Pedestrian safety is #1
        if pedestrian:
            speed_limit = 0
            alert = "🚶 Pedestrian Crossing: STOP!"
        # Priority Override: Traffic management
        elif traffic == "High":
            alert = "🚗 Heavy Traffic - Take Alt Route!"

        # 3. Build IoT Payload
        payload = {
            "city":        CITY,
            "speed_limit": speed_limit,
            "alert":       alert,
            "temperature": temp,
            "weather":     condition,
            "pedestrian":  pedestrian,
            "traffic":     traffic,
            "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # 4. Publish to Cloud (HiveMQ -> Node-RED)
        client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)

        # 5. Store in Cloud Database (MongoDB Atlas)
        if MONGO_ENABLED:
            try:
                logs_collection.insert_one(payload.copy())
                print("💾 Database: Entry saved to MongoDB.")
            except Exception as e:
                print(f"⚠️  Database error: {e}")

        # Local Monitoring Print
        print(f"📊 Status: {alert} | Speed: {speed_limit}km/h")
        print("─" * 50)
        
        time.sleep(10)

except KeyboardInterrupt:
    print("\n🛑 System stopping...")
    client.loop_stop()
    client.disconnect()
    if MONGO_ENABLED:
        mongo_client.close()
    print("✅ System offline.")