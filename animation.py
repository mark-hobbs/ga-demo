from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Animation:
    def __init__(self, name=None):
        self.name = name or self._generate_animation_name()
        self.frames = []

    @staticmethod
    def _generate_animation_name():
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{timestamp}-animation.gif"

    def save_frame(self, population):
        fig = population.plot()
        subplots = fig.axes
        frame_data = []

        for ax in subplots:
            lines = ax.get_lines()
            if lines:
                line = lines[0]
                frame_data.append((line.get_xdata(), line.get_ydata()))

        self.frames.append(frame_data)
        plt.close(fig)

    def _update(self, frame):
        ncols = 5

        for ax in self.ax.flat:
            ax.clear()
            ax.axis("off")
            ax.set_aspect("equal")

        self.fig.suptitle(f"Generation {frame}")

        for idx, (xdata, ydata) in enumerate(self.frames[frame]):
            ax_parent = self.ax[idx // ncols, idx % ncols]
            ax_parent.plot(xdata, ydata, "o")
            ax_parent.plot(xdata, ydata, "k-", label="Polygon")
            ax_parent.fill(xdata, ydata, "c", alpha=0.3, label="Polygon Area")
            ax_parent.set_aspect("equal")

        return self.ax.flat

    def generate(self):
        num_frames = len(self.frames)
        num_subplots = len(self.frames[0])

        ncols = 5
        nrows = (num_subplots + ncols - 1) // ncols

        self.fig, self.ax = plt.subplots(
            nrows, ncols, figsize=(12, 12), constrained_layout=True
        )
        self.ani = animation.FuncAnimation(
            self.fig, self._update, frames=num_frames, interval=200, blit=False
        )
        self.ani.save(self.name, writer=animation.PillowWriter(fps=5))
