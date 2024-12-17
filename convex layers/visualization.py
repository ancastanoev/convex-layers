import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class Visualization:
    def __init__(self, dynamic_layers):
        self.dynamic_layers = dynamic_layers

    def get_static_plot(self):
        fig, ax = plt.subplots()
        points = self.dynamic_layers.get_all_points()  # Retrieve all points
        layers = self.dynamic_layers.get_layers()  # Retrieve each convex layer

        if points.size > 0:
            ax.scatter(points[:, 0], points[:, 1], color='blue', s=10, label='Points')

        for i, layer in enumerate(layers):
            hull_x = np.append(layer[:, 0], layer[0][0])
            hull_y = np.append(layer[:, 1], layer[0][1])
            ax.plot(hull_x, hull_y, '-o', label=f'Layer {i + 1}')

        ax.set_title("Static Convex Layers")
        ax.legend()
        return fig

    def get_animation_plot(self):
        fig, ax = plt.subplots()
        steps = self.dynamic_layers.get_computation_steps()

        # if no steps, no animation
        if not steps:
            ax.set_title("No layers to compute.")
            return None, fig

        def init():
            ax.clear()
            ax.set_title("Convex Layers Computation Animation")
            return []

        def update(frame):
            ax.clear()
            step = steps[frame]

            #the steps below are from teh convex layers class
            points = np.array(step["points"])
            current_hull = np.array(step["current_hull"])

            if len(points) > 0:
                ax.scatter(points[:, 0], points[:, 1], color='blue', s=10, label='Remaining Points')

            if len(current_hull) > 0:
                hull_x = np.append(current_hull[:, 0], current_hull[0][0])
                hull_y = np.append(current_hull[:, 1], current_hull[0][1])
                ax.plot(hull_x, hull_y, '-o', color='red', label='Current Hull')

            ax.set_title(f"Step {frame + 1}/{len(steps)}")
            ax.legend()
            return []

        ani = animation.FuncAnimation(fig, update, frames=len(steps), init_func=init, blit=False, interval=1000,
                                      repeat=False)
        return ani, fig
