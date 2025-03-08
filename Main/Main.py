import tkinter as tk

import graph_plotting as gp

module = tk.Tk()
module.title("Hello World")
module.geometry("1000x1000")

plot_button = tk.Button(module, text="Show Plot", font=("Arial", 24), command= gp.create_plot)

plot_button.pack(pady=50)


module.mainloop()
