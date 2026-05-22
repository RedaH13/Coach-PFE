import os
from pymongo import MongoClient
from PyPDF2 import PdfReader
from google import genai
from dotenv import load_dotenv
import time

# Charger les variables d'environnement
load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB")
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = MongoClient(mongo_uri)
db = client[mongo_db]

# Créer un client Gemini
genai_client = genai.Client(api_key=gemini_api_key)

def ingest_folder(folder_path, collection_name, chunk_size=2000, overlap=300, batch_size=10):
    collection = db[collection_name]

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            reader = PdfReader(pdf_path)
            text = "".join(page.extract_text() or "" for page in reader.pages)

            # Découper en chunks plus grands
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size - overlap)]

            # Traiter par batchs
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i+batch_size]
                try:
                    response = genai_client.models.embed_content(
                        model="gemini-embedding-001",
                        contents=batch
                    )
                    for j, emb in enumerate(response.embeddings):
                        doc = {
                            "text": batch[j],
                            "metadata": {"source": filename, "chunk_id": i+j},
                            "embedding": list(emb.values)
                        }
                        existing = collection.find_one(doc["metadata"])
                        if not existing:
                            collection.insert_one(doc)

                    # Pause légère pour lisser le débit
                    time.sleep(1)

                except genai.errors.ClientError as e:
                    if "RESOURCE_EXHAUSTED" in str(e):
                        print("Quota limited, Waiting 40s...")
                        time.sleep(40)
                        continue
                    else:
                        raise

            print(f"{filename} ingéré dans {collection_name}")

# Exemple d’utilisation
ingest_folder("../Docs/Guides Academic", "academic_docs.chunks")
ingest_folder("../Docs/Memoires", "memoires")
ingest_folder("../Docs/Normes Biblio", "normes_biblio")
ingest_folder("../Docs/Regles Typographiques", "regles_typo")
