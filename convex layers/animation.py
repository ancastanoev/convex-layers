# animation.py
import turtle
import time
import numpy as np

class TurtleAnimation:
    def __init__(self, dynamic_layers, width=800, height=600, margin=50):

        self.dynamic_layers = dynamic_layers
        self.width = width
        self.height = height
        self.margin = margin

        self.screen = turtle.Screen()
        self.screen.title("Convex Layers Computation Animation")
        self.screen.setup(width=self.width, height=self.height)

        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.hideturtle()

        self.scale = 1
        self.offset_x = 0
        self.offset_y = 0

    def _compute_scale_and_offset(self, steps):

        #we compute the scale and offset so that points fit within the Turtle window

        all_x = [p[0] for step in steps for p in step["points"]]
        all_y = [p[1] for step in steps for p in step["points"]]

        if not all_x or not all_y:
            return

        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        data_width = max_x - min_x
        data_height = max_y - min_y

        if data_width == 0:
            data_width = 1
        if data_height == 0:
            data_height = 1

        # calculate scale to fit points in window
        scale_x = (self.width - 2 * self.margin) / data_width
        scale_y = (self.height - 2 * self.margin) / data_height
        self.scale = min(scale_x, scale_y)

        # offset to center the points
        data_center_x = (min_x + max_x) / 2.0
        data_center_y = (min_y + max_y) / 2.0

        self.offset_x = -data_center_x * self.scale
        self.offset_y = -data_center_y * self.scale

    def _to_screen_coords(self, x, y):
       #we convert points to turtle screen coordinates

        sx = x * self.scale + self.offset_x
        sy = y * self.scale + self.offset_y
        return sx, sy

    def _draw_points(self, points, color='blue'):

        self.t.penup()
        self.t.color(color)
        for p in points:
            x, y = self._to_screen_coords(p[0], p[1])
            self.t.goto(x, y)
            self.t.dot(5)

    def _draw_hull_animated(self, hull, draw_color='red', final_color='green'):

        if len(hull) == 0:
            return

        # Draw hull in red with animation
        self.t.color(draw_color)
        self.t.width(3)
        self.t.penup()
        x0, y0 = self._to_screen_coords(hull[0][0], hull[0][1])
        self.t.goto(x0, y0)
        self.t.pendown()

        for i in range(1, len(hull)):
            x, y = self._to_screen_coords(hull[i][0], hull[i][1])
            self.t.goto(x, y)
            time.sleep(0.1)

        # close the hull
        self.t.goto(x0, y0)
        time.sleep(0.5)

        # redraw hull in final green color
        self.t.color(final_color)
        self.t.width(1)
        self.t.penup()
        self.t.goto(x0, y0)
        self.t.pendown()
        for i in range(1, len(hull)):
            x, y = self._to_screen_coords(hull[i][0], hull[i][1])
            self.t.goto(x, y)
        self.t.goto(x0, y0)

    def run_animation(self):

        steps = self.dynamic_layers.get_computation_steps()
        if not steps:
            print("No steps to animate. Make sure layers are being computed.")
            return

        # we compute scale and offsets
        self._compute_scale_and_offset(steps)

        for i, step in enumerate(steps):
            self.screen.title(f"Step {i + 1} of {len(steps)}")

            #draw remaining points in blue
            self._draw_points(step["points"], color='blue')

            self._draw_hull_animated(step["current_hull"], draw_color='red', final_color='green')
            time.sleep(0.2)

        turtle.done()
