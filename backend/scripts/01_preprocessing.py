"""import os 
import cv2
import pandas as pd 

IMG_DIR = 'data/images_with_product_ids'
META_FILE = '../data/fashion.csv'

df = pd.read_csv(META_FILE)

valid_images = []

for _, row in df.iterrows():
    img_path = os.path.join(IMG_DIR, f"{row['id']}.jpg")

    if not os.path.exists(img_path):
        continue

    img = cv2.imread(img_path)
    if img is None:
        continue

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img= cv2.resize(img, (224, 224))

    valid_images.append((row['id'], img))

print(f"Valid images : {len(valid_images)}") """

import os
import cv2

IMG_DIR = "../data/images_with_product_ids"  # adjust only if folder name differs

# picking one image to test preprocessing
img_name = os.listdir(IMG_DIR)[0]
img_path = os.path.join(IMG_DIR, img_name)

img = cv2.imread(img_path)

if img is None:
    raise ValueError("Image could not be loaded")

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (224, 224))

print("Image name:", img_name)
print("Image shape:", img.shape)
