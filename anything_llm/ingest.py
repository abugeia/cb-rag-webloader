import os
import requests
from tqdm import tqdm # Pour avoir une jolie barre de progression !
from dotenv import load_dotenv

# --- À CONFIGURER ---
load_dotenv()
API_KEY = os.getenv("anything_llm_apikey")
# WORKSPACE_SLUG = "global_rag" # Le "slug" de l'URL
ANYTHINGLLM_URL = "http://localhost:3001"
SOURCE_DIRECTORY = "./src" # Le dossier contenant les fichiers .mdx
# --------------------

# Point de terminaison de l'API pour l'upload
# upload_url = f"{ANYTHINGLLM_URL}/api/v1/workspace/{WORKSPACE_SLUG}/upload"
upload_url = f"{ANYTHINGLLM_URL}/api/v1/document/upload"
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def find_mdx_files(directory):
    """Trouve tous les fichiers .mdx dans le répertoire et ses sous-dossiers."""
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith((".mdx", ".md")):
                file_list.append(os.path.join(root, file))
    return file_list

def upload_file(filepath):
    """Envoie un seul fichier à l'API Anything LLM."""
    try:
        with open(filepath, 'rb') as f:
            files = {'file': (os.path.basename(filepath), f)}
            response = requests.post(upload_url, headers=headers, files=files)

            if response.status_code == 200:
                return True, None
            else:
                return False, response.json().get('error', 'Erreur inconnue')
    except Exception as e:
        return False, str(e)

# --- Exécution Principale ---
print(f"Recherche des fichiers .mdx dans {SOURCE_DIRECTORY}...")
files_to_upload = find_mdx_files(SOURCE_DIRECTORY)
print(f"Trouvé {len(files_to_upload)} fichiers à téléverser.")

if not files_to_upload:
    print("Aucun fichier .mdx trouvé. Vérifiez le chemin SOURCE_DIRECTORY.")
    exit()

success_count = 0
fail_count = 0

# Utilise tqdm pour une barre de progression
for filepath in tqdm(files_to_upload, desc="Téléversement des fichiers"):
    success, error_msg = upload_file(filepath)
    if success:
        success_count += 1
    else:
        fail_count += 1
        print(f"\nÉchec du téléversement pour {filepath}: {error_msg}")

print("\n--- Téléversement Terminé ---")
print(f"Succès : {success_count}")
print(f"Échecs : {fail_count}")
print("\nIMPORTANT : Allez dans l'interface web d'Anything LLM pour 'Move to workspace' et lancer l'embedding !")
