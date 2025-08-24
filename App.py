import os 

from IAClient import IAClient
from ProblemProcessor import ProblemProcessor
from ProblemSolver import ProblemSolver
import ProblemVisualizer

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


client = IAClient(os.getenv("GROQAPI"))

with open("prompt.txt", "r", encoding="utf-8") as f:
    contenido = f.read()


raw_problem_text = client.new_message('''
Se dispone de 600 g de un determinado fármaco para elaborar pastillas grandes y pequeñas.
Las grandes pesan 40 g y las pequeñas 30 g. Se necesitan al menos tres pastillas grandes, y
al menos el doble de pequeñas que de las grandes. Cada pastilla grande proporciona un
beneficio de $ 2 dólares y la pequeña de $ 1 dólar.
¿Cuántas pastillas se han de elaborar de cada clase para que el beneficio sea máximo?''', contenido)

print(raw_problem_text)

processor = ProblemProcessor()
processor.load_from_text(raw_problem_text)

print(processor.raw_problem)

try:
    processor.process()
    problem = processor.problem
    solver = ProblemSolver(problem)
    print(problem)
    solver.solve_objective()

    fig, ax = ProblemVisualizer.create_plot(problem["constraints"], processor.get_symbols(), solver.solution, solver.vertices)

    root = tk.Tk()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    root.mainloop()
except Exception as e:
    print("Tipo:", type(e))
    print("Args:", e.args)
    print("Mensaje:", str(e))