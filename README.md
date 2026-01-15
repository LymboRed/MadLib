# 🎭 Mad Libs AI - Édition 2026

Une application moderne de Mad Libs alimentée par l'Intelligence Artificielle (**OpenAI DALL-E 3**). Créez des histoires délirantes et laissez l'IA générer des illustrations épiques en temps réel !

## ✨ Fonctionnalités
- **7 Thèmes Épiques** : Lion King, Space Adventure, Medieval, Cyberpunk, Pirates, Samurai, et Vikings.
- **IA Génératice** : Intégration de DALL-E 3 pour illustrer chaque histoire.
- **Multilingue** : Interface entièrement commutable entre **Français 🇫🇷** et **Anglais 🇬🇧**.
- **Galerie Intégrée** : Visualisez vos créations précédentes dans une interface élégante.
- **Design Moderne** : Interface "Glassmorphism" utilisant `customtkinter`.

---

## 🔑 Configuration de la Clé API

L'application nécessite une clé API OpenAI pour générer les images.

1. Créez un fichier nommé `.env` à la racine du projet.
2. Ajoutez-y votre clé comme ceci :
   ```env
   OPENAI_API_KEY=sk-votre_cle_ici
   ```
   *Note : Assurez-vous d'avoir des crédits actifs sur votre compte OpenAI.*

---

## 🛠️ Installation (Développement)

Si vous souhaitez lancer le script manuellement :

1. **Cloner le projet**
2. **Créer un environnement virtuel** :
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Installer les dépendances** :
   ```bash
   pip install customtkinter openai pillow python-dotenv requests
   ```
4. **Lancer l'application** :
   ```bash
   python3 madlibs_tk_project_1.py
   ```

---

## 📦 Compilation en Application (.app ou .exe)

Pour transformer ce script en véritable application autonome :

1. Installez PyInstaller :
   ```bash
   pip install pyinstaller
   ```
2. Lancez la compilation via le fichier de configuration fourni :
   ```bash
   python3 -m PyInstaller madlibs_tk_project_1.spec --noconfirm
   ```
3. L'application finale se trouvera dans le dossier **/dist**.

---

## 📁 Structure du Projet
- `madlibs_tk_project_1.py` : Script principal.
- `madlibs_tk_project_1.spec` : Configuration pour la compilation.
- `images/` : Stockage des illustrations générées par l'IA.
- `.env` : Votre clé API secrète (exclu du Git).
- `.gitignore` : Protège vos fichiers sensibles.

---
*Développé sur VSCode avec GH Copilot - Janvier 2026*
