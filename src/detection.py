import random

def detect_object():

    objects = [
        ("Drone", "THREAT"),
        ("Aircraft", "THREAT"),
        ("Unknown Object", "THREAT"),
        ("Unidentified Object", "THREAT"),
        ("Bird", "NON-THREAT"),
        ("Flock of Birds", "NON-THREAT")
    ]

    detected_object, threat_type = random.choice(objects)

    return detected_object, threat_type
