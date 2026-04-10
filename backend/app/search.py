"""
import os
import faiss
import json
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "http://localhost:8000"
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMB_PATH = os.path.join(BACKEND_DIR, "embeddings", "image_embeddings.npy")
META_PATH = os.path.join(BACKEND_DIR, "index", "metadata.json")
FAISS_PATH = os.path.join(BACKEND_DIR, "index", "product.index")

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
"""

# fix-1-Replacing hardcoded localhost with env variable:

import os
import faiss
import json
import numpy as np
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")  # env-based
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMB_PATH = os.path.join(BACKEND_DIR, "embeddings", "image_embeddings.npy")
META_PATH = os.path.join(BACKEND_DIR, "index", "metadata.json")
FAISS_PATH = os.path.join(BACKEND_DIR, "index", "product.index")

try:
    index = faiss.read_index(FAISS_PATH)
    with open(META_PATH, "r") as f:
        metadata = json.load(f)
    assert len(metadata) == index.ntotal, \
        f"Mismatch: {len(metadata)} metadata vs {index.ntotal} index entries"
    print(f" FAISS index loaded: {index.ntotal} vectors", flush=True)
except FileNotFoundError as e:
    raise RuntimeError(f"Index files missing — run precompute script first: {e}")

def search_similar(query_emb, k=10, category=None):
    import time
    t0 = time.time()

    query_emb = query_emb / np.linalg.norm(query_emb)
    query_emb = np.expand_dims(query_emb.astype("float32"), axis=0)
    scores, indices = index.search(query_emb, k * 2)

    t1 = time.time()
    print(f"⏱ FAISS search      : {(t1-t0)*1000:.1f}ms", flush=True)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        item = metadata[idx]
        if category and item.get("category") != category:
            continue
        image_url = item.get("cloudinary_url") or f"{BASE_URL}/images/{item['image_path']}"
        results.append({
            "Score": float(score),
            "score": float(score),
            "image_url": image_url,
            **item
        })
        if len(results) == k:
            break

    t2 = time.time()
    print(f"⏱ Result building   : {(t2-t1)*1000:.1f}ms", flush=True)
    print(f"⏱ Total search      : {(t2-t0)*1000:.1f}ms", flush=True)

    return results