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

        self.fig, self.ax = plt.subplots(
            subplot_kw={"polar": True},
            figsize=(6, 6)
        )
        self.fig.canvas.manager.set_window_title("Live Radar Monitor")

        # Radar limits
        self.ax.set_ylim(0, self.radius)
        self.ax.set_yticks([])
        self.ax.set_xticks([])

        # Grid / rings
        for r in range(30, self.radius + 1, 30):
            self.ax.plot(
                np.linspace(0, 2*np.pi, 300),
                [r]*300,
                color="green",
                alpha=0.15,
                linewidth=1
            )

        # Crosshair
        for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
            self.ax.plot(
                [angle, angle],
                [0, self.radius],
                color="green",
                alpha=0.2,
                linewidth=1
            )

        # Sweep (filled sector)
        self.sweep, = self.ax.fill(
            [], [],
            color="lime",
            alpha=0.25
        )

        # Bright sweep edge
        self.sweep_line, = self.ax.plot(
            [], [],
            color="lime",
            linewidth=2
        )

        # Target blip
        self.scatter = self.ax.scatter(
            [], [],
            s=120,
            c="lime",
            alpha=0.9
        )

        self.anim = FuncAnimation(
            self.fig,
            self._animate,
            interval=40,
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
        self.angle += 0.035
        sweep_width = 0.35

        theta = np.linspace(
            self.angle,
            self.angle + sweep_width,
            100
        )
        r = np.linspace(0, self.radius, 100)

        # Filled sweep
        self.sweep.remove()
        self.sweep, = self.ax.fill(
            np.concatenate([theta, theta[::-1]]),
            np.concatenate([r, np.zeros_like(r)]),
            color="lime",
            alpha=0.18
        )

        # Sweep edge
        self.sweep_line.set_data(theta, r)

        # Target
        if self.target:
            t, r_val = self.target
            self.scatter.set_offsets([[t, r_val]])
        else:
            self.scatter.set_offsets(np.empty((0, 2)))

        return self.sweep_line, self.scatter, self.sweep
