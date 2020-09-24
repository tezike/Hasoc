# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/en_task.run_folds_task2.ipynb (unless otherwise specified).

__all__ = ['SEED', 'df', 'le', 'test_df', 'run', 'ensemble']

# Cell
import os

import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
import transformers

import Hasoc.config as config
import Hasoc.utils.utils as utils
import Hasoc.utils.engine as engine
import Hasoc.model.model as model
import Hasoc.dataset.dataset as dataset

from functools import partial
from sklearn.metrics import f1_score
from sklearn.preprocessing import LabelEncoder
from catalyst.data.sampler import BalanceClassSampler
from transformers import AdamW, get_linear_schedule_with_warmup

# Cell
SEED = 42
utils.seed_everything(SEED)

# Cell
df = pd.read_csv(config.DATA_PATH/'fold_df.csv')

# Cell
le = LabelEncoder()
le.fit_transform(df.task2)
le.classes_

# Cell
df['task2_encoded'] = le.transform(df.task2.values)

# Cell
test_df = pd.read_csv(config.DATA_PATH/'en_task_a/english_test.csv')

# Cell
def run(fold, num_epochs=6):
    NUM_EPOCHS = num_epochs
    train_df = df.query(f'kfold_task2!={fold}').reset_index(drop=True)
    valid_df = df.query(f'kfold_task2=={fold}').reset_index(drop=True)

    #export
    train_ds = utils.create_loader(train_df.text.values, train_df.task2_encoded, bs=config.TRAIN_BATCH_SIZE,
                                   ret_dataset=True)
    train_dl = utils.create_loader(train_df.text.values, train_df.task2_encoded, bs=config.TRAIN_BATCH_SIZE,
                                   sampler=BalanceClassSampler(labels=train_ds.get_labels(), mode="upsampling"))
    valid_dl = utils.create_loader(valid_df.text.values, valid_df.task2_encoded, bs=config.VALID_BATCH_SIZE)

    #export
    modeller = model.HasocModel(len(le.classes_), drop=0.6)

    #export
    model_params = list(modeller.named_parameters())

    #export
    # we don't want weight decay for these
    no_decay = ['bias', 'LayerNorm.weight', 'LayerNorm.bias']

    optimizer_params = [
        {'params': [p for n, p in model_params if n not in no_decay],
        'weight_decay':0.001},
        #  no weight decay should be applied
        {'params': [p for n, p in model_params if n in no_decay],
        'weight_decay':0.0}
    ]

    #export
    # lr = config.LR
    lr = 1e-4

    #export
    optimizer = AdamW(optimizer_params, lr=lr)

    #export
    num_train_steps = int(len(df) / config.TRAIN_BATCH_SIZE * config.NUM_EPOCHS)

    #export
    scheduler = get_linear_schedule_with_warmup(optimizer=optimizer,
                                                    num_warmup_steps=20,
                                                    num_training_steps=num_train_steps-20)

    #export
    # fit = engine.BertFitter(modeller, (train_dl, valid_dl), optimizer, nn.CrossEntropyLoss(), partial(f1_score, average='macro'), config.DEVICE, scheduler=scheduler, log_file='en_task2_log.txt')
    fit = engine.BertFitter(modeller, (train_dl, valid_dl), optimizer, utils.LabelSmoothingCrossEntropy(), partial(f1_score, average='macro'), config.DEVICE, scheduler=scheduler, log_file='en_task2_log.txt')

    #export
    fit.fit(NUM_EPOCHS, model_path=os.path.join(config.MODEL_PATH/f'en_task2_{fold}.pth'), show_graph=False)

    #export
    test_dl = utils.create_loader(test_df.text.values, lbls=[None]*len(test_df.text.values), bs=config.VALID_BATCH_SIZE, is_test=True)

    #export
    modeller = model.HasocModel(len(le.classes_))
    modeller.load_state_dict(torch.load(config.MODEL_PATH/f'en_task2_{fold}.pth'))

    #export
    preds = engine.get_preds(test_dl.dataset, test_dl, modeller, config.DEVICE, ensemble_proba=True)

    np.save(os.path.join('..', 'outputs', f'submission_EN_B_{fold}.npy'), preds)

# Cell
for i in range(5):
    run(i)

# Cell
def ensemble():
    preds_0 = np.load(os.path.join('..', 'outputs', f'submission_EN_B_0.npy'))
    preds_1 = np.load(os.path.join('..', 'outputs', f'submission_EN_B_1.npy'))
    preds_2 = np.load(os.path.join('..', 'outputs', f'submission_EN_B_2.npy'))
    preds_3 = np.load(os.path.join('..', 'outputs', f'submission_EN_B_3.npy'))
    preds_4 = np.load(os.path.join('..', 'outputs', f'submission_EN_B_4.npy'))

    preds = (preds_0 + preds_1 + preds_2 + preds_3 + preds_4) / 5

    preds = le.inverse_transform(torch.tensor(preds).argmax(dim=-1).numpy())

    #export
    sub = pd.read_csv(config.DATA_PATH/'en_task_a/english_test.csv')

    #export
    submission_en_task1_df = test_df.drop(columns=['text', 'task1', 'task2']).copy()

    #export
    submission_en_task1_df['task2'] = preds

    #export
    submission_en_task1_df.to_csv(os.path.join('..', 'outputs', f'submission_EN_B.csv'), index=False)

# Cell
ensemble()