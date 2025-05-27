import tkinter as tk
from tkinter import ttk
from sympy import symbols, latex, together, parse_expr
from sympy.parsing.sympy_parser import parse_expr
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import io

# Define the symbolic variable x for SymPy
x = symbols('x')

class ProbabilidadDiscreta:
    """
    Handles the mathematical calculations for discrete probability functions.
    """
    def __init__(self):
        self.x = x
        self.func = None
        self.dominio = []
        self.probabilidades = {}

    def establecer_funcion(self, funcion_str, inicio, fin):
        """
        Establishes the probability function f(x) and its domain,
        then calculates the probability distribution.
        """
        try:
            # Parse the function string, replacing '^' with '**' for SymPy compatibility
            self.func = parse_expr(funcion_str.replace('^', '**'), local_dict={'x': self.x})
            self.func = together(self.func) # Simplify the expression
            self.dominio = list(range(inicio, fin + 1))
            self._calcular_distribucion()
        except Exception as e:
            raise ValueError(f"Error al establecer f(x): {e}")

    def _calcular_distribucion(self):
        """
        Calculates the probability distribution for the given function and domain.
        Normalizes the values so they sum to 1.
        """
        valores = [self.func.subs(self.x, xi) for xi in self.dominio]

        if any(v < 0 for v in valores):
            raise ValueError("Valores negativos en f(x) no permitidos para una función de probabilidad.")
        
        total = sum(valores)
        if total == 0:
            raise ValueError("La suma de f(x) en el dominio es 0. No se puede normalizar.")
        
        self.probabilidades = {xi: val/total for xi, val in zip(self.dominio, valores)}

    def calcular_esperanza(self, gx_str):
        """
        Calculates the expected value E[g(x)].
        """
        gx = parse_expr(gx_str.replace('^', '**'), local_dict={'x': self.x})
        gx = together(gx)
        return sum(gx.subs(self.x, xi) * p for xi, p in self.probabilidades.items())

    def calcular_varianza(self, gx_str):
        """
        Calculates the variance V[g(x)].
        """
        ex = self.calcular_esperanza(gx_str)
        gx2 = f"({gx_str})**2" # Square the function g(x)
        ex2 = self.calcular_esperanza(gx2)
        return ex2 - ex**2

    def probabilidad_condicion(self, condicion_str):
        """
        Calculates the probability P(condition) based on the distribution.
        """
        try:
            # Evaluate the condition for each x in the domain
            # Filter based on the boolean result of the condition
            expr = parse_expr(condicion_str.replace('^', '**'), local_dict={'x': self.x})
            return sum(p for xi, p in self.probabilidades.items() if expr.subs(self.x, xi))
        except Exception as e:
            raise ValueError(f"Error al evaluar la condición: {e}. Asegúrese de usar operadores lógicos y de comparación válidos (por ejemplo, 'x > 5', 'x <= 10').")


class CalculadoraGUI:
    """
    The Tkinter GUI for the discrete probability calculator.
    """
    def __init__(self, root):
        self.root = root
        self.modelo = ProbabilidadDiscreta()
        self._update_timer = None # For debouncing key presses
        self._construir_interfaz()

    def _construir_interfaz(self):
        """
        Builds the graphical user interface components.
        """
        self.root.title("Calculadora de Probabilidad Discreta")
        self.root.geometry("1050x750") # Set initial window size
        self.root.resizable(True, True) # Allow window resizing

        # --- THEME AND STYLING ---
        style = ttk.Style()
        # Choose a modern theme. 'clam' often provides a clean, flat look.
        # Other options: 'alt', 'default', 'classic', 'vista' (Windows), 'xpnative' (Windows)
        style.theme_use('clam') 

        # Define common font sizes for consistency
        label_font_size = 12
        entry_font_size = 12
        button_font_size = 12
        result_font_size = 16 

        # Configure styles for ttk widgets
        style.configure('TLabel', font=('Segoe UI', label_font_size)) # Using 'Segoe UI' for a modern feel
        style.configure('TButton', font=('Segoe UI', button_font_size, 'bold'), padding=8) # Bold buttons, more padding
        style.configure('TEntry', font=('Segoe UI', entry_font_size), padding=5) 
        style.configure('TFrame', background=style.lookup('TFrame', 'background')) # Ensure frame background matches theme

        # Custom style for the result label to make it stand out
        style.configure('Result.TLabel', font=('Segoe UI', result_font_size, 'bold'), foreground='#2c3e50') # Dark blue/grey

        # --- MAIN FRAME ---
        main_frame = ttk.Frame(self.root, padding=30, relief='flat') # Increased padding for more whitespace
        main_frame.pack(fill='both', expand=True)

        # Configure columns for responsiveness: labels take minimal space, content column expands
        main_frame.grid_columnconfigure(0, weight=0) # Column for labels
        main_frame.grid_columnconfigure(1, weight=1) # Column for entries/main content, set to expand

        # Configure rows for responsiveness: distribute vertical space
        # Rows containing the equation displays and result label get more weight
        for i in range(10): # Iterating through potential rows (0-9)
            # Give more weight to rows containing equation displays (1, 4) and the result label (8)
            main_frame.grid_rowconfigure(i, weight=1 if i in [1, 5, 8] else 0) 

        # --- INPUT DEFINITIONS SECTION (LabelFrame for grouping) ---
        input_frame = ttk.LabelFrame(main_frame, text="Definiciones", padding=(20, 15)) # Group inputs
        input_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 20)) # Spacing below the group
        input_frame.grid_columnconfigure(1, weight=1) # Make entry column expandable within this frame

        # f(x) Input
        ttk.Label(input_frame, text="Función de probabilidad f(x):").grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.entry_fx = ttk.Entry(input_frame, font=('Segoe UI', entry_font_size))
        self.entry_fx.grid(row=0, column=1, sticky='ew', padx=10) # 'ew' for horizontal expansion
        self.entry_fx.bind('<KeyRelease>', self._programar_actualizacion_fx) # Update LaTeX on key release
        
        self.display_fx = ttk.Label(input_frame) # Label to display rendered f(x)
        self.display_fx.grid(row=1, column=0, columnspan=2, pady=(5, 15), sticky='ew') # More padding below equation

        # Domain Input (grouped in a sub-frame)
        dominio_frame = ttk.Frame(input_frame) 
        dominio_frame.grid(row=2, column=0, columnspan=2, sticky='w', pady=(0, 5), padx=5)
        ttk.Label(dominio_frame, text="Dominio (x):").pack(side='left', padx=(0, 10))
        ttk.Label(dominio_frame, text="Desde:").pack(side='left', padx=(0, 5))
        self.entry_inicio = ttk.Entry(dominio_frame, width=8, font=('Segoe UI', entry_font_size))
        self.entry_inicio.pack(side='left')
        ttk.Label(dominio_frame, text="Hasta:").pack(side='left', padx=(10, 5))
        self.entry_fin = ttk.Entry(dominio_frame, width=8, font=('Segoe UI', entry_font_size))
        self.entry_fin.pack(side='left')

        # Separator after domain input for visual separation
        ttk.Separator(input_frame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky='ew', pady=(15, 10))

        # g(x) Input
        ttk.Label(input_frame, text="Función g(x) para cálculos:").grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.entry_gx = ttk.Entry(input_frame, font=('Segoe UI', entry_font_size))
        self.entry_gx.grid(row=4, column=1, sticky='ew', padx=10)
        self.entry_gx.bind('<KeyRelease>', self._programar_actualizacion_gx)

        self.display_gx = ttk.Label(input_frame) # Label to display rendered g(x)
        self.display_gx.grid(row=5, column=0, columnspan=2, pady=(5, 15), sticky='ew')

        # Separator after g(x) input
        ttk.Separator(input_frame, orient='horizontal').grid(row=6, column=0, columnspan=2, sticky='ew', pady=(15, 10))

        # Condition Input
        ttk.Label(input_frame, text="Condición para P(x):").grid(row=7, column=0, sticky='w', pady=5, padx=5)
        self.entry_cond = ttk.Entry(input_frame, font=('Segoe UI', entry_font_size))
        self.entry_cond.grid(row=7, column=1, sticky='ew', padx=10)
        input_frame.grid_rowconfigure(7, weight=0) # This row doesn't need to expand vertically

        # --- CALCULATIONS SECTION (LabelFrame for grouping) ---
        calc_frame = ttk.LabelFrame(main_frame, text="Cálculos", padding=(20, 15))
        calc_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        calc_frame.grid_columnconfigure(0, weight=1) # Allows content inside to expand

        # Buttons Frame (to center buttons horizontally)
        button_frame = ttk.Frame(calc_frame)
        button_frame.pack(pady=10) # Centered within calc_frame with vertical padding

        # Calculation Buttons
        ttk.Button(button_frame, text="Calcular Esperanza E[g(x)]", 
                   command=self.calcular_esperanza).pack(side='left', padx=10, ipady=5) # ipady adds internal padding
        ttk.Button(button_frame, text="Calcular Varianza V[g(x)]", 
                   command=self.calcular_varianza).pack(side='left', padx=10, ipady=5)
        ttk.Button(button_frame, text="Calcular P(condición)", 
                   command=self.calcular_prob_cond).pack(side='left', padx=10, ipady=5)

        # Results Label
        self.label_resultados = ttk.Label(
            calc_frame, 
            text="", 
            wraplength=800, # Increased wraplength for wider layout
            justify='center', # Center text if it wraps to multiple lines
            style='Result.TLabel' # Apply the custom result style
        )
        self.label_resultados.pack(fill='x', pady=(10, 0)) # fill='x' to allow horizontal centering with pack

        # --- Initial Display of Equations (Corrected Calls) ---
        # Now calls the unified _actualizar_display method directly
        self._actualizar_display(self.entry_fx.get(), self.display_fx, "f(x)")
        self._actualizar_display(self.entry_gx.get(), self.display_gx, "g(x)")

    def _programar_actualizacion(self, func_to_call):
        """Helper to debounce LaTeX updates."""
        if self._update_timer:
            self.root.after_cancel(self._update_timer)
        self._update_timer = self.root.after(200, func_to_call) # Update after 200ms of no key presses

    def _programar_actualizacion_fx(self, event=None):
        # This method now just calls the debouncer for the unified display update
        self._programar_actualizacion(lambda: self._actualizar_display(self.entry_fx.get(), self.display_fx, "f(x)"))

    def _programar_actualizacion_gx(self, event=None):
        # This method now just calls the debouncer for the unified display update
        self._programar_actualizacion(lambda: self._actualizar_display(self.entry_gx.get(), self.display_gx, "g(x)"))

    def _actualizar_display(self, expr_str, label, nombre):
        """Renders a SymPy expression as LaTeX and displays it in a label.
           Handles incomplete expressions by showing the raw input string.
        """
        latex_str = "" # Initialize with an empty string

        if not expr_str:
            # If the input string is empty, just show the function name
            latex_str = f"{nombre} = "
        else:
            try:
                # Attempt to parse the expression
                # Replace '^' with '**' for SymPy compatibility
                expr = parse_expr(expr_str.replace('^', '**'), local_dict={'x': x})
                expr = together(expr) # Simplify the expression for cleaner LaTeX output
                latex_str = f"{nombre} = {latex(expr)}"
            except Exception:
                # If SymPy fails to parse (e.g., incomplete expression like 'x*'),
                # display the raw input string instead of an error message.
                latex_str = f"{nombre} = {expr_str}"
        
        self._mostrar_latex(latex_str, label)

    def _mostrar_latex(self, latex_str, label):
        """Uses Matplotlib to render LaTeX and display it as an image in a Tkinter label."""
        plt.clf() # Clear current figure
        fig = plt.figure(figsize=(9, 1.5), dpi=100) # Increased width for potentially longer equations
        # Render the LaTeX string. usetex=False ensures no external LaTeX installation is needed.
        fig.text(0.05, 0.5, f"${latex_str}$", fontsize=20, usetex=False) 
        
        # Make the background of the plot and axes transparent for a cleaner look
        fig.patch.set_alpha(0.0) 
        if fig.axes: # Check if axes exist before trying to set facecolor
            fig.axes[0].set_facecolor((0.0, 0.0, 0.0, 0.0)) 

        # Save the plot to a BytesIO object as a PNG image
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0) # Rewind the buffer to the beginning
        
        # Open the image with PIL and convert to PhotoImage for Tkinter
        image = Image.open(buf)
        photo = ImageTk.PhotoImage(image)
        
        label.config(image=photo) # Update the Tkinter label with the image
        label.image = photo # Keep a reference to prevent garbage collection
        plt.close(fig) # Close the Matplotlib figure to free memory
        buf.close()

    def _validar_entradas(self):
        """
        Validates the f(x) and domain inputs and sets the model's function.
        Updates result label with errors or clears it on success.
        """
        try:
            fx_str = self.entry_fx.get()
            inicio = int(self.entry_inicio.get())
            fin = int(self.entry_fin.get())
            
            self.modelo.establecer_funcion(fx_str, inicio, fin)
            # Clear previous error message on successful validation
            # Retrieve the foreground color from the custom style directly
            self.label_resultados.config(text="", foreground=self.root.tk.call('ttk::style', 'lookup', 'Result.TLabel', '-foreground')) 
            return True
        except ValueError as e:
            self.label_resultados.config(text=f"Error de entrada: {e}", foreground='#e74c3c') # Bright red for input errors
            return False
        except Exception as e:
            self.label_resultados.config(text=f"Error inesperado: {e}", foreground='#e74c3c')
            return False

    def calcular_esperanza(self):
        """Handles the calculation and display of expectation."""
        if self._validar_entradas():
            try:
                gx_str = self.entry_gx.get()
                if not gx_str:
                    raise ValueError("Debe ingresar una función g(x) para calcular la esperanza.")
                esperanza = self.modelo.calcular_esperanza(gx_str)
                self.label_resultados.config(
                    text=f"Esperanza E[g(x)] = {esperanza:.6f}", 
                    foreground=self.root.tk.call('ttk::style', 'lookup', 'Result.TLabel', '-foreground') # Use style's foreground color
                )
            except Exception as e:
                self.label_resultados.config(text=f"Error de cálculo: {e}", foreground='#e74c3c')

    def calcular_varianza(self):
        """Handles the calculation and display of variance."""
        if self._validar_entradas():
            try:
                gx_str = self.entry_gx.get()
                if not gx_str:
                    raise ValueError("Debe ingresar una función g(x) para calcular la varianza.")
                varianza = self.modelo.calcular_varianza(gx_str)
                self.label_resultados.config(
                    text=f"Varianza V[g(x)] = {varianza:.6f}", 
                    foreground=self.root.tk.call('ttk::style', 'lookup', 'Result.TLabel', '-foreground')
                )
            except Exception as e:
                self.label_resultados.config(text=f"Error de cálculo: {e}", foreground='#e74c3c')

    def calcular_prob_cond(self):
        """Handles the calculation and display of conditional probability."""
        if self._validar_entradas():
            try:
                condicion = self.entry_cond.get()
                if not condicion:
                    raise ValueError("Debe ingresar una condición (ej. 'x > 5').")
                prob = self.modelo.probabilidad_condicion(condicion)
                self.label_resultados.config(
                    text=f"Probabilidad P({condicion}) = {prob:.6f}", 
                    foreground=self.root.tk.call('ttk::style', 'lookup', 'Result.TLabel', '-foreground')
                )
            except Exception as e:
                self.label_resultados.config(text=f"Error de cálculo: {e}", foreground='#e74c3c')


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraGUI(root)
    root.mainloop()