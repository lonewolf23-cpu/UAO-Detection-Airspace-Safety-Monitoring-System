import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os

class FrameGenerator:

    def __init__(self, radius=150):

        self.radius = radius

        if not os.path.exists("frames"):
            os.makedirs("frames")

    def generate(self, current_position, predicted_position, frame):

        fig, ax = plt.subplots(figsize=(6,6))

        ax.set_title("Airspace Radar Monitoring")
        ax.set_xlim(-200, 200)
        ax.set_ylim(-200, 200)

        circle = plt.Circle((0,0), self.radius, fill=False)
        ax.add_patch(circle)

        cx, cy, _ = current_position
        px, py, _ = predicted_position

        ax.scatter(cx, cy)
        ax.scatter(px, py, marker="x")

        ax.plot([cx,px], [cy,py])

        plt.savefig(f"frames/frame_{frame:04d}.png")
        plt.close()
