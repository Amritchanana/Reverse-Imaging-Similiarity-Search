import cv2
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    pooling="avg"
)

def get_query_embedding(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Invalid image")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = preprocess_input(np.expand_dims(img, axis=0))

    emb = model.predict(img, verbose=0)[0]
    emb = emb / np.linalg.norm(emb)

    return emb.astype("float32")
