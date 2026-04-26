"""
gemini_gameplay.py
Analyse les vidéos gameplay avec Gemini et génère gameplay_spec.md —
un document exhaustif qui sert de seul prompt pour Claude Code.
Usage: python gemini_gameplay.py
"""

import os
import pathlib
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
Tu es un expert en analyse de gameplay mobile. Tu vas analyser une vidéo de gameplay et produire un document Markdown structuré, destiné à être utilisé directement comme brief technique par un développeur HTML5 Canvas.

Règles strictes :
- Ne décris JAMAIS les personnages visuellement (sprites, couleurs, taille) — ils sont déjà disponibles en PNG
- Ne décris JAMAIS les assets visuels (châteaux, projectiles, fonds) — idem
- Concentre-toi UNIQUEMENT sur la logique de jeu, les mécaniques, les positions, les timings, les états
- Sois précis et chiffré quand c'est possible (fractions d'écran, durées en ms, nombre de coups)
- Si tu n'es pas sûr d'une valeur, indique [ESTIMÉ] et donne quand même une valeur
- Output : Markdown pur, pas d'intro, pas de conclusion, pas de commentaire
"""

USER_PROMPT = """
Analyse cette vidéo de gameplay de Castle Clasher et génère un document Markdown avec exactement ces sections :

---

## 1. FORMAT ET ORIENTATION
- Orientation (portrait/landscape)
- Ratio observé
- Résolution logique recommandée pour Canvas HTML5

## 2. LAYOUT ÉCRAN
- Position et contenu de chaque zone UI (HP bars, VS, sélecteur de persos, tutoriel)
- Dimensions en fraction d'écran ET en pixels (pour canvas recommandé)
- Style visuel de chaque élément UI (couleurs, taille texte, icônes)

## 3. CHÂTEAUX
- Position gauche/droite en fraction d'écran
- Largeur et hauteur en fraction d'écran
- Ce qu'il y a SOUS les châteaux (roues, base, etc.)
- Ce qu'il y a À L'INTÉRIEUR des châteaux (plateformes, personnages, canons)
- Nombre d'états de dégâts observés et leur déclencheur (% HP ou nombre de coups)
- Description de chaque état : qu'est-ce qui change visuellement (trous, noircissement, effondrement partiel)

## 4. MÉCANIQUES DE TIR

### Sélection du personnage
- Comment le joueur sélectionne un personnage (tap sur carte, tap sur perso dans château, etc.)
- Position des cartes de sélection
- Comportement de la carte après utilisation (grisée, croix, disparition)

### Visée et lancement
- Type de mécanique (drag depuis perso, drag depuis slingshot fixe, etc.)
- Point d'ancrage exact du slingshot (position sur le château joueur, en fraction)
- Direction du drag (vers quelle direction le joueur tire)
- Distance max de drag observée (fraction d'écran)
- Comportement des élastiques visuels
- Arc preview : visible ou non, nombre de points, couleur, mise à jour temps réel

### Projectile en vol
- Trajectoire (parabolique, droite, etc.)
- Vitesse ressentie (lente/moyenne/rapide)
- Symétrie montée/descente
- Hauteur de pic estimée (fraction d'écran)
- Rotation du projectile en vol (oui/non, vitesse)

## 5. TYPES D'ATTAQUES PAR PERSONNAGE
Pour chaque personnage jouable observé :
- Nom/identifiant
- Nombre de projectiles tirés simultanément
- Pattern de tir (droit, éventail, explosif, etc.)
- Délai entre tirs si plusieurs projectiles
- Trail visuel (couleur, densité)
- Effet à l'impact (explosion, rayon estimé, débris)
- Dégâts estimés (si visible dans la vidéo)

## 6. TOUR PAR TOUR
- Qui commence
- Ce qui déclenche la fin du tour joueur
- Délai avant le tour ennemi (en ms [ESTIMÉ])
- Animation de charge de l'ennemi avant de tirer
- Nombre de tirs ennemis par tour
- Ce qui déclenche la fin du tour ennemi

## 7. CONDITIONS DE VICTOIRE / DÉFAITE
- Condition exacte de victoire
- Condition exacte de défaite
- Ce qui se passe visuellement à la victoire (overlay, texte, bouton)
- Ce qui se passe visuellement à la défaite (overlay, texte, bouton)

## 8. FLOW DE NIVEAUX
- Nombre de niveaux observés
- Différences entre les niveaux (HP ennemi, vitesse, comportement IA)
- Transition entre les niveaux (durée, texte affiché)

## 9. JUICE ET FEEDBACK
Liste uniquement les effets observés avec :
- Nom de l'effet
- Déclencheur exact
- Durée estimée en ms
- Intensité (faible/moyenne/forte)
- Priorité MVP (essentiel / nice-to-have)

## 10. CONVERSION FLOW
- Après combien de tirs sans victoire le jeu redirige (si observable)
- Quel événement déclenche la redirection en niveau 2
- Y a-t-il un CTA visible pendant le jeu

---

Ne rajoute rien en dehors de ces sections. Sois factuel, chiffré, et orienté implémentation.
"""


def upload_videos(folder: str) -> dict:
    uploaded = {}
    for f in pathlib.Path(folder).iterdir():
        if f.suffix in (".mp4", ".mov", ".avi"):
            print(f"Upload : {f.name}")
            file = client.files.upload(file=str(f))
            uploaded[f.name] = file
    return uploaded


def wait_ready(files: dict, timeout: int = 120) -> dict:
    for name, f in list(files.items()):
        elapsed = 0
        while f.state.name == "PROCESSING":
            if elapsed >= timeout:
                print(f"{name} -> timeout, skip")
                files[name] = None
                break
            time.sleep(3)
            elapsed += 3
            files[name] = client.files.get(name=f.name)
            f = files[name]
        if files[name] and files[name].state.name == "ACTIVE":
            print(f"{name} -> prêt")
        else:
            state = files[name].state.name if files[name] else "timeout"
            print(f"{name} -> état : {state}")
    return {k: v for k, v in files.items() if v is not None}


def analyze_video(video_file) -> str:
    video_part = types.Part(
        file_data=types.FileData(
            file_uri=video_file.uri,
            mime_type=video_file.mime_type,
        ),
        video_metadata=types.VideoMetadata(fps=2),
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[video_part, USER_PROMPT],
        config=types.GenerateContentConfig(
            temperature=0,
            system_instruction=SYSTEM_PROMPT,
        ),
    )
    return response.text


if __name__ == "__main__":
    videos = upload_videos("./videos")
    videos = wait_ready(videos)

    if not videos:
        print("Aucune vidéo prête, arrêt.")
        exit(1)

    full_spec = ""
    for name, file in videos.items():
        print(f"Analyse : {name}")
        spec = analyze_video(file)
        full_spec += f"\n\n---\n# Source: {name}\n\n{spec}"

    pathlib.Path("gameplay_spec.md").write_text(full_spec, encoding="utf-8")
    print("Done -> gameplay_spec.md")