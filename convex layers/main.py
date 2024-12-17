import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from input_handler import InputHandler
from convex_layers import DynamicConvexLayers
from visualization import Visualization
from animation import TurtleAnimation

class ConvexLayersGUI:
    def __init__(self, root):
        # initialize the GUI and its components
        self.root = root
        self.root.title("Dynamic Convex Layers GUI")

        # basic styling and layout
        self.bg_color = "#fdf6e4"
        self.root.configure(bg=self.bg_color)
        self.root.minsize(900, 650)

        self.input_handler = InputHandler()
        self.dynamic_layers = DynamicConvexLayers()
        self.visualization = Visualization(self.dynamic_layers)
        self.canvas = None
        self.algo_var = tk.StringVar(value="graham")

        self.create_style()
        self.create_menu()
        self.create_main_layout()

    def create_style(self):
        # ttk styles for the GUI
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#fbe9d5")
        self.style.configure("TLabel", background="#fbe9d5", font=("Segoe UI", 11))
        self.style.configure("TButton", background="#faecd6", font=("Segoe UI", 11, "bold"), padding=5)
        self.style.configure("TRadiobutton", background="#fbe9d5", font=("Segoe UI", 11))
        self.style.configure("TLabelframe", background="#fbe9d5", font=("Segoe UI", 11, "bold"))
        self.style.configure("TEntry", font=("Segoe UI", 11))

    def create_menu(self):
        # menu bar for the application
        menubar = tk.Menu(self.root, bg="#fbe9d5", fg="#000")
        file_menu = tk.Menu(menubar, tearoff=0, bg="#fbe9d5", fg="#000")
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def create_main_layout(self):
        # main frames and widgets
        title_frame = ttk.Frame(self.root, padding=20)
        title_frame.pack(side=tk.TOP, fill=tk.X)
        title_label = ttk.Label(title_frame, text="Dynamic Convex Layers", font=("Segoe UI", 18, "bold"))
        title_label.pack(side=tk.TOP, pady=10)

        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        controls_frame = ttk.Frame(top_frame, padding=10)
        controls_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # algorithm selection
        algo_frame = ttk.Frame(controls_frame)
        algo_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        ttk.Label(algo_frame, text="Hull Algorithm:").pack(side=tk.LEFT, padx=5)
        algo_combo = ttk.Combobox(algo_frame, textvariable=self.algo_var, values=["graham", "jarvis", "andrew"], state='readonly')
        algo_combo.pack(side=tk.LEFT, padx=5)
        algo_combo.bind('<<ComboboxSelected>>', self.change_algorithm)

        # buttons for loading points
        load_frame = ttk.Frame(controls_frame)
        load_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        ttk.Button(load_frame, text="Load Random Points", command=self.load_random_points).pack(side=tk.LEFT, padx=5)
        ttk.Button(load_frame, text="Load Points (Cartesian File)", command=self.load_points_from_file).pack(side=tk.LEFT, padx=5)

        #buttons for adding and removing points
        modify_frame = ttk.Frame(controls_frame)
        modify_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        ttk.Button(modify_frame, text="Add a Point", command=self.add_point).pack(side=tk.LEFT, padx=5)
        ttk.Button(modify_frame, text="Remove a Point", command=self.remove_point).pack(side=tk.LEFT, padx=5)

        #peeling and re-adding layers
        peeling_frame = ttk.Frame(controls_frame)
        peeling_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        ttk.Button(peeling_frame, text="Peel One Layer", command=self.peel_one_layer).pack(side=tk.LEFT, padx=5)
        ttk.Button(peeling_frame, text="Re-add Layer", command=self.re_add_layer).pack(side=tk.LEFT, padx=5)

        # animation buttons
        animation_frame = ttk.Frame(controls_frame)
        animation_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        ttk.Button(animation_frame, text="Turtle Animation", command=self.show_turtle_animation).pack(side=tk.LEFT, padx=5)
        ttk.Button(animation_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)

        #input for number of points
        entry_frame = ttk.Frame(controls_frame)
        entry_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        ttk.Label(entry_frame, text="Number of Points:").pack(side=tk.LEFT, padx=5)
        self.num_points_entry = ttk.Entry(entry_frame, width=10)
        self.num_points_entry.pack(side=tk.LEFT)
        self.num_points_entry.insert(0, "20")

        #status bar for performance metrics
        status_frame = ttk.Frame(self.root, padding=10)
        status_frame.pack(side=tk.TOP, fill=tk.X)
        self.status_label = ttk.Label(status_frame, text="No data yet")
        self.status_label.pack(side=tk.LEFT)

        #  plot frame for Matplotlib visualization
        self.plot_frame = ttk.Frame(self.root, padding=10)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

    def change_algorithm(self, event):
        # we update the algorithm and recompute layers
        new_algo = self.algo_var.get()
        self.dynamic_layers.set_algorithm(new_algo)
        if len(self.dynamic_layers.points) > 0:
            self.dynamic_layers.compute_layers()
            self.display_visualiation()

    def load_random_points(self):
        # load random points and update visualization
        try:
            n = int(self.num_points_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for the number of points")
            return

        points = self.input_handler.generate_random_points(n=n)
        self.dynamic_layers.initialize(points)
        messagebox.showinfo("Success", f"Loaded {len(points)} points")
        self.display_visualization()

    def load_points_from_file(self):
        # load Cartesian points from a file
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text Files", "*.txt")])
        if file_path:
            points = self.input_handler.from_file(file_path)
            if points:
                self.dynamic_layers.initialize(points)
                messagebox.showinfo("Success", f"Loaded {len(points)} points from file")
                self.display_visualization()
            else:
                messagebox.showerror("Error", "Failed to load points. Check the file format")

    def add_point(self):
        # add a single point through user input
        prompt = "Enter a point as 'x y':"
        point_str = simpledialog.askstring("Add Point", prompt)
        if point_str:
            try:
                x, y = map(float, point_str.split())
                self.dynamic_layers.add_point((x, y))
                messagebox.showinfo("Success", f"Added point ({x}, {y})")
                self.display_visualization()
            except Exception:
                messagebox.showerror("Error", "Invalid input. Please enter coordinates as 'x y'")

    def remove_point(self):
        # remove a point specified by user input
        prompt = "Enter the point (x y) to remove:"
        point_str = simpledialog.askstring("Remove Point", prompt)
        if point_str:
            try:
                x, y = map(float, point_str.split())
                self.dynamic_layers.remove_point((x, y))
                messagebox.showinfo("Success", f"Removed point ({x}, {y})")
                self.display_visualization()
            except Exception:
                messagebox.showerror("Error", "Invalid input format")

    def peel_one_layer(self):
        # peel off the outermost layer
        if len(self.dynamic_layers.layers) > 0:
            self.dynamic_layers.peel_one_layer()
            self.display_visualization()
        else:
            messagebox.showinfo("Info", "No layers left to peel")

    def re_add_layer(self):
        # re-add the most recently peeled layer
        if len(self.dynamic_layers.peeled_layers) > 0:
            self.dynamic_layers.re_add_layer()
            self.display_visualization()
        else:
            messagebox.showinfo("Info", "No peeled layers to re-add")

    def display_visualization(self):
        # display the current static visualization (matplotlib) on the GUI
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig = self.visualization.get_static_plot()
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # update status with performance info
        runtime, layer_count = self.dynamic_layers.get_performance_info()
        self.status_label.config(text=f"Algorithm: {self.algo_var.get()} | Layers: {layer_count} | Runtime: {runtime:.4f}s")

    def show_turtle_animation(self):
        # show the turtle-based animation in a separate window
        turtle_anim = TurtleAnimation(self.dynamic_layers)
        turtle_anim.run_animation()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConvexLayersGUI(root)
    root.mainloop()
