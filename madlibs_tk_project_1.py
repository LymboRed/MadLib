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

# -------------------- 🏗️ 2. FONCTIONS ET DONNÉES ------------------------------------------------
# 🔑 CONFIGURATION API
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
client = None
if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-votre"):
    client = OpenAI(api_key=OPENAI_API_KEY)

# 🌍 SYSTÈME DE TRADUCTION
CURRENT_LANG = "FR"

TRANSLATIONS = {
    "FR": {
        "title": "Mad Libs AI - Édition 2026",
        "select_theme": "CHOIX DU THÈME",
        "story_inputs": "VOS MOTS MAGIQUES",
        "preview": "APERÇU DE L'HISTOIRE",
        "generate": "GÉNÉRER LA MAGIE ✨",
        "copy": "COPIER L'HISTOIRE 📋",
        "save": "SAUVEGARDER 💾",
        "clear": "EFFACER 🧹",
        "history": "GALERIE 🖼️",
        "status_start": "Choisissez un thème et remplissez les champs ci-dessus",
        "status_generating": "🎨 L'IA dessine votre histoire... (Attendez ~15s)",
        "status_complete": "✅ Génération magique terminée !",
        "placeholder": "Votre histoire apparaîtra ici...",
        "img_placeholder": "L'illustration apparaîtra ici ✨",
        "warning_fields": "Merci de remplir tous les champs !",
        "warning_save": "Génère d'abord une histoire !",
        "save_success": "Histoire sauvegardée dans 'mon_histoire.txt' ! ✅",
        "copy_success": "Copié dans le presse-papier ! 📋",
        "safety_error": "⚠️ Sécurité IA : Le prompt a été rejeté. Essayez des mots plus doux."
    },
    "EN": {
        "title": "Mad Libs AI - 2026 Edition",
        "select_theme": "SELECT THEME",
        "story_inputs": "STORY INPUTS",
        "preview": "LIVE STORY PREVIEW",
        "generate": "GENERATE MAGIC ✨",
        "copy": "COPY STORY 📋",
        "save": "SAVE STORY 💾",
        "clear": "CLEAR ALL 🧹",
        "history": "GALLERY 🖼️",
        "status_start": "Choose a theme and fill the fields above",
        "status_generating": "🎨 AI is drawing your story... (Wait ~15s)",
        "status_complete": "✅ Magic generation complete!",
        "placeholder": "Your story will appear here...",
        "img_placeholder": "Illustration will appear here ✨",
        "warning_fields": "Please fill all fields!",
        "warning_save": "Generate a story first!",
        "save_success": "Story saved to 'mon_histoire.txt'! ✅",
        "copy_success": "Copied to clipboard! 📋",
        "safety_error": "⚠️ AI Safety: Prompt rejected. Try milder words."
    }
}

THEMES_DATA = {
    "Lion King 🦁": {
        "FR": {
            "fields": ["Nom de l'animal", "Métier", "Nom du père", "Royaume", "Nom du méchant", "Lieu d'exil", "Ami 1", "Ami 2", "Phrase marrante", "Arme", "Titre Royal"],
            "template": (
                "Au cœur de la savane africaine, un jeune lion nommé {0} était destiné à devenir {1}. "
                "Un jour, son père le Roi {2} lui dit : \"Tout ce que {3} touche est notre royaume.\" "
                "Mais après un tragique accident causé par {4}, il s'enfuit vers {5}. "
                "Là, il rencontra deux amis insolites : {6} et {7}, qui lui apprirent à dire {8} ! "
                "Des années plus tard, il revint affronter son passé avec {9} et reprit sa place de {10}."
            )
        },
        "EN": {
            "fields": ["Animal Name", "Job", "Father's Name", "Kingdom", "Villain Name", "Exile Place", "Friend 1", "Friend 2", "Funny Phrase", "Weapon", "Title"],
            "template": (
                "In the heart of the African savannah, a young lion named {0} was destined to become a {1}. "
                "One day, his father, King {2}, told him: \"Everything the {3} touches is our kingdom.\" "
                "But after a tragic accident caused by {4}, he ran away to {5}. "
                "There, he met two unusual friends: {6} and {7}, who taught him to say {8}! "
                "Years later, he returned to face his past, battle {4} with a {9}, and reclaim his place as the rightful {10}."
            )
        },
        "visual_template": "A majestic lion standing on a grand natural rock overlooking a vast African savannah ecosystem. Royal atmosphere, golden hour sun, cinematic high-quality digital animation style."
    },
    "Space Adventure 🚀": {
        "FR": {
            "fields": ["Nom du pilote", "Planète cible", "Nom de la mission", "Espèce alien", "Nom du vaisseau", "Arme", "Nourriture spatiale", "Nom du droïde", "Cri du droïde", "Système solaire", "Rang militaire"],
            "template": (
                "Dans le système {9}, le pilote {0} était en mission pour {2}. "
                "Après avoir atterri sur {1}, il a croisé un vaisseau {3} nommé {4}. "
                "Soudain, des ennemis ont attaqué ! {0} a saisi son {5}. "
                "Son fidèle droïde {7} criait '{8}' en jetant des {6} sur les robots. "
                "À la fin, la paix fut restaurée et {0} fut nommé {10}."
            )
        },
        "EN": {
            "fields": ["Pilot Name", "Target Planet", "Mission Name", "Alien Species", "Ship Name", "Weapon", "Space Food", "Droid Name", "Droid Catchphrase", "Star System", "Honorary Rank"],
            "template": (
                "Deep in the {9}, the brave pilot {0} was on the '{2}' mission. "
                "After landing on {1}, they encountered a friendly {3} ship named the {4}. "
                "Suddenly, a swarm of enemies attacked! {0} grabbed a {5} and fought back. "
                "Their loyal droid {7} shouted '{8}!' while throwing {6} at the enemies. "
                "In the end, peace was restored, and {0} was granted the rank of {10}."
            )
        },
        "visual_template": "A high-tech futuristic explorer ship flying through a glowing colorful galactic nebula. Stars and planets in the background, epic space opera style, digital painting."
    },
    "Medieval Tale ⚔️": {
        "FR": {
            "fields": ["Nom du héros", "Nom du royaume", "Quête", "Monstre mythique", "Objet magique", "Personne royale", "Village", "Pire ennemi", "Vieux Mage", "Relique ancienne", "Titre final"],
            "template": (
                "Dans le royaume de {1}, un héros nommé {0} partit pour {2}. "
                "Armé d'un {4}, il dut affronter le terrible {3} envoyé par {7}. "
                "En chemin, il croisa {8} qui lui donna une {9}. "
                "Après avoir sauvé {5} au village de {6}, il rentra en gloire. "
                "Désormais, on l'appelle {10}."
            )
        },
        "EN": {
            "fields": ["Hero Name", "Kingdom", "Quest", "Mythical Beast", "Magical Item", "Royal Person", "Village", "Worst Enemy", "Old Wizard", "Ancient Relic", "Ending Title"],
            "template": (
                "In the glorious kingdom of {1}, a humble hero named {0} set out on a quest to {2}. "
                "Armed only with a {4}, they had to face the terrifying {3} sent by {7}. "
                "Along the way, they met {8}, who gave them a mysterious {9}. "
                "After a long journey through the village of {6}, they saved {5} and returned home. "
                "For their bravery, the citizens of the Realm now call them the {10}."
            )
        },
        "visual_template": "An epic fantasy hero standing before a magnificent castle with banners flying. Mythical landscapes, legendary quest atmosphere, oil painting art style."
    },
    "Cyberpunk Neon ⚡️": {
        "FR": {
            "fields": ["Alias Netrunner", "Quartier", "Corporation", "Augmentation", "Nom du Hack", "Nom du Fixer", "Contact", "Véhicule", "Base secrète", "Puce neuronale", "Rang de réputation"],
            "template": (
                "Dans les rues néons de {1}, le netrunner {0} préparait un casse contre {2}. "
                "Avec son {3} installé, il activa le virus '{4}'. "
                "Son fixer {5} lui dit : 'Retrouve {6} à la base {8}.' "
                "Il sauta sur sa {7} et fonça. "
                "Après avoir volé la puce {9}, il est devenu {10} de la ville."
            )
        },
        "EN": {
            "fields": ["Netrunner Alias", "Megacity District", "Corporate Name", "Augmentation", "Hack Name", "Fixer Name", "Contact Person", "Vehicle", "Hidden Base", "Neural Chip", "Street Cred Rank"],
            "template": (
                "In the neon-drenched streets of {1}, the legendary netrunner {0} was planning a heist against {2}. "
                "Equipped with a deadly {3}, they prepared the '{4}' exploit. "
                "Their fixer, {5}, sent a message: 'Meet {6} at the {8} immediately.' "
                "They hopped on their {7} and sped through the city. "
                "After a high-speed chase, they successfully stole the {9}. "
                "Word spread across the Net, and {0} was finally recognized as a {10}."
            )
        },
        "visual_template": "A futuristic city at night with massive neon billboards in pink and blue. Rain reflecting on asphalt, aesthetic synthwave atmosphere, hyper-detailed digital art."
    },
    "Pirate Legends 🏴‍☠️": {
        "FR": {
            "fields": ["Nom du Capitaine", "Navire", "Île secrète", "Monstre marin", "Type de trésor", "Amiral ennemi", "Membre d'équipage", "Boisson favorite", "Cri de guerre", "Second", "Titre légendaire"],
            "template": (
                "Le Capitaine {0} voguait sur le '{1}' à la recherche de {4}. "
                "Près de {2}, ils furent attaqués par {3} ! "
                "'{8} !' cria {9} en chargeant les canons. "
                "Après le combat, ils burent du {7} avec {6}. "
                "Malgré l'Amiral {5} à leurs trousses, {0} s'échappa et devint {10}."
            )
        },
        "EN": {
            "fields": ["Captain Name", "Pirate Ship", "Hidden Island", "Sea Monster", "Treasure Type", "Enemy Admiral", "Crew Member", "Signature Drink", "Battle Cry", "First Mate", "Legendary Title"],
            "template": (
                "The fearsome Captain {0} set sail on the '{1}' in search of {4}. "
                "While navigating near {2}, they were suddenly attacked by a giant {3}! "
                "'{8}!' shouted {9} as they loaded the cannons. "
                "After defeating the beast, they shared a round of {7} with {6}. "
                "However, Admiral {5} was hot on their trail. "
                "The battle was fierce, but {0} escaped and became known as the {10} of the Seven Seas."
            )
        },
        "visual_template": "An old wooden pirate ship with white sails on a turquoise ocean. Tropical island with palm trees in the background, adventure art style, golden hour lighting."
    },
    "Samurai Path 🏮": {
        "FR": {
            "fields": ["Nom du Samouraï", "Seigneur féodal", "Nom du Clan", "Katana légendaire", "Village", "Rival", "Thé favori", "Dicton Zen", "Lieu du duel", "Technique spéciale", "Titre d'honneur"],
            "template": (
                "À l'ère du clan {2}, le samouraï {0} servait le Seigneur {1}. "
                "Avec son sabre '{3}', il protégeait le village de {4}. "
                "Un jour, {5} le défia en duel à {8}. "
                "Avant le combat, {0} but un {6} et dit : '{7}'. "
                "D'un coup de '{9}', il gagna. Désormais, il est appelé {10}."
            )
        },
        "EN": {
            "fields": ["Samurai Name", "Feudal Lord", "Clan Name", "Legendary Katana", "Village Name", "Arch Rival", "Favorite Tea", "Zen Saying", "Battle Location", "Special Technique", "Honor Title"],
            "template": (
                "In the era of the {2} clan, the wandering samurai {0} served Lord {1}. "
                "Armed with the '{3}', they protected the peaceful village of {4}. "
                "One day, their arch rival {5} challenged them to a duel at {8}. "
                "Before the fight, {0} sat calmly drinking {6} and whispered: '{7}'. "
                "With a swift '{9}' move, the battle was won. "
                "From that day on, {0} was honored with the title of {10}."
            )
        },
        "visual_template": "A lone samurai in traditional armor standing in a field of cherry blossoms (sakura). Ancient Japanese architecture in the mist, Zen atmosphere, artistic digital illustration."
    },
    "Viking Saga 🪓": {
        "FR": {
            "fields": ["Chef Viking", "Drakkar", "Royaume cible", "Dieu Nordique", "Arme", "Grande Salle", "Jarl Rival", "Bête de guerre", "Cri de rage", "Plat de fête", "Titre de la Saga"],
            "template": (
                "Venu du Nord, {0} menait le drakkar '{1}' vers {2}. "
                "Invoquant {3}, ils saisirent leur {4}. "
                "Le Jarl {6} les attendait avec un {7}. "
                "'{8} !' rugirent les Vikings. Après la victoire, ils fêtèrent au {5} avec du {9}. "
                "Voici la saga de {0}, le {10}."
            )
        },
        "EN": {
            "fields": ["Viking Leader", "Longship Name", "Target Kingdom", "Norse God", "Weapon", "Great Hall", "Rival Jarl", "Beast", "War Cry", "Feast Food", "Saga Title"],
            "template": (
                "From the frozen North, {0} led the crew of the '{1}' towards the shores of {2}. "
                "They prayed to {3} for strength and gripped their mighty {4}. "
                "In the distance, Jarl {6} was waiting with a massive army and a trained {7}. "
                "'{8}!' roared the Vikings as they charged. "
                "Victory was theirs, and they celebrated in the {5} with plenty of {9}. "
                "The skalds would forever sing the saga of {0}, the {10}."
            )
        },
        "visual_template": "A majestic viking longship on a dark sea under a green aurora borealis. Snowy mountains and fjords, epic Norse mythology aesthetic, cinematic digital art."
    }
}

# Mapping des couleurs par thème
THEME_COLORS = {
    "Lion King 🦁": "#fbbf24",
    "Space Adventure 🚀": "#818cf8",
    "Medieval Tale ⚔️": "#f87171",
    "Cyberpunk Neon ⚡️": "#f472b6",
    "Pirate Legends 🏴‍☠️": "#fb923c",
    "Samurai Path 🏮": "#4ade80",
    "Viking Saga 🪓": "#60a5fa",
}

# Mapping des images locales (Fallback)
THEME_IMAGES = {
    "Lion King 🦁": "images/lion.png",
    "Space Adventure 🚀": "images/space.png",
    "Medieval Tale ⚔️": "images/medieval.png",
    "Cyberpunk Neon ⚡️": "images/cyberpunk.png",
    "Pirate Legends 🏴‍☠️": "images/pirate.png",
    "Samurai Path 🏮": "images/samurai.png",
    "Viking Saga 🪓": "images/viking.png",
}


# 🖼️ Système de Galerie Photo intégrée
def show_gallery():
    gallery_window = ctk.CTkToplevel(root)
    gallery_window.title("Galerie MadLibs AI 🖼️")
    gallery_window.geometry("900x700")
    gallery_window.configure(fg_color=BG_MAIN)
    gallery_window.after(100, lambda: gallery_window.focus()) # Fix focus on macOS

    title = ctk.CTkLabel(gallery_window, text="VOS GÉNÉRATIONS PRÉCÉDENTES", font=("SF Pro Display", 24, "bold"), text_color=ACCENT_COLOR)
    title.pack(pady=20)

    # Scrollable area for images
    scroll_canvas = ctk.CTkScrollableFrame(gallery_window, fg_color="transparent", width=850, height=550)
    scroll_canvas.pack(padx=20, pady=20, fill="both", expand=True)

    if not os.path.exists("images"):
        ctk.CTkLabel(scroll_canvas, text="Aucune image encore générée...").pack()
        return

    # List files in images/ folder
    all_images = [f for f in os.listdir("images") if f.endswith(('.png', '.jpg', '.jpeg'))]
    all_images.sort(reverse=True) # Show newest first

    if not all_images:
        ctk.CTkLabel(scroll_canvas, text="Votre galerie est vide pour le moment 🎨").pack()
        return

    cols = 3
    for i, img_name in enumerate(all_images):
        img_path = os.path.join("images", img_name)
        try:
            pil_img = Image.open(img_path)
            # Create thumbnail
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(250, 250))
            
            frame = ctk.CTkFrame(scroll_canvas, fg_color=BG_CARD, corner_radius=15)
            frame.grid(row=i//cols, column=i%cols, padx=10, pady=10)
            
            lbl = ctk.CTkLabel(frame, image=ctk_img, text="")
            lbl.pack(padx=5, pady=5)
            
            date_str = datetime.datetime.fromtimestamp(os.path.getctime(img_path)).strftime("%d/%m/%Y %H:%M")
            ctk.CTkLabel(frame, text=date_str, font=("SF Pro Text", 10), text_color="#94a3b8").pack()
        except:
            continue

# 🌍 Changement de langue
def switch_language():
    global CURRENT_LANG
    CURRENT_LANG = "EN" if CURRENT_LANG == "FR" else "FR"
    lang_btn.configure(text=f"🌐 {CURRENT_LANG}")
    refresh_ui_text()
    # Refresh themes if one is selected
    choice = theme_selector.get()
    if choice in THEMES_DATA:
        change_theme(choice)

def refresh_ui_text():
    t = TRANSLATIONS[CURRENT_LANG]
    title_label.configure(text=t["title"])
    theme_label.configure(text=t["select_theme"])
    input_title.configure(text=t["story_inputs"])
    preview_title.configure(text=t["preview"])
    gen_btn.configure(text=t["generate"])
    copy_btn.configure(text=t["copy"])
    save_btn.configure(text=t["save"])
    clear_btn.configure(text=t["clear"])
    gallery_btn.configure(text=t["history"])
    
    # Placeholder texts
    if not text_output.get("1.0", tk.END).strip() or "histoire" in text_output.get("1.0", tk.END).lower() or "story" in text_output.get("1.0", tk.END).lower():
        text_output.config(state='normal')
        text_output.delete("1.0", tk.END)
        text_output.insert("1.0", t["placeholder"])
        text_output.config(state='disabled')
    
    if not story_image_label.cget("image"):
        story_image_label.configure(text=t["img_placeholder"])

# Fonction pour mettre à jour l'image de l'histoire (Haut: Texte, Bas: Image)
def update_story_image(theme=None, pil_img=None):
    t = TRANSLATIONS[CURRENT_LANG]
    if not theme and not pil_img:
        story_image_label.configure(image=None, text=t["img_placeholder"])
        return
    
    if pil_img:
        try:
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(600, 600))
            story_image_label.configure(image=ctk_img, text="")
            return
        except Exception as e:
            print(f"Error displaying AI image: {e}")

    img_path = THEME_IMAGES.get(theme)
    if img_path and os.path.exists(img_path):
        try:
            pil_img = Image.open(img_path)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(600, 400))
            story_image_label.configure(image=ctk_img, text="")
        except Exception as e:
            story_image_label.configure(image=None, text=f"Error loading {theme} image ❌")
    else:
        story_image_label.configure(image=None, text=f"🎨 Visualization: {theme}")

# 🤖 Fonction pour appeler l'IA OpenAI dans un thread séparé
def fetch_ai_image(prompt, callback):
    print(f"DEBUG: Starting AI Generation for prompt: {prompt[:100]}...")
    try:
        if not client:
            print("DEBUG: Client OpenAI not initialized")
            root.after(0, lambda: callback(None))
            return

        response = client.images.generate(
            model="dall-e-3",
            prompt=f"{prompt} High resolution, artistic style, masterpiece, without any text or labels.",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        img_data = requests.get(image_url).content
        pil_img = Image.open(BytesIO(img_data))
        
        if not os.path.exists("images"):
            os.makedirs("images")
            
        filename = f"images/generated_{int(datetime.datetime.now().timestamp())}.png"
        pil_img.save(filename)
        root.after(0, lambda: callback(pil_img))
    except Exception as e:
        print(f"DEBUG: AI Error: {e}")
        if "policy" in str(e).lower() or "safety" in str(e).lower():
            root.after(0, lambda: status_label.configure(text=TRANSLATIONS[CURRENT_LANG]["safety_error"], text_color="red"))
        root.after(0, lambda: callback(None))

# Fonction pour changer de thème
def change_theme(choice):
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    entries.clear()
    
    new_color = THEME_COLORS.get(choice, ACCENT_COLOR)
    theme_selector.configure(button_color=new_color)
    progress_bar.configure(progress_color=new_color)
    
    update_story_image(None)
    progress_bar.pack_forget()
    status_label.configure(text=f"Thème {choice} - Ready!", text_color="#94a3b8")
    
    # Utilisation des nouveaux champs multilingues
    theme_data = THEMES_DATA[choice][CURRENT_LANG]
    for field in theme_data["fields"]:
        ctk.CTkLabel(scroll_frame, text=field.upper(), font=("SF Pro Text", 10, "bold"),
                     text_color=TEXT_COLOR).pack(anchor="w", padx=15, pady=(12, 2))
        entry = ctk.CTkEntry(scroll_frame, placeholder_text=f"...",
                             fg_color=BG_ENTRY, border_color="#475569", 
                             height=45, corner_radius=12)
        entry.pack(fill="x", padx=10, pady=(0, 5))
        entries.append(entry)

# 💾 Sauvegarder l’histoire
def save_story():
    t = TRANSLATIONS[CURRENT_LANG]
    story = text_output.get("1.0", tk.END).strip()
    if not story or story == t["placeholder"]:
        messagebox.showwarning("Save", t["warning_save"])
        return
    
    try:
        with open("mon_histoire.txt", "w", encoding="utf-8") as file:
            file.write(story)
        messagebox.showinfo("Success", t["save_success"])
    except Exception as e:
        messagebox.showerror("Error", f"Impossible : {e}")

# 📋 Copier dans le presse-papier
def copy_to_clipboard():
    t = TRANSLATIONS[CURRENT_LANG]
    story = text_output.get("1.0", tk.END).strip()
    if not story or story == t["placeholder"]:
        messagebox.showwarning("Copy", t["warning_save"])
        return
    root.clipboard_clear()
    root.clipboard_append(story)
    messagebox.showinfo("Copy", t["copy_success"])

# 🎬 Générer l’histoire avec animation Typewriter et Highlighting
def generate_story():
    t = TRANSLATIONS[CURRENT_LANG]
    values = [entry.get() for entry in entries]
    if not all(values):
        messagebox.showwarning("Fields", t["warning_fields"])
        return
    
    current_theme = theme_selector.get()
    status_label.configure(text=t["status_generating"], text_color=ACCENT_COLOR)
    progress_bar.set(0)
    progress_bar.pack(fill="x", padx=100, pady=(10, 20))
    
    theme_entry = THEMES_DATA[current_theme]
    template = theme_entry[CURRENT_LANG]["template"]
    visual_template = theme_entry.get("visual_template", "A cinematic scene")
    visual_text = visual_template # Dans cette version, on utilise le template visuel artistique brut pour éviter les blocks
    
    def complete_generation(pil_img=None):
        update_story_image(current_theme, pil_img)
        progress_bar.pack_forget()
        
        current_color = THEME_COLORS.get(current_theme, ACCENT_COLOR)
        text_output.tag_configure("highlight", foreground=current_color, font=("Georgia", 16, "bold"))
        status_label.configure(text=t["status_complete"], text_color=GENERATE_COLOR)
        
        parts = re.split(r'(\{.*?\})', template)
        full_sequence = []
        
        for part in parts:
            if part.startswith("{") and part.endswith("}"):
                try:
                    idx = int(part[1:-1])
                    if 0 <= idx < len(values):
                        full_sequence.append((values[idx], True))
                except: pass
            elif part:
                full_sequence.append((part, False))
                
        text_output.config(state='normal')
        text_output.delete("1.0", tk.END)
        
        def type_writer(seq_idx, char_idx):
            if seq_idx >= len(full_sequence):
                text_output.config(state='disabled')
                return
            content, is_val = full_sequence[seq_idx]
            if char_idx < len(content):
                text_output.insert(tk.END, content[char_idx])
                if is_val:
                    end_pos = text_output.index("end-1c")
                    start_pos = f"{end_pos.split('.')[0]}.{int(end_pos.split('.')[1])-1}"
                    text_output.tag_add("highlight", start_pos, end_pos)
                root.after(10, type_writer, seq_idx, char_idx + 1)
            else:
                type_writer(seq_idx + 1, 0)
        type_writer(0, 0)

    def start_ai_thread():
        if client:
            thread = threading.Thread(target=fetch_ai_image, args=(visual_text, complete_generation))
            thread.daemon = True
            thread.start()
        else:
            simulate_progress(0)

    def simulate_progress(val):
        if val <= 1.0:
            progress_bar.set(val)
            root.after(30, simulate_progress, val + 0.05)
        else:
            complete_generation()
            
    start_ai_thread()

def reset_fields():
    t = TRANSLATIONS[CURRENT_LANG]
    for entry in entries:
        entry.delete(0, tk.END)
    text_output.config(state='normal')
    text_output.delete("1.0", tk.END)
    text_output.insert("1.0", t["placeholder"])
    text_output.config(state='disabled')
    update_story_image(None)
    progress_bar.pack_forget()
    status_label.configure(text=t["status_start"], text_color="#94a3b8")


# -------------------- 🖼️ 3. INTERFACE GRAPHIQUE --------------------------------------------------
# Palette de couleurs Glassmorphism
BG_MAIN = "#0f172a"
BG_SIDE = "#1e293b"
BG_ENTRY = "#334155"
BG_CARD = "#1e293b"
ACCENT_COLOR = "#38bdf8"
TEXT_COLOR = "#f8fafc"

# Couleurs des boutons
GENERATE_COLOR = "#059669"
COPY_COLOR = "#6366f1"
SAVE_COLOR = "#d97706"
RESET_COLOR = "#dc2626"

# Fenêtre principale
root = ctk.CTk()
root.title("Mad Libs AI 2026")
root.geometry("1100x950")
root.minsize(1100, 900)
root.configure(fg_color=BG_MAIN)

# Main Containers with padding
main_container = ctk.CTkFrame(root, fg_color=BG_MAIN)
main_container.pack(fill="both", expand=True, padx=30, pady=30)

left_panel = ctk.CTkFrame(main_container, fg_color=BG_SIDE, corner_radius=25)
left_panel.pack(side="left", fill="both", expand=False, padx=(0, 20))

right_panel = ctk.CTkFrame(main_container, fg_color=BG_SIDE, corner_radius=25)
right_panel.pack(side="right", fill="both", expand=True)

# -------------------- 🔝 1. Barre de Titre & Langue ----------------------------------------
header_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
header_frame.pack(fill="x", padx=25, pady=(25, 5))

title_label = ctk.CTkLabel(header_frame, text="Mad Libs AI - Édition 2026", font=("SF Pro Display", 28, "bold"), text_color=ACCENT_COLOR)
title_label.pack(side="left")

lang_btn = ctk.CTkButton(header_frame, text=f"🌐 {CURRENT_LANG}", width=60, height=35, corner_radius=10, 
                         fg_color=BG_ENTRY, command=switch_language)
lang_btn.pack(side="right", padx=5)

gallery_btn = ctk.CTkButton(header_frame, text="GALERIE 🖼️", width=120, height=35, corner_radius=10, 
                            fg_color=COPY_COLOR, command=show_gallery)
gallery_btn.pack(side="right", padx=5)

# -------------------- 📝 2. Zone de Statut et Texte ----------------------------------------
status_label = ctk.CTkLabel(right_panel, text="Choisissez un thème et remplissez les champs ci-dessus", 
                            font=("SF Pro Text", 13, "italic"), text_color="#94a3b8")
status_label.pack(pady=(0, 10))

progress_bar = ctk.CTkProgressBar(right_panel, width=400, height=12, corner_radius=10,
                                   progress_color=ACCENT_COLOR, fg_color=BG_ENTRY)
progress_bar.set(0)

preview_title = ctk.CTkLabel(right_panel, text="APERÇU DE L'HISTOIRE", font=("SF Pro Display", 22, "bold"), text_color=ACCENT_COLOR)
preview_title.pack(pady=(10, 5))

text_container = ctk.CTkFrame(right_panel, fg_color="transparent")
text_container.pack(fill="x", expand=False, padx=25, pady=(5, 0))

text_output = tk.Text(text_container, wrap="word", font=("Georgia", 16), 
                      bg=BG_SIDE, fg=TEXT_COLOR, relief="flat", 
                      padx=40, pady=20, spacing1=12, height=6)
text_output.pack(side="left", fill="both", expand=True)

text_scroll = ctk.CTkScrollbar(text_container, command=text_output.yview, width=12)
text_output.configure(yscrollcommand=text_scroll.set)
text_scroll.pack(side="right", fill="y")
text_output.tag_configure("highlight", foreground=ACCENT_COLOR, font=("Georgia", 16, "bold"))

# 🖼️ Zone pour l'image
image_container = ctk.CTkFrame(right_panel, fg_color="transparent")
image_container.pack(fill="both", expand=True, padx=25, pady=20)

story_image_label = ctk.CTkLabel(image_container, text="L'illustration apparaîtra ici ✨", 
                                 font=("SF Pro Text", 12, "italic"),
                                 fg_color=BG_ENTRY, corner_radius=20)
story_image_label.pack(expand=True, fill="both")

# -------------------- ✏️ 3. PANNEAU GAUCHE (CHAMPS) ----------------------------------------
theme_label = ctk.CTkLabel(left_panel, text="CHOIX DU THÈME", font=("SF Pro Display", 16, "bold"), text_color=ACCENT_COLOR)
theme_label.pack(pady=(20, 5))

theme_selector = ctk.CTkOptionMenu(left_panel, values=list(THEMES_DATA.keys()), 
                                  command=change_theme, fg_color=BG_ENTRY, 
                                  button_color=ACCENT_COLOR, button_hover_color=GENERATE_COLOR,
                                  corner_radius=10)
theme_selector.pack(fill="x", padx=20, pady=(0, 20))

input_title = ctk.CTkLabel(left_panel, text="VOS MOTS MAGIQUES", font=("SF Pro Display", 18, "bold"), text_color=ACCENT_COLOR)
input_title.pack(pady=(10, 5))

scroll_frame = ctk.CTkScrollableFrame(left_panel, fg_color="transparent", width=320)
scroll_frame.pack(fill="both", expand=True, padx=15, pady=10)

entries = []

# -------------------- 🔘 4. BOUTONS ACTION ------------------------------------------------
btn_container = ctk.CTkFrame(left_panel, fg_color="transparent")
btn_container.pack(fill="x", padx=20, pady=25)

gen_btn = ctk.CTkButton(btn_container, text="GÉNÉRER LA MAGIE ✨", command=generate_story, 
                        fg_color=GENERATE_COLOR, hover_color="#047857", font=("SF Pro Text", 13, "bold"),
                        height=55, corner_radius=18)
gen_btn.pack(fill="x", pady=6)

copy_btn = ctk.CTkButton(btn_container, text="COPIER L'HISTOIRE 📋", command=copy_to_clipboard, 
                         fg_color=COPY_COLOR, font=("SF Pro Text", 12, "bold"), height=45, corner_radius=15)
copy_btn.pack(fill="x", pady=4)

save_btn = ctk.CTkButton(btn_container, text="SAUVEGARDER 💾", command=save_story, 
                         fg_color=SAVE_COLOR, font=("SF Pro Text", 12, "bold"), height=45, corner_radius=15)
save_btn.pack(fill="x", pady=4)

clear_btn = ctk.CTkButton(btn_container, text="EFFACER 🧹", command=reset_fields, 
                          fg_color=RESET_COLOR, font=("SF Pro Text", 12, "bold"), height=45, corner_radius=15)
clear_btn.pack(fill="x", pady=4)

# Initialisation
change_theme(list(THEMES_DATA.keys())[0])
refresh_ui_text()

root.mainloop()
