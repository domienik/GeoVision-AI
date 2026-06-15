from pathlib import Path
import numpy as np
import tensorflow as tf
from PIL import Image

# Caminhos principais
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "eurosat_model.keras"
DATASET_PATH = BASE_DIR.parent / "data" / "raw"

# Classes na mesma ordem usada pelo TensorFlow
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

# Carrega o modelo treinado
model = tf.keras.models.load_model(MODEL_PATH)

# Pega uma imagem de teste do próprio dataset
image_path = next((DATASET_PATH / "Forest").glob("*"))

print(f"Imagem testada: {image_path}")

# Abre e prepara a imagem
image = Image.open(image_path).convert("RGB")
image = image.resize(IMG_SIZE)

image_array = np.array(image)
image_array = np.expand_dims(image_array, axis=0)

# Faz a previsão
predictions = model.predict(image_array)
predicted_index = np.argmax(predictions[0])
predicted_class = CLASS_NAMES[predicted_index]
confidence = predictions[0][predicted_index] * 100

print("\nResultado da previsão:")
print(f"Classe prevista: {predicted_class}")
print(f"Confiança: {confidence:.2f}%")