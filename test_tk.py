import tkinter as tk
root = tk.Tk()
root.title("Test Tkinter")
label = tk.Label(root, text="Si tu vois cette fenêtre, Tkinter fonctionne !")
label.pack(pady=20)
root.after(3000, lambda: root.destroy()) # Ferme après 3s
root.mainloop()
