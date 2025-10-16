# consensual_keylogger.py
# Outil éthique de capture de frappes (consentement requis, visible, non furtif).
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

class ConsensualLogger(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consensual Key Logger (éthique)")
        self.geometry("640x420")
        self.resizable(False, False)

        tk.Label(self, text="Outil éthique de capture de frappes", font=("Segoe UI", 14, "bold")).pack(pady=8)
        tk.Label(self, text="Cet outil n'enregistre que si vous cliquez sur 'Start' et confirmez le consentement.", wraplength=600).pack()

        self.status_var = tk.StringVar(value="État : stopped")
        tk.Label(self, textvariable=self.status_var, fg="red", font=("Segoe UI", 10, "bold")).pack(pady=6)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=6)
        self.start_btn = tk.Button(btn_frame, text="Start recording", command=self.start_recording)
        self.start_btn.pack(side="left", padx=6)
        self.stop_btn = tk.Button(btn_frame, text="Stop recording", command=self.stop_recording, state="disabled")
        self.stop_btn.pack(side="left", padx=6)
        tk.Button(btn_frame, text="Choose file", command=self.choose_file).pack(side="left", padx=6)

        self.filepath_var = tk.StringVar(value="Aucun fichier sélectionné")
        tk.Label(self, textvariable=self.filepath_var, wraplength=600).pack(pady=4)

        tk.Label(self, text="Dernière touche :", font=("Segoe UI", 11)).pack(pady=(10,0))
        self.last_var = tk.StringVar(value="—")
        tk.Label(self, textvariable=self.last_var, font=("Consolas", 18)).pack(pady=6)

        tk.Label(self, text="Historique (en mémoire, non sauvegardé automatiquement) :", font=("Segoe UI", 10)).pack()
        self.hist_text = tk.Text(self, width=78, height=12, state="disabled", wrap="none", font=("Consolas", 10))
        self.hist_text.pack(padx=10, pady=6)

        bottom = tk.Frame(self)
        bottom.pack(fill="x", padx=10, pady=6)
        tk.Button(bottom, text="Clear", command=self.clear_history).pack(side="left")
        tk.Button(bottom, text="Quit", command=self.on_quit).pack(side="right")

        self.bind("<Key>", self.on_key)
        self.bind("<FocusIn>", lambda e: None)

        self.recording = False
        self.filepath = None
        self.history = []

    def choose_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files","*.txt"),("All files","*.*")])
        if path:
            self.filepath = path
            self.filepath_var.set(f"Fichier: {self.filepath}")

    def start_recording(self):
        if not self.filepath:
            messagebox.showwarning("Fichier manquant", "Choisis d'abord un fichier pour sauvegarder.")
            return
        confirm = messagebox.askyesno("Consentement requis",
                                      "Tu confirmes que toutes les personnes dont les frappes seront enregistrées ont donné leur CONSENTEMENT explicite ?")
        if not confirm:
            return
        self.recording = True
        self.status_var.set("État : recording")
        self.status_var_label_color("green")
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        # write header
        try:
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(f"\n--- Enregistrement démarré: {datetime.now().isoformat()} ---\n")
        except Exception as e:
            messagebox.showerror("Erreur fichier", f"Impossible d'ouvrir le fichier: {e}")
            self.recording = False
            self.status_var.set("État : stopped")
            self.status_var_label_color("red")

    def stop_recording(self):
        if self.recording:
            try:
                with open(self.filepath, "a", encoding="utf-8") as f:
                    f.write(f"--- Enregistrement arrêté: {datetime.now().isoformat()} ---\n")
            except Exception:
                pass
        self.recording = False
        self.status_var.set("État : stopped")
        self.status_var_label_color("red")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

    def status_var_label_color(self, color):
        # quick hack to color the label
        for widget in self.pack_slaves():
            pass
        # set color (there's only one status label)
        # find label by var
        for w in self.winfo_children():
            if isinstance(w, tk.Label) and getattr(w, "cget", lambda x:None)("textvariable") == str(self.status_var):
                w.config(fg=color)

    def on_key(self, event):
        keyname = event.keysym
        ch = event.char if event.char and event.char.isprintable() else ""
        entry = f"{datetime.now().isoformat(timespec='seconds')}  {keyname}" + (f"  ({ch})" if ch else "")
        self.last_var.set(keyname)
        self.history.insert(0, entry)
        if len(self.history) > 200:
            self.history.pop()
        self.refresh_history()
        if self.recording and self.filepath:
            try:
                with open(self.filepath, "a", encoding="utf-8") as f:
                    f.write(entry + "\n")
            except Exception:
                pass

    def refresh_history(self):
        self.hist_text.config(state="normal")
        self.hist_text.delete("1.0", tk.END)
        for line in self.history:
            self.hist_text.insert(tk.END, line + "\n")
        self.hist_text.config(state="disabled")

    def clear_history(self):
        self.history.clear()
        self.refresh_history()
        self.last_var.set("—")

    def on_quit(self):
        if self.recording:
            if not messagebox.askyesno("Quitter", "L'enregistrement est en cours. Arrêter et quitter ?"):
                return
            self.stop_recording()
        self.destroy()

if __name__ == "__main__":
    app = ConsensualLogger()
    app.mainloop()
