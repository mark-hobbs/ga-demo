from datetime import datetime
import copy

import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Animation:
    def __init__(self, name=None):
        """
        Initialise the Animation object

        Parameters
        ----------
        name : str, optional
            The name of the animation file to be saved. If not provided, a default
            name based on the timestamp will be generated.
        """
        self.name = name or self._generate_animation_name()
        self.frames = []

    @staticmethod
    def _generate_animation_name():
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{timestamp}-animation.gif"

    def save_frame(self, population):
        """
        Append subplot data to self.frames list
        """
        fig = population.plot()
        subplots = fig.axes
        self.frames.append([copy.deepcopy(ax) for ax in subplots])
        plt.close(fig)

    def _update(self, frame):
        """
        Update the plot for each frame in the animation

        Notes
        -----
        Required signature: `def func(frame, *fargs) -> iterable_of_artists`
        """
        ncols = 5

        for ax in self.ax.flat:
            ax.clear()
            ax.axis("off")
            ax.set_aspect("equal")

        self.fig.suptitle(f"Generation {frame}")

        for idx, ax in enumerate(self.frames[frame]):
            ax_parent = self.ax[idx // ncols, idx % ncols]
            current_plot = ax.lines[0]
            ax_parent.plot(current_plot.get_xdata(), current_plot.get_ydata(), "o")
            ax_parent.plot(
                current_plot.get_xdata(),
                current_plot.get_ydata(),
                "k-",
                label="Polygon",
            )
            ax_parent.fill(
                current_plot.get_xdata(),
                current_plot.get_ydata(),
                "c",
                alpha=0.3,
                label="Polygon Area",
            )
            ax_parent.set_aspect("equal")

        return self.ax.flat

    def generate(self):
        """
        Generate an animation from the saved frames (matplotlib.figure.Figure
        objects)
        """
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
