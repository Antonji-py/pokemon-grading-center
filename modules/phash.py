import os
import pickle
import imagehash
import cv2
import numpy as np
from PIL import Image


def create_phashes(database_path):
    phashes = []

    for expansion in os.listdir(f"{database_path}/stock_images"):
        for card in os.listdir(f"{database_path}/stock_images/{expansion}"):
            print(f"Calculating pHash for: {expansion}/{card}")
            img = cv2.imdecode(np.fromfile(f"{database_path}/stock_images/{expansion}/{card}", dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            pil_img = Image.fromarray(img)
            img_hash = imagehash.phash(pil_img, 32, 4)

            phashes.append(str(img_hash))

    with open(f"{database_path}/phashes.txt", "wb") as hashes_file:
        pickle.dump(phashes, hashes_file)


def load_phashes(phashes_path):
    with open(phashes_path, 'rb') as file:
        phashes = [imagehash.hex_to_hash(phash) for phash in pickle.load(file)]

    return phashes


def get_img_phash(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    work_pil_img = Image.fromarray(img)
    work_img_hash = imagehash.phash(work_pil_img, 32, 4)

    return work_img_hash


def find_similar_imgs(input_img, phashes):
    input_img_phash = get_img_phash(input_img)

    distances = []
    for i, stock_hash in enumerate(phashes):
        distances.append({i: stock_hash - input_img_phash})

    top_matches = sorted(distances, key=lambda x: list(x.values())[0])[:3]

    return top_matches
