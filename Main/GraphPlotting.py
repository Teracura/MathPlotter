import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import tkinter as tk


class graph_plotting:

    def __init__(self):
        pass

    def create_plot(self):
        fig, ax = plt.subplots()
        ax.set_title('Simple Line Graph')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.grid(True)

        plot_module = tk.Tk()
        plot_module.title("Graph output")
        plot_module.geometry("1000x1000")

        canvas = FigureCanvasTkAgg(fig, master=plot_module)  # A Tkinter widget
        canvas.get_tk_widget().pack(pady=20, fill=tk.BOTH, expand=True)

        x_values = []
        y_values = []

        for x in range(20):
            x_values.append(x)
            y_values.append(math.pow(x, 2))
            ax.plot(x_values, y_values, 'bo-', label='y = ')
            canvas.draw()
            plot_module.update()
