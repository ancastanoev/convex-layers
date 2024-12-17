# animation.py
import turtle
import time
import multiprocessing

class TurtleAnimation:
    def __init__(self, dynamic_layers, width=800, height=600, margin=50):

        self.dynamic_layers = dynamic_layers
        self.width = width
        self.height = height
        self.margin = margin

        self.process = None  # To keep track of the animation process

    @staticmethod
    def _compute_scale_and_offset_static(steps, width, height, margin):

        all_x = [p[0] for step in steps for p in step["points"]]
        all_y = [p[1] for step in steps for p in step["points"]]

        if not all_x or not all_y:
            return 1, 0, 0  # Default scale and offsets

        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        data_width = max_x - min_x
        data_height = max_y - min_y

        # Prevent division by zero
        data_width = data_width if data_width != 0 else 1
        data_height = data_height if data_height != 0 else 1

        # Calculate scale to fit points within the window considering margins
        scale_x = (width - 2 * margin) / data_width
        scale_y = (height - 2 * margin) / data_height
        scale = min(scale_x, scale_y)

        # Calculate offsets to center the points
        data_center_x = (min_x + max_x) / 2.0
        data_center_y = (min_y + max_y) / 2.0

        offset_x = -data_center_x * scale
        offset_y = -data_center_y * scale

        return scale, offset_x, offset_y

    @staticmethod
    def _to_screen_coords(x, y, scale, offset_x, offset_y):

        sx = x * scale + offset_x
        sy = y * scale + offset_y
        return sx, sy

    @staticmethod
    def _draw_points(t, points, scale, offset_x, offset_y, color='blue'):

        t.penup()
        t.color(color)
        for p in points:
            x, y = TurtleAnimation._to_screen_coords(p[0], p[1], scale, offset_x, offset_y)
            t.goto(x, y)
            t.dot(5)

    @staticmethod
    def _draw_hull_animated(t, hull, scale, offset_x, offset_y, draw_color='red', final_color='green'):

        if len(hull) == 0:
            return

        # Draw hull in red with animation
        t.color(draw_color)
        t.width(3)
        t.penup()
        x0, y0 = TurtleAnimation._to_screen_coords(hull[0][0], hull[0][1], scale, offset_x, offset_y)
        t.goto(x0, y0)
        t.pendown()

        for i in range(1, len(hull)):
            x, y = TurtleAnimation._to_screen_coords(hull[i][0], hull[i][1], scale, offset_x, offset_y)
            t.goto(x, y)
            time.sleep(0.1)  # Control animation speed

        # Close the hull
        t.goto(x0, y0)
        time.sleep(0.5)

        # Redraw hull in final green color
        t.color(final_color)
        t.width(1)
        t.penup()
        t.goto(x0, y0)
        t.pendown()
        for i in range(1, len(hull)):
            x, y = TurtleAnimation._to_screen_coords(hull[i][0], hull[i][1], scale, offset_x, offset_y)
            t.goto(x, y)
        t.goto(x0, y0)

    @staticmethod
    def _animate(steps, width, height, margin):

        try:
            # Initialize Turtle screen
            screen = turtle.Screen()
            screen.title("Convex Layers Computation Animation")
            screen.setup(width=width, height=height)
            screen.tracer(0)  # Turn off automatic updating for performance

            # Initialize Turtle
            t = turtle.Turtle()
            t.speed(0)
            t.hideturtle()

            # Compute scale and offset based on all steps
            scale, offset_x, offset_y = TurtleAnimation._compute_scale_and_offset_static(steps, width, height, margin)

            for i, step in enumerate(steps):
                screen.title(f"Step {i + 1} of {len(steps)}")

                # Draw remaining points in blue
                TurtleAnimation._draw_points(t, step["points"], scale, offset_x, offset_y, color='blue')

                # Draw current hull
                TurtleAnimation._draw_hull_animated(t, step["current_hull"], scale, offset_x, offset_y, draw_color='red', final_color='green')

                screen.update()  # Update the Turtle screen
                time.sleep(0.2)    # Control animation speed

            turtle.done()

        except turtle.Terminator:
            print("Turtle animation terminated.")
        except Exception as e:
            print(f"An error occurred in Turtle animation: {e}")

    def run_animation(self):
        """
        Start the Turtle animation in a separate process.
        """
        # Check if 'layers' attribute exists in dynamic_layers
        if not hasattr(self.dynamic_layers, 'layers'):
            print("Error: 'DynamicConvexLayers' object has no attribute 'layers'.")
            return

        # Ensure that layers have been computed
        layers = self.dynamic_layers.layers  # Assuming 'layers' is a list of layers
        if not layers:
            print("No layers to animate. Make sure layers are being computed.")
            return

        # Prepare steps data
        steps = []
        remaining_points = self.dynamic_layers.points.copy()  # Assuming 'points' is a list of (x, y) tuples
        for layer in layers:
            steps.append({"points": remaining_points.copy(), "current_hull": layer.copy()})
            # Remove the current hull points from remaining points for the next layer
            remaining_points = [p for p in remaining_points if p not in layer]

        if not steps:
            print("No steps to animate. Ensure that layers are correctly computed.")
            return

        # Start the separate process for animation
        self.process = multiprocessing.Process(target=self._animate, args=(steps, self.width, self.height, self.margin))
        self.process.start()

    def stop_animation(self):

        if self.process and self.process.is_alive():
            self.process.terminate()
            self.process.join()
            self.process = None
