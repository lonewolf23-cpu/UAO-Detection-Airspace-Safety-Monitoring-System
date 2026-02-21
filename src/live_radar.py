import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge
import time
import math

plt.ion()

# Radar display setup
fig, ax = plt.subplots(figsize=(7, 7))
fig.canvas.manager.set_window_title("Live Airspace Radar")

SWEEP_ANGLE = 0


def show_live_radar(current_position, next_position, restricted_zone_center, radius):
    global SWEEP_ANGLE

    ax.clear()

    # Radar limits
    ax.set_xlim(-200, 200)
    ax.set_ylim(-200, 200)
    ax.set_aspect("equal")
    ax.axis("off")

    # Background
    ax.set_facecolor("#001010")
    fig.patch.set_facecolor("#001010")

    # Radar grid rings
    for r in range(50, 201, 50):
        ax.add_patch(
            Circle((0, 0), r, fill=False, color="#00ff99", alpha=0.2)
        )

    # Cross lines
    ax.plot([-200, 200], [0, 0], color="#00ff99", alpha=0.2)
    ax.plot([0, 0], [-200, 200], color="#00ff99", alpha=0.2)

    # Rotating sweep beam
    sweep = Wedge(
        (0, 0),
        200,
        SWEEP_ANGLE,
        SWEEP_ANGLE + 25,
        color="#00ff99",
        alpha=0.25
    )
    ax.add_patch(sweep)

    SWEEP_ANGLE = (SWEEP_ANGLE + 8) % 360

    # Restricted airspace
    ax.add_patch(
        Circle(
            (restricted_zone_center[0], restricted_zone_center[1]),
            radius,
            fill=False,
            edgecolor="red",
            linewidth=2
        )
    )

    # UAV current position
    ax.scatter(
        current_position[0],
        current_position[1],
        color="#00ff00",
        s=40
    )

    # Predicted position
    ax.scatter(
        next_position[0],
        next_position[1],
        color="yellow",
        marker="x",
        s=60
    )

    # Trajectory line
    ax.plot(
        [current_position[0], next_position[0]],
        [current_position[1], next_position[1]],
        color="#00ff99",
        linewidth=1
    )

    # HUD text
    ax.text(
        -190,
        185,
        f"SCAN TIME: {time.strftime('%H:%M:%S')}",
        color="#00ff99",
        fontsize=9
    )

    ax.text(
        -190,
        170,
        "MODE: LIVE TRACKING",
        color="#00ff99",
        fontsize=9
    )

    plt.draw()
    plt.pause(0.05)
