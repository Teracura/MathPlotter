import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import tkinter as tk
import numpy as np
from scipy.integrate import solve_ivp
import re


class GraphPlotting:

    def __init__(self):
        pass

    def preprocess_equation(self, text_input):
        text_input = re.sub(r"y'", "dy_dx", text_input)

        return text_input

    def create_plot(self, text_input):
        global y_expr, is_diff
        x = sp.Symbol('x')
        y = sp.Function('y')(x)

        processed_input = self.preprocess_equation(text_input)

        try:

            expr = sp.sympify(processed_input, locals={"pi": sp.pi, "e": sp.E, "y": y, "x": x})
        except (sp.SympifyError, TypeError):
            print("Invalid equation input")
            return

        if "dy_dx" in processed_input:
            self.solve_ode(expr, x, y)
        else:
            self.solve_algebraic(expr, x, y)

    def solve_ode(self, expr, x, y):
        """Solves and plots first-order ODEs using SciPy."""
        try:
            dydx = sp.solve(expr, "dy_dx")  # Extract dy/dx
            if not dydx:
                print("Could not solve for dy/dx.")
                return

            dydx_func = sp.lambdify((x, y), dydx[0], "numpy")

        except Exception as e:
            print(f"ODE Parsing Error: {e}")
            return

        # Define ODE system for SciPy
        def ode_system(t, y_val):
            return dydx_func(t, y_val)

        x_vals = np.linspace(-100, 100, 200)
        y0 = [1]

        sol = solve_ivp(ode_system, [x_vals[0], x_vals[-1]], y0, t_eval=x_vals)

        self.plot_solution(sol.t, sol.y[0], f"ODE: {expr}")

    def solve_algebraic(self, expr, x, y):
        """Solves and plots algebraic equations using SymPy."""
        try:
            solutions = sp.solve(expr, y)
            if not solutions:
                print("No real solutions found for y.")
                return
        except Exception as e:
            print(f"Algebraic Parsing Error: {e}")
            return

        x_values = np.linspace(-100, 100, 200)
        fig, ax = plt.subplots()
        ax.set_title('Algebraic Equation Solution')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.grid(True)

        for sol in solutions:
            y_func = sp.lambdify(x, sol, "numpy")
            y_values = np.real_if_close(y_func(x_values))
            ax.plot(x_values, y_values, label=f"y = {sol}")

        self.show_plot(fig, ax)

    def plot_solution(self, x_vals, y_vals, title):
        """Plots numerical solutions."""
        fig, ax = plt.subplots()
        ax.set_title(title)
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.grid(True)
        ax.plot(x_vals, y_vals, label="Numerical Solution")

        self.show_plot(fig, ax)

    def show_plot(self, fig, ax):
        plot_module = tk.Toplevel()
        plot_module.title("Graph output")
        plot_module.geometry("1000x1000")

        canvas = FigureCanvasTkAgg(fig, master=plot_module)
        canvas.get_tk_widget().pack(pady=20, fill=tk.BOTH, expand=True)

        ax.legend()
        canvas.draw()
        plot_module.update()