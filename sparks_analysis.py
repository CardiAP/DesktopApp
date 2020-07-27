import numpy as np                # funciones numéricas (arrays, matrices, etc.)
import pandas as pd
import  csv
#     '''This function finds a tList in sec yList - measurements ySS - the steady state value of y returns amplitude of exponent tau - the time constant'''
from math import log
from pylab import lstsq
from pylab import matrix
from pylab import exp

def fitExponent(tList,yList,ySS=0):
    bList = [log(max(y-ySS,1e-6)) for y in yList]
    (w,residuals,rank,sing_vals) = lstsq(matrix([[1,t] for t in tList]),matrix(bList).T)
    tau = -1.0/w[1,0]
    amplitude = exp(w[0,0])
    return (amplitude,tau)