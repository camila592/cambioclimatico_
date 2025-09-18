from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from PIL import Image
from species_info import species_info

app = Flask(__name__)

# Cargar modelo
model = tf.keras.models.load_model("models/keras_model.h5")

#Cargar etiquetas
with open("labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/info")
def informacion():
    return render_template("informacion.html")

@app.route("/clasificador")
def clasificador():
    return render_template("clasificador.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return "No se subió ningún archivo."
    
    file = request.files["file"]

    if file.filename == "":
        return "Archivo vacío."
    
    # Guardar temporalmente la imagen para mostrar en result.html
    filepath = "static/uploaded_image.jpg"
    file.save(filepath)

    #Procesar la imagen
    image = Image.open(file).convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    #Predicción
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    species = labels[predicted_class]

    #Info desde species_info.py
    detalles = species_info.get(species, {
    "descripcion": "Información no disponible.",
    "ayuda": "Consulta fuentes oficiales de conservación.",
    "beneficio": "Clave para el equilibrio del ecosistema."
    })

    return render_template("result.html",
                           species=species,
                           description=detalles["descripcion"],
                           ayuda=detalles["ayuda"],
                           beneficio=detalles["beneficio"],
                           img_url=filepath)

@app.route("/calculadora")
def calculadora():
    return render_template("calculadora.html")

@app.route("/calcular", methods=['POST'])
def calcular():
    km_auto = float(request.form["km_auto"])
    km_publico = float(request.form["km_publico"])
    kwh_mes = float(request.form["kwh_mes"])
    comidas_carne = int(request.form["comidas_carne"])

    # Factores de emisión
    CO2_auto = km_auto * 0.21 * 52
    CO2_publico = km_publico * 0.10 * 52
    CO2_energia = kwh_mes * 0.36 * 12
    CO2_carne = comidas_carne * 5 * 52

    total = CO2_auto + CO2_publico + CO2_energia + CO2_carne

    # Tips personalizados
    tips = []
    if CO2_auto > 2000:
        tips.append("Considera usar transporte público, bicicleta o caminar para trayectos cortos.")
    if CO2_energia > 1500:
        tips.append("Reducí tu consumo eléctrico apagando luces innecesarias o usando LED.")
    if CO2_carne > 1000:
        tips.append("Proba reducir 1 comida con carne por semana: ahorrarías ~260 kg CO₂ al año.")
    if total < 3000:
        tips.append("¡Excelente! Tu huella está por debajo del promedio, seguí así.")

    return render_template("carbono.html", total=round(total, 2), tips=tips)


if __name__ == "__main__":
    app.run(debug=True)

