import time
import numpy as np
import matplotlib.pyplot as plt

class PerformanceAnalysis:
    def __init__(self, dynamic_layers, static_algos):
        self.dynamic_layers = dynamic_layers
        self.static_algos = static_algos

    def run_tests(self, points):
        # Example performance test
        # 1. Test dynamic insertion time
        start_time = time.time()
        self.dynamic_layers.initialize(points)
        dyn_init_time = time.time() - start_time

        # 2. Test static algorithms
        start_time = time.time()
        _ = self.static_algos.compute_convex_layers(points, method='graham')
        static_time = time.time() - start_time

        print(f"Dynamic Initialization Time: {dyn_init_time:.4f}s")
        print(f"Static Algorithm Time (Graham): {static_time:.4f}s")

        # Extend this to plot runtime for varying input sizes, etc.
