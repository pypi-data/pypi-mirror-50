import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

from rhymex.utils import prepare_input
import sys
from rhymex.hyperparams import SEQ_LENGTH, STRESS_TOKEN, STRESS_MODEL


class StressModel:
  def __init__(self):
    self.model = STRESS_MODEL
    self.token = STRESS_TOKEN

  def predict(self, text):
    seq = prepare_input([text], self.token, SEQ_LENGTH)
    return np.argmax(self.model.predict(seq))