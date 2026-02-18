import random

def detect_object():
    objects = ["Drone", "Aircraft", "Unknown Object","Unidentified Object","Drones", "Aircrafts", "Unknown Objects","Unidentified Objects" ]
    detected = random.choice(objects)
    return detected
