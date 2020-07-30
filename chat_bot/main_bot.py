import os
import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class chatBot:
    def __init__(self, file: str):
        DIR_PATH = os.path.dirname(os.path.abspath(__file__))
        path = DIR_PATH + "\\" + file
        f = open(path, "r", errors="ignore")
        raw = f.read().lower()

        nltk.download("punkt")
        nltk.download("wordnet")

        self.sent_tokens = nltk.sent_tokenize(raw)
        self.word_tokens = nltk.word_tokenize(raw)

        self.lemmer = nltk.stem.WordNetLemmatizer()

        self.remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def lem_tokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    def lem_normalize(self, text):
        return self.lem_tokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))

    def response(self, user_response: str) -> str:
        robo_response = ''
        self.sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=self.lem_normalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if req_tfidf == 0:
            robo_response = robo_response + "I am sorry! I don't understand you"
            return robo_response
        else:
            robo_response = robo_response + self.sent_tokens[idx]
            return robo_response