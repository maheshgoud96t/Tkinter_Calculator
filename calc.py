import tkinter as tk
import math

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("380x650")
root.configure(bg="#1f2933")
root.resizable(False, False)

FG = "white"
BTN_BG = "#374151"
OP_BG = "#4b5563"
DANGER_BG = "#dc2626"

# ---------------- TITLE ----------------
label = tk.Label(
    root,
    text="Scientific Calculator",
    font=("Segoe UI", 13, "bold"),
    bg="#1f2933",
    fg=FG
)
label.pack(pady=8)

calc_frame = tk.Frame(root, bg="#1f2933")
calc_frame.pack()

# ---------------- DISPLAY ----------------
entry = tk.Entry(
    calc_frame,
    font=("Segoe UI", 22),
    bg="#020617",
    fg=FG,
    justify="right",
    bd=0,
    width=21
)
entry.grid(row=0, column=0, columnspan=5, pady=12, ipady=10)

# ---------------- CORE LOGIC ----------------
def click(x):
    current = entry.get()

    # auto-multiply before functions or '('
    if x in ("sin(", "cos(", "tan(", "sqrt(", "log(", "("):
        if current and (current[-1].isdigit() or current[-1] == ')'):
            entry.insert(tk.END, "*")

    entry.insert(tk.END, x)

def clear():
    entry.delete(0, tk.END)

def backspace():
    entry.delete(len(entry.get()) - 1, tk.END)

def calculate():
    try:
        expr = entry.get()

        # auto close brackets
        expr += ")" * (expr.count("(") - expr.count(")"))

        result = eval(expr, {"__builtins__": None}, {
            "sqrt": math.sqrt,
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "log": math.log10,
            "pi": math.pi,
            "e": math.e
        })

        entry.delete(0, tk.END)
        entry.insert(0, result)

        history.insert(tk.END, f"{expr} = {result}")
        history.yview(tk.END)

    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# ---------------- HISTORY PANEL ----------------
history_label = tk.Label(
    root,
    text="History",
    font=("Segoe UI", 11, "bold"),
    bg="#1f2933",
    fg=FG
)
history_label.pack(pady=(8, 2))

history = tk.Listbox(
    root,
    height=5,
    bg="#020617",
    fg=FG,
    font=("Segoe UI", 10),
    bd=0
)
history.pack(fill=tk.X, padx=12, pady=(0, 10))

# ---------------- BUTTON HELPER ----------------
def make_btn(text, cmd, r, c, w=5, bg=BTN_BG):
    tk.Button(
        calc_frame,
        text=text,
        command=cmd,
        font=("Segoe UI", 12, "bold"),
        width=w,
        height=2,
        bg=bg,
        fg=FG,
        bd=0
    ).grid(row=r, column=c, padx=5, pady=5)

# ---------------- ROW 1: ( ) POWER ----------------
make_btn("(", lambda: click("("), 1, 0)
make_btn(")", lambda: click(")"), 1, 1)
make_btn("xʸ", lambda: click("**"), 1, 2)
make_btn("√", lambda: click("sqrt("), 1, 3, bg=OP_BG)
make_btn("%", lambda: click("/100"), 1, 4, bg=OP_BG)

# ---------------- ROW 2: CLEAR / DEL ----------------
tk.Button(
    calc_frame,
    text="C",
    command=clear,
    font=("Segoe UI", 12, "bold"),
    width=11,
    height=2,
    bg=DANGER_BG,
    fg=FG,
    bd=0
).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

tk.Button(
    calc_frame,
    text="DEL",
    command=backspace,
    font=("Segoe UI", 12, "bold"),
    width=11,
    height=2,
    bg="#b91c1c",
    fg=FG,
    bd=0
).grid(row=2, column=2, columnspan=2, padx=5, pady=5)

make_btn("/", lambda: click("/"), 2, 4, bg=OP_BG)

# ---------------- ROW 3–6: NUMBERS + SCI ----------------
layout = [
    ("7", "8", "9", "*", "sin("),
    ("4", "5", "6", "-", "cos("),
    ("1", "2", "3", "+", "tan("),
    ("0", ".", "=", "pi", "log(")
]

row = 3
for line in layout:
    col = 0
    for item in line:
        if item == "=":
            make_btn(item, calculate, row, col, bg=OP_BG)
        elif item in "+-*/":
            make_btn(item, lambda x=item: click(x), row, col, bg=OP_BG)
        else:
            make_btn(item, lambda x=item: click(x), row, col)
        col += 1
    row += 1

# ---------------- KEYBOARD SUPPORT ----------------
def key_input(event):
    if event.char in "0123456789+-*/().":
        click(event.char)
    elif event.keysym == "Return":
        calculate()
    elif event.keysym == "BackSpace":
        backspace()

root.bind("<Key>", key_input)

# ---------------- START ----------------
root.mainloop()
