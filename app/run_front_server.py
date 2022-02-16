from flask import Flask, render_template, redirect, url_for, request, jsonify
from time import strftime
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.resnet import preprocess_input
import numpy as np
import logging
import magic
from logging.handlers import RotatingFileHandler
import os


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess')


def get_model(path):
    global model
    model = load_model(path)


model_path = "app/models/model.h5"
# model_path = "models/model.h5"
get_model(model_path)

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def get_prediction(data):
    data["type"] = magic.from_file('last_photo.jpg', mime=True)
    types = ['image/jpeg', 'image/png']
    if data["type"] not in types:
        data["success"] = False
        data["predictions"] = "This is not a positive type file!!"
        return data
    img = image.load_img('last_photo.jpg', target_size=(150, 150))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    predict = model.predict(x)
    data["predictions"] = "men" if int(np.around(predict[0][0], 0)) == 1 else "women"
    data['predict_proba'] = predict[0][0]
    data["success"] = True
    return data


@app.route("/api/predict", methods=['POST'])
def upload_file():
    data = dict()
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    if request.method == 'POST':
        try:
            file = request.files['file']
            file.save(os.path.join('last_photo.jpg'))
        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            data['success'] = False
            return jsonify(data)
        data = get_prediction(data)
        logger.info(f'{dt} Data: {data}')
        del data['predict_proba']
    return jsonify(data)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    data = dict()
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    if request.method == 'POST':
        try:
            file = request.files['profile']
            file.save(os.path.join('last_photo.jpg'))
            data = get_prediction(data)
        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            data['success'] = False
            return redirect(url_for('predict_form'))
        logger.info(f'{dt} Data: {data}')
        return redirect(url_for('predicted', response=data['predictions']))
    return render_template('form.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
