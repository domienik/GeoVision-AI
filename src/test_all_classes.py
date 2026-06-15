from pathlib import Path
import numpy as np
import tensorflow as tf
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "eurosat_model.keras"
DATASET_PATH = BASE_DIR.parent / "data" / "raw"

CLASS_NAMES = [
    "AnnualCrop",
    "Forest",
    "HerbaceousVegetation",
    "Highway",
    "Industrial",
    "Pasture",
    "PermanentCrop",
    "Residential",
    "River",
    "SeaLake"
]

IMG_SIZE = (128, 128)

model = tf.keras.models.load_model(MODEL_PATH)

print("\nTestando uma imagem de cada classe:\n")

for real_class in CLASS_NAMES:
    image_path = next((DATASET_PATH / real_class).glob("*"))

    image = Image.open(image_path).convert("RGB")
    image = image.resize(IMG_SIZE)

    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array, verbose=0)
    predicted_index = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = predictions[0][predicted_index] * 100

    status = "OK" if predicted_class == real_class else "ERRO"

    print(f"{status} | Real: {real_class} | Previsto: {predicted_class} | Confiança: {confidence:.2f}%")