import tkinter as tk

from GraphPlotting import GraphPlotting

module = tk.Tk()
module.title("Main window")
module.geometry("500x300")

gp = GraphPlotting()

text_input_equation_box = tk.Text(module, font=("Arial", 18), height=5)
plot_button = tk.Button(module, text="Show Plot", font=("Arial", 18),
                        command=lambda: gp.create_plot(text_input_equation_box.get("1.0", "end-1c")))
guide_text = tk.Label(
    module,
    text="Write your equation below (equals zero) (only x and y defined as variables)",
    font=("Arial", 18),
    wraplength=450,
)

guide_text.pack(pady=1, fill=tk.X)
text_input_equation_box.pack(pady=1, fill=tk.X)
plot_button.pack(pady=1)


module.mainloop()


