import pandas as pd
import openpyxl
from random import *


class Wordlist:
    def __init__(self):
        self.common_words = pd.read_excel(io='commonEnglishWords.xlsx')

        self.words = [row[0] for index, row in self.common_words.iterrows() if len(row[0]) < 7]
        # print(choices(words, k=1000))
        self.word_selection = choices(self.words, k=1000)
