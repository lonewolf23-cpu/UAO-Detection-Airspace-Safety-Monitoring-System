from src.radar_visualization import show_radar
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

def show_radar(current_position, next_position, restricted_zone_center, radius):

    plt.clf()

    fig = plt.gcf()
    ax = fig.add_subplot(111)

    ax.set_xlim(-200, 200)
    ax.set_ylim(-200, 200)

    radar = plt.Circle(
        (restricted_zone_center[0], restricted_zone_center[1]),
        radius,
        fill=False
    )

    ax.add_patch(radar)

    ax.scatter(current_position[0], current_position[1], marker='o')
    ax.scatter(next_position[0], next_position[1], marker='x')

    ax.plot(
        [current_position[0], next_position[0]],
        [current_position[1], next_position[1]]
    )

    plt.title("Airspace Radar Monitoring")

    plt.pause(0.1)
