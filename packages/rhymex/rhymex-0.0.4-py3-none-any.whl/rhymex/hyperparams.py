from pathlib import Path
from tensorflow.keras.models import load_model
from rhymex.utils import load_tokenizer
import os

# import pkg_resources
SEQ_LENGTH = 15 #max length of word
NUM_CHARS = 50 #size of vocabulary in tokenizer. max number of chars it can hold
MODEL_OUTPUT_PATH = Path(__file__).parent.joinpath('model').resolve()

STRESS_MODEL = load_model(os.path.join(MODEL_OUTPUT_PATH, 'model.h5'))
STRESS_TOKEN = load_tokenizer(os.path.join(MODEL_OUTPUT_PATH, 'tokenizer.bin'))