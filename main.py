import time
from src.detection import detect_object
from src.trajectory import predict_path, restricted_airspace_violation
from src.risk_assessment import assess_risk
from src.alert_system import issue_alert

import random

def generate_simulated_motion():

    previous_position = (
        random.randint(0,100),
        random.randint(0,100),
        random.randint(50,200)
    )

    current_position = (
        random.randint(0,100),
        random.randint(0,100),
        random.randint(50,200)
    )

    speed = random.randint(20,200)
    altitude_change = random.randint(10,100)
    speed_change = random.randint(10,150)

    return previous_position, current_position, speed, altitude_change, speed_change

def main():

    detected_object, threat_type = detect_object()

    print("Detected Object:", detected_object)

    if threat_type == "NON-THREAT":
        print("Status: Natural Aerial Activity")
        print("Action: Normal Monitoring")
        return


    previous_position, current_position, speed, altitude_change, speed_change = generate_simulated_motion()

    previous_altitude = previous_position[2]
    current_altitude  = current_position[2]

    next_position = predict_path(previous_position, current_position, previous_altitude, current_altitude)

    print("Predicted Path:", next_position)

    restricted_zone_center = (50, 50, 200)
    radius = 100

    violation = restricted_airspace_violation(next_position, restricted_zone_center, radius)

    risk = assess_risk(speed, violation, altitude_change, speed_change)

    action = issue_alert(risk)

    print("\nUAV Risk Assessment Result")
    print("----------------------------")
    print("Risk Level:", risk)
    print("Recommended Actions:")

    for act in action:
        print("-", act)

if __name__ == "__main__":
    import time

    while True:
        print("\n==============================")
        print(" Airspace Safety Monitoring ")
        print("==============================\n")

        main()

        print("\nNext Scan in 3 seconds...\n")
        time.sleep(3)

#Note:
#All spatial and motion parameters used in this project are simulated units for academic safety monitoring and do not represent real-world operational airspace data.
