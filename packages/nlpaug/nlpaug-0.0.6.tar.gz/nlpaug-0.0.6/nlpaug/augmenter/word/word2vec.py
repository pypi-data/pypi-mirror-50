import re, os
import numpy as np

from nlpaug.augmenter.word import WordEmbsAugmenter
from nlpaug.util import Action, DownloadUtil
import nlpaug.model.word_embs as nmw

WORD2VEC_MODEL = None


def init_word2vec_model(model_path, force_reload=False):
    """
        Load model once at runtime
    """
    global WORD2VEC_MODEL
    if WORD2VEC_MODEL and not force_reload:
        return WORD2VEC_MODEL

    word2vec = nmw.Word2vec()
    word2vec.read(model_path)
    WORD2VEC_MODEL = word2vec

    return WORD2VEC_MODEL


class Word2vecAug(WordEmbsAugmenter):
    def __init__(self, model_path='.', model=None, action=Action.SUBSTITUTE,
                 name='Word2vec_Aug', aug_min=1, aug_p=0.3, aug_n=5, stopwords=[],
                 tokenizer=None, reverse_tokenizer=None, force_reload=False, verbose=0):
        super().__init__(
            model_path=model_path, aug_n=aug_n,
            action=action, name=name, aug_p=aug_p, aug_min=aug_min, stopwords=stopwords,
            tokenizer=tokenizer, reverse_tokenizer=reverse_tokenizer, verbose=verbose)

        if model is None:
            self.model = self.get_model(force_reload=force_reload)
        else:
            self.model = model

    def get_model(self, force_reload=False):
        return init_word2vec_model(self.model_path, force_reload)
