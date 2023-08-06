from rhymex.stress_model import StressModel
from rhymex.hyperparams import MODEL_OUTPUT_PATH
from rhymex.syllables import get_syllables

class WordProfile:
  def __init__(self, word):
    self.word = word
    self.stress_model = StressModel(MODEL_OUTPUT_PATH)
    self.syllables = get_syllables(word)
    self.syllables_count = len(self.syllables)
    self.stressed_syllable_index = -1
    index = self.stress_model.predict(word)
    j = 0
    for i, slb in enumerate(self.syllables):
      j = j + len(slb.text)
      if index <= j:
        self.stressed_syllable_index = i
        break
    self.stressed_syllable_index_from_end = self.syllables_count - self.stressed_syllable_index - 1

  def get_stressed_syllable_text(self):
    if self.stressed_syllable_index == -1:
      return self.word
    else:
      return self.syllables[self.stressed_syllable_index].text


  def __str__(self):
    return "Syllables count: {}\n Stressed syllable from end: {}\n " \
          "Stressed syllable text: {}\n".format(self.syllables_count, self.stressed_syllable_index_from_end,
                                      self.get_stressed_syllable_text())
  


