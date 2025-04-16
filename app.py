from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np
import os
from io import BytesIO

app = Flask(__name__)
model = load_model("cats_vs_dogs_model.h5")
classes = ['cat', 'dog', 'human']

def prepare_image(img):
    img = img.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    img_file = request.files["file"]
    img = image.load_img(BytesIO(img_file.read()), target_size=(224, 224))
    img_array = prepare_image(img)

    prediction = model.predict(img_array)
    class_index = np.argmax(prediction)
    return jsonify({"result": classes[class_index]})
# write a test route
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Test route is working!"})

if __name__ == "__main__":
    app.run(debug=True)
