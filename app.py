from flask import Flask, request, jsonify
from PIL import Image, ImageOps
from tensorflow import keras
from tensorflow.keras.utils import img_to_array #ImageDataGenerator, load_img
from google.cloud import storage
#from googleapiclient.discovery import build
#from google.oauth2 import service_account
import tensorflow as tf
import numpy as np
import io
import os

#credentials file path and Google Drive file ID
#credentials_file = 'path/to/credentials.json' #blm
#drive_file_id = 'your_google_drive_file_id' #blm

#bikin credentials drive
#credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=['https://www.googleapis.com/auth/drive']) #diisi sama path nya
#drive_service = build('drive', 'v3', credentials = credentials)

#req = drive_service.files().get_media(fileId=drive_file_id)
#file = drive_service.files().get(fileId=drive_file_id).execute()
#filename = file['machine learning model converted.tflite']

#model_path = 'machine learning model converted.tflite'
#interpreter = tf.lite.Interpreter(model_path=model_path)
#interpreter.allocate_tensors()

#bucket
storage_client = storage.Client()
bucket_name = 'onikku-bucket'
model_file_name = 'model.h5'
bucket = storage_client.bucket(bucket_name)
model_blob = bucket.blob('model.h5')
model_blob.download_to_filename('/tmp/model.h5')

model = keras.models.load_model('/tmp/model.h5')

#input and output details
#input_details = interpreter.get_input_details()
#output_details = interpreter.get_output_details()

#image to array
def transform_image(img):
    #imgs = []
    img = img.resize((256, 256)) #masih kira2
    img_array = img_to_array(img)
    img_array = img_array.astype(np.float32) / 255 #masih kira2
    #img_array = tf.image.resize(img_array, [256, 256]) #masih kira2
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

#construct prediction, dah diubah
def predict(x):
    predictions = model(x)
    pred = np.argmax(predictions, axis=1)
    return pred

app = Flask(__name__)
   
@app.route("/status", methods=["POST"])
def status():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})
        try:
            image_bytes = file.read()
            pillow_img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            prediction = predict(transform_image(pillow_img))
            data = {"prediction": int(prediction)}
            return jsonify(data)
                
        except Exception as e:
            return jsonify({"error": str(e)})

@app.route("/", methods=["GET"])
def upload_file():
    return "OK"



if __name__ == '__main__':
    # Menjalankan aplikasi Flask di port yang ditentukan oleh variabel lingkungan PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True)
    

