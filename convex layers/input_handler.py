# input_handler.py
import random

class InputHandler:



    def generate_random_points(self, n=20, range_x=(0, 100), range_y=(0, 100)):
        return [(random.uniform(*range_x), random.uniform(*range_y)) for _ in range(n)]

    def from_file(self, filepath):
        #load points from a text file
        try:
            with open(filepath, 'r') as file:
                points = []
                for line in file:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        x, y = float(parts[0]), float(parts[1])
                        points.append((x, y))
                return points
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
