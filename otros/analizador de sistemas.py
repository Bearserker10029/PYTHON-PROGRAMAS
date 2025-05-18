import tkinter as tk
from tkinter import ttk, messagebox
from sympy import symbols, Function, simplify, sympify, preorder_traversal

t, tau = symbols('t tau')
x = Function('x')

class SystemAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Sistemas")
        self.create_widgets()
    
    def create_widgets(self):
        self.entry = ttk.Entry(self.root, width=40, font=('Arial', 12))
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        
        buttons = [
            ('Linealidad', 1, 0), ('Causalidad', 1, 1),
            ('Invarianza', 1, 2), ('Limpiar', 1, 3)
        ]
        
        for (text, row, col) in buttons:
            ttk.Button(
                self.root, text=text,
                command=lambda t=text: self.on_button_click(t)
            ).grid(row=row, column=col, sticky='ew', padx=2, pady=2)
        
        self.result_text = tk.Text(self.root, height=10, width=50, font=('Courier', 10))
        self.result_text.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
    
    def on_button_click(self, action):
        input_expr = self.entry.get()
        try:
            if action == 'Linealidad':
                result = self.check_linearity(input_expr)
            elif action == 'Causalidad':
                result = self.check_causality(input_expr)
            elif action == 'Invarianza':
                result = self.check_time_invariance(input_expr)
            else:
                self.entry.delete(0, tk.END)
                self.result_text.delete(1.0, tk.END)
                return
            
            self.show_result(action, result)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def check_linearity(self, input_expr):
        expr = sympify(input_expr)
        a1, a2 = symbols('a1 a2')
        x1 = Function('x1')
        x2 = Function('x2')
        
        lhs = expr.replace(x, lambda arg: a1*x1(arg) + a2*x2(arg))
        rhs = a1*expr.replace(x, x1) + a2*expr.replace(x, x2)
        
        return simplify(lhs - rhs) == 0
    
    def check_causality(self, input_expr):
        expr = sympify(input_expr)
        for node in preorder_traversal(expr):
            if node.func == x:
                arg = node.args[0]
                if (arg - t).simplify().is_positive:
                    return False
        return True
    
    def check_time_invariance(self, input_expr):
        expr = sympify(input_expr)
        shifted_input = expr.replace(x, lambda arg: x(arg - tau))
        shifted_output = expr.subs(t, t - tau)
        return simplify(shifted_input - shifted_output) == 0
    
    def show_result(self, property, result):
        self.result_text.insert(tk.END, f"=== {property} ===\n")
        self.result_text.insert(tk.END, f"Expresión: {self.entry.get()}\n")
        self.result_text.insert(tk.END, f"Resultado: {'SÍ' if result else 'NO'}\n\n")
        self.result_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemAnalyzerApp(root)
    root.mainloop()