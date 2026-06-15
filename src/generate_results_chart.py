from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR / "outputs" / "confianca_por_classe.png"

classes = [
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

confiancas = [
    93.77,
    99.08,
    74.76,
    99.90,
    99.93,
    81.35,
    61.76,
    99.99,
    58.99,
    99.94
]

plt.figure(figsize=(12, 5))
plt.bar(classes, confiancas)
plt.ylim(0, 100)
plt.title("Confiança do modelo em uma imagem por classe")
plt.xlabel("Classes")
plt.ylabel("Confiança da previsão (%)")
plt.xticks(rotation=45, ha="right")

for i, valor in enumerate(confiancas):
    plt.text(i, valor + 1, f"{valor:.1f}%", ha="center", fontsize=8)

plt.tight_layout()

OUTPUT_PATH.parent.mkdir(exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=300)
plt.show()

print(f"Gráfico salvo em: {OUTPUT_PATH}")