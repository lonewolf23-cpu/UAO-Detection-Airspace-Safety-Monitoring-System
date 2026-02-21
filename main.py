# ==============================
# main.py
# Live Airspace Safety Monitoring System
# ==============================

import time
import random

from src.detection import detect_object
from src.trajectory import predict_path, restricted_airspace_violation
from src.risk_assessment import assess_risk
from src.alert_system import issue_alert
from src.live_radar import LiveRadar


# ------------------------------
# GLOBAL CONFIGURATION
# ------------------------------
restricted_zone_center = (0, 0)
radius = 150


# ------------------------------
# SIMULATED MOTION
# ------------------------------
def generate_simulated_motion():
    current_position = (
        random.randint(-120, 120),
        random.randint(-120, 120),
        random.randint(50, 200)
    )

    next_position = (
        current_position[0] + random.randint(-20, 20),
        current_position[1] + random.randint(-20, 20),
        current_position[2]
    )

    speed = random.randint(20, 200)
    altitude_change = random.randint(5, 80)
    speed_change = random.randint(5, 100)

    return current_position, next_position, speed, altitude_change, speed_change


# ------------------------------
# MAIN LOOP
# ------------------------------
def main():

    radar = LiveRadar(radius=radius)

    while True:
        print("\n==============================")
        print(" Airspace Safety Monitoring ")
        print("==============================\n")

        detected_object, threat_type = detect_object()
        print("Detected Object:", detected_object)

        if threat_type == "NON-THREAT":
            print("Status: Natural Activity")
            time.sleep(2)
            radar.update(None)
            continue

        current_position, next_position, speed, altitude_change, speed_change = generate_simulated_motion()

        violation = restricted_airspace_violation(
            next_position,
            restricted_zone_center,
            radius
        )

        risk = assess_risk(speed, violation, altitude_change, speed_change)
        action = issue_alert(risk)

        print("Predicted Path:", next_position)
        print("Risk Level:", risk)

        for act in action:
            print("-", act)

        radar.update(current_position)

        time.sleep(2)


if __name__ == "__main__":
    main()
