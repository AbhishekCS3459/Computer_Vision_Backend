from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np
import os
from io import BytesIO
from flask_cors import CORS 

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
model_path = os.path.join(os.path.dirname(__file__), "cats_vs_dogs_model.h5")
model = load_model(model_path)
classes = ['cat', 'dog', 'human']

def prepare_image(img):
    img = img.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

@app.route("/predict", methods=["POST"])
def predict():
    print("Predict route called!")
    if "file" not in request.files:
        print("No file part in request")
        return jsonify({"error": "No file uploaded"}), 400

    img_file = request.files["file"]
    print(f"Received file: {img_file.filename}")
    
    try:
        img = image.load_img(BytesIO(img_file.read()), target_size=(224, 224))
        print("Image loaded successfully")
    except Exception as e:
        print(f"Image loading error: {str(e)}")
        return jsonify({"error": f"Failed to load image: {str(e)}"}), 500

    try:
        img_array = prepare_image(img)
        prediction = model.predict(img_array)
        print("Prediction successful:", prediction)
        class_index = np.argmax(prediction)
        return jsonify({"result": classes[class_index]})
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

# write a test route
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Test route is working!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
