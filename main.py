from src.detection import detect_object
from src.trajectory import predict_path, restricted_airspace_violation
from src.risk_assessment import assess_risk
from src.alert_system import issue_alert


def main():

    detected_object, threat_type = detect_object()

    print("Detected Object:", detected_object)

    if threat_type == "NON-THREAT":
        print("Status: Natural Aerial Activity")
        print("Action: Normal Monitoring")
        return


    previous_position = (10, 20, 100)
    current_position  = (25, 40, 180)

    next_position = predict_path(previous_position, current_position)

    print("Predicted Path:", next_position)


    restricted_zone_center = (50, 50, 200)
    radius = 100

    violation = restricted_airspace_violation(next_position, restricted_zone_center, radius)

    speed = 160
    altitude_change = 80
    speed_change = 120

    risk = assess_risk(speed, violation, restricted_entry, altitude_change, speed_change)

    action = issue_alert(risk)

    print("\nUAV Risk Assessment Result")
    print("----------------------------")
    print("Risk Level:", risk)
    print("Recommended Actions:")

    for act in action:
        print("-", act)

if __name__ == "__main__":
    main()



#Note:
#All spatial and motion parameters used in this project are simulated units for academic safety monitoring and do not represent real-world operational airspace data.
