import random

def detect_object():
    
    objects = [
        "Drone",
        "Aircraft",
        "Unknown Object",
        "Unidentified Object",
        "Bird",
        "Flock of Birds",
        "Drones",
        "Aircrafts",
        "Unknown Objects",
        "Unidentified Objects",
        "Birds"
    ]

    detected = random.choice(objects)

    if detected == "Bird" or detected == "Flock of Birds":
        return detected, "NON-THREAT"
    
    else:
        return detected
