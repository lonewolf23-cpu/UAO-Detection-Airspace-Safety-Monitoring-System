import numpy as np

def predict_path(previous_position, current_position,previous_altitude,current_altitude):
    
    x1, y1, z1 = previous_position
    x2, y2, z2 = current_position
    z1 = previous_altitude
    z2 = current_altitude

    velocity_x = x2 - x1
    velocity_y = y2 - y1
    velocity_z = z2 - z1

    next_x = x2 + velocity_x
    next_y = y2 + velocity_y
    next_z = z2 + velocity_z

    return (next_x, next_y, next_z)


def restricted_airspace_violation(object_position, zone_center, radius):

    ox, oy, oz = object_position
    zx, zy, zz = zone_center

    distance = ((ox - zx)**2 + (oy - zy)**2 + (oz - zz)**2) ** 0.5

    if distance <= radius:
        return True
    else:
        return False


def restricted_airspace_violation(object_position, zone_center, radius):

    ox, oy, oz = object_position
    zx, zy, zz = zone_center

    distance = ((ox - zx)**2 + (oy - zy)**2 + (oz - zz)**2) ** 0.5

    if distance <= radius:
        return True
    else:
        return False
