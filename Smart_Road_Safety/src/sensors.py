import random

def get_simulated_data():
    return {
        "traffic_density": random.choice(["Low", "Medium", "High"]),
        "pedestrian_detected": random.choice([True, False]),
        "accident_ahead": random.choice([True, False, False, False]), # 25% chance
        "sign_mode": random.choice(["School", "Hospital", "Default"])
    }