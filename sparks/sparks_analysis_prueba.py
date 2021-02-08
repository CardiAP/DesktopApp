import numpy as np                # funciones numéricas (arrays, matrices, etc.)
import pandas as pd
import  csv
# import scipy.stats
#     '''This function finds a tList in sec yList - measurements ySS - the steady state value of y returns amplitude of exponent tau - the time constant'''
from math import log
from scipy.linalg import lstsq
from scipy import matrix
from scipy import exp

def maximo_peak (vector):
    try:
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
    except:
        return 'nan','nan'


def maximo_spark(lista_ydatas):
    picos = maximo_peak (lista_ydatas)
    datos_tiempos = picos [0]
    datos_intensidades = picos [1]
    return datos_tiempos, datos_intensidades


#  Detección de mínimos locales
# Calculate the n-th discrete difference along the given axis. The first difference is given by out[i] = a[i+1] - a[i] along the given axis, higher differences are calculated by using diff recursively.
# The sign function returns -1 if x < 0, 0 if x==0, 1 if x > 0. nan is returned for nan inputs.

def minimo_bl (vector):
    data = np.asarray(vector,dtype=np.int)
    b = (np.diff(np.sign(np.diff(data))) > 0).nonzero()[0] + 1
    return b

# Esta función calcula los mínimos de la selección de toda la célula tomando los mínimos calculados, quedandose con el más chico entre dos máximos.
# Devuelve el valor de tiempos y las intensidades en dataframes por separado.
def minimo_sparks (list_img_col, data_time_values):

    picos = minimo_bl (list_img_col)
    lista_min = []
    for minimo in picos:
        picomenor = int(data_time_values)
        if minimo < picomenor:
            y_min = list_img_col[minimo]
            lista_min.append((minimo,y_min))
    try:
        minimo_lista_mins = min(lista_min, key = lambda t: t[1])
        sparks_tiempo0 = minimo_lista_mins[0]
        sparks_intensidad0 = minimo_lista_mins[1]
    except ValueError:
        sparks_intensidad0 = min (list_img_col[0:int(data_time_values)])
        sparks_tiempo0 = list_img_col.index(sparks_intensidad0)


    # final minimun

    picos = minimo_bl (list_img_col)
    lista_mins = []
    for minimo in picos:
        picomenor = int(data_time_values)
        if minimo > picomenor:
            y_min = list_img_col [minimo]
            lista_mins.append((minimo,y_min))
    try:
        minimo_lista_min = min(lista_mins, key = lambda t: t[1])
        sparks_tiempo_n = minimo_lista_min[0]
        sparks_intensidad_n = minimo_lista_min[1]
    except ValueError:
        sparks_intensidad_n = min (list_img_col[int(data_time_values):])
        sparks_tiempo_n = list_img_col.index(sparks_intensidad_n)
    return sparks_tiempo0, sparks_intensidad0, sparks_tiempo_n, sparks_intensidad_n

# Calcula la amplitud de cada pico como la diferencia entre la intensidad máximo y mínimo 
def sparks_amplitude(maximum_int, minimum_int):
    sparks_amplitud = (maximum_int - minimum_int)/minimum_int
    return sparks_amplitud


# Cálculo del tiempo al pico como la diferencia en el tiempo máximo y mínimo para toda la selección
def time_to_peak (maximum_time, minimum_time):
    sparks_tiempo_al_pico = maximum_time - minimum_time
    return sparks_tiempo_al_pico

def fitExponent(tList,yList,ySS=0):
    try:
        bList = [log(max(y-ySS,1e-6)) for y in yList]
        (w,residuals,rank,sing_vals) = lstsq(matrix([[1,t] for t in tList]),matrix(bList).T)
        tau = -1.0/w[1,0]
        amplitude = exp(w[0,0])
        return (amplitude,tau)
    except ValueError:
        return('nan','nan')

# Calcula el tiempo al 50% del pico de cada pico de la selección y el calculo del FDHM
def sparks_ttpeak50 (list_img_col, maximum_int, minimum_int, maximum_time, minimum_time):
    sp_amp50 = (maximum_int + minimum_int)/2   
    x1 = np.asarray (range (int(minimum_time), int(maximum_time + 1))) 
    y1 = np.asarray (list_img_col [int(minimum_time) : int(maximum_time+1)])
    ySS = 0
    (amplitudeEst,tauEst) = fitExponent(x1,y1,ySS)
    if tauEst == 'nan':
        sparks_tiempo_pico50 = 'nan'
    else:
        sparks_tiempo_pico50 = (np.log((sp_amp50 -ySS)/ amplitudeEst))*(-tauEst)
    return sparks_tiempo_pico50            

# Aplico la función para tau a la selección
def tau(list_img_col, maximum_time, minimum_time):
    x = np.asarray(list (range(int(maximum_time), int(minimum_time)+1))) #* x_calibracion
    y = np.asarray(list_img_col[int(maximum_time) : int(minimum_time)+1],dtype=np.float64)
    ySS = 0
    (amplitudeEst,tauEst) = fitExponent(x,y,ySS)
    if tauEst == 'nan':
        sp_tau = 'nan'
    else:
        yEst = amplitudeEst*(exp(-x/tauEst))+ySS
        sp_tau = (tauEst)
    return sp_tau

##  Calculo fullWidth
def width (list_img_row):
    max_tiempos_row, max_intensidades_row = maximo_spark(list_img_row)
    minim_row =  minimo_sparks (list_img_row, max_tiempos_row)

    # Calculo del FWHM

    sparks_tiempo_pico50 = []
    sp_amp50 = (max_intensidades_row + minim_row [1])/2   
    x1 = np.asarray (range (int(minim_row [0]), int(max_tiempos_row+1))) 
    y1 = np.asarray (list_img_row [int(minim_row [0]) : int(max_tiempos_row +1)])
    ySS = 0
    (amplitudeEst,tauEst) = fitExponent(x1,y1,ySS)
    if tauEst == 'nan':
        sparks_tiempo_pico50.append (tauEst)
    else:
        yEst = amplitudeEst*(exp(-x1/tauEst))+ySS
        sp_ttp50 = (np.log((sp_amp50 -ySS)/ amplitudeEst))*(-tauEst)
        sparks_tiempo_pico50.append (sp_ttp50)

    sparks_tiempo_pico50_2 = []

    sp_amp50 = (max_intensidades_row + minim_row [1])/2
    x2 = np.asarray (range (int(max_tiempos_row), int(minim_row [2] +1))) 
    y2 = np.asarray (list_img_row [int(max_tiempos_row) : int(minim_row [2] +1)])
    (amplitudeEst2,tauEst2) = fitExponent(x2,y2,ySS)
    if tauEst2 == 'nan':
        sparks_tiempo_pico50_2.append (tauEst2)
    else:    
        yEst2 = amplitudeEst2*(exp(-x2/tauEst2))+ySS
        sp_ttp50_2 = (np.log((sp_amp50 -ySS)/ amplitudeEst2))*(-tauEst2)
        sparks_tiempo_pico50_2.append (sp_ttp50_2)
    full_width = minim_row [2] - minim_row [0]
    return full_width, sparks_tiempo_pico50, sparks_tiempo_pico50_2

def analysis_process (list_img_col, list_img_row,x,y,w,h,flag):
    if list_img_col and list_img_row:
        maxim = maximo_spark(list_img_col)
        datos_tiempos = maxim[0]
        datos_intensidades = maxim[1]
    
        out_data = {}

        out_data['tiempo_maximo'] = datos_tiempos
        out_data['intensidad_maxima'] = datos_intensidades

        if datos_tiempos != 'nan':
            minim = minimo_sparks (list_img_col, datos_tiempos)
            sparks_amplitud = sparks_amplitude(datos_intensidades, minim[1])
            sparks_tiempo_al_pico = time_to_peak (datos_tiempos, minim[0])
            sparks_tiempo_pico50 = sparks_ttpeak50 (list_img_col, datos_intensidades, minim[1], datos_tiempos, minim[0])
            sp_tau = tau(list_img_col,  datos_tiempos, minim[2])
            full_width = width (list_img_row)[0]

            out_data['tiempo_minimo'] = minimo_sparks (list_img_col, datos_tiempos)[0]
            out_data['intensidad_minima'] = minimo_sparks (list_img_col, datos_tiempos)[1]
            out_data['tiempo_valle'] = minimo_sparks (list_img_col, datos_tiempos)[2]
            out_data['intensidad_valle'] = minimo_sparks (list_img_col, datos_tiempos)[3]
            out_data['sparks_amplitud'] = sparks_amplitude(datos_intensidades, minim[1])
            out_data['TTP'] = time_to_peak (datos_tiempos, minim[0])
            out_data['sparks_tiempo_pico50'] = sparks_ttpeak50 (list_img_col, datos_intensidades, minim[1], datos_tiempos, minim[0])
            out_data['sparks_tiempo_pico50_2'] = sparks_ttpeak50 (list_img_col, datos_intensidades, minim[3], datos_tiempos, minim[2])
            out_data['sp_tau'] = tau(list_img_col,  datos_tiempos, minim[2])
            out_data['full_width'] = width (list_img_row)[0]
       
        else:
            out_data['minim'] = 'nan'
            out_data['sparks_amplitud'] = 'nan'
            out_data['TTP'] = 'nan'
            out_data['sparks_tiempo_pico50'] = 'nan'
            out_data['sparks_tiempo_pico50_2'] = 'nan'
            out_data['sp_tau'] = 'nan'
            out_data['full_width'] = 'nan'

        print(type(out_data['sparks_tiempo_pico50_2']), out_data['sparks_tiempo_pico50_2'])
        try:
            out_data['TTP50'] = sparks_tiempo_pico50 - out_data['tiempo_minimo']
        except:
            out_data['TTP50'] = 'nan'
        try:
            out_data['FDHM'] = [A - B for (A, B) in zip(out_data['sparks_tiempo_pico50_2'], sparks_tiempo_pico50)]
        except:
            out_data['FDHM'] = 'nan'

        out_data['fullWidth'] = full_width
        try:
            out_data['(ΔF/F0)/ΔTmax'] = out_data['sparks_amplitud']/out_data['TTP']
        except:
            out_data['(ΔF/F0)/ΔTmax'] = 'nan'
        try:
            out_data['fullDuration'] = out_data['tiempo_valle'] - out_data['tiempo_minimo']
        except:
            out_data['fullDuration'] = 'nan'
        try:
            out_data['FWHM'] = [A - B for (A, B) in zip(width (list_img_row)[2], width (list_img_row)[1])]
        except TypeError:
            out_data['FWHM'] = 'nan'
        out_data['pos_x'] = x
        out_data['pos_y'] = y
        out_data['width'] = w
        out_data['high'] = h
        out_data['flag'] = flag
        
        out_sparks = pd.DataFrame([out_data], columns=out_data.keys())
        
        return out_sparks
    else:
        print ('not possible analysis')