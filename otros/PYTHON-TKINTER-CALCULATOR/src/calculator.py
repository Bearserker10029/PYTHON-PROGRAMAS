from tkinter import *

root = Tk()
root.title("Calculator")
root.geometry("400x400")  # Tamaño inicial
root.resizable(True, True)

# Permitir que todas las filas y columnas se expandan
for x in range(6):  # columnas
    root.columnconfigure(x, weight=1)
for y in range(6):  # filas
    root.rowconfigure(y, weight=1)

# Campo de entrada
display = Entry(root, font=("Arial", 18))
display.grid(row=1, columnspan=6, sticky=N+S+E+W, ipady=10)

i = 0

def get_numbers(n):
    global i
    display.insert(i, n)
    i += 1

def get_operation(operator):
    global i
    opertor_length = len(operator)
    display.insert(i, operator)
    i += opertor_length

def calculate():
    display_state = display.get()
    try:
        result = eval(display_state)
        clear_display()
        display.insert(0, result)
    except Exception:
        clear_display()
        display.insert(0, 'Error')

def clear_display():
    display.delete(0, END)

def undo():
    display_state = display.get()
    if len(display_state):
        display_new_state = display_state[:-1]
        clear_display()
        display.insert(0, display_new_state)
    else:
        clear_display()
        display.insert(0, 'Error')

# Botones numéricos
Button(root, text="1", command=lambda: get_numbers(1)).grid(row=2, column=0, sticky=N+S+E+W)
Button(root, text="2", command=lambda: get_numbers(2)).grid(row=2, column=1, sticky=N+S+E+W)
Button(root, text="3", command=lambda: get_numbers(3)).grid(row=2, column=2, sticky=N+S+E+W)

Button(root, text="4", command=lambda: get_numbers(4)).grid(row=3, column=0, sticky=N+S+E+W)
Button(root, text="5", command=lambda: get_numbers(5)).grid(row=3, column=1, sticky=N+S+E+W)
Button(root, text="6", command=lambda: get_numbers(6)).grid(row=3, column=2, sticky=N+S+E+W)

Button(root, text="7", command=lambda: get_numbers(7)).grid(row=4, column=0, sticky=N+S+E+W)
Button(root, text="8", command=lambda: get_numbers(8)).grid(row=4, column=1, sticky=N+S+E+W)
Button(root, text="9", command=lambda: get_numbers(9)).grid(row=4, column=2, sticky=N+S+E+W)

# Botones inferiores
Button(root, text="AC", command=lambda: clear_display()).grid(row=5, column=0, sticky=N+S+E+W)
Button(root, text="0", command=lambda: get_numbers(0)).grid(row=5, column=1, sticky=N+S+E+W)
Button(root, text="%", command=lambda: get_operation("%")).grid(row=5, column=2, sticky=N+S+E+W)

Button(root, text="+", command=lambda: get_operation("+")).grid(row=2, column=3, sticky=N+S+E+W)
Button(root, text="-", command=lambda: get_operation("-")).grid(row=3, column=3, sticky=N+S+E+W)
Button(root, text="*", command=lambda: get_operation("*")).grid(row=4, column=3, sticky=N+S+E+W)
Button(root, text="/", command=lambda: get_operation("/")).grid(row=5, column=3, sticky=N+S+E+W)

# Más operadores
Button(root, text="⟵", command=lambda: undo()).grid(row=2, column=4, columnspan=2, sticky=N+S+E+W)
Button(root, text="exp", command=lambda: get_operation("**")).grid(row=3, column=4, sticky=N+S+E+W)
Button(root, text="^2", command=lambda: get_operation("**2")).grid(row=3, column=5, sticky=N+S+E+W)
Button(root, text="(", command=lambda: get_operation("(")).grid(row=4, column=4, sticky=N+S+E+W)
Button(root, text=")", command=lambda: get_operation(")")).grid(row=4, column=5, sticky=N+S+E+W)
Button(root, text="=", command=lambda: calculate()).grid(row=5, column=4, columnspan=2, sticky=N+S+E+W)

root.mainloop()