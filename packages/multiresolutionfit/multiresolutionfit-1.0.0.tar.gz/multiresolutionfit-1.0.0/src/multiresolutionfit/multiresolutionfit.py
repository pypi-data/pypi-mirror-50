#!/usr/bin/env python3
# -*- Coding: UTF-8 -*-
"""
Multiple Resolution Goodness of Fit.

The thesis of [cuevs2013]_ is that:

    "...there is no one `proper` resolution, but rather a range of
         resolutions is necessary to adequately describe the fit of
         models with reality."

License
-------

Developed by: E. S. Pereira.
e-mail: pereira.somoza@gmail.com

Copyright [2019] [E. S. Pereira]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

References
----------

.. [costanza89] COSTANZA, Robert. Model goodness of fit: a multiple resolution
                 procedure. Ecological modelling, v. 47, n. 3-4,
                 p. 199-215, 1989.

"""
from math import floor, ceil
import time

from numpy import array, exp
from numba import njit, prange, jit, float64, int64, uint8
from numba.typed import Dict
from numba import types

from numpy.random import shuffle
from numpy import unique

from progressbar import  progressbar


class ImageSizeError(Exception):
    def __init__(self, value):
        value = value

    def __str__(self):
        return repr(value)


TYPEF = "float64(int64, int64[:,:], int64[:,:])"
TYPEFW = "float64(int64, int64, int64, int64[:,:], int64[:,:])"


@njit(TYPEF, nogil=True)
def _f(win, window1, window2):
    """
    Count class.
    Return $f = 1 - \frac{\sum_{i=1}^{p}{|a_{1i} -a_{2i}|}}{2w^{2}}$
    """
    unq1 = unique(window1)
    unq2 = unique(window2)

    cnt1 = Dict.empty(key_type=types.int64,
                      value_type=types.int64,
                      )
    cnt2 = Dict.empty(key_type=types.int64,
                      value_type=types.int64,
                      )

    for key in unq1:
        cnt1[key] = (window1 == key).sum()

    for key in unq2:
        cnt2[key] = (window2 == key).sum()

    A = set(cnt1.keys())
    B = set(cnt2.keys())
    common = list(A.intersection(B))
    only_in_A = list(A - B)
    only_in_B = list(B - A)

    aki = 0

    for cl in common:
        aki += abs(cnt1[cl] - cnt2[cl])
    for cl in only_in_A:
        aki += cnt1[cl]
    for cl in only_in_B:
        aki += cnt2[cl]
    f = 1 - aki / (2.0 * win * win)
    return f


@njit(TYPEFW, nogil=True, parallel=True)
def _fw(win, lines, cols, scene1, scene2):
    """
    Parallel comparation of images.
    """
    fw = 0
    for i in prange(lines - win):
        for j in prange(cols - win):
            f = _f(win,
                   scene1[i:i + win, j:j + win],
                   scene2[i:i + win, j:j + win]
                   )
            fw += f
    return fw

def _fwin(win, scene1, scene2, zvalue):
    """
    Fit at a particular sampling window size.
    :parameter int win: window size
    Return:  $F_{w}= \frac{\sum_{s=1}^{t_{w}}{
              \left[ 1 - \frac{\sum_{i=1}^{p}{|a_{1i} -a_{2i}|}}{2w^{2}}
              \right]_{s}}}{t_{w}}$
    """
    if scene1.shape[0] != scene2.shape[0]:
        raise ImageSizeError("The images have diferent number of lines")

    if scene1.shape[1] != scene2.shape[1]:
        raise ImageSizeError("The images have diferent number of columns")

    lines, cols = scene1.shape

    scene1s = scene1.copy()
    if zvalue is True:
        shuffle(scene1s)

    fw = _fw(win, lines, cols, scene1s, scene2)

    n = ((lines - win) * (cols - win))
    if n == 0:
        fw = _f(win, scene1s, scene2)
    else:
        fw = fw / n
    return fw


class Multiresoutionfit:
    r"""
    Multiple Resolution Goodness of Fit.

    :param 2d_array scene1: Gray scale image
    :param 2d_array scene2: Gray scale image
    :param boolean verbose: verbose option default False
    """

    def __init__(self, scene1, scene2, verbose=False):

        if scene1.shape[0] != scene2.shape[0]:
            raise ImageSizeError("The images have diferent number of lines")

        if scene1.shape[1] != scene2.shape[1]:
            raise ImageSizeError("The images have diferent number of columns")

        self._scene1 = scene1
        self._scene2 = scene2
        self._verbose = verbose
        self._zvalue = False

        self._lines, self._cols = self._scene1.shape
        self._golden_ratio = (1.0 + 5.0 ** 0.5) / 2.0
        self._golden_rectangle = None

    @property
    def golden_rectangles(self):
        '''
        Return golden rectangle used to analyse image.
        '''
        return self._golden_rectangle

    def golden_rectangle_generator(self, cl):
        r"""
        Golden rectangle Generator.

        Calculate the Golden Rectangle side that is possible to draw inside the
        image.
        :return int w: side of golden rectangles.
        """
        w = floor(cl / self._golden_ratio)
        i = 1
        was_one = False
        while w > 1:
            if i == 1:
                yield cl
            w = floor(w / self._golden_ratio ** i)

            if w == 1:
                was_one = True
            if w == 0:
                if was_one is False:
                    yield 1
                break
            yield w
            i += 1

    def fwin(self, win):
        '''
        Fit at a particular sampling window size.
        :parameter int win: window size
        Return:  $F_{w}= \frac{\sum_{s=1}^{t_{w}}{
                  \left[ 1 - \frac{\sum_{i=1}^{p}{|a_{1i} -a_{2i}|}}{2w^{2}}
                  \right]_{s}}}{t_{w}}$
        '''
        return _fwin(win, self._scene1, self._scene2, self._zvalue)

    def ft(self, k, wins=None):
        """
        Weight average of the fits over all window sizes.
        :parameter float k: weight range [0,1].
        :parameter list wins:  list of windows size.
        """
        self._print("\n* Calculating Ft *")

        fw = []

        cl = min(self._lines, self._cols)

        if wins is None:
            wins = array(list(self.golden_rectangle_generator(cl)))
            self._golden_rectangle = wins.copy()

        prog = range(len(wins))
        prog = progressbar(prog) if self._verbose is True else prog

        for i in prog:
            fw.append(self.fwin(wins[i]))

        self._print("\n")

        fw = array(fw)
        e = exp(- k * (wins - 1))
        ftot = (fw * e).sum() / e.sum()
        return ftot, fw, wins

    def ft_par(self, k, wins=None, npixels=100):
        """
        Weight average of the fits over all window sizes.
        :parameter float k: weight range [0,1].
        :parameter list wins:  list of windows size.
        """
        if self._lines // npixels <= 1 or self._cols // npixels <= 1:
            return self.ft(k=k, wins=wins)[0]

        self._print("\n* Calculating Ft DC *")

        nlines = self._lines // npixels
        ncols = self._cols // npixels

        imgs1 = [self._scene1[i: i + npixels, j: j + npixels]
                 for i in range(0, self._lines, npixels)
                 for j in range(0, self._cols, npixels)]
        imgs2 = [self._scene2[i: i + npixels, j: j + npixels]
                 for i in range(0, self._lines, npixels)
                 for j in range(0, self._cols, npixels)]

        cl = min(imgs1[0].shape[0], imgs1[0].shape[1])

        if wins is None:
            wins = array(list(self.golden_rectangle_generator(cl)))
            self._golden_rectangle = wins.copy()

        ftot = []
        prog = range(len(imgs1))
        prog = progressbar(prog) if self._verbose is True else  prog
        for wi in prog:
            fw = []
            for win in wins:
                fw.append(_fwin(win, imgs1[wi], imgs2[wi], self._zvalue))
            fw = array(fw)
            e = exp(- k * (wins - 1))
            ftot.append((fw * e).sum() / e.sum())
        self._print("\n")
        ftot = array(ftot)
        return ftot.mean()

    def zvalue(self, k, wins=None, permutations=20, npixels=100):
        """
        z-value.

        :parameter float k: weight range [0,1].
        :parameter list wins:  list of windows size.
        :parameter int permutation: total of permutations.

        Significance guidelines
        -----------------------
         - z > 3: possibly significant
         - z > 6: probably significant
         - z > 10: significant
        """
        frand = []
        print("* Calculating z-value *")
        ft = self.ft_par(k, wins=wins, npixels=npixels)
        self._zvalue = True
        tmp = self._verbose
        self._verbose = False
        print("* Permutations *")
        for i in progressbar(range(1, permutations + 1)):
            frand.append(self.ft_par(k, wins=wins, npixels=npixels))
        self._zvalue = False
        self._verbose = tmp
        print("\n")
        frand = array(frand)
        z = (ft - frand.mean()) / frand.std()
        return z, ft

    def _print(self, text):
        if self._verbose is True:
            print(text)
