# Smart-Road-Safety
# Signs with Smart Connectivity for Better Road Safety 🚦🌐

An IoT-based smart traffic management system that utilizes real-time weather data and simulated sensors to enhance road safety through dynamic signage.

## 🚀 Overview
This project replaces static road signs with smart, connected digital displays. It integrates real-time weather APIs to adjust speed limits and uses IoT connectivity (MQTT) to broadcast hazard warnings such as pedestrian presence or traffic congestion to a centralized dashboard and cloud database.

### Core Features
- **Dynamic Speed Limits:** Automatically lowers speed limits based on real-time weather (e.g., Icy/Rainy conditions).
- **Proactive Safety Alerts:** Instant alerts for pedestrian crossings and high traffic density.
- **Cloud Analytics:** All road events are logged to MongoDB Atlas for safety auditing.
- **Live Monitoring:** A professional high-tech dashboard built with Node-RED.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **IoT Protocol:** MQTT (via HiveMQ Cloud)
- **Logic & UI:** Node-RED (Local)
- **Database:** MongoDB Atlas (Cloud NoSQL)
- **Data Source:** OpenWeatherMap API

## 📋 Prerequisites
- Python 3.10+
- Node-RED installed locally (`npm install -g node-red`)
- HiveMQ Cloud Account (Free Tier)
- MongoDB Atlas Account (Free Tier)

## 🔧 Setup Instructions

### 1. Python Environment
Install required libraries:
```bash
pip install paho-mqtt requests pymongo python-dotenv

## 🗄️ Database Structure (MongoDB)
The system uses **MongoDB Atlas** (Cloud NoSQL) to store road safety logs. 

- **Database Name:** `road_safety`
- **Collection Name:** `RoadLogs`

### Sample Document:
Refer to `data/sample_log.json` for the full data structure. Each entry captures the real-time weather conditions alongside the smart sign's decision and simulated sensor events.