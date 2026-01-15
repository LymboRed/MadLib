# -------------------- 🧱 1. IMPORTATION DES OUTILS ----------------------------------------
import tkinter as tk
from tkinter import messagebox
import pygame # Pour la musique
import os

# Initialisation de Pygame Mixer
pygame.mixer.init()

# -------------------- 🏗️ 2. FONCTIONS PRINCIPALES ------------------------------------------------
# 🎵 Gérer la musique
music_playing = False

def toggle_music():
    global music_playing
    music_file = "background_music.mp3" # Nom du fichier attendu
    
    if not os.path.exists(music_file):
        messagebox.showinfo("Musique", f"Fichier '{music_file}' introuvable. Ajoutes-en un pour activer la musique !")
        return

    if not music_playing:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1) # -1 pour tourner en boucle
        btn_music.config(text="Stop Music 🔇")
        music_playing = True
    else:
        pygame.mixer.music.stop()
        btn_music.config(text="Play Music 🎵")
        music_playing = False

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
root.geometry("900x600") # Un peu plus haut pour accommoder les champs
root.configure(bg="#f0f0f0") # Couleur de fond gris clair

# Chargement de l'icône (si le fichier existe)
try:
    img = tk.PhotoImage(file="icon.png")
    root.iconphoto(False, img)
except Exception as e:
    print(f"Erreur chargement icône : {e}")

# Styles pour les widgets
label_style = {"bg": "#f0f0f0", "font": ("Helvetica", 10, "bold"), "fg": "#333333"}
entry_style = {"font": ("Helvetica", 10), "relief": "flat", "highlightthickness": 1, "highlightbackground": "#cccccc"}

# Main Containers
left_frame = tk.Frame(root, width=360, bg="#f0f0f0") # 40% of 900 = 360px
right_frame = tk.Frame(root, width=540, bg="white") # 60% of 900 = 540px
left_frame.pack(side="left", fill="both", expand=False, padx=20, pady=20)
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

# Conteneur pour le scroll des champs si nécessaire
canvas = tk.Canvas(left_frame, bg="#f0f0f0", highlightthickness=0)
scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="both")

# Pour chaque champ :
for field in fields:
    label = tk.Label(scrollable_frame, text=field, **label_style)
    label.pack(anchor="w", pady=(5, 0))
    entry = tk.Entry(scrollable_frame, **entry_style)
    entry.pack(fill="x", pady=(0, 5), ipady=3)
    entries.append(entry)

# -------------------- 🔘 5. Les boutons -----------------------------------------------------------
button_frame = tk.Frame(left_frame, bg="#f0f0f0")
button_frame.pack(fill="x", pady=20)

gen_button = tk.Button(button_frame, text="Generate Story ✨", command=generate_story, 
                       bg="#4CAF50", fg="black", font=("Helvetica", 11, "bold"), 
                       relief="flat", cursor="hand2")
gen_button.pack(fill="x", pady=5)

reset_button = tk.Button(button_frame, text="Reset 🧹", command=reset_fields, 
                         bg="#f44336", fg="black", font=("Helvetica", 11), 
                         relief="flat", cursor="hand2")
reset_button.pack(fill="x")

# Nouveau bouton pour la musique
btn_music = tk.Button(button_frame, text="Play Music 🎵", command=toggle_music,
                      bg="#2196F3", fg="black", font=("Helvetica", 11),
                      relief="flat", cursor="hand2")
btn_music.pack(fill="x", pady=(10, 0))

# -------------------- 📝 6. Zone d’affichage de l’histoire ----------------------------------------
# C’est ici que l’histoire s’affiche.
# state='disabled' = empêche l’utilisateur de modifier l’histoire
# wrap=tk.WORD = coupe les lignes proprement entre les mots
# --- Right Panel - Text output ---
title_label = tk.Label(right_frame, text="Your Story", font=("Helvetica", 16, "bold"), bg="white", fg="#333333")
title_label.pack(pady=(20, 10))

text_output = tk.Text(right_frame, wrap="word", font=("Helvetica", 13), 
                      bg="white", fg="#444444", relief="flat", padx=20, pady=20)
text_output.pack(fill="both", expand=True)
text_output.config(state='disabled')

# -------------------- 🏁 7. Démarrage de l’application --------------------------------------------
# 🎬 C’est la boucle principale : elle lance l’interface et la garde ouverte jusqu’à ce que tu fermes la fenêtre.
root.mainloop()