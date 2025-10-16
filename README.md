# cb-rag-webloader

-- Début de la partie a ne jamais modifier. --

Ce répo heberge une app, pour mon homelab, qui permet de scraper des site internet et mettre le contenu dans une base vecteur qdrant.
- **Scraper Service** : Collecte et traitement des données web
Un premier service est le scraper il pourra être lancé manuellement, via une url ou être planifié en tant que job.
- **RAG Service** : Chatbot avec recherche vectorielle
Un 2e service permet d'interroger un chatbot en francais et d'avoir des réponses plus pertinentes grâce à la base vecteur.  
- **Vector Database** : Qdrant (externe)
La base vecteur est un service externe. Sont url sera donnée par un fichier .env  
En local elle tournera sur docker.

L'app doit pouvoir être exec en local, avec docker et hébergée sur kubernetes.
L'utilisation de python est privilégiée ainsi que de librairies avec une large communauté et qui sont documentées.
Par exemple pourquoi pas crawl4ai pour le scrap.

Il faudra déterminer l'archi service, fichier et bdd.  
Il y aura une collection par thématique, donc par exemple immigration ou emploi.  
Faut il un service qui peut scraper tous les site (qui ont peut etre chacun leur méthode) ou un service pour chaque site ?
Faut il un dossier pour chaque site a scraper ou un dossier scrap dans lequel on met tout ? Comment 
Les fichiers doivent dans la mesure du possible contenir un nombre raisonable de ligne, si c'est trop long il faudra découper.

Pour gérer les dépendances UV est privilégié. Ainsi pour débuter un projet on peut faire `uv init`, pour instancier un virtual env `uv venv`, pour ajouter un lib `uv add nomdelalib `, pour éxécuter un script il faudra soit activer le virtual env soit faire `uv run python main.py`  
La machine de dev tourne sous windows et le terminal par defaut est git bash.

Le 1er site a scraper est un site australien pour avoir des visa de travail, il est en anglais : https://immi.homeaffairs.gov.au/visas/working-in-australia/skill-occupation-list  
Les pages exactes à scraper ne sont pas connues, il faudra parcourir le site et déterminer ce qu'on garde.


### Structure des données
- Collection par domaine thématique (ex: "immigration", "emploi")
- Métadonnées : URL source, date scraping, langue, type de contenu


-- Fin de la partie a ne jamais modifier. --


# Modèles légers et performants (< 500MB)
"sentence-transformers/all-MiniLM-L6-v2"        # 80MB, très bon
"sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  # 470MB, excellent pour FR+EN

FROM python:3.11-slim
# Pré-télécharger seulement le modèle nécessaire
RUN pip install sentence-transformers
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
# Image finale ~1.5GB au lieu de 10GB

class CollectionManager:
    def __init__(self):
        self.collections = {
            "immigration": ["visa", "permis", "résidence", "citoyenneté"],
            "emploi": ["job", "travail", "cv", "entretien", "salaire"],
            "logement": ["location", "achat", "immobilier"]
        }
    
    def detect_collection(self, user_query: str) -> str:
        # 1. Classification par mots-clés
        query_lower = user_query.lower()
        for collection, keywords in self.collections.items():
            if any(keyword in query_lower for keyword in keywords):
                return collection
        
        # 2. Classification par embedding (similiarité sémantique)
        return self.semantic_classification(user_query)
    
    def create_new_collection_if_needed(self, content: str, existing_collections: list):
        # Analyser si le contenu est suffisamment différent
        similarity_threshold = 0.7
        # Si similarité < threshold avec toutes les collections → nouvelle collection

Workflow intelligent :
Au scraping : Analyse automatique du contenu → suggestion de collection
À la requête : Classification de la question → routage vers la bonne collection
Fallback : Si incertain → recherche dans toutes les collections + scoring


# Validation humaine pour les nouvelles collections
if new_collection_detected:
    print(f"Nouvelle catégorie détectée: '{suggested_name}'")
    print(f"Similarité max avec existantes: {max_similarity:.2f}")
    confirm = input("Créer cette collection ? (y/n): ")