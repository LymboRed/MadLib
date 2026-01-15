# -------------------- 🧱 1. IMPORTATION DES OUTILS ----------------------------------------
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk # Pour le look ultra-moderne 2025
import os

# Configuration globale de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -------------------- 🏗️ 2. FONCTIONS PRINCIPALES ------------------------------------------------
# Dictionnaire des thèmes
THEMES_DATA = {
    "Lion King 🦁": {
        "fields": ["Animal Name", "Job", "First Name", "Thing", "Villain Name", "Place", "Silly Name 1", "Silly Name 2", "Funny Phrase", "Object", "Title"],
        "template": (
            "In the heart of the African savannah, a young lion named {} was destined to become a {}. "
            "One day, his father, King {}, told him: \"Everything the {} touches is our kingdom.\" "
            "But after a tragic accident caused by {}, he ran away to {}. "
            "There, he met two unusual friends: {} and {}, who taught him to say {}! "
            "Years later, he returned to face his past, battle {} with a {}, and reclaim his place as the rightful {}."
        )
    },
    "Space Adventure 🚀": {
        "fields": ["Pilot Name", "Planet", "Mission", "Alien Species", "Ship Name", "Weapon", "Strange Food", "Droid Name", "Galactic Law", "Star System", "Honorary Rank"],
        "template": (
            "Deep in the {}, the brave pilot {} was on a mission to {}. "
            "After landing on {}, they encountered a friendly {} ship named the {}. "
            "Suddenly, a swarm of {} attacked! {} grabbed a {} and fought back. "
            "Their loyal droid {} shouted '{}!' while throwing {} at the enemies. "
            "In the end, peace was restored, and {} was granted the rank of {}."
        )
    },
    "Medieval Tale ⚔️": {
        "fields": ["Hero Name", "Kingdom", "Quest", "Mythical Beast", "Magical Item", "Royal Family Member", "Village", "Worst Enemy", "Old Wizard", "Ancient Relic", "Ending Title"],
        "template": (
            "In the glorious kingdom of {}, a humble hero named {} set out on a quest to {}. "
            "Armed only with a {}, they had to face the terrifying {} sent by {}. "
            "Along the way, they met {}, who gave them a mysterious {}. "
            "After a long journey through the village of {}, they saved {} and returned home. "
            "For their bravery, the {} of the Realm now call them the {}."
        )
    }
}

# Fonction pour changer de thème
def change_theme(choice):
    # Nettoyer les anciens champs
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    entries.clear()
    
    # Créer les nouveaux champs
    for field in THEMES_DATA[choice]["fields"]:
        ctk.CTkLabel(scroll_frame, text=field.upper(), font=("SF Pro Text", 10, "bold"),
                     text_color=TEXT_COLOR).pack(anchor="w", padx=15, pady=(12, 2))
        entry = ctk.CTkEntry(scroll_frame, placeholder_text=f"Enter {field}...",
                             fg_color=BG_ENTRY, border_color="#475569", 
                             height=45, corner_radius=12)
        entry.pack(fill="x", padx=10, pady=(0, 5))
        entries.append(entry)

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

# 🎬 Générer l’histoire avec animation Typewriter et Highlighting
def generate_story():
    values = [entry.get() for entry in entries]
    if not all(values):
        messagebox.showwarning("Champs manquants", "Merci de remplir tous les champs.")
        return
    
    current_theme = theme_selector.get()
    template = THEMES_DATA[current_theme]["template"]
    
    # Préparation des segments pour l'animation
    # On découpe le template pour savoir où insérer les mots de l'utilisateur
    parts = template.split("{}")
    full_sequence = [] # Liste de tuples (texte, est_un_mot_utilisateur)
    
    for i in range(len(parts)):
        full_sequence.append((parts[i], False))
        if i < len(values):
            full_sequence.append((values[i], True))
            
    text_output.config(state='normal')
    text_output.delete("1.0", tk.END)
    
    # Fonction récursive pour l'effet d'écriture
    def type_writer(seq_idx, char_idx):
        if seq_idx >= len(full_sequence):
            text_output.config(state='disabled')
            return
        
        content, is_val = full_sequence[seq_idx]
        
        if char_idx < len(content):
            char = content[char_idx]
            text_output.insert(tk.END, char)
            
            # Si c'est un mot utilisateur, on applique le style "highlight"
            if is_val:
                # Applique le tag sur le dernier caractère inséré
                end_pos = text_output.index("end-1c")
                start_pos = f"{end_pos.split('.')[0]}.{int(end_pos.split('.')[1])-1}"
                text_output.tag_add("highlight", start_pos, end_pos)
            
            text_output.see(tk.END) # Scroll automatique
            root.after(15, type_writer, seq_idx, char_idx + 1)
        else:
            # Passe au segment suivant
            type_writer(seq_idx + 1, 0)

    type_writer(0, 0)
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
ctk.CTkLabel(left_panel, text="SELECT THEME", font=("SF Pro Display", 16, "bold"), 
             text_color=ACCENT_COLOR).pack(pady=(20, 5))

theme_selector = ctk.CTkOptionMenu(left_panel, values=list(THEMES_DATA.keys()), 
                                  command=change_theme, fg_color=BG_ENTRY, 
                                  button_color=ACCENT_COLOR, button_hover_color=GENERATE_COLOR,
                                  corner_radius=10)
theme_selector.pack(fill="x", padx=20, pady=(0, 20))

ctk.CTkLabel(left_panel, text="STORY INPUTS", font=("SF Pro Display", 18, "bold"), 
             text_color=ACCENT_COLOR).pack(pady=(10, 5))

scroll_frame = ctk.CTkScrollableFrame(left_panel, fg_color="transparent", width=320)
scroll_frame.pack(fill="both", expand=True, padx=15, pady=10)

entries = []

# Initialisation des champs avec le premier thème
change_theme(list(THEMES_DATA.keys())[0])

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

# Configuration du style pour les mots mis en évidence (Highlight)
text_output.tag_configure("highlight", foreground=ACCENT_COLOR, font=("Georgia", 16, "bold"))

text_output.insert(tk.END, "Your story will appear here...")
text_output.config(state='disabled')

# -------------------- 🏁 7. Démarrage de l’application --------------------------------------------
# 🎬 C’est la boucle principale : elle lance l’interface et la garde ouverte jusqu’à ce que tu fermes la fenêtre.
root.mainloop()