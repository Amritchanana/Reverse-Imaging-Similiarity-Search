import os
import json
import cv2
import numpy as np
import pandas as pd
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

#paths
CSV_PATH = "../data/metadata/fashion.csv"
IMG_DIR = "../data/images_with_product_ids"
EMB_OUT = "../embeddings/image_embeddings.npy"
META_OUT = "../index/metadata.json"

os.makedirs(os.path.dirname(EMB_OUT), exist_ok=True)
os.makedirs(os.path.dirname(META_OUT), exist_ok=True)

# loading model
model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    pooling="avg")

df = pd.read_csv(CSV_PATH)

embeddings = []
metadata = []
skipped_count = 0
for _, row in df.iterrows():
    img_path = os.path.join(IMG_DIR, row["Image"])

    img = cv2.imread(img_path)
    if img is None:
        continue    #skipping corrupted/missing images

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = preprocess_input(np.expand_dims(img, axis=0))

    emb = model.predict(img, verbose=0)[0]
    norm = np.linalg.norm(emb)
    if norm == 0:
        skipped_count += 1
        continue
    emb = emb / norm  # L2 normalize

    embeddings.append(emb.astype("float32"))

    metadata.append({
        "image_path" : row["Image"],
        "product_id" : int(row["ProductId"]),
        "category" : row["Category"]
    })

#converting to numpy array

if len(embeddings) == 0:
    raise RuntimeError("No embeddings extracted. Check image paths.")
embeddings = np.vstack(embeddings)
print(f"Processed {len(embeddings)} images, skipped {skipped_count}")


#saving outputs
np.save(EMB_OUT, embeddings)

with open(META_OUT, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"Saved embeddings: {embeddings.shape}")
print("saved metadata.json")
