import tkinter as tk
import sympy as sp


# beginning
def begin(s):
    global started
    started = True
    change_status(0, 1)
    print(s)


# button function
def give_next_token(token):
    global turn, active_status
    if not started:
        return
    if token == "del":
        change_status(0, 1)
        active_status = 1
        turn = []
    else:
        turn.append(token)
        active_status = 1 - active_status
        change_status(0, active_status)
        print(turn)
        if len(turn) <= 1:
            return
        elif len(turn) == operators.get(turn[1]) + 1:
            execute()
            change_status(1, 1)
            active_status = 1
            turn = []
    return


# execution
def execute():
    global Buttons_f
    op = turn[1]
    if op == "+":
        ex1 = players_f[int(turn[0][0])][int(turn[0][1])]
        ex2 = players_f[int(turn[2][0])][int(turn[2][1])]
        ex1 += ex2
        players_f[int(turn[0][0])][int(turn[0][1])] = ex1
        Buttons_f[int(turn[0][0])][int(turn[0][1])].config(text=str(ex1))
    elif op == "*":
        ex1 = players_f[int(turn[0][0])][int(turn[0][1])]
        ex2 = players_f[int(turn[2][0])][int(turn[2][1])]
        ex1 *= ex2
        players_f[int(turn[0][0])][int(turn[0][1])] = ex1
        Buttons_f[int(turn[0][0])][int(turn[0][1])].config(text=str(ex1))
    elif op == "s":
        ex1 = players_f[int(turn[0][0])][int(turn[0][1])]
        ex2 = players_f[int(turn[2][0])][int(turn[2][1])]
        ex1 = ex1.subs({x: ex2})
        players_f[int(turn[0][0])][int(turn[0][1])] = ex1
        Buttons_f[int(turn[0][0])][int(turn[0][1])].config(text=str(ex1))
    elif op == "-":
        ex1 = players_f[int(turn[0][0])][int(turn[0][1])]
        ex1 *= -1
        players_f[int(turn[0][0])][int(turn[0][1])] = ex1
        Buttons_f[int(turn[0][0])][int(turn[0][1])].config(text=str(ex1))
    elif op == "d":
        ex1 = players_f[int(turn[0][0])][int(turn[0][1])]
        ex1 = ex1.diff(x)
        players_f[int(turn[0][0])][int(turn[0][1])] = ex1
        Buttons_f[int(turn[0][0])][int(turn[0][1])].config(text=str(ex1))


def change_status(change_player, mode):
    global active_player, Buttons_f, Buttons_op
    if change_player:
        active_player = 1 - active_player
        label1.config(text="ACTIVE: PLAYER " + str(active_player + 1))
    if mode:
        for i in range(n):
            Buttons_f[active_player][i].config(state=tk.NORMAL, fg="green")
            Buttons_f[1 - active_player][i].config(state=tk.ACTIVE, fg="black")
        for j in range(m):
            Buttons_op[active_player][j].config(state=tk.DISABLED)
            Buttons_op[1 - active_player][j].config(state=tk.DISABLED)
    else:
        for i in range(n):
            Buttons_f[active_player][i].config(state=tk.DISABLED)
            Buttons_f[1 - active_player][i].config(state=tk.DISABLED)
        for j in range(m):
            Buttons_op[active_player][j].config(state=tk.NORMAL, fg="green")
            Buttons_op[1 - active_player][j].config(state=tk.DISABLED, fg="black")


# game parameters
n = 5
m = 5

# pre-window parameters
lx = 300
dx = 60
delta = 160

# standard kit
x = sp.symbols("x")
functions = [x + 5, sp.exp(x), sp.sin(x), x**2 - 7 * x + 10, sp.asin(x)]
operators = {"+": 2, "*": 2, "d": 1, "-": 1, "s": 2}
texts_op = [["+", "-", "*", "d/dx", "sp"], ["+", "-", "*", "d", "s"]]

# active data
started = 0
turn = []
players_f = [functions[:], functions[:]]
active_player = 0
active_status = 1
turn_number = 0

# window
window = tk.Tk()
window.title("Zerocity")
window.config(height=str(dx * (n + 2) + delta), width=str(lx + m * dx), bg="black")
window.resizable(width=False, height=False)

# frames
frame1 = tk.Frame(window)
frame1.place(x=0, y=dx, height=dx * (n + 1) + delta, width=lx + m * dx)
frame1.config(bg="#aaccff")

# labels
label1 = tk.Label(window, text="ACTIVE: PLAYER " + str(active_player + 1), bg="black", fg="green", font="Arial 20")
label1.place(x=0, y=0, height=dx, width=lx + m * dx)

# binding
window.bind('<s>', lambda event: begin("started"))


# buttons set
Buttons_f = [[], []]
Buttons_op = [[], []]


for i in range(len(functions)):
    button_1 = tk.Button(frame1, text=str(functions[i]), font="Arial 20")
    button_2 = tk.Button(frame1, text=str(functions[i]), font="Arial 20")
    button_1.place(x=0, y=i * dx, width=lx, height=dx)
    button_2.place(x=m * dx, y=dx + delta + i * dx, width=lx, height=dx)
    Buttons_f[0].append(button_1)
    Buttons_f[1].append(button_2)

for j in range(len(texts_op[0])):
    button_1 = tk.Button(frame1, text=str(texts_op[0][j]), font="Arial 20")
    button_2 = tk.Button(frame1, text=str(texts_op[0][j]), font="Arial 20")

    button_1.place(x=lx + j * dx, y=0, width=dx, height=dx)
    button_2.place(x=j * dx, y=dx * n + delta, width=dx, height=dx)
    Buttons_op[0].append(button_1)
    Buttons_op[1].append(button_2)

# button config
for i in range(len(functions)):
    Buttons_f[0][i].config(command=lambda i=i: give_next_token("0" + str(i)))
    Buttons_f[1][i].config(command=lambda i=i: give_next_token("1" + str(i)))

for j in range(len(texts_op[0])):
    Buttons_op[0][j].config(command=lambda j=j: give_next_token(texts_op[1][j]))
    Buttons_op[1][j].config(command=lambda j=j: give_next_token(texts_op[1][j]))


window.mainloop()