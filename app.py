python
import streamlit as st
import pandas as pd
import time
from flask import Flask, request, jsonify

# Inicializa la aplicación Flask
app = Flask(__name__)

# Variables para almacenar los datos de los sensores
sensor_data = {
    "temperature": [],
    "humidity": [],
    "soilMoisture": []
}

@app.route('/', methods=['POST'])
def receive_data():
    data = request.get_json()
    sensor_data["temperature"].append(data.get("temperature"))
    sensor_data["humidity"].append(data.get("humidity"))
    sensor_data["soilMoisture"].append(data.get("soilMoisture"))
    return jsonify({"status": "success"})

def start_flask():
    app.run(port=8501)

# Inicia la aplicación Flask en segundo plano
import threading
flask_thread = threading.Thread(target=start_flask)
flask_thread.start()

# Configura la interfaz Streamlit
st.title("Sistema de Monitoreo IoT para Huertas Urbanas")

# Placeholder para los datos
placeholder = st.empty()

# Loop para actualizar los datos
while True:
    with placeholder.container():
        st.header("Datos del Sensor")
        df = pd.DataFrame(sensor_data)
        st.write(df)

        st.header("Indicadores")
        if len(sensor_data["temperature"]) > 0:
            st.metric(label="Temperatura (°C)", value=f"{sensor_data['temperature'][-1]:.2f}")
        if len(sensor_data["humidity"]) > 0:
            st.metric(label="Humedad (%)", value=f"{sensor_data['humidity'][-1]:.2f}")
        if len(sensor_data["soilMoisture"]) > 0:
            st.metric(label="Humedad del Suelo", value=sensor_data['soilMoisture'][-1])

    time.sleep(2)
