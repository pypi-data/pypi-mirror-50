from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import os
import time
import tensorflow as tf
from tensorflow import keras
from vibra.firefly import file


class built_in(object):
    def sequence_generation(self,src,src_encoding='utf-8',seq_length=100,batch_size=64,embedding_dim=256,
                            rnn_units=1024,save_model=True):
        self.sg_src=src
        self.sg_seq_length=seq_length
        self.sg_src_encoding=src_encoding
        self.sg_batch_size