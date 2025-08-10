import tkinter as tk

counter = 0
running = False

def counter_label(label):
    def count():
        if running:
            global counter

            if counter == 0:
                display = "00:00:00"
            else:
                hrs, secs = divmod(counter, 3600)
                mins, secs = divmod(secs, 60)
                display = f"{hrs:02d}:{mins:02d}:{secs:02d}"

            label.config(text=display)
            label.after(1000, count)
            counter += 1

    count()

def Start(label):
    global running
    running = True
    counter_label(label)

def Stop():
    global running
    running = False

def Reset(label):
    global counter
    counter = 0
    label.config(text="00:00:00")

root = tk.Tk()
root.title("Stopwatch")
root.geometry("300x150")
root.resizable(False, False)

label = tk.Label(root, text="00:00:00", font=("Helvetica", 30), fg="black")
label.pack()

frame = tk.Frame(root)
frame.pack()

start_btn = tk.Button(frame, text='Start', width=10, command=lambda: Start(label))
start_btn.pack(side="left", padx=5, pady=10)

stop_btn = tk.Button(frame, text='Stop', width=10, command=Stop)
stop_btn.pack(side="left", padx=5, pady=10)

reset_btn = tk.Button(frame, text='Reset', width=10, command=lambda: Reset(label))
reset_btn.pack(side="left", padx=5, pady=10)

root.mainloop()
