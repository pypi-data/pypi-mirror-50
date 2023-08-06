import tensorflow as tf
from tensorflow import keras
import numpy as np
import pickle

def load_data(fn, maxlen=-1):
  lines = []
  X = []
  Y = []
  with open(fn, 'r') as f:
    lines = f.readlines()
  for l in lines:
    word, stress = l.split('\t')
    if maxlen==-1 or len(word) < maxlen:
      X.append(word)
      Y.append(stress.strip())
  return X, np.array(Y, dtype='int16')

def save_tokenizer(token, fn):
  with open(fn, 'wb') as f:
    pickle.dump(token, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_tokenizer(fn):
  with open(fn, 'rb') as f:
    return pickle.load(f)

def prepare_input(input, token, maxlen):
  input_seq = token.texts_to_sequences(input)
  return keras.preprocessing.sequence.pad_sequences(input_seq, maxlen=maxlen, padding='post')



