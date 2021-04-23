from __future__ import division 
import numpy as np
import pandas as pd
import ROOT as R
import root_numpy as rp

def estimate_energy(sizelist, p0 = 0.42, p1 = 0.04):
    '''measure of energy from size of shower, from linear relation p0 + p1 *x'''
    Erec = np.zeros(len(sizelist))
    for index, size in enumerate(sizelist):
        Erec[index]  = p1*size + p0
    return Erec