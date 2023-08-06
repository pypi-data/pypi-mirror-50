#!/usr/bin/env python3
# coding: utf-8

import threading

import mmh3
from bitarray import bitarray

from joker.minions import utils


def _bitarray_get(bitarr, idx):
    try:
        return bitarr[idx]
    except IndexError:
        return False


class BloomFilter(object):
    def __init__(self, size, seed=3):
        self.size = size
        self.seed = seed
        self.bitarr = bitarray(size)
        self.bitarr ^= self.bitarr

    def _compute_hash(self, item):
        return mmh3.hash(item, self.seed) % self.size

    def get(self, key):
        idx = self._compute_hash(key)
        return self.bitarr[idx]

    def getset(self, key, value):
        idx = self._compute_hash(key)
        rv = self.bitarr[idx]
        self.bitarr[idx] = bool(value)
        return rv

    def toggle(self, key):
        idx = self._compute_hash(key)
        with threading.Lock():
            rv = not bool(self.bitarr[idx])
            self.bitarr[idx] = rv
            return rv


class BloomMixin(object):
    val_toggle = b'~'

    def __init__(self, size, seed=3):
        self.bloom = BloomFilter(size, seed)

    def lookup(self, key, val):
        if not val:
            rv = self.bloom.get(key)
        elif val == self.val_toggle:
            rv = self.bloom.toggle(key)
        else:
            rv = self.bloom.getset(key, int(val.decode()))
        return b'01'[int(rv)]


class BloomServer(BloomMixin, utils.ServerBase):
    pass


class PipedBloomServer(BloomMixin, utils.PipedServerBase):
    pass
