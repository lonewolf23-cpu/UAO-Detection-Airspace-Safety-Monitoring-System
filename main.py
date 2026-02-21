# ==============================
# main.py
# Airspace Safety Monitoring System
# ==============================

import time
import random

# ==============================
# RADAR MODE SWITCH
# ==============================
USE_LIVE_RADAR = True   # True = Live external radar (Windows/local)
                        # False = Frame-based radar (Codespaces)

if USE_LIVE_RADAR:
    from src.live_radar import show_live_radar
else:
    from src.radar_visualization import show_radar


from src.detection import detect_object
from src.trajectory import predict_path, restricted_airspace_violation
from src.risk_assessment import assess_risk
from src.alert_system import issue_alert


# ==============================
# GLOBAL CONFIGURATION
# ==============================
restricted_zone_center = (50, 50, 200)
radius = 100
step = 0   # used only for frame-based radar


# ==============================
# SIMULATED MOTION GENERATOR
# ==============================
def generate_simulated_motion():

    previous_position = (
        random.randint(0, 100),
        random.randint(0, 100),
        random.randint(50, 200)
    )

    current_position = (
        random.randint(0, 100),
        random.randint(0, 100),
        random.randint(50, 200)
    )

    speed = random.randint(20, 200)
    altitude_change = random.randint(10, 100)
    speed_change = random.randint(10, 150)

    return previous_position, current_position, speed, altitude_change, speed_change


# ==============================
# MAIN SYSTEM LOGIC
# ==============================
def main():
    global step

    detected_object, threat_type = detect_object()
    print("Detected Object:", detected_object)

    # Ignore natural aerial objects
    if threat_type == "NON-THREAT":
        print("Status: Natural Aerial Activity")
        print("Action: Normal Monitoring")
        return

    previous_position, current_position, speed, altitude_change, speed_change = generate_simulated_motion()

    previous_altitude = previous_position[2]
    current_altitude = current_position[2]

    # Predict next position
    next_position = predict_path(
        previous_position,
        current_position,
        previous_altitude,
        current_altitude
    )

    print("Predicted Path:", next_position)

    # ==============================
    # RADAR VISUALIZATION
    # ==============================
    if USE_LIVE_RADAR:
        show_live_radar(
            current_position,
            next_position,
            restricted_zone_center,
            radius
        )
    else:
        step += 1
        show_radar(
            current_position,
            next_position,
            restricted_zone_center,
            radius,
            step
        )

    # ==============================
    # RISK ANALYSIS
    # ==============================
    violation = restricted_airspace_violation(
        next_position,
        restricted_zone_center,
        radius
    )

    risk = assess_risk(speed, violation, altitude_change, speed_change)
    action = issue_alert(risk)

    print("\nUAV Risk Assessment Result")
    print("----------------------------")
    print("Risk Level:", risk)
    print("Recommended Actions:")
    for act in action:
        print("-", act)


# ==============================
# CONTINUOUS MONITORING LOOP
# ==============================
if __name__ == "__main__":

    while True:
        print("\n==============================")
        print(" Airspace Safety Monitoring ")
        print("==============================\n")

        main()

        time.sleep(1)   # smoother animation for live radar


# NOTE:
# All spatial and motion parameters used in this project are simulated units
# for academic airspace safety monitoring only.
