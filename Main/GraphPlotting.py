import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import tkinter as tk
import numpy as np
from scipy.integrate import solve_ivp
import re
from scipy.interpolate import interp1d
from sympy.parsing.sympy_parser import null


class GraphPlotter:
    expression = null
    fig, ax = plt.subplots()
    x = sp.Symbol('x')
    y = sp.Function('y')(x)

    def __init__(self):
        pass

    def refresh_graph(self):
        self.fig.clear()
        self.ax.clear()
        self.fig, self.ax = plt.subplots()
    def solve(self, text_input):
        type_of_equation = self.discover_equation_type(text_input)
        if type_of_equation == "ode":
            sol = self.solve_ode(self.expression)
            self.plot_solution(sol.t, sol.y[0], f"ODE: {self.expression}")
        elif type_of_equation == "algebraic":
            self.solve_algebraic(self.expression, self.x, self.y)
        else:
            print("unknown type")

    def preprocess_equation(self, text_input):
        text_input = re.sub(r"y'", "dy_dx", text_input)
        return text_input

    def discover_equation_type(self, text_input):
        processed_input = self.preprocess_equation(text_input)
        try:
            # turns expression to a form understood by sympy
            self.expression = sp.sympify(processed_input, locals={"pi": sp.pi, "e": sp.E, "y": self.y, "x": self.x})
        except (sp.SympifyError, TypeError):
            print("Invalid equation input")
            return
        if "dy_dx" in processed_input:
            return "ode"
        else:
            return "algebraic"

    def solve_ode(self, expr):
        try:
            dydx = sp.solve(expr, "dy_dx")  # Extract dy/dx
            if not dydx:
                print("Could not solve for dy/dx.")
                return
            # converts function to a form understood by numpy
            dydx_func = sp.lambdify((self.x, self.y), dydx[0], "numpy")
        except Exception as e:
            print(f"ODE Parsing Error: {e}")
            return

        # Define ODE system for SciPy
        def ode_system(t, y_val):
            return dydx_func(t, y_val)

        x_vals = np.linspace(0, 200, 200)  # plot limits from 0 to 200 with 200 points
        y0 = [1]  # initial value
        sol = solve_ivp(ode_system, [x_vals[0], x_vals[-1]], y0,
                        t_eval=x_vals)  # integrates function for exact solution
        return sol

    def solve_algebraic(self, expr, x, y):
        try:
            solutions = sp.solve(expr, y)  # Extract y
            if not solutions:
                print("No real solutions found for y.")
                return
        except Exception as e:
            print(f"Algebraic Parsing Error: {e}")
            return

        x_vals = np.linspace(0, 200, 200)
        for sol in solutions:
            y_func = sp.lambdify(x, sol, "numpy")
            y_vals = np.real_if_close(y_func(x_vals))
            self.plot_solution(x_vals, y_vals, "Numerical Solution")

        self.show_plot()

    def plot_solution(self, x_vals, y_vals, title):
        """Plots numerical solutions."""

        self.ax.set_title(title)
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.grid()
        self.ax.plot(x_vals, y_vals, label=f"function: {self.expression}")

        self.show_plot()

    def show_plot(self):
        plot_module = tk.Toplevel()
        plot_module.title("Graph output")
        plot_module.geometry("1000x1000")
        canvas = FigureCanvasTkAgg(self.fig, master=plot_module)
        canvas.get_tk_widget().pack(pady=20, fill=tk.BOTH, expand=True)
        self.ax.legend()
        canvas.draw()
        plot_module.update()
        fig, ax = plt.subplots()

    def open_euler_window(self, equation):
        euler_module = tk.Toplevel()
        euler_module.title("Graph output")
        euler_module.geometry("500x300")
        x0_text = tk.Label(
            euler_module,
            text="X0",
            font=("Arial", 14),
            wraplength=450,
        )
        x0_input = tk.Text(euler_module, font=("Arial", 18), height=1)
        y0_text = tk.Label(
            euler_module,
            text="Y0",
            font=("Arial", 14),
            wraplength=450,
        )
        y0_input = tk.Text(euler_module, font=("Arial", 18), height=1)
        h_text = tk.Label(
            euler_module,
            text="h",
            font=("Arial", 14),
            wraplength=450,
        )
        h_input = tk.Text(euler_module, font=("Arial", 18), height=1)
        x_text = tk.Label(
            euler_module,
            text="X",
            font=("Arial", 14),
            wraplength=450,
        )
        x_input = tk.Text(euler_module, font=("Arial", 18), height=1)
        plot_button = tk.Button(euler_module, text="Plot", font=("Arial", 18),
                                command=lambda: self.solve_euler(equation,
                                                                 float(x0_input.get("1.0", "end-1c")),
                                                                 float(y0_input.get("1.0", "end-1c")),
                                                                 float(h_input.get("1.0", "end-1c")),
                                                                 float(x_input.get("1.0", "end-1c"))))

        x0_text.pack(pady=1, fill=tk.X)
        x0_input.pack(pady=1, fill=tk.X)
        y0_text.pack(pady=1, fill=tk.X)
        y0_input.pack(pady=1, fill=tk.X)
        h_text.pack(pady=1, fill=tk.X)
        h_input.pack(pady=1, fill=tk.X)
        x_text.pack(pady=1, fill=tk.X)
        x_input.pack(pady=1, fill=tk.X)
        plot_button.pack(pady=1, fill=tk.X)
        euler_module.mainloop()

    def evaluate_euler(self, equation, x0, y0):
        equation = self.preprocess_equation(equation)
        x, y = sp.symbols('x y')
        dy_dx = sp.symbols("dy_dx")
        expr = sp.sympify(equation)
        solutions = sp.solve(expr, dy_dx)

        expr = solutions[0]
        result = expr.evalf(subs={x: x0, y: y0, "pi": sp.pi, "e": sp.E})

        return result

    def solve_euler(self, equation, x0, y0, h, x):
        x_vals = [x0]  # Store x points
        y_vals = [y0]  # Store y points
        while x0 < x:
            y0 = y0 + h * self.evaluate_euler(equation, x0, y0) # euler's equation for y
            x0 = x0 + h # euler's equation for x
            x_vals.append(x0)
            y_vals.append(y0)
        # vvv convert to a value readable by numpy
        x_vals = np.array(x_vals)
        y_vals = np.array(y_vals)
        x_smooth = np.linspace(min(x_vals), max(x_vals), 500)
        y_smooth = interp1d(x_vals, y_vals, kind='cubic')(x_smooth)
        self.plot_euler_solution(x_smooth, y_smooth, x_vals, y_vals)

    def plot_euler_solution(self, x_smooth, y_smooth, x_vals, y_vals):
        plt.figure(figsize=(8, 6))
        self.ax.plot(x_smooth, y_smooth, linestyle='-', color='b', label="Euler's Approximation")
        self.ax.scatter(x_vals, y_vals, color='red', s=5, label="Euler Points")  # Mark actual points
        self.ax.set_xlabel("x_axis")
        self.ax.set_ylabel("y_axis")
        self.ax.set_title("Euler's Method Approximation")
        self.ax.grid()
        self.show_plot()
