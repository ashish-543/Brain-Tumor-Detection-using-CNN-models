import tensorflow as tf
import numpy as np
import os 
import sys

# Keras
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
from tensorflow.keras.applications.vgg16 import preprocess_input



# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH ='model0.keras'

# Load your trained model
model = load_model(MODEL_PATH)




def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img = tf.cast(img, tf.float32)
    x = preprocess_input(img)
    # Preprocessing the image
    # x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    # x=x/255
    x = np.expand_dims(x, axis=0)
   

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    # x = preprocess_input(x)
    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds == 0:
        preds = "The Person has Glioma. Visit nearest hospital for further checkup."
    elif preds == 1:
        preds = "The Person has Meningioma. Visit nearest hospital for further checkup."
    elif preds == 2:
        preds = "The Person has No Tumor."
    elif preds == 3:
        preds = "The person has Pituitary. Visit nearest hospital for further checkup."

    
    
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)