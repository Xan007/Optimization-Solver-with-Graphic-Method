import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import ProblemVisualizer
from IAClient import IAClient
from ProblemProcessor import ProblemProcessor
from ProblemSolver import ProblemSolver
from PIL import Image
import pytesseract
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("GROQAPI"))

class ProblemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Solver de Problemas de Optimización")
        self.geometry("1200x700")
        self.configure(bg="#f5f5f5")

        self.client = IAClient(os.getenv("GROQAPI"))

        with open("prompt.txt", "r", encoding="utf-8") as f:
                prompt = f.read()
        self.client.set_system_prompt(prompt)

        # --- Frames principales ---
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.middle_frame = ttk.Frame(self)
        self.middle_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # --- Entrada de texto ---
        self.text_input = scrolledtext.ScrolledText(self.top_frame, height=6)
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.upload_btn = ttk.Button(self.top_frame, text="Subir imagen", command=self.upload_image)
        self.upload_btn.pack(side=tk.LEFT, padx=5)

        # --- Botón resolver ---
        self.solve_btn = ttk.Button(self.middle_frame, text="Resolver problema", command=self.solve_problem)
        self.solve_btn.pack(side=tk.LEFT, padx=5)

        # --- Panel de resultados ---
        self.result_frame = ttk.Frame(self.bottom_frame)
        self.result_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_frame = ttk.Frame(self.bottom_frame)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.result_text = scrolledtext.ScrolledText(self.result_frame, width=60)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.figure_canvas = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            # Leer imagen y extraer texto con pytesseract
            try:
                self.temp_image_paths = [file_path]

                self.text_input.delete("1.0", tk.END)                
                self.text_input.insert(tk.END, f"[Imagen cargada: {os.path.basename(file_path)}]\n")

                #self.client.new_message(None, None, image_paths=[file_path])
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer la imagen:\n{str(e)}")

    def solve_problem(self):
        raw_text = self.text_input.get("1.0", tk.END).strip()
        if not raw_text:
            messagebox.showwarning("Aviso", "Ingresa un problema primero")
            return

        try:
            # Enviar a IA para procesar
            
            raw_problem_text = self.client.new_message(raw_text, None, self.temp_image_paths, None)
            print(raw_problem_text)
            

            processor = ProblemProcessor()
            processor.load_from_text(raw_problem_text)
            processor.process()
            problem = processor.problem

            solver = ProblemSolver(problem)
            solver.solve_objective()

            # Limpiar texto previo
            self.result_text.delete("1.0", tk.END)

            # Mostrar info
            #self.result_text.insert(tk.END, "=== Problema ===\n")
            #self.result_text.insert(tk.END, processor.raw_problem + "\n\n")

            print(problem)

            self.result_text.insert(tk.END, "=== Variables ===\n")
            for var, description in problem["variables"].items():
                self.result_text.insert(tk.END, f"{var} : {description}\n")
            self.result_text.insert(tk.END, "\n")

            self.result_text.insert(tk.END, "=== Función Objetivo ===\n")
            self.result_text.insert(tk.END, str(problem["objective"]) + " z = " + str(problem["objective_function"]) + "\n\n")

            self.result_text.insert(tk.END, "=== Restricciones ===\n")
            for c in problem["constraints"]:
                self.result_text.insert(tk.END, str(c) + "\n")
            self.result_text.insert(tk.END, "\n")

            self.result_text.insert(tk.END, "=== Vértices y Evaluación ===\n")
            for v in solver.vertices:
                eval_val = solver.evaluate_vertice(v)
                self.result_text.insert(tk.END, f"{v} -> Objetivo: {eval_val}\n")

            # --- Graficar ---
            if self.figure_canvas:
                self.figure_canvas.get_tk_widget().destroy()
            fig, ax = ProblemVisualizer.create_plot(problem["constraints"], processor.get_symbols(), solver.solution, solver.vertices)
            self.figure_canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            self.figure_canvas.draw()
            self.figure_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"{type(e).__name__}: {str(e)}")
        finally:
            self.client.clear_history()
            self.temp_image_paths = []


if __name__ == "__main__":
    app = ProblemApp()
    app.mainloop()
