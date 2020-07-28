import numpy as np                # funciones numéricas (arrays, matrices, etc.)
import pandas as pd
import  csv
# import scipy.stats
#     '''This function finds a tList in sec yList - measurements ySS - the steady state value of y returns amplitude of exponent tau - the time constant'''
from math import log
from pylab import lstsq
from pylab import matrix
from pylab import exp

def maximo_peak (vector):
    import numpy as np
    from peakutils.peak import indexes
    import peakutils
    indexes = indexes(np.array(vector), thres=1.0/max(vector), min_dist=10)
    kk = list(indexes)
    for j in kk:
        if vector[j]> (sum(vector) / len(vector)):
            tiempos = j
            intensidades = vector[j]
    return tiempos,intensidades

def maximo_spark(lista_ydatas):
    cantidad_sparks = len(lista_ydatas)
    datos_tiempos = {}
    datos_intensidades = {}
    for i in range (0,cantidad_sparks):
        picos = maximo_peak (lista_ydatas[i])
        datos_tiempos [i] = picos [0]
        datos_intensidades [i] = picos [1]
    return cantidad_sparks, datos_tiempos, datos_intensidades
#  Detección de mínimos locales
# Calculate the n-th discrete difference along the given axis. The first difference is given by out[i] = a[i+1] - a[i] along the given axis, higher differences are calculated by using diff recursively.
# The sign function returns -1 if x < 0, 0 if x==0, 1 if x > 0. nan is returned for nan inputs.

def minimo_bl (vector):
    data = np.asarray(vector,dtype=np.int)
    b = (np.diff(np.sign(np.diff(data))) > 0).nonzero()[0] + 1
    return b
# Esta función calcula los mínimos de la selección de toda la célula tomando los mínimos calculados, quedandose con el más chico entre dos máximos.
# Devuelve el valor de tiempos y las intensidades en dataframes por separado.
def minimo_sparks (cantidad_sparks, list_img_col, data_time_values):
    sparks_tiempo0 = []
    sparks_intensidad0 = []        
    sparks_tiempo_n = []
    sparks_intensidad_n = []

    for i in range (0,cantidad_sparks):
        picos = minimo_bl (list_img_col[i])
        lista_min = []
        for minimo in picos:
            picomenor = int(data_time_values[i])
            if minimo < picomenor:
                y_min = list_img_col[i] [minimo]
                lista_min.append((minimo,y_min))
        try:
            minimo_lista_mins = min(lista_min, key = lambda t: t[1])
            sparks_tiempo0.append(minimo_lista_mins[0])
            sparks_intensidad0.append (minimo_lista_mins[1])
        except ValueError:
            minimo_lista_mins = min (list_img_col[i][0:int(data_time_values[i])])
            minimimo = list_img_col[i].index(minimo_lista_mins)
            sparks_tiempo0.append(minimimo)
            sparks_intensidad0.append (minimo_lista_mins)

    # final minimun

    for i in range (0,cantidad_sparks):
        picos = minimo_bl (list_img_col[i])
        lista_min = []
        for minimo in picos:
            picomenor = int(data_time_values[i])
            if minimo > picomenor:
                y_min = list_img_col[i] [minimo]
                lista_min.append((minimo,y_min))
        try:
            minimo_lista_mins = min(lista_min, key = lambda t: t[1])
            sparks_tiempo_n.append(minimo_lista_mins[0])
            sparks_intensidad_n.append (minimo_lista_mins[1])
        except ValueError:
            minimo_lista_mins = min (list_img_col[i][int(data_time_values[i]):len (list_img_col[i])])
            minimimo = list_img_col[i].index(minimo_lista_mins)
            sparks_tiempo_n.append(minimimo)
            sparks_intensidad_n.append (minimo_lista_mins)
    return sparks_tiempo0, sparks_intensidad0, sparks_tiempo_n, sparks_intensidad_n


# Calcula la amplitud de cada pico como la diferencia entre la intensidad máximo y mínimo 
def sparks_amplitude(cantidad_sparks, maximum_int, minimum_int):
    sparks_amplitud = []
    for sp in range(0, cantidad_sparks):
        sp_amplitud = (maximum_int [sp] - minimum_int [sp])/minimum_int [sp]
        sparks_amplitud.append(sp_amplitud)
    return sparks_amplitud

# Cálculo del tiempo al pico como la diferencia en el tiempo máximo y mínimo para toda la selección
def time_to_peak (cantidad_sparks, maximum_time, minimum_time):
    sparks_tiempo_al_pico = []
    for sp in range  (0, cantidad_sparks):
        sp_ttp = maximum_time[sp] - minimum_time [sp]
        sparks_tiempo_al_pico.append(sp_ttp)
    return sparks_tiempo_al_pico
#Acá me quedé
# Calcula el tiempo al 50% del pico de cada pico de la selección
def sparks_tiempo_pico50 ():
    sparks_tiempo_pico50 = []
    for sp in range  (0, cantidad_sparks):
        sp_amp50 = (out_sparks['intensidad_maxima'] [sp] + out_sparks['intensidad_minima'] [sp])/2   
        x1 = np.asarray (range (int(out_sparks['tiempo_minimo'] [sp]), int(out_sparks['tiempo_maximo'] [sp]+1))) 
        y1 = np.asarray (list_img_col [sp] [int(out_sparks['tiempo_minimo'] [sp]) : int(out_sparks['tiempo_maximo'] [sp]+1)])
        ySS = 0
        (amplitudeEst,tauEst) = fitExponent(x1,y1,ySS)
        yEst = amplitudeEst*(exp(-x1/tauEst))+ySS
        sp_ttp50 = (np.log((sp_amp50 -ySS)/ amplitudeEst))*(-tauEst)
        sparks_tiempo_pico50.append (sp_ttp50)

# Calculo del FDHM
def sparks_tiempo_pico50_2 ():
    sparks_tiempo_pico50_2 = []
    for sp in range  (0, cantidad_sparks):
        sp_amp50 = (out_sparks['intensidad_maxima'] [sp] + out_sparks['intensidad_minima'] [sp])/2
        x2 = np.asarray (range (int(out_sparks['tiempo_maximo'] [sp]), int(out_sparks['tiempo_valle'] [sp]+1))) 
        y2 = np.asarray (list_img_col [sp] [int(out_sparks['tiempo_maximo'] [sp]) : int(out_sparks['tiempo_valle'] [sp]+1)])
        (amplitudeEst2,tauEst2) = fitExponent(x2,y2,ySS)  
        yEst2 = amplitudeEst2*(exp(-x2/tauEst2))+ySS
        sp_ttp50_2 = (np.log((sp_amp50 -ySS)/ amplitudeEst2))*(-tauEst2)
        sparks_tiempo_pico50_2.append (sp_ttp50_2)

def fitExponent(tList,yList,ySS=0):
    bList = [log(max(y-ySS,1e-6)) for y in yList]
    (w,residuals,rank,sing_vals) = lstsq(matrix([[1,t] for t in tList]),matrix(bList).T)
    tau = -1.0/w[1,0]
    amplitude = exp(w[0,0])
    return (amplitude,tau)