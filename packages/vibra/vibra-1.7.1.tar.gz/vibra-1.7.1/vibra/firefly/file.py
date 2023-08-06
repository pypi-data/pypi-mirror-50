from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
from tensorflow import keras


class file(object):
    def __init__ (self,src,filename='',encoding='utf-8'):
        self.src=src
        if filename is '':
            self.filename=self.src[:3]
        else:
            self.filename=filename
        self.encing = encoding
        self.file = keras.utils.get_file(self.filename, self.src)
        self.txt = open(self.file, 'rb').read().decode(encoding=self.encing)
        self.chrs = sorted(set(self.txt))
        self.chr2idx={u:i for i, u in enumerate(self.chrs)}
        self.idx2chr=np.array(self.chrs)
        self.txt_as_int = np.array([self.chr2idx[c] for c in self.txt])
        self.length=len(self.txt)
        self.chr_size=len(self.chrs)

    def text(self):
        return (self.txt)

    def chars(self):
        return (self.chrs)

    def char2idx(self):
        return (self.chr2idx)

    def idx2char(self):
        return (self.idx2chr)

    def text_as_int(self):
        return (self.txt_as_int)

    def len(self):
        return (self.length)

    def char_size(self):
        return (self.chr_size)

    def encoding(self):
        return (self.encing)