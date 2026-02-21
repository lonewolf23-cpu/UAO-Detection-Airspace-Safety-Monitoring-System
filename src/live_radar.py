# src/live_radar.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class LiveRadar:
    def __init__(self, radius=150):

        self.radius = radius
        self.angle = 0.0
        self.target = None
        self.history = []   # afterglow memory

        plt.style.use("dark_background")

        self.fig, self.ax = plt.subplots(
            subplot_kw={"polar": True},
            figsize=(7, 7)
        )
        self.fig.canvas.manager.set_window_title("Advanced Radar Display")

        self.ax.set_ylim(0, self.radius)
        self.ax.set_yticks([])
        self.ax.set_xticks([])
        self.ax.set_facecolor("#020a02")

        # Radar rings
        for r in range(25, self.radius + 1, 25):
            self.ax.plot(
                np.linspace(0, 2*np.pi, 360),
                [r]*360,
                color="#00ff66",
                alpha=0.08,
                linewidth=1
            )

        # Crosshair
        for a in [0, np.pi/2, np.pi, 3*np.pi/2]:
            self.ax.plot(
                [a, a],
                [0, self.radius],
                color="#00ff66",
                alpha=0.15,
                linewidth=1
            )

        # Noise clutter (static)
        noise_theta = np.random.uniform(0, 2*np.pi, 400)
        noise_r = np.random.uniform(0, self.radius, 400)
        self.ax.scatter(
            noise_theta,
            noise_r,
            s=2,
            c="#00ff66",
            alpha=0.03
        )

        # Sweep glow (sector)
        self.sweep, = self.ax.fill([], [], color="#00ff66", alpha=0.25)
        self.sweep_edge, = self.ax.plot([], [], color="#66ff99", linewidth=2)

        # Target afterglow points
        self.glow = self.ax.scatter([], [], s=120, c="#66ff99", alpha=0.4)

        # Main target
        self.target_dot = self.ax.scatter([], [], s=160, c="#00ff66", alpha=1)

        self.anim = FuncAnimation(
            self.fig,
            self._animate,
            interval=35,
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
            return

        theta = np.arctan2(y, x)
        self.target = (theta, r)

        # store history for glow
        self.history.append((theta, r))
        if len(self.history) > 15:
            self.history.pop(0)

    def _animate(self, frame):
        self.angle += 0.035
        sweep_width = 0.45

        theta = np.linspace(self.angle, self.angle + sweep_width, 200)
        r = np.linspace(0, self.radius, 200)

        # redraw sweep
        self.sweep.remove()
        self.sweep, = self.ax.fill(
            np.concatenate([theta, theta[::-1]]),
            np.concatenate([r, np.zeros_like(r)]),
            color="#00ff66",
            alpha=0.18
        )
        self.sweep_edge.set_data(theta, r)

        # afterglow
        if self.history:
            ht, hr = zip(*self.history)
            self.glow.set_offsets(np.c_[ht, hr])
        else:
            self.glow.set_offsets(np.empty((0, 2)))

        # main target
        if self.target:
            self.target_dot.set_offsets([[self.target[0], self.target[1]]])
        else:
            self.target_dot.set_offsets(np.empty((0, 2)))

        return self.sweep, self.sweep_edge, self.glow, self.target_dot
