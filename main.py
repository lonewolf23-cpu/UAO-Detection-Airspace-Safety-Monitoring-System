# ==============================
# main.py
# Airspace Safety Monitoring System (LIVE RADAR VERSION)
# ==============================

import signal
import sys
import random
import os
import platform
import pygame
import matplotlib.pyplot as plt

from src.detection import detect_object
from src.frame_generator import FrameGenerator
from src.trajectory import restricted_airspace_violation
from src.risk_assessment import assess_risk
from src.alert_system import issue_alert
from src.advanced_radar import AdvancedRadar   # ✅ ONLY THIS IMPORT


# ------------------------------
# GLOBAL CONFIGURATION
# ------------------------------
restricted_zone_center = (0, 0, 150)
radius = 150

HEADLESS = (
    os.environ.get("CODESPACES") == "true"
    or (
        platform.system() == "Linux"
        and os.environ.get("DISPLAY") is None
    )
)


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
# STOP HANDLER
# ------------------------------
def signal_handler(sig, frame):
    print("\nStopping Airspace Monitoring System...")
    pygame.quit()
    plt.close('all')
    sys.exit(0)


# ------------------------------
# MAIN FUNCTION
# ------------------------------
def main():

    signal.signal(signal.SIGINT, signal_handler)

    # ==========================
    # HEADLESS MODE
    # ==========================
    if HEADLESS:
        print("Headless Mode → Generating 2D Map Frames")

        generator = FrameGenerator(radius=radius)

        for frame in range(300):

            current_position, next_position, speed, altitude_change, speed_change = generate_simulated_motion()

            generator.generate(
                current_position,
                next_position,
                frame
            )

        print("2D Frames Generated Successfully!")
        return


    # ==========================
    # GUI MODE
    # ==========================
    print("GUI Mode → Advanced Radar Activated")

    radar = AdvancedRadar()   # ✅ created ONLY in GUI

    clock = pygame.time.Clock()

    while True:

    clock.tick(2)   # 🔥 THIS CONTROLS THREAT UPDATE SPEED
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        print("\n==============================")
        print(" Airspace Safety Monitoring ")
        print("==============================\n")

        detected_object, threat_type = detect_object()
        print("Detected Object:", detected_object)

        if threat_type == "NON-THREAT":
            print("Status: Natural Activity")
            radar.update(None)
            radar.run_frame()
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
        radar.run_frame()


# ------------------------------
# PROGRAM ENTRY
# ------------------------------
if __name__ == "__main__":
    main()
