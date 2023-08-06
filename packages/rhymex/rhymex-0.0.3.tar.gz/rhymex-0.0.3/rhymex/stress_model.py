import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
from tensorflow.keras.models import load_model
from rhymex.utils import load_tokenizer, prepare_input
import sys
from rhymex.hyperparams import SEQ_LENGTH

class StressModel:
  def __init__(self, path_to_model):
    self.model = load_model(os.path.join(path_to_model, 'model.h5'))
    self.token = load_tokenizer(os.path.join(path_to_model, 'tokenizer.bin'))

  def predict(self, text):
    seq = prepare_input([text], self.token, SEQ_LENGTH)
    return np.argmax(self.model.predict(seq))