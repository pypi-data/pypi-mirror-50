# -*-coding:utf-8-*-

"""
    {0: 'Strawberry', 1: 'apple', 2: 'banana', 3: 'cabbage', 4: 'cucumber',
    5: 'fig', 6: 'lemon', 7: 'orange', 8: 'pineapple'}
"""

import numpy as np
import tensorflow as tf
import cv2
from keras.applications.densenet import preprocess_input
import os
import git

# pip install --index-url https://pypi.org/simple/  vegetablesclassify
if not os.path.exists('./Model'):
    git.Repo.clone_from('git://github.com/juebanchengzi/vegetablesclassify.git', './Model')
try:
    interpreter = tf.contrib.lite.Interpreter(model_path="./Model/model.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
except AttributeError:
    interpreter = tf.lite.Interpreter(model_path="./Model/model.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()


class classify(object):
    def __init__(self, image_path):
        self.image_path = image_path

    def vegetables_classify(self):

        image = cv2.imread(self.image_path)
        img_resize = cv2.resize(image, (224, 224))
        img_resize = np.expand_dims(img_resize, axis=0)
        x = preprocess_input(img_resize)

        interpreter.set_tensor(input_details[0]['index'], x)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        return list(output_data[0]).index(max(output_data[0]))


