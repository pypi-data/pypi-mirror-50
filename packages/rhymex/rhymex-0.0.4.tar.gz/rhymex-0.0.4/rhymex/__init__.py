from rhymex.word_profile import WordProfile
VOWELS = "aeiouAEIOUаоэиуыеёюяАОЭИУЫЕЁЮЯ"

def is_rhyme(word1, word2, score_border=4, syllable_number_border=4):
  """
  Проверка рифмованности 2 слов.

  :param word1: первое слово для проверки рифмы, уже акцентуированное (Word).
  :param word2: второе слово для проверки рифмы, уже акцентуированное (Word).
  :param score_border: граница определния рифмы, чем выше, тем строже совпадение.
  :param syllable_number_border: ограничение на номер слога с конца, на который падает ударение.
  :return result: является рифмой или нет.
  """
  p1 = WordProfile(word1)
  p2 = WordProfile(word2)


  score = 0
  for i, ch1 in enumerate(p1.get_stressed_syllable_text()):
      for j, ch2 in enumerate(p2.get_stressed_syllable_text()[i:]):
          if ch1 != ch2:
              continue
          if ch1 in VOWELS:
              score += 3
          else:
              score += 1

  return (p1.stressed_syllable_index_from_end == p2.stressed_syllable_index_from_end and
        p1.syllables_count == p2.syllables_count and
        p1.stressed_syllable_index_from_end <= syllable_number_border and
        score >= score_border)
