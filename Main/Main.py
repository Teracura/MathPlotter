import tkinter as tk

from GraphPlotting import GraphPlotter

module = tk.Tk()
module.title("Main window")
module.geometry("500x300")

gp = GraphPlotter()

text_input_equation_box = tk.Text(module, font=("Arial", 18), height=5)
plot_button = tk.Button(module, text="Plot normally", font=("Arial", 18),
                        command=lambda: gp.create_plot(text_input_equation_box.get("1.0", "end-1c")))
guide_text = tk.Label(
    module,
    text="Write your equation below (equals zero) (only x and y defined as variables)",
    font=("Arial", 18),
    wraplength=450,
)

euler_button = tk.Button(module, text="Plot with euler's method", font=("Arial", 18),
                        command=lambda: gp.open_euler_window(text_input_equation_box.get("1.0", "end-1c")))

guide_text.pack(pady=1, fill=tk.X)
text_input_equation_box.pack(pady=1, fill=tk.X)
plot_button.pack(pady=1)
euler_button.pack(pady=1)

module.mainloop()


