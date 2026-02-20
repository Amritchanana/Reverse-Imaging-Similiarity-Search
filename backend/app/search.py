import os
import faiss
import json
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "http://localhost:8000"

EMB_PATH = os.path.join(BASE_DIR, "embeddings", "image_embeddings.npy")
META_PATH = os.path.join(BASE_DIR, "index", "metadata.json")
FAISS_PATH = os.path.join(BASE_DIR, "index", "product.index")

index = faiss.read_index(FAISS_PATH)

with open(META_PATH, "r") as f:
    metadata = json.load(f)

assert len(metadata) == index.ntotal

def search_similar(query_emb, k=10, category=None):
    query_emb = query_emb / np.linalg.norm(query_emb)
    query_emb = np.expand_dims(query_emb.astype("float32"), axis=0)

    scores, indices = index.search(query_emb, k*2)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        item = metadata[idx]
        if category and item["category"] != category:
            continue
        item["image_url"] = f"{BASE_URL}/images/{item['image_path']}"
        results.append({
                "Score": float(score),
                **item
        })
        
        if len(results) == k:
            break
    return results