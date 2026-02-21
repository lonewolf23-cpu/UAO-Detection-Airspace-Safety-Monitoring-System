# src/live_radar.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class LiveRadar:
    def __init__(self, radius=150):

        self.radius = radius
        self.angle = 0
        self.targets = []

        plt.style.use("dark_background")
        self.fig, self.ax = plt.subplots(subplot_kw={"polar": True})
        self.fig.canvas.manager.set_window_title("Live Radar Monitor")

        self.ax.set_ylim(0, self.radius)
        self.ax.set_yticks([])
        self.ax.set_xticks([])

        self.sweep_line, = self.ax.plot([], [], color="lime", linewidth=2)
        self.scatter = self.ax.scatter([], [], color="lime", s=60)

        self.anim = FuncAnimation(
            self.fig,
            self._animate,
            interval=50,
            blit=True
        )

        plt.show(block=False)

    def update(self, position):
        if position:
            x, y, _ = position
            r = np.sqrt(x**2 + y**2)
            theta = np.arctan2(y, x)
            self.targets = [(theta, r)]
        else:
            self.targets = []

    def _animate(self, frame):
        self.angle += 0.05

        theta = np.linspace(self.angle, self.angle + 0.02, 100)
        r = np.linspace(0, self.radius, 100)
        self.sweep_line.set_data(theta, r)

        if self.targets:
            t, r = zip(*self.targets)
            self.scatter.set_offsets(np.c_[t, r])
        else:
            self.scatter.set_offsets([])

        return self.sweep_line, self.scatter
