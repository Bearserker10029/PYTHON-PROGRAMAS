import tkinter as tk
from tkinter import ttk, messagebox
from sympy import symbols, Function, simplify, sympify, preorder_traversal, latex
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import io

# Define symbolic variables and functions
t, tau = symbols('t tau')
x = Function('x') # Input function x(t)
y = Function('y') # Output function y(t) - though not explicitly used in checks directly, it's good for context

class SystemAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Sistemas")
        self._update_timer = None # For debouncing key presses
        self.create_widgets()
        # Initial display of the input expression (e.g., when app starts with empty entry)
        self._update_input_display()
    
    def create_widgets(self):
        # --- Styling ---
        style = ttk.Style()
        style.theme_use('clam') # Use a modern theme
        
        # Define common font sizes
        label_font_size = 12
        entry_font_size = 12
        button_font_size = 12
        result_font_size = 10 # Keep text box font distinct

        style.configure('TLabel', font=('Segoe UI', label_font_size))
        style.configure('TButton', font=('Segoe UI', button_font_size, 'bold'), padding=8)
        style.configure('TEntry', font=('Segoe UI', entry_font_size), padding=5)
        style.configure('TFrame', background=style.lookup('TFrame', 'background'))
        style.configure('Result.TLabel', font=('Segoe UI', result_font_size, 'bold'), foreground='#2c3e50')

        # --- Main Frame for Padding ---
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill='both', expand=True)

        # Configure columns for responsiveness
        main_frame.grid_columnconfigure(0, weight=1) # Make the entry column expandable
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_columnconfigure(3, weight=1)

        # --- Input Section ---
        input_label = ttk.Label(main_frame, text="Ingrese la expresión del sistema y(t) en términos de x(t):")
        input_label.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='w')

        self.entry = ttk.Entry(main_frame, width=60, font=('Arial', entry_font_size)) # Adjusted width for initial size
        self.entry.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky='ew')
        self.entry.bind('<KeyRelease>', self._program_display_update) # Bind key release to update display

        # --- LaTeX Display for Input Expression ---
        self.display_expr_label = ttk.Label(main_frame)
        self.display_expr_label.grid(row=2, column=0, columnspan=4, pady=(5, 15), sticky='ew')
        
        ttk.Separator(main_frame, orient='horizontal').grid(row=3, column=0, columnspan=4, sticky='ew', pady=10)

        # --- Buttons ---
        buttons = [
            ('Linealidad', 4, 0), ('Causalidad', 4, 1),
            ('Invarianza', 4, 2), ('Limpiar', 4, 3)
        ]
        
        for (text, row, col) in buttons:
            ttk.Button(
                main_frame, text=text,
                command=lambda t=text: self.on_button_click(t)
            ).grid(row=row, column=col, sticky='ew', padx=5, pady=5) # Added padx/pady for button spacing
        
        ttk.Separator(main_frame, orient='horizontal').grid(row=5, column=0, columnspan=4, sticky='ew', pady=10)

        # --- Results Text Area ---
        result_label = ttk.Label(main_frame, text="Resultados del Análisis:")
        result_label.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky='w')

        self.result_text = tk.Text(main_frame, height=12, width=60, font=('Courier', result_font_size), wrap='word') # Added word wrap
        self.result_text.grid(row=7, column=0, columnspan=4, padx=10, pady=5, sticky='nsew')
        
        # Make the text widget resizable with the window
        main_frame.grid_rowconfigure(7, weight=1) # Row containing the text box will expand
        
    def on_button_click(self, action):
        input_expr_str = self.entry.get()
        if not input_expr_str and action != 'Limpiar':
            messagebox.showwarning("Entrada Vacía", "Por favor, ingrese una expresión del sistema.")
            return

        try:
            if action == 'Linealidad':
                result = self.check_linearity(input_expr_str)
            elif action == 'Causalidad':
                result = self.check_causality(input_expr_str)
            elif action == 'Invarianza':
                result = self.check_time_invariance(input_expr_str)
            else: # Limpiar button
                self.entry.delete(0, tk.END)
                self.result_text.delete(1.0, tk.END)
                self._update_input_display() # Clear LaTeX display as well
                return
            
            self.show_result(action, result)
        
        except Exception as e:
            messagebox.showerror("Error de Análisis", f"Error al procesar la expresión: {str(e)}\n\nAsegúrese de que su expresión solo contenga 'x(t)' y operaciones válidas. Por ejemplo: x(t) + x(t-1) o t*x(t).")
    
    def check_linearity(self, input_expr_str):
        expr = sympify(input_expr_str)
        a1, a2 = symbols('a1 a2')
        x1 = Function('x1')
        x2 = Function('x2')
        
        # Output due to a1*x1(t) + a2*x2(t)
        # We need to ensure that 't' in x(t) remains 't'
        lhs = expr.replace(x, lambda arg: a1*x1(arg) + a2*x2(arg))
        
        # a1 * (Output due to x1(t)) + a2 * (Output due to x2(t))
        rhs = a1 * expr.replace(x, x1) + a2 * expr.replace(x, x2)
        
        # Check if LHS - RHS simplifies to 0
        is_linear = simplify(lhs - rhs) == 0
        
        self.result_text.insert(tk.END, "--- Prueba de Linealidad ---\n")
        self.result_text.insert(tk.END, f"Expresión original: {input_expr_str}\n")
        self.result_text.insert(tk.END, f"LHS (a1*x1 + a2*x2): {lhs}\n")
        self.result_text.insert(tk.END, f"RHS (a1*y1 + a2*y2): {rhs}\n")
        self.result_text.insert(tk.END, f"Diferencia (LHS - RHS): {simplify(lhs - rhs)}\n")
        return is_linear
    
    def check_causality(self, input_expr_str):
        expr = sympify(input_expr_str)
        is_causal = True
        for node in preorder_traversal(expr):
            if node.func == x: # Find instances of x(...)
                arg = node.args[0] # Get the argument of x, e.g., 't', 't-1', 't+2'
                # Check if the argument is greater than 't'
                # This identifies future values, making the system non-causal
                # We need to simplify (arg - t) and check if it's positive.
                diff = simplify(arg - t)
                if diff.is_positive: # e.g., (t+1) - t = 1, which is positive
                    is_causal = False
                    break # Found a future dependency, no need to check further
        
        self.result_text.insert(tk.END, "--- Prueba de Causalidad ---\n")
        self.result_text.insert(tk.END, f"Expresión original: {input_expr_str}\n")
        self.result_text.insert(tk.END, f"Análisis de dependencias futuras: {'No encontradas' if is_causal else 'Encontrada(s) - e.g., ' + str(arg)}\n")
        return is_causal
    
    def check_time_invariance(self, input_expr_str):
        expr = sympify(input_expr_str)
        
        # Calculate y(t - tau) - shifted output
        shifted_output_expr = expr.subs(t, t - tau)
        
        # Calculate T[x(t - tau)] - output due to shifted input
        # This replaces every instance of x(arg) with x(arg - tau)
        shifted_input_expr = expr.replace(x, lambda arg: x(arg - tau))
        
        # Check if the two expressions are equivalent
        is_time_invariant = simplify(shifted_input_expr - shifted_output_expr) == 0
        
        self.result_text.insert(tk.END, "--- Prueba de Invarianza Temporal ---\n")
        self.result_text.insert(tk.END, f"Expresión original: {input_expr_str}\n")
        self.result_text.insert(tk.END, f"y(t - tau): {shifted_output_expr}\n")
        self.result_text.insert(tk.END, f"T[x(t - tau)]: {shifted_input_expr}\n")
        self.result_text.insert(tk.END, f"Diferencia: {simplify(shifted_input_expr - shifted_output_expr)}\n")
        return is_time_invariant
    
    def show_result(self, property_name, result):
        self.result_text.insert(tk.END, f"\n=== Resultado de {property_name} ===\n")
        self.result_text.insert(tk.END, f"El sistema es {'' if result else 'NO '} {property_name.lower()}.\n\n")
        self.result_text.see(tk.END) # Scroll to the end
    
    # --- LaTeX Display Methods (Copied and Adapted) ---
    def _program_display_update(self, event=None):
        """Debounces the call to update the LaTeX display."""
        if self._update_timer:
            self.root.after_cancel(self._update_timer)
        self._update_timer = self.root.after(300, self._update_input_display) # 300ms delay

    def _update_input_display(self):
        """Updates the LaTeX rendering for the input expression."""
        expr_str = self.entry.get()
        # For system analysis, the output is y(t) = expression
        self._render_latex(expr_str, self.display_expr_label, "y(t)")

    def _render_latex(self, expr_str, label, name):
        """Renders a SymPy expression as LaTeX and displays it as an image."""
        latex_str = ""
        if not expr_str:
            latex_str = f"{name} = " # Display just "y(t) ="
        else:
            try:
                # SymPy's sympify can handle more general expressions than parse_expr
                # It can sometimes struggle with x(t) + x(t-1) for direct LaTeX unless told to interpret x as a Function.
                # However, with x = Function('x'), sympify should convert 'x(t)' correctly.
                parsed_expr = sympify(expr_str.replace('^', '**'), locals={'t': t, 'x': x})
                # Check for instances of x to ensure it's not just a raw symbol 'x'
                if x in parsed_expr.free_symbols:
                    # If the expression contains a raw 'x' symbol (not x(t)), it's likely an error.
                    # Or, more robustly, check for Function instances:
                    has_function_x = any(isinstance(arg, Function) and arg.func == x for arg in parsed_expr.atoms())
                    if not has_function_x and 'x' in expr_str and 'x(' not in expr_str:
                         latex_str = f"{name} = \\text{{'{expr_str}' (use x(t))}}"
                    else:
                        latex_str = f"{name} = {latex(parsed_expr)}"
                else:
                    # If x is not explicitly a function in the input, but it's part of the expression
                    # and sympify can handle it, let it go.
                    latex_str = f"{name} = {latex(parsed_expr)}"

            except Exception:
                # If parsing fails (e.g., incomplete expression like 'x*'), display the raw input
                latex_str = f"{name} = {expr_str}"
        
        self._mostrar_latex_image(latex_str, label)

    def _mostrar_latex_image(self, latex_str, label):
        """Uses Matplotlib to render LaTeX and display it as an image in a Tkinter label."""
        plt.clf() # Clear current figure
        # Adjust figsize as needed; wider for potentially long system expressions
        fig = plt.figure(figsize=(10, 1.5), dpi=100) 
        # Render the LaTeX string. usetex=False ensures no external LaTeX installation is needed.
        fig.text(0.05, 0.5, f"${latex_str}$", fontsize=20, usetex=False) 
        
        # Make the background of the plot and axes transparent for a cleaner look
        fig.patch.set_alpha(0.0) 
        if fig.axes: 
            fig.axes[0].set_facecolor((0.0, 0.0, 0.0, 0.0)) 

        # Save the plot to a BytesIO object as a PNG image
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0) # Rewind the buffer to the beginning
        
        # Open the image with PIL and convert to PhotoImage for Tkinter
        image = Image.open(buf)
        photo = ImageTk.PhotoImage(image)
        
        label.config(image=photo) # Update the Tkinter label with the image
        label.image = photo # Keep a reference to prevent garbage collection by Tkinter
        plt.close(fig) # Close the Matplotlib figure to free memory
        buf.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = SystemAnalyzerApp(root)
    root.mainloop()