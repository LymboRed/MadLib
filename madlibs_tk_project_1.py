# -------------------- 🧱 1. IMPORTATION DES OUTILS ----------------------------------------
import tkinter as tk
from tkinter import messagebox
import os

# -------------------- 🏗️ 2. FONCTIONS PRINCIPALES ------------------------------------------------
# 💾 Sauvegarder l’histoire
def save_story():
    story = text_output.get("1.0", tk.END).strip()
    if not story:
        messagebox.showwarning("Sauvegarde", "Génère d'abord une histoire avant de sauvegarder !")
        return
    
    try:
        with open("mon_histoire.txt", "w", encoding="utf-8") as file:
            file.write(story)
        messagebox.showinfo("Sauvegarde", "Histoire sauvegardée dans 'mon_histoire.txt' ! ✅")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")

# 🎬 Générer l’histoire
# ✅ On vérifie si tous les champs sont remplis. Si non → alerte !
def generate_story():
    values = [entry.get() for entry in entries] # Récupere tout ce que l'utilisateur a tapé
    if not all(values): # Vérifie que tout est remplie
        messagebox.showwarning("Champs manquants", "Merci de remplir tous les champs.")
        return
    # 🎩 On donne un nom à chaque réponse (comme des variables normales).
    animal_name, job, first_name, thing, villain_name, place, silly_name_1, silly_name_2, funny_phrase, an_object, title = values
    # 🧠 On crée l'histoire avec les variables insérées dedans
    story = (
        f"In the heart of the African savannah, "
        f"a young lion named {animal_name} was destined to become a {job}. "
        f"One day, his father, King {first_name}, told him: "
        f"\"Everything the {thing} touches is our kingdom.\" "
        f"But after a tragic accident caused by {villain_name}, "
        f"he ran away to {place}. "
        f"There, he met two unusual friends: {silly_name_1} and {silly_name_2}, "
        f"who taught him to say {funny_phrase}! "
        f"Years later, he returned to face his past, "
        f"battle {villain_name} with a {an_object}, "
        f"and reclaim his place as the rightful {title}."
    )
    text_output.config(state='normal') # Active le champs de texte
    text_output.delete("1.0", tk.END) # Vide l'ancien texte
    text_output.insert(tk.END, story) # Insère la nouvelle histoire
    text_output.config(state='disabled') # Re-désactive le champ de texte pour empêcher la modification
# 🔄 Réinitialiser les champs
# 🧹 Vide tous les champs de texte
def reset_fields():
    for entry in entries:
        entry.delete(0, tk.END)
    # 🧽 Vide aussi le champ de l’histoire
    text_output.config(state='normal')
    text_output.delete("1.0", tk.END)
    text_output.config(state='disabled')

# -------------------- 🖼️ 3. INTERFACE GRAPHIQUE --------------------------------------------------
# Couleurs Modernes (Look 2025+ Dark Mode)
BG_MAIN = "#0f172a"      # Bleu ardoise très sombre
BG_SIDE = "#1e293b"      # Bleu ardoise moyen
BG_ENTRY = "#334155"     # Pour les champs de saisie
TEXT_COLOR = "#f8fafc"   # Blanc cassé
ACCENT_COLOR = "#38bdf8" # Bleu ciel brillant
GENERATE_COLOR = "#10b981" # Vert émeraude
RESET_COLOR = "#ef4444"    # Rouge corail
SAVE_COLOR = "#f59e0b"     # Ambre

# Création de la fenêtre principale
root = tk.Tk()
root.title("Mad Libs - Lion King Edition")
root.geometry("1000x650")
root.configure(bg=BG_MAIN)

# Chargement de l'icône (si le fichier existe)
try:
    img = tk.PhotoImage(file="icon.png")
    root.iconphoto(False, img)
except Exception as e:
    print(f"Erreur chargement icône : {e}")

# Styles personnalisés
label_style = {"bg": BG_SIDE, "fg": ACCENT_COLOR, "font": ("SF Pro Display", 10, "bold")}
entry_style = {
    "font": ("SF Pro Text", 11),
    "bg": BG_ENTRY,
    "fg": "white",
    "insertbackground": "white", # Curseur blanc
    "relief": "flat",
    "highlightthickness": 1,
    "highlightbackground": "#475569",
    "highlightcolor": ACCENT_COLOR
}

# Main Containers with padding
main_container = tk.Frame(root, bg=BG_MAIN)
main_container.pack(fill="both", expand=True, padx=20, pady=20)

left_frame = tk.Frame(main_container, width=380, bg=BG_SIDE, padx=20, pady=20)
right_frame = tk.Frame(main_container, bg=BG_MAIN, padx=20)

left_frame.pack(side="left", fill="both", expand=False)
right_frame.pack(side="right", fill="both", expand='True')

# Coins arrondis visuels (simulation via structure)
left_frame.config(highlightthickness=0) # Pour garder un look flat et propre

# -------------------- ✏️ 4. CREATION DES CHAMPS DE SAISIE ----------------------------------------
fields = [
    "Animal Name", "Job", "First Name", "Thing", "Villain Name",
    "Place", "Silly Name 1", "Silly Name 2", "Funny Phrase",
    "Object", "Title"
]
entries = []

# Header à gauche
tk.Label(left_frame, text="STORY INPUTS", font=("SF Pro Display", 14, "bold"), 
         bg=BG_SIDE, fg=TEXT_COLOR).pack(pady=(0, 20))

# Conteneur pour le scroll
canvas = tk.Canvas(left_frame, bg=BG_SIDE, highlightthickness=0)
scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=BG_SIDE)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=300)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)

# Pour chaque champ :
for field in fields:
    label = tk.Label(scrollable_frame, text=field.upper(), **label_style)
    label.pack(anchor="w", pady=(8, 2))
    entry = tk.Entry(scrollable_frame, **entry_style)
    entry.pack(fill="x", pady=(0, 5), ipady=5)
    entries.append(entry)

# -------------------- 🔘 5. Les boutons -----------------------------------------------------------
button_frame = tk.Frame(left_frame, bg=BG_SIDE)
button_frame.pack(fill="x", pady=(20, 0))

def create_modern_button(parent, text, color, cmd):
    btn = tk.Button(parent, text=text, command=cmd, 
                    bg=color, fg="white", font=("SF Pro Text", 11, "bold"), 
                    relief="flat", cursor="hand2", activebackground=color,
                    pady=10)
    btn.pack(fill="x", pady=5)
    return btn

create_modern_button(button_frame, "GENERATE MAGIC ✨", GENERATE_COLOR, generate_story)
create_modern_button(button_frame, "SAVE STORY 💾", SAVE_COLOR, save_story)
create_modern_button(button_frame, "CLEAR ALL 🧹", RESET_COLOR, reset_fields)

# -------------------- 📝 6. Zone d’affichage de l’histoire ----------------------------------------
title_label = tk.Label(right_frame, text="LIVE STORY PREVIEW", font=("SF Pro Display", 16, "bold"), 
                       bg=BG_MAIN, fg=ACCENT_COLOR)
title_label.pack(pady=(0, 15))

# Zone de texte stylisée
text_container = tk.Frame(right_frame, bg=BG_ENTRY, padx=2, pady=2) # Pour simuler une bordure
text_container.pack(fill="both", expand=True)

text_output = tk.Text(text_container, wrap="word", font=("Georgia", 14), 
                      bg=BG_MAIN, fg=TEXT_COLOR, relief="flat", padx=30, pady=30,
                      spacing1=10, spacing2=5) # Meilleure lisibilité
text_output.pack(fill="both", expand=True)
text_output.insert(tk.END, "Your story will appear here...")
text_output.config(state='disabled')

# -------------------- 🏁 7. Démarrage de l’application --------------------------------------------
# 🎬 C’est la boucle principale : elle lance l’interface et la garde ouverte jusqu’à ce que tu fermes la fenêtre.
root.mainloop()