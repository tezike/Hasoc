# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/utils.ipynb (unless otherwise specified).

__all__ = ['bert_cls_splitter', 'HFTokenizer', 'Add_Special_Cls']

# Cell
import torch
import torch.nn as nn
import transformers
from fastcore.test import *
from fastcore.transform import Transform
from fastcore.foundation import L
from fastai.text.data import TensorText
from fastai.text.core import Tokenizer

# Cell
def bert_cls_splitter(m):
    "Split the classifier head from the backbone"
    groups = [nn.Sequential(m.model.embeddings,
                m.model.encoder.layer[0],
                m.model.encoder.layer[1],
                m.model.encoder.layer[2],
                m.model.encoder.layer[3],
                m.model.encoder.layer[4],
                m.model.encoder.layer[5],
                m.model.encoder.layer[6],
                m.model.encoder.layer[7],
                m.model.encoder.layer[8],
                m.model.encoder.layer[9],
                m.model.encoder.layer[10],
                m.model.encoder.layer[11],
                m.model.pooler)]
#     groups = L(groups + [m.model.classifier])
    groups = L(groups) #using BertModel which ends at pool
    # fastai stores the parametes in each layer in a `params` variable
    return groups.map(params)

# Cell
class HFTokenizer():
    def __init__(self, tokenizer):
        self.tok = tokenizer

    def tokenize(self, text):
        tokens = self.tok.tokenize(text)
        return tokens

    def __call__(self, items):
        # ALways yeild the tokenized text before passing it to the Tokenizer Transform
        for text in items:
            yield self.tokenize(text)

# Cell
class Add_Special_Cls(Transform):
    order = 7
    def __init__(self, tokenizer):
        self.tok = tokenizer

    def encodes(self, o):
        return TensorText(self.tok.build_inputs_with_special_tokens(list(o)))