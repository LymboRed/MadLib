# -------------------- 🧱 1. IMPORTATION DES OUTILS ----------------------------------------
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk # Pour le look ultra-moderne 2025
import os
import re
import threading
import datetime
from PIL import Image, ImageTk
import requests
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
# override=True permet d'écraser les variables d'environnement si elles existent déjà
load_dotenv(override=True)

# Configuration globale de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -------------------- 🏗️ 2. FONCTIONS PRINCIPALES ------------------------------------------------
# 🔑 CONFIGURATION API (Chargée depuis le fichier .env)
# NE PARTAGE JAMAIS TON FICHIER .env SUR GITHUB
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 

# Debug: Affiche si la clé est détectée (SANS l'afficher en entier)
if OPENAI_API_KEY:
    print(f"DEBUG: API Key detected (Starts with: {OPENAI_API_KEY[:8]}...)")
else:
    print("DEBUG: No API Key found in environment or .env file.")

# Initialisation du client OpenAI (sera configuré si la clé est présente)
client = None
if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-votre"):
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    print("DEBUG: OpenAI Client NOT initialized (Key is missing or is still a placeholder)")

# Dictionnaire des thèmes
THEMES_DATA = {
    "Lion King 🦁": {
        "fields": ["Animal Name", "Job", "Father's Name", "Kingdom", "Villain Name", "Exile Place", "Friend 1", "Friend 2", "Funny Phrase", "Weapon", "Title"],
        "template": (
            "In the heart of the African savannah, a young lion named {0} was destined to become a {1}. "
            "One day, his father, King {2}, told him: \"Everything the {3} touches is our kingdom.\" "
            "But after a tragic accident caused by {4}, he ran away to {5}. "
            "There, he met two unusual friends: {6} and {7}, who taught him to say {8}! "
            "Years later, he returned to face his past, battle {4} with a {9}, and reclaim his place as the rightful {10}."
        ),
        "visual_template": "A majestic lion standing on a grand natural rock overlooking a vast African savannah ecosystem. Royal atmosphere, golden hour sun, cinematic high-quality digital animation style."
    },
    "Space Adventure 🚀": {
        "fields": ["Pilot Name", "Target Planet", "Mission Name", "Alien Species", "Ship Name", "Weapon", "Space Food", "Droid Name", "Droid Catchphrase", "Star System", "Honorary Rank"],
        "template": (
            "Deep in the {9}, the brave pilot {0} was on the '{2}' mission. "
            "After landing on {1}, they encountered a friendly {3} ship named the {4}. "
            "Suddenly, a swarm of enemies attacked! {0} grabbed a {5} and fought back. "
            "Their loyal droid {7} shouted '{8}!' while throwing {6} at the enemies. "
            "In the end, peace was restored, and {0} was granted the rank of {10}."
        ),
        "visual_template": "A high-tech futuristic explorer ship flying through a glowing colorful galactic nebula. Stars and planets in the background, epic space opera style, digital painting."
    },
    "Medieval Tale ⚔️": {
        "fields": ["Hero Name", "Kingdom", "Quest", "Mythical Beast", "Magical Item", "Royal Person", "Village", "Worst Enemy", "Old Wizard", "Ancient Relic", "Ending Title"],
        "template": (
            "In the glorious kingdom of {1}, a humble hero named {0} set out on a quest to {2}. "
            "Armed only with a {4}, they had to face the terrifying {3} sent by {7}. "
            "Along the way, they met {8}, who gave them a mysterious {9}. "
            "After a long journey through the village of {6}, they saved {5} and returned home. "
            "For their bravery, the citizens of the Realm now call them the {10}."
        ),
        "visual_template": "An epic fantasy hero standing before a magnificent castle with banners flying. Mythical landscapes, legendary quest atmosphere, oil painting art style."
    },
    "Cyberpunk Neon ⚡️": {
        "fields": ["Netrunner Alias", "Megacity District", "Corporate Name", "Augmentation", "Hack Name", "Fixer Name", "Contact Person", "Vehicle", "Hidden Base", "Neural Chip", "Street Cred Rank"],
        "template": (
            "In the neon-drenched streets of {1}, the legendary netrunner {0} was planning a heist against {2}. "
            "Equipped with a deadly {3}, they prepared the '{4}' exploit. "
            "Their fixer, {5}, sent a message: 'Meet {6} at the {8} immediately.' "
            "They hopped on their {7} and sped through the city. "
            "After a high-speed chase, they successfully stole the {9}. "
            "Word spread across the Net, and {0} was finally recognized as a {10}."
        ),
        "visual_template": "A futuristic city at night with massive neon billboards in pink and blue. Rain reflecting on asphalt, aesthetic synthwave atmosphere, hyper-detailed digital art."
    },
    "Pirate Legends 🏴‍☠️": {
        "fields": ["Captain Name", "Pirate Ship", "Hidden Island", "Sea Monster", "Treasure Type", "Enemy Admiral", "Crew Member", "Signature Drink", "Battle Cry", "First Mate", "Legendary Title"],
        "template": (
            "The fearsome Captain {0} set sail on the '{1}' in search of {4}. "
            "While navigating near {2}, they were suddenly attacked by a giant {3}! "
            "'{8}!' shouted {9} as they loaded the cannons. "
            "After defeating the beast, they shared a round of {7} with {6}. "
            "However, Admiral {5} was hot on their trail. "
            "The battle was fierce, but {0} escaped and became known as the {10} of the Seven Seas."
        ),
        "visual_template": "An old wooden pirate ship with white sails on a turquoise ocean. Tropical island with palm trees in the background, adventure art style, golden hour lighting."
    },
    "Samurai Path 🏮": {
        "fields": ["Samurai Name", "Feudal Lord", "Clan Name", "Legendary Katana", "Village Name", "Arch Rival", "Favorite Tea", "Zen Saying", "Battle Location", "Special Technique", "Honor Title"],
        "template": (
            "In the era of the {2} clan, the wandering samurai {0} served Lord {1}. "
            "Armed with the '{3}', they protected the peaceful village of {4}. "
            "One day, their arch rival {5} challenged them to a duel at {8}. "
            "Before the fight, {0} sat calmly drinking {6} and whispered: '{7}'. "
            "With a swift '{9}' move, the battle was won. "
            "From that day on, {0} was honored with the title of {10}."
        ),
        "visual_template": "A lone samurai in traditional armor standing in a field of cherry blossoms (sakura). Ancient Japanese architecture in the mist, Zen atmosphere, artistic digital illustration."
    },
    "Viking Saga 🪓": {
        "fields": ["Viking Leader", "Longship Name", "Target Kingdom", "Norse God", "Weapon", "Great Hall", "Rival Jarl", "Beast", "War Cry", "Feast Food", "Saga Title"],
        "template": (
            "From the frozen North, {0} led the crew of the '{1}' towards the shores of {2}. "
            "They prayed to {3} for strength and gripped their mighty {4}. "
            "In the distance, Jarl {6} was waiting with a massive army and a trained {7}. "
            "'{8}!' roared the Vikings as they charged. "
            "Victory was theirs, and they celebrated in the {5} with plenty of {9}. "
            "The skalds would forever sing the saga of {0}, the {10}."
        ),
        "visual_template": "A majestic viking longship on a dark sea under a green aurora borealis. Snowy mountains and fjords, epic Norse mythology aesthetic, cinematic digital art."
    }
}

# Mapping des couleurs par thème
THEME_COLORS = {
    "Lion King 🦁": "#fbbf24",     # Jaune ambre
    "Space Adventure 🚀": "#818cf8", # Indigo
    "Medieval Tale ⚔️": "#f87171",   # Rouge soft
    "Cyberpunk Neon ⚡️": "#f472b6", # Rose Néon
    "Pirate Legends 🏴‍☠️": "#fb923c", # Orange
    "Samurai Path 🏮": "#4ade80",   # Vert Jade
    "Viking Saga 🪓": "#60a5fa",     # Bleu Azur
}

# Mapping des images locales (à remplir avec vos fichiers)
THEME_IMAGES = {
    "Lion King 🦁": "images/lion.png",
    "Space Adventure 🚀": "images/space.png",
    "Medieval Tale ⚔️": "images/medieval.png",
    "Cyberpunk 2077 ⚡️": "images/cyberpunk.png",
    "Pirate Legends 🏴‍☠️": "images/pirate.png",
    "Samurai Path 🏮": "images/samurai.png",
    "Viking Saga 🪓": "images/viking.png",
}

def update_story_image(theme=None, pil_img=None):
    if not theme and not pil_img:
        story_image_label.configure(image=None, text="Illustration will appear here when you generate magic ✨")
        return
    
    if pil_img:
        try:
            # On passe à un format CARRE plus grand (600x600) pour mieux voir l'IA
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(600, 600))
            story_image_label.configure(image=ctk_img, text="")
            return
        except Exception as e:
            print(f"Error displaying AI image: {e}")

    img_path = THEME_IMAGES.get(theme)
    if img_path and os.path.exists(img_path):
        try:
            pil_img = Image.open(img_path)
            # Les images par défaut des thèmes restent en 512x200 ou s'adaptent au nouveau format carré
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(600, 250))
            story_image_label.configure(image=ctk_img, text="")
        except Exception as e:
            story_image_label.configure(image=None, text=f"Error loading {theme} image ❌")
    else:
        # Si on n'a pas encore l'image, on affiche un texte sympa style IA
        story_image_label.configure(image=None, text=f"🎨 Visualization: {theme}\n(Add {img_path} to see it!)")

# 🤖 Fonction pour appeler l'IA OpenAI dans un thread séparé
def fetch_ai_image(prompt, callback):
    print(f"DEBUG: Starting AI Generation for prompt: {prompt[:100]}...")
    try:
        if not client:
            print("DEBUG: Client OpenAI not initialized (Check your .env and API Key)")
            root.after(0, lambda: callback(None))
            return

        # Appel à DALL-E 3
        # On utilise le prompt formaté qui est déjà visuel et sûr
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"{prompt} High resolution, artistic style, masterpiece.",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        print(f"DEBUG: Image generated successfully! URL: {image_url}")
        
        img_data = requests.get(image_url).content
        pil_img = Image.open(BytesIO(img_data))
        
        # Sauvegarder localement dans un dossier 'images' s'il existe
        if not os.path.exists("images"):
            os.makedirs("images")
            
        filename = f"images/generated_{int(datetime.datetime.now().timestamp())}.png"
        pil_img.save(filename)
        print(f"DEBUG: Image saved to {filename}")
        
        # Retourner à l'UI thread pour mettre à jour
        root.after(0, lambda: callback(pil_img))
    except Exception as e:
        print(f"DEBUG: AI Error occurred: {e}")
        # Message spécifique pour la violation de politique
        if "policy" in str(e).lower() or "safety" in str(e).lower():
            print("DEBUG: Safety filter triggered. The prompt was considered non-compliant.")
            root.after(0, lambda: status_label.configure(text="⚠️ AI Safety: Prompt was rejected. Try milder words.", text_color="red"))
        root.after(0, lambda: callback(None))

# Fonction pour changer de thème
def change_theme(choice):
    # Nettoyer les anciens champs
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    entries.clear()
    
    # 🎨 Mise à jour des couleurs dynamiques
    new_color = THEME_COLORS.get(choice, ACCENT_COLOR)
    theme_selector.configure(button_color=new_color)
    progress_bar.configure(progress_color=new_color)
    
    # 🖼️ Réinitialiser l'image vers le placeholder par défaut du thème
    update_story_image(None)
    progress_bar.pack_forget()
    status_label.configure(text=f"Theme {choice} selected. Ready for magic?", text_color="#94a3b8")
    
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

# 📋 Copier dans le presse-papier
def copy_to_clipboard():
    story = text_output.get("1.0", tk.END).strip()
    if not story or story == "Your story will appear here...":
        messagebox.showwarning("Presse-papier", "Génère d'abord une histoire !")
        return
    root.clipboard_clear()
    root.clipboard_append(story)
    messagebox.showinfo("Presse-papier", "Histoire copiée dans le presse-papier ! 📋")

# 🎬 Générer l’histoire avec animation Typewriter et Highlighting
def generate_story():
    values = [entry.get() for entry in entries]
    if not all(values):
        messagebox.showwarning("Champs manquants", "Merci de remplir tous les champs.")
        return
    
    current_theme = theme_selector.get()
    
    # ⏳ Début du chargement
    status_label.configure(text="🪄 Casting magic spells... Generating story and visuals...", text_color=ACCENT_COLOR)
    progress_bar.set(0)
    progress_bar.pack(fill="x", padx=100, pady=(0, 20))
    
    # Prépare le template final pour l'IA
    theme_entry = THEMES_DATA[current_theme]
    template = theme_entry["template"]
    story_text = template.format(*values)
    
    # 🖼️ Prépare un prompt visuel SÛR pour l'IA (évite les violations de politique)
    visual_template = theme_entry.get("visual_template", "A cinematic scene representing {0}")
    visual_text = visual_template.format(*values)

    # 🖼️ Mettre à jour l'image du thème
    def complete_generation(pil_img=None):
        update_story_image(current_theme, pil_img)
        progress_bar.pack_forget()
        
        # Couleur dynamique pour le texte mis en évidence
        current_color = THEME_COLORS.get(current_theme, ACCENT_COLOR)
        text_output.tag_configure("highlight", foreground=current_color, font=("Georgia", 16, "bold"))
        
        status_label.configure(text="✅ Magic generation complete!", text_color=GENERATE_COLOR)
        
        # 2. Préparation des segments pour l'animation typewriter AVEC highlighting
        parts = re.split(r'(\{.*?\})', template)
        full_sequence = [] # Liste de tuples (texte, est_un_mot_utilisateur)
        
        for part in parts:
            if part.startswith("{") and part.endswith("}"):
                try:
                    idx = int(part[1:-1])
                    if 0 <= idx < len(values):
                        full_sequence.append((values[idx], True))
                except ValueError:
                    pass
            elif part:
                full_sequence.append((part, False))
                
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
                
                if is_val:
                    end_pos = text_output.index("end-1c")
                    start_pos = f"{end_pos.split('.')[0]}.{int(end_pos.split('.')[1])-1}"
                    text_output.tag_add("highlight", start_pos, end_pos)
                
                text_output.see(tk.END)
                root.after(10, type_writer, seq_idx, char_idx + 1)
            else:
                type_writer(seq_idx + 1, 0)

        type_writer(0, 0)

    # Simulation de barre de progression pendant que l'IA travaille
    def start_ai_thread():
        if client:
            status_label.configure(text="🎨 AI is drawing your story... (Wait ~15s)", text_color=ACCENT_COLOR)
            thread = threading.Thread(target=fetch_ai_image, args=(visual_text, complete_generation))
            thread.daemon = True
            thread.start()
        else:
            # Fallback si pas de clé API
            simulate_progress(0)

    def simulate_progress(val):
        if val <= 1.0:
            progress_bar.set(val)
            root.after(30, simulate_progress, val + 0.05)
        else:
            complete_generation()
            
    start_ai_thread()
# 🔄 Réinitialiser les champs
# 🧹 Vide tous les champs de texte
def reset_fields():
    for entry in entries:
        entry.delete(0, tk.END)
    # 🧽 Vide aussi le champ de l’histoire et l'image
    text_output.config(state='normal')
    text_output.delete("1.0", tk.END)
    text_output.config(state='disabled')
    update_story_image(None)
    progress_bar.pack_forget()
    status_label.configure(text="Choose a theme and fill the fields above", text_color="#94a3b8")

# -------------------- 🖼️ 3. INTERFACE GRAPHIQUE --------------------------------------------------
# Palette de couleurs Glassmorphism
BG_MAIN = "#0f172a"
BG_SIDE = "#1e293b"
BG_ENTRY = "#334155"
ACCENT_COLOR = "#38bdf8"
TEXT_COLOR = "#f8fafc"

# Couleurs des boutons (plus sombres pour le contraste)
GENERATE_COLOR = "#059669" # Vert Emeraude sombre
COPY_COLOR = "#6366f1"     # Indigo
SAVE_COLOR = "#d97706"     # Orange Ambre sombre
RESET_COLOR = "#dc2626"    # Rouge sombre

# Fenêtre principale
root = ctk.CTk()
root.title("Mad Libs - Ultimate Multi-Theme Edition")
root.geometry("1100x950")
root.minsize(1100, 900) # Empêche de réduire la fenêtre trop petit pour voir les boutons
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

# -------------------- 📝 6. Zone d’affichage ----------------------------------------
# On définit l'affichage d'abord pour qu'il soit disponible pour les fonctions
ctk.CTkLabel(right_panel, text="LIVE STORY PREVIEW", font=("SF Pro Display", 22, "bold"), 
             text_color=ACCENT_COLOR).pack(pady=(25, 5))

# Label de statut pour l'IA
status_label = ctk.CTkLabel(right_panel, text="Choose a theme and fill the fields above", 
                            font=("SF Pro Text", 13, "italic"), text_color="#94a3b8")
status_label.pack(pady=(0, 10))

# Barre de progression (cachée par défaut)
progress_bar = ctk.CTkProgressBar(right_panel, width=400, height=12, corner_radius=10,
                                   progress_color=ACCENT_COLOR, fg_color=BG_ENTRY)
progress_bar.set(0)

# Zone de texte stylisée (Désormais EN HAUT)
text_container = ctk.CTkFrame(right_panel, fg_color="transparent")
text_container.pack(fill="x", expand=False, padx=25, pady=(10, 0))

text_output = tk.Text(text_container, wrap="word", font=("Georgia", 16), 
                      bg=BG_SIDE, fg=TEXT_COLOR, relief="flat", 
                      padx=40, pady=20, spacing1=12, height=8)
text_output.pack(side="left", fill="both", expand=True)

# Petite barre de défilement discrète pour le texte
text_scroll = ctk.CTkScrollbar(text_container, command=text_output.yview, width=12)
text_output.configure(yscrollcommand=text_scroll.set)
text_scroll.pack(side="right", fill="y")

# Configuration du style pour les mots mis en évidence (Highlight)
text_output.tag_configure("highlight", foreground=ACCENT_COLOR, font=("Georgia", 16, "bold"))

text_output.insert(tk.END, "Your story will appear here...")
text_output.config(state='disabled')

# 🖼️ Zone pour l'image (Désormais EN BAS)
image_container = ctk.CTkFrame(right_panel, fg_color="transparent")
image_container.pack(fill="both", expand=True, padx=25, pady=20)

story_image_label = ctk.CTkLabel(image_container, text="Illustration will appear here when you generate magic ✨", 
                                 font=("SF Pro Text", 12, "italic"),
                                 fg_color=BG_ENTRY, corner_radius=20)
story_image_label.pack(expand=True, fill="both")

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
create_btn("COPY TO CLIPBOARD 📋", COPY_COLOR, copy_to_clipboard)
create_btn("SAVE STORY 💾", SAVE_COLOR, save_story)
create_btn("CLEAR ALL 🧹", RESET_COLOR, reset_fields)

# -------------------- 🏁 7. Démarrage de l’application --------------------------------------------
# 🎬 C’est la boucle principale : elle lance l’interface et la garde ouverte jusqu’à ce que tu fermes la fenêtre.
root.mainloop()