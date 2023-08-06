from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import os
import time
import tensorflow as tf
from tensorflow import keras
import random


class dataset(object):
    def __init__(self, train_data=None, train_labels=None, test_data=None, test_labels=None):
        if train_data is not None:
            self.train_data = np.asarray(train_data)
            self.train_size = self.train_data.shape[0]
            self.train_seed_hist = [0 for i in range(self.train_size)]
        else:
            self.train_data = None
        if train_labels is not None:
            self.train_labels = np.asarray(train_labels)
        else:
            self.train_labels = None
        if test_data is not None:
            self.test_data = np.asarray(test_data)
            self.test_size = self.test_data.shape[0]
            self.test_seed_hist = [0 for i2 in range(self.test_size)]
        else:
            self.test_data = None
        if test_labels is not None:
            self.test_labels = np.asarray(test_labels)
        else:
            self.test_labels = None
        self.train_call = -1
        self.test_call = -1

    def take(self, idx, type='train'):
        if type is 'train':
            if self.train_data is not None:
                if self.train_labels is not None:
                    return self.train_data[idx], self.train_labels[idx]
                else:
                    return self.train_data[idx]
        elif type is 'test':
            if self.test_data is not None:
                if self.test_labels is not None:
                    return self.test_data[idx], self.test_labels[idx]
                else:
                    return self.test_data[idx]

    def iterate(self, type='train', from_start=False):
        if type is 'train':
            if self.train_data is not None:
                if self.train_call == self.train_size - 1:
                    self.train_call = 0
                elif from_start:
                    self.train_call = 0
                else:
                    self.train_call += 1

                if self.train_labels is not None:
                    return self.train_data[self.train_call], self.train_labels[self.train_call]
                else:
                    return self.train_data[self.train_call]

        elif type is 'test':
            if self.test_data is not None:
                if self.test_call == self.test_size - 1:
                    self.test_call = 0
                elif from_start:
                    self.test_call = 0
                else:
                    self.test_call += 1

                if self.test_labels is not None:
                    return self.test_data[self.test_call], self.test_labels[self.test_call]
                else:
                    return self.test_data[self.test_call]

    def rand(self, type='train'):
        if type is 'train':
            if self.train_data is not None:

                full = True
                for i3 in range(self.train_size):
                    if self.train_seed_hist[i3] is 0:
                        full = False
                if not full:
                    seed = random.randint(0, self.train_size - 1)
                    while self.train_seed_hist[seed] is 1:
                        seed = seed = random.randint(0, self.train_size - 1)
                    self.train_seed_hist[seed] = 1
                else:
                    self.train_seed_hist = [0 for i in range(self.train_size)]
                    seed = random.randint(0, self.train_size - 1)
                    self.train_seed_hist[seed] = 1

                if self.train_labels is not None:
                    return self.train_data[seed], self.train_labels[seed]
                else:
                    return self.train_data[seed]

        if type is 'test':
            if self.test_data is not None:

                full = True
                for i3 in range(self.test_size):
                    if self.test_seed_hist[i3] is 0:
                        full = False
                if not full:
                    seed = random.randint(0, self.test_size - 1)
                    while self.test_seed_hist[seed] is 1:
                        seed = seed = random.randint(0, self.test_size - 1)
                    self.test_seed_hist[seed] = 1
                else:
                    self.test_seed_hist = [0 for i in range(self.test_size)]
                    seed = random.randint(0, self.test_size - 1)
                    self.test_seed_hist[seed] = 1

                if self.test_labels is not None:
                    return self.test_data[seed], self.test_labels[seed]
                else:
                    return self.test_data[seed]
