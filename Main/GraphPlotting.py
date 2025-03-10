import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import tkinter as tk
import numpy as np
from scipy.integrate import solve_ivp
import re
from scipy.interpolate import interp1d


class GraphPlotter:

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

        x_vals = np.linspace(0, 200, 200)
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

        x_values = np.linspace(0, 200, 200)
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
            y0 = y0 + float(h) * float(self.evaluate_euler(equation, x0, y0))
            x0 = x0 + h
            x_vals.append(x0)
            y_vals.append(y0)

        x_vals = np.array(x_vals)
        y_vals = np.array(y_vals)
        x_smooth = np.linspace(min(x_vals), max(x_vals), 500)
        y_smooth = interp1d(x_vals, y_vals, kind='cubic')(x_smooth)
        self.plot_euler_solution(x_smooth, y_smooth, x_vals, y_vals)

    def plot_euler_solution(self, x_smooth, y_smooth, x_vals, y_vals):

        plt.figure(figsize=(8, 6))
        fig, ax = plt.subplots()

        plot_module = tk.Toplevel()
        plot_module.title("Graph output")
        plot_module.geometry("1000x1000")

        canvas = FigureCanvasTkAgg(fig, master=plot_module)
        canvas.get_tk_widget().pack(pady=20, fill=tk.BOTH, expand=True)

        ax.plot(x_smooth, y_smooth, linestyle='-', color='b', label="Euler's Approximation")
        ax.scatter(x_vals, y_vals, color='red', s=10, label="Euler Points")  # Mark actual points
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Euler's Method Approximation")
        ax.grid()
        ax.legend()
        canvas.draw()
        plot_module.update()
