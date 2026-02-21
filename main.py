# ==============================
# main.py
# Airspace Safety Monitoring System (LIVE RADAR VERSION)
# ==============================

import random
import matplotlib.pyplot as plt

from src.detection import detect_object
from src.trajectory import predict_path, restricted_airspace_violation
from src.risk_assessment import assess_risk
from src.alert_system import issue_alert
from src.live_radar import LiveRadar


# ------------------------------
# GLOBAL CONFIGURATION
# ------------------------------
restricted_zone_center = (0, 0, 150)   # MUST be 3D (x, y, z)
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
# MAIN FUNCTION
# ------------------------------
def main():

    radar = LiveRadar(radius=radius)

    while True:
        print("\n==============================")
        print(" Airspace Safety Monitoring ")
        print("==============================\n")

        detected_object, threat_type = detect_object()
        print("Detected Object:", detected_object)

        # Ignore natural activity
        if threat_type == "NON-THREAT":
            print("Status: Natural Activity")
            radar.update(None)
            plt.pause(1.5)
            continue

        current_position, next_position, speed, altitude_change, speed_change = generate_simulated_motion()

        print("Predicted Path:", next_position)

        violation = restricted_airspace_violation(
            next_position,
            restricted_zone_center,
            radius
        )

        risk = assess_risk(speed, violation, altitude_change, speed_change)
        actions = issue_alert(risk)

        print("Risk Level:", risk)
        for act in actions:
            print("-", act)

        radar.update(current_position)

        # IMPORTANT: keep GUI responsive
        plt.pause(1.5)


# ------------------------------
# PROGRAM ENTRY POINT
# ------------------------------
if __name__ == "__main__":
    main()
