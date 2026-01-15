# -------------------- 🧱 1. IMPORTATION DES OUTILS TKINTER ----------------------------------------
# 🧰 On importe Tkinter pour créer l’interface graphique. messagebox permet d’afficher des alertes, comme "Tu as oublié de remplir un champ !"
import tkinter as tk
from tkinter import messagebox

# -------------------- 🏗️ 2. FONCTIONS PRINCIPALES ------------------------------------------------
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
# Création de la fenêtre principale, avec un titre
root = tk.Tk()
root.title("Mad Libs - Lion King Edition")
root.geometry("900x500") # Large Window

# Main Containers
left_frame = tk.Frame(root, width=360) # 40% of 900 = 360px
right_frame = tk.Frame(root, width=540) # 60% of 900 = 540px
left_frame.pack(side="left", fill="both", expand=False)
right_frame.pack(side="right", fill="both", expand='True')

# -------------------- ✏️ 4. CREATION DES CHAMPS DE SAISIE ----------------------------------------
# 📋 Liste de tous les types de champs qu’on va demander à l’utilisateur.
# --- Left Panel - Inputs ---
fields = [
    "Animal Name", "Job", "First Name", "Thing", "Villain Name",
    "Place", "Silly Name 1", "Silly Name 2", "Funny Phrase",
    "Object", "Title"
]
entries = []
# Pour chaque champ :
# On crée une étiquette (Label)
# Un champ de saisie (Entry)
# Et on le garde dans une liste entries pour pouvoir le récupérer plus tard
for field in fields:
    label = tk.Label(left_frame, text=field)
    label.pack(anchor="w", padx=10)
    entry = tk.Entry(left_frame)
    entry.pack(fill="x", padx=10, pady=2)
    entries.append(entry)

# -------------------- 🔘 5. Les boutons -----------------------------------------------------------
# Deux boutons :
# "Generate" lance generate_story
# "Reset" vide les champs avec reset_fields
tk.Button(root, text="Generate Story", command=generate_story).pack(pady=10)
tk.Button(root, text="Reset", command=reset_fields).pack()

# -------------------- 📝 6. Zone d’affichage de l’histoire ----------------------------------------
# C’est ici que l’histoire s’affiche.
# state='disabled' = empêche l’utilisateur de modifier l’histoire
# wrap=tk.WORD = coupe les lignes proprement entre les mots
# --- Right Panel - Text output ---
text_output = tk.Text(right_frame, wrap="word", font=("Helvetica", 12))
text_output.pack(fill="both", expand=True, padx=10, pady=10)

# -------------------- 🏁 7. Démarrage de l’application --------------------------------------------
# 🎬 C’est la boucle principale : elle lance l’interface et la garde ouverte jusqu’à ce que tu fermes la fenêtre.
root.mainloop()