# src/live_radar.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class LiveRadar:
    def __init__(self, radius=150):

        self.radius = radius
        self.angle = 0.0
        self.target = None

        plt.style.use("dark_background")

        self.fig, self.ax = plt.subplots(subplot_kw={"polar": True})
        self.fig.canvas.manager.set_window_title("Live Radar Monitor")

        self.ax.set_ylim(0, self.radius)
        self.ax.set_yticks([])
        self.ax.set_xticks([])
        self.ax.grid(color="green", alpha=0.2)

        # Radar sweep
        self.sweep_line, = self.ax.plot(
            [], [], color="lime", linewidth=2, alpha=0.9
        )

        # Target blip
        self.scatter = self.ax.scatter(
            [], [], s=80, c="lime", alpha=0.9
        )

        self.anim = FuncAnimation(
            self.fig,
            self._animate,
            interval=50,
            cache_frame_data=False
        )

        plt.show(block=False)

    def update(self, position):
        if position is None:
            self.target = None
            return

        x, y, _ = position
        r = np.sqrt(x**2 + y**2)

        if r > self.radius:
            self.target = None
            return

        theta = np.arctan2(y, x)
        self.target = (theta, r)

    def _animate(self, frame):
        # Rotate sweep
        self.angle += 0.04
        theta = np.linspace(self.angle, self.angle + 0.03, 100)
        r = np.linspace(0, self.radius, 100)
        self.sweep_line.set_data(theta, r)

        # Update target
        if self.target:
            t, r_val = self.target
            self.scatter.set_offsets([[t, r_val]])
        else:
            self.scatter.set_offsets(np.empty((0, 2)))

        return self.sweep_line, self.scatter
