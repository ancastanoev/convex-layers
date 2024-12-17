import numpy as np

class StaticConvexHullAlgorithms:
    def __init__(self):
        # initialize the convex hull algorithms class
        pass

    def graham_scan(self, points):
        # implement Graham's scan to compute the convex hull
        # sort points by x, then y
        pts = np.array(sorted(points, key=lambda p: (p[0], p[1])))

        # define cross product function
        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        # build lower hull
        lower = []
        for p in pts:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(tuple(p))

        # build upper hull
        upper = []
        for p in reversed(pts):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(tuple(p))

        # combine hulls, remove duplicate endpoints
        hull = lower[:-1] + upper[:-1]
        return np.array(hull)

    def jarvis_march(self, points):
        # implement Jarvis March (gift wrapping algorithm) for the convex hull
        def orientation(p, q, r):
            return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

        # initialize variables
        hull = []
        pts = np.array(points)
        n = len(pts)
        l = np.argmin(pts[:, 0])  # find leftmost point

        p = l
        while True:
            hull.append(tuple(pts[p]))
            q = (p + 1) % n

            for i in range(n):
                if orientation(pts[p], pts[i], pts[q]) < 0:
                    q = i

            p = q
            if p == l:  # back to the starting point
                break

        return np.array(hull)

    def divide_and_conquer_hull(self, points):
        # implement divide and conquer convex hull
        def merge_hulls(left, right):
            # find upper and lower tangents connecting the two hulls
            def is_clockwise(p, q, r):
                return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]) < 0

            # find rightmost point of left hull and leftmost point of right hull
            lmax = max(left, key=lambda p: p[0])
            rmin = min(right, key=lambda p: p[0])

            # find upper tangent
            upper_left, upper_right = lmax, rmin
            done = False
            while not done:
                done = True
                while is_clockwise(upper_left, upper_right, right[(right.index(upper_right) + 1) % len(right)]):
                    upper_right = right[(right.index(upper_right) + 1) % len(right)]
                while is_clockwise(left[(left.index(upper_left) - 1) % len(left)], upper_left, upper_right):
                    upper_left = left[(left.index(upper_left) - 1) % len(left)]
                    done = False

            # find lower tangent
            lower_left, lower_right = lmax, rmin
            done = False
            while not done:
                done = True
                while not is_clockwise(lower_left, lower_right, right[(right.index(lower_right) - 1) % len(right)]):
                    lower_right = right[(right.index(lower_right) - 1) % len(right)]
                while not is_clockwise(left[(left.index(lower_left) + 1) % len(left)], lower_left, lower_right):
                    lower_left = left[(left.index(lower_left) + 1) % len(left)]
                    done = False

            # combine hulls
            combined = []
            index = left.index(upper_left)
            while index != left.index(lower_left):
                combined.append(left[index])
                index = (index + 1) % len(left)
            combined.append(lower_left)

            index = right.index(lower_right)
            while index != right.index(upper_right):
                combined.append(right[index])
                index = (index + 1) % len(right)
            combined.append(upper_right)

            return combined

        # base case: return sorted points
        if len(points) <= 1:
            return points

        # divide step
        mid = len(points) // 2
        left_hull = self.divide_and_conquer_hull(points[:mid])
        right_hull = self.divide_and_conquer_hull(points[mid:])

        # merge step
        return merge_hulls(left_hull, right_hull)

    def compute_convex_layers(self, points, method='graham'):
        # compute convex layers by iteratively removing hull points
        points = list(map(tuple, points))  # ensure points are tuples
        layers = []

        while len(points) >= 3:
            if method == 'graham':
                hull = self.graham_scan(points)
            elif method == 'jarvis':
                hull = self.jarvis_march(points)
            elif method == 'divide':
                hull = self.divide_and_conquer_hull(points)
            else:
                raise ValueError("Unknown method. Use 'graham', 'jarvis', or 'divide'")

            layers.append(hull)
            points = [p for p in points if tuple(p) not in hull]

        return layers
