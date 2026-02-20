import os 
import faiss
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

EMB_PATH = os.path.join(PROJECT_ROOT, "embeddings", "image_embeddings.npy")
FAISS_PATH = os.path.join(PROJECT_ROOT, "index", "product.index")

# load embeddings
embeddings = np.load(EMB_PATH).astype("float32")

dim = embeddings.shape[1]

# cosine similarity (building FAISS Index (cosine via inner product on normalized vector))
index = faiss.IndexFlatIP(dim)
index.add(embeddings)

# save index
faiss.write_index(index, FAISS_PATH)

print(f"FAISS index saved at: {FAISS_PATH}")
print(f"Total vectors indexed: {index.ntotal}")





'''
#---test with one query image---
q_name= names[0]
q_img = cv2.imread(os.path.join(IMG_DIR, q_name))
q_img = cv2.cvtColor(q_img, cv2.COLOR_BGR2RGB)
q_img = cv2.resize(q_img, (224,224))
q_img = preprocess_input(np.expand_dims(q_img, 0))
q_emb = model.predict(q_img, verbose=0)[0]
q_emb = (q_emb / np.linalg.norm(q_emb)).astype("float32")
D, I = index.search(q_emb.reshape(1,-1), k=5) #find top 5 similiar images

print("Query:", q_name)
print("Top 5 similiar images:")
for idx, score in zip(I[0], D[0]):
    print(names[idx], score)

faiss.write_index(index, "../index/product_index.faiss")

with open("../index/image_names.txt", "w") as f:
    for name in names:
        f.write(name + "\n")

print("Index and metadata saved.")

'''