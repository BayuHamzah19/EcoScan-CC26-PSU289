from fastapi import FastAPI, UploadFile, File
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI(title="EcoScan AI API")


@tf.keras.utils.register_keras_serializable()
class CustomNormalizationLayer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(CustomNormalizationLayer, self).__init__(**kwargs)
        
    def call(self, inputs):
        return inputs 


MODEL_PATH = 'model_terbaik.keras'

try:
    MODEL = tf.keras.models.load_model(
        MODEL_PATH, 
        custom_objects={'CustomNormalizationLayer': CustomNormalizationLayer},
        compile=False
    )
    print("✅ Berhasil! Otak AI EcoScan sukses dimuat ke dalam API.")
except Exception as e:
    print(f"❌ Gagal memuat model: {e}")
    raise e

CLASS_NAMES = ['Kaca', 'Kardus', 'Kertas', 'Logam', 'Organik', 'Plastik', 'Residu']

@app.get("/")
def home():
    return {"message": "EcoScan API is Running!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    
    image = image.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = np.expand_dims(img_array, 0) 
    img_array = img_array / 255.0            

    predictions = MODEL.predict(img_array)
    
    predicted_index = np.argmax(predictions[0])
    label = CLASS_NAMES[predicted_index]
    
    confidence = float(predictions[0][predicted_index] * 100)

    return {
        "status": "success",
        "prediction": label,
        "confidence": f"{confidence:.2f}%",
        "message": f"Ini terdeteksi sebagai {label}"
    }

if __name__ == "__main__":
    import uvicorn
    print("Memulai Server EcoScan...") 
    uvicorn.run(app, host="0.0.0.0", port=8000)
