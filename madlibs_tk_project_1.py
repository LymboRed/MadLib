# -------------------- 🧱 1. IMPORTATION DES OUTILS ----------------------------------------
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk # Pour le look ultra-moderne 2025
import os

# Configuration globale de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

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
# Palette de couleurs Glassmorphism
BG_MAIN = "#0f172a"
BG_SIDE = "#1e293b"
BG_ENTRY = "#334155"
ACCENT_COLOR = "#38bdf8"
TEXT_COLOR = "#f8fafc"

# Couleurs des boutons (plus sombres pour le contraste)
GENERATE_COLOR = "#059669" # Vert Emeraude sombre
SAVE_COLOR = "#d97706"     # Orange Ambre sombre
RESET_COLOR = "#dc2626"    # Rouge sombre

# Fenêtre principale
root = ctk.CTk()
root.title("Mad Libs - Lion King Edition")
root.geometry("1100x700")
root.configure(fg_color=BG_MAIN)

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
main_container = ctk.CTkFrame(root, fg_color=BG_MAIN)
main_container.pack(fill="both", expand=True, padx=30, pady=30)

left_panel = ctk.CTkFrame(main_container, fg_color=BG_SIDE, corner_radius=25)
left_panel.pack(side="left", fill="both", expand=False, padx=(0, 20))

right_panel = ctk.CTkFrame(main_container, fg_color=BG_SIDE, corner_radius=25)
right_panel.pack(side="right", fill="both", expand=True)

# -------------------- ✏️ 4. CHAMPS DE SAISIE ----------------------------------------
ctk.CTkLabel(left_panel, text="STORY INPUTS", font=("SF Pro Display", 18, "bold"), 
             text_color=ACCENT_COLOR).pack(pady=(25, 15))

scroll_frame = ctk.CTkScrollableFrame(left_panel, fg_color="transparent", width=320)
scroll_frame.pack(fill="both", expand=True, padx=15, pady=10)

# Pour chaque champ :
for field in fields:
    ctk.CTkLabel(scroll_frame, text=field.upper(), font=("SF Pro Text", 10, "bold"),
                 text_color=TEXT_COLOR).pack(anchor="w", padx=15, pady=(12, 2))
    entry = ctk.CTkEntry(scroll_frame, placeholder_text=f"Enter {field}...",
                         fg_color=BG_ENTRY, border_color="#475569", 
                         height=45, corner_radius=12)
    entry.pack(fill="x", padx=10, pady=(0, 5))
    entries.append(entry)

# -------------------- 🔘 5. Boutons stylisés Glass ------------------------------------------------
btn_container = ctk.CTkFrame(left_panel, fg_color="transparent")
btn_container.pack(fill="x", padx=20, pady=25)

def create_btn(text, color, cmd):
    btn = ctk.CTkButton(btn_container, text=text, command=cmd, 
                        fg_color=color, hover_color="#047857", 
                        font=("SF Pro Text", 13, "bold"),
                        height=50, corner_radius=18)
    btn.pack(fill="x", pady=6)

create_btn("GENERATE MAGIC ✨", GENERATE_COLOR, generate_story)
create_btn("SAVE STORY 💾", SAVE_COLOR, save_story)
create_btn("CLEAR ALL 🧹", RESET_COLOR, reset_fields)

# -------------------- 📝 6. Zone d’affichage ----------------------------------------
ctk.CTkLabel(right_panel, text="LIVE STORY PREVIEW", font=("SF Pro Display", 22, "bold"), 
             text_color=ACCENT_COLOR).pack(pady=(25, 10))

# Zone de texte stylisée
text_output = tk.Text(right_panel, wrap="word", font=("Georgia", 16), 
                      bg=BG_SIDE, fg=TEXT_COLOR, relief="flat", 
                      padx=40, pady=40, spacing1=12)
text_output.pack(fill="both", expand=True, padx=25, pady=25)
text_output.insert(tk.END, "Your story will appear here...")
text_output.config(state='disabled')

# -------------------- 🏁 7. Démarrage de l’application --------------------------------------------
# 🎬 C’est la boucle principale : elle lance l’interface et la garde ouverte jusqu’à ce que tu fermes la fenêtre.
root.mainloop()