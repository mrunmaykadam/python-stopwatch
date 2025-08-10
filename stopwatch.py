import tkinter as tk
from tkinter import messagebox, filedialog
import time
import csv
import pyttsx3  # For voice alerts
from datetime import datetime

class StopwatchPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch Pro Edition ⏱️")
        self.root.geometry("500x400")
        self.root.configure(bg="#202124")
        
        # Variables
        self.start_time = None
        self.running = False
        self.laps = []
        self.mode = "Stopwatch"  # or "Countdown"
        self.countdown_time = 0
        self.voice_enabled = True
        
        # Voice engine
        self.engine = pyttsx3.init()

        # Mode buttons
        tk.Button(root, text="Stopwatch Mode", font=("Arial", 12), bg="#34a853", fg="white", command=self.set_stopwatch_mode).pack(pady=5)
        tk.Button(root, text="Countdown Mode", font=("Arial", 12), bg="#4285f4", fg="white", command=self.set_countdown_mode).pack(pady=5)
        
        # Display
        self.time_label = tk.Label(root, text="00:00:00", font=("Arial", 30), bg="#202124", fg="white")
        self.time_label.pack(pady=20)
        
        # Controls
        control_frame = tk.Frame(root, bg="#202124")
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="Start", font=("Arial", 12), bg="#0f9d58", fg="white", command=self.start).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Lap", font=("Arial", 12), bg="#fbbc05", fg="black", command=self.lap).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Stop", font=("Arial", 12), bg="#ea4335", fg="white", command=self.stop).grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="Reset", font=("Arial", 12), bg="#5f6368", fg="white", command=self.reset).grid(row=0, column=3, padx=5)
        
        # Lap display
        self.lap_listbox = tk.Listbox(root, width=40, height=8, font=("Arial", 12))
        self.lap_listbox.pack(pady=10)
        
        # Save button
        tk.Button(root, text="Save Laps to CSV", font=("Arial", 12), bg="#ff7043", fg="white", command=self.save_to_csv).pack(pady=5)
        
    def set_stopwatch_mode(self):
        self.mode = "Stopwatch"
        self.time_label.config(text="00:00:00")
        messagebox.showinfo("Mode", "Stopwatch mode selected.")
        
    def set_countdown_mode(self):
        self.mode = "Countdown"
        try:
            mins = int(input("Enter countdown minutes: "))
            self.countdown_time = mins * 60
            self.time_label.config(text=f"{mins:02}:00:00")
            messagebox.showinfo("Mode", f"Countdown mode set for {mins} minutes.")
        except:
            messagebox.showerror("Error", "Please enter a valid number.")
        
    def update_time(self):
        if self.running:
            if self.mode == "Stopwatch":
                elapsed = time.time() - self.start_time
                self.display_time(elapsed)
            elif self.mode == "Countdown":
                remaining = self.countdown_time - (time.time() - self.start_time)
                if remaining <= 0:
                    self.display_time(0)
                    self.running = False
                    if self.voice_enabled:
                        self.engine.say("Time's up!")
                        self.engine.runAndWait()
                    messagebox.showinfo("Countdown Finished", "Time's up!")
                    return
                self.display_time(remaining)
            self.root.after(50, self.update_time)
        
    def display_time(self, seconds):
        mins, secs = divmod(int(seconds), 60)
        hours, mins = divmod(mins, 60)
        self.time_label.config(text=f"{hours:02}:{mins:02}:{secs:02}")
        
    def start(self):
        if not self.running:
            self.start_time = time.time() if self.start_time is None else self.start_time
            self.running = True
            self.update_time()
            if self.voice_enabled:
                self.engine.say(f"{self.mode} started")
                self.engine.runAndWait()
        
    def lap(self):
        if self.running:
            lap_time = self.time_label.cget("text")
            self.laps.append(lap_time)
            self.lap_listbox.insert(tk.END, f"Lap {len(self.laps)}: {lap_time}")
        
    def stop(self):
        if self.running:
            self.running = False
            if self.voice_enabled:
                self.engine.say(f"{self.mode} stopped")
                self.engine.runAndWait()
        
    def reset(self):
        self.running = False
        self.start_time = None
        self.laps.clear()
        self.lap_listbox.delete(0, tk.END)
        self.time_label.config(text="00:00:00")
        
    def save_to_csv(self):
        if not self.laps:
            messagebox.showerror("Error", "No laps to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Lap Number", "Time"])
                for i, lap in enumerate(self.laps, 1):
                    writer.writerow([i, lap])
            messagebox.showinfo("Saved", f"Laps saved to {file_path}")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchPro(root)
    root.mainloop()
