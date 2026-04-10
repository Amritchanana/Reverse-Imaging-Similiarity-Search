"""
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


import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")

@tf.function(input_signature=[tf.TensorSpec(shape=(1, 224, 224, 3), dtype=tf.float32)])
def _infer(tensor):
    return model(tensor, training=False)

def get_query_embedding(image_path: str) -> np.ndarray:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = preprocess_input(np.expand_dims(img, axis=0).astype("float32"))
    tensor = tf.constant(img)
    emb = _infer(tensor).numpy()[0]
    emb = emb / np.linalg.norm(emb)
    return emb.astype("float32")
"""

import cv2
import numpy as np
import tensorflow as tf
import time
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")

@tf.function(input_signature=[tf.TensorSpec(shape=(1, 224, 224, 3), dtype=tf.float32)])
def _infer(tensor):
    return model(tensor, training=False)

def get_query_embedding(image_path: str) -> np.ndarray:
    t0 = time.time()

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = preprocess_input(np.expand_dims(img, axis=0).astype("float32"))
    t1 = time.time()

    tensor = tf.constant(img)
    emb = _infer(tensor).numpy()[0]
    t2 = time.time()

    emb = emb / np.linalg.norm(emb)
    t3 = time.time()

    print(f"⏱ Image read+resize : {(t1-t0)*1000:.1f}ms", flush=True)
    print(f"⏱ Model inference   : {(t2-t1)*1000:.1f}ms", flush=True)
    print(f"⏱ Normalize         : {(t3-t2)*1000:.1f}ms", flush=True)
    print(f"⏱ Total embedding   : {(t3-t0)*1000:.1f}ms", flush=True)

    return emb.astype("float32")