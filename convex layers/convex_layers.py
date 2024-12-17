# dynamic_convex_layers.py
import numpy as np
import time


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


class DynamicConvexLayers:
    def __init__(self, algorithm="graham"):
        self.points = np.empty((0, 2))
        self.layers = []
        self.steps = []
        self.algorithm = algorithm
        self.peeled_layers = []
        self.last_runtime = 0
        self.last_layer_count = 0

    def set_algorithm(self, algo):
        self.algorithm = algo

    def initialize(self, points):
        self.points = np.array(points)
        self.compute_layers()

    def compute_layers(self):
        start = time.time()
        self.layers = []
        self.steps = []
        remaining_points = self.points.copy()

        while len(remaining_points) > 0:
            step = {"points": remaining_points.copy(), "current_hull": []}

            if len(remaining_points) >= 3:
                hull_points = self.compute_hull(remaining_points)
                step["current_hull"] = hull_points.tolist()
                self.layers.append(hull_points)

                # remove hull points
                hull_set = set(tuple(p) for p in hull_points)
                remaining_points = np.array([p for p in remaining_points if tuple(p) not in hull_set])
            else:
                # all remaining points form the last layer
                hull_points = remaining_points.tolist()
                step["current_hull"] = hull_points
                self.layers.append(remaining_points)
                remaining_points = np.empty((0, 2))

            self.steps.append(step)

        end = time.time()
        self.last_runtime = end - start
        self.last_layer_count = len(self.layers)

    def compute_hull(self, points):
        if self.algorithm == "graham":
            return self.graham_scan(points)
        elif self.algorithm == "andrew":
            return self.andrew_monotone_chain(points)
        elif self.algorithm == "jarvis":
            return self.jarvis_march(points)
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")

    def graham_scan(self, points):
        pts = sorted(points, key=lambda p: (p[0], p[1]))
        lower = []
        for p in pts:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(tuple(p))
        upper = []
        for p in reversed(pts):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(tuple(p))
        return np.array(lower[:-1] + upper[:-1])

    def andrew_monotone_chain(self, points):

        return self.graham_scan(points)

    def jarvis_march(self, points):
        if len(points) < 3:
            return points
        pts = list(map(tuple, points))
        hull = []
        leftmost = min(pts, key=lambda p: (p[0], p[1]))
        p = leftmost
        while True:
            hull.append(p)
            q = pts[0]
            for r in pts[1:]:
                o = cross(p, q, r)
                if q == p or o < 0 or (o == 0 and np.linalg.norm(np.array(r) - np.array(p)) > np.linalg.norm(
                        np.array(q) - np.array(p))):
                    q = r
            p = q
            if p == hull[0]:
                break
        return np.array(hull)

    def peel_one_layer(self):
        if self.layers:
            top_layer = self.layers.pop()
            self.peeled_layers.append(top_layer)
            # recompute points from remaining layers
            self.points = np.vstack([layer for layer in self.layers]) if self.layers else np.empty((0, 2))
            self.compute_layers()

    def re_add_layer(self):
        if self.peeled_layers:
            layer = self.peeled_layers.pop()
            self.points = np.vstack([self.points, layer])
            self.compute_layers()

    def add_point(self, point):
        self.points = np.vstack([self.points, point])
        self.compute_layers()

    def remove_point(self, point):
        idx = np.where((self.points == point).all(axis=1))
        if len(idx[0]) > 0:
            self.points = np.delete(self.points, idx[0][0], axis=0)
            self.compute_layers()

    def get_layers(self):
        return self.layers

    def get_computation_steps(self):
        return self.steps

    def get_all_points(self):
        return self.points

    def get_performance_info(self):
        return self.last_runtime, self.last_layer_count
