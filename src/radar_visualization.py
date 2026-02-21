import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os


def show_radar(current_position, next_position, restricted_zone_center, radius, step):

    if not os.path.exists("radar_frames"):
        os.makedirs("radar_frames")

    plt.figure(figsize=(6, 6))

    plt.xlim(-200, 200)
    plt.ylim(-200, 200)

    # Restricted airspace
    circle = plt.Circle(
        (restricted_zone_center[0], restricted_zone_center[1]),
        radius,
        fill=False
    )
    plt.gca().add_patch(circle)

    # UAV current & predicted position
    plt.scatter(current_position[0], current_position[1], label="Current Position")
    plt.scatter(next_position[0], next_position[1], marker="x", label="Predicted Position")

    # Path line
    plt.plot(
        [current_position[0], next_position[0]],
        [current_position[1], next_position[1]]
    )

    plt.title("Airspace Radar Monitoring")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()

    filename = f"radar_frames/frame_{step}.png"
    plt.savefig(filename)
    plt.close()
