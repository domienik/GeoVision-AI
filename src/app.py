from pathlib import Path
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
import pandas as pd
from database import save_classification, get_classifications

# Caminhos
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "eurosat_model.keras"

# Configurações
IMG_SIZE = (128, 128)

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

CLASS_DESCRIPTIONS = {
    "AnnualCrop": "Área de cultivo anual, útil para monitoramento agrícola e planejamento de safras.",
    "Forest": "Área de floresta, importante para monitoramento ambiental e preservação.",
    "HerbaceousVegetation": "Vegetação herbácea, comum em áreas naturais ou rurais.",
    "Highway": "Rodovia ou via de transporte, útil para análise de infraestrutura.",
    "Industrial": "Área industrial, relacionada ao uso urbano e econômico do solo.",
    "Pasture": "Área de pastagem, relevante para pecuária e uso agrícola.",
    "PermanentCrop": "Cultivo permanente, como plantações de longo prazo.",
    "Residential": "Área residencial, útil para planejamento urbano e análise territorial.",
    "River": "Área com rio ou curso d'água, importante para gestão hídrica e prevenção de riscos.",
    "SeaLake": "Área de mar ou lago, relevante para monitoramento ambiental e recursos hídricos."
}

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

def predict_image(image):
    image = image.convert("RGB")
    image = image.resize(IMG_SIZE)

    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array, verbose=0)[0]

    predicted_index = np.argmax(predictions)
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = predictions[predicted_index] * 100

    return predicted_class, confidence, predictions

st.set_page_config(
    page_title="GeoVision AI",
    page_icon="🛰️",
    layout="centered"
)

st.title("🛰️ GeoVision AI")
st.subheader("Classificação inteligente de imagens orbitais com Deep Learning")

st.write(
    """
    Esta POC utiliza Inteligência Artificial para classificar imagens orbitais do dataset EuroSAT.
    A solução demonstra como dados de satélite podem apoiar decisões em agricultura,
    meio ambiente, planejamento urbano e gestão territorial.
    """
)

model = load_model()

uploaded_file = st.file_uploader(
    "Envie uma imagem orbital para classificação",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(image, caption="Imagem enviada", use_container_width=True)

    predicted_class, confidence, predictions = predict_image(image)

    save_classification(
    nome_arquivo=uploaded_file.name,
    classe_prevista=predicted_class,
    confianca=confidence
    )

    st.markdown("## Resultado da classificação")
    st.success(f"Classe prevista: **{predicted_class}**")
    st.info(f"Confiança do modelo: **{confidence:.2f}%**")

    st.markdown("### Top 3 previsões do modelo")

    top_indices = np.argsort(predictions)[-3:][::-1]

    for position, index in enumerate(top_indices, start=1):
        class_name = CLASS_NAMES[index]
        probability = predictions[index] * 100
        st.write(f"{position}. **{class_name}** — {probability:.2f}%")

    st.markdown("### Probabilidade por classe")

    probabilities = {
        CLASS_NAMES[i]: float(predictions[i] * 100)
        for i in range(len(CLASS_NAMES))
    }

    st.bar_chart(probabilities)

else:
    st.warning("Envie uma imagem para testar o modelo.")


st.markdown("---")
st.markdown("## Histórico de classificações")

historico = get_classifications()

if historico:
    df_historico = pd.DataFrame(
        historico,
        columns=[
            "ID",
            "Nome do arquivo",
            "Classe prevista",
            "Confiança (%)",
            "Data e hora"
        ]
    )

    st.dataframe(df_historico, use_container_width=True)
else:
    st.info("Nenhuma classificação registrada ainda.")


st.markdown("---")
st.markdown("## 🔥 Módulo IoT - Risco de Queimada")

st.write(
    """
    Esta seção representa a integração com o ESP32 simulado no Wokwi.
    O módulo utiliza temperatura e umidade do ar para identificar condições
    favoráveis a risco de queimada.
    """
)

col1, col2 = st.columns(2)

with col1:
    temperatura_iot = st.slider(
        "Temperatura captada pelo ESP32 (°C)",
        min_value=0.0,
        max_value=50.0,
        value=28.0,
        step=0.5
    )

with col2:
    umidade_iot = st.slider(
        "Umidade do ar captada pelo ESP32 (%)",
        min_value=0.0,
        max_value=100.0,
        value=45.0,
        step=1.0
    )

risco_queimada = temperatura_iot > 35 or umidade_iot < 35

st.markdown("### Resultado do monitoramento IoT")

col3, col4 = st.columns(2)

with col3:
    st.metric("Temperatura", f"{temperatura_iot:.1f} °C")

with col4:
    st.metric("Umidade do ar", f"{umidade_iot:.0f} %")

if risco_queimada:
    st.error("🚨 RISCO DE QUEIMADA DETECTADO")
    st.write(
        """
        As condições ambientais indicam possível risco de queimada.
        Em uma aplicação real, esse alerta poderia ser enviado para uma central
        de monitoramento, banco de dados ou serviço em nuvem.
        """
    )
else:
    st.success("✅ Condição ambiental normal")
    st.write(
        """
        Os dados atuais não indicam condição crítica de risco de queimada.
        """
    )

st.caption(
    "Regra usada: risco quando temperatura > 35°C ou umidade do ar < 35%."
)


st.markdown("---")
st.markdown("## ☁️ Arquitetura em Nuvem com AWS")

st.write(
    """
    Esta arquitetura representa como a solução poderia ser implantada em uma versão real,
    usando serviços em nuvem para armazenar imagens, processar previsões e registrar os resultados.
    """
)

st.markdown("### Fluxo proposto")

st.write(
    """
    1. O usuário envia uma imagem orbital pelo dashboard.
    2. A imagem é armazenada em um bucket Amazon S3.
    3. Uma função AWS Lambda executa o processamento da imagem.
    4. O modelo de IA realiza a classificação do uso do solo.
    5. O resultado é salvo em um banco de dados, como Amazon RDS ou DynamoDB.
    6. O dashboard exibe a classe prevista, a confiança e o histórico das análises.
    7. Dados de sensores ESP32 poderiam ser enviados via API ou AWS IoT Core.
    """
)

st.markdown("### Serviços utilizados na proposta")

st.table({
    "Serviço": [
        "Amazon S3",
        "AWS Lambda",
        "Amazon RDS / DynamoDB",
        "AWS IoT Core",
        "API Gateway",
        "Dashboard Streamlit"
    ],
    "Função no projeto": [
        "Armazenar imagens orbitais enviadas pelo usuário",
        "Executar o processamento e acionar a classificação",
        "Guardar histórico das previsões e dados dos sensores",
        "Receber dados enviados por dispositivos ESP32",
        "Criar uma API para comunicação entre sensores, backend e dashboard",
        "Exibir resultados, gráficos, histórico e alertas"
    ]
})

st.info(
    """
    Nesta POC, o processamento foi executado localmente para simplificar a demonstração.
    A arquitetura em nuvem mostra como a solução poderia evoluir para um ambiente real,
    escalável e integrado com sensores IoT.
    """
)