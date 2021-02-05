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
        lista_mins = []
        for minimo in picos:
            picomenor = int(data_time_values[i])
            if minimo > picomenor:
                y_min = list_img_col[i] [minimo]
                lista_mins.append((minimo,y_min))
        try:
            minimo_lista_min = min(lista_mins, key = lambda t: t[1])
            sparks_tiempo_n.append(minimo_lista_min[0])
            sparks_intensidad_n.append (minimo_lista_min[1])
        except ValueError:
            minimo_lista_min = min (list_img_col[i][int(data_time_values[i]):])
            minimimo_n = list_img_col[i].index(minimo_lista_min)
            sparks_tiempo_n.append(minimimo_n)
            sparks_intensidad_n.append (minimo_lista_min)
    return sparks_tiempo0, sparks_intensidad0, sparks_tiempo_n, sparks_intensidad_n

# Calcula la amplitud de cada pico como la diferencia entre la intensidad máximo y mínimo 
def sparks_amplitude(cantidad_sparks, maximum_int, minimum_int):
    sparks_amplitud = []
    for sp in range(0, cantidad_sparks):
        if  ('nan' not in maximum_int or 'nan' not in minimum_int):
            sp_amplitud = (maximum_int [sp] - minimum_int [sp])/minimum_int [sp]
            sparks_amplitud.append(sp_amplitud)
        else:
            sparks_amplitud.append('nan')
        return sparks_amplitud


# Cálculo del tiempo al pico como la diferencia en el tiempo máximo y mínimo para toda la selección
def time_to_peak (cantidad_sparks, maximum_time, minimum_time):
    sparks_tiempo_al_pico = []
    for sp in range  (0, cantidad_sparks):
        if  ('nan' not in maximum_time or 'nan' not in minimum_time):    
            sp_ttp = maximum_time[sp] - minimum_time [sp]
            sparks_tiempo_al_pico.append(sp_ttp)
        else:
            sparks_tiempo_al_pico.append('nan')
    return sparks_tiempo_al_pico

def fitExponent(tList,yList,ySS=0):
    try:
        bList = [log(max(y-ySS,1e-6)) for y in yList]
        (w,residuals,rank,sing_vals) = lstsq(matrix([[1,t] for t in tList]),matrix(bList).T)
        tau = -1.0/w[1,0]
        amplitude = exp(w[0,0])
        return (amplitude,tau)
    
    except ValueError:
        return ('nan','nan')
    

# Calcula el tiempo al 50% del pico de cada pico de la selección y el calculo del FDHM
def sparks_ttpeak50 (cantidad_sparks, list_img_col, maximum_int, minimum_int, maximum_time, minimum_time):
    sparks_tiempo_pico50 = []
    for sp in range  (0, cantidad_sparks):
        if  ('nan' not in maximum_time or 'nan' not in minimum_time): 
            sp_amp50 = (maximum_int [sp] + minimum_int [sp])/2   
            x1 = np.asarray (range (int(minimum_time [sp]), int(maximum_time [sp]+1))) 
            y1 = np.asarray (list_img_col [sp] [int(minimum_time [sp]) : int(maximum_time [sp]+1)])
            ySS = 0
            (amplitudeEst,tauEst) = fitExponent(x1,y1,ySS)
            sp_ttp50 = (np.log((sp_amp50 -ySS)/ amplitudeEst))*(-tauEst)
            sparks_tiempo_pico50.append (sp_ttp50)
        else:
            sparks_tiempo_pico50.append ('nan')
    return sparks_tiempo_pico50            

# Aplico la función para tau a la selección
def tau(cantidad_sparks, list_img_col, maximum_time, minimum_time):
    sp_tau = []
    for sp in range (0, cantidad_sparks):
        x = np.asarray(list (range(int(maximum_time [sp]), int(minimum_time [sp])+1))) #* x_calibracion
        y = np.asarray(list_img_col[sp][int(maximum_time [sp]) : int(minimum_time [sp])+1],dtype=np.float64)
        ySS = 0
        (amplitudeEst,tauEst) = fitExponent(x,y,ySS)
        yEst = amplitudeEst*(exp(-x/tauEst))+ySS
        sp_tau.append (tauEst)
    return sp_tau

##  Calculo fullWidth
def width (list_img_row):
    maxim_row = maximo_spark(list_img_row)
    cantidad_sparks = maxim_row[0]
    datos_tiempos_row = maxim_row[1]
    datos_intensidades_row = maxim_row[2]

    Columns = ['Spark_'+ str(x) for x in range(0, cantidad_sparks)]
    out_sparks_row = pd.DataFrame([datos_tiempos_row.values(),datos_intensidades_row.values()], columns = Columns).T
    out_sparks_row = pd.DataFrame(out_sparks_row.values, columns = ['tiempo_maximo', 'intensidad_maxima'])

    minim_row =  minimo_sparks (cantidad_sparks, list_img_row, datos_tiempos_row)
    out_sparks_row['tiempo_minimo'] = minim_row [0]
    out_sparks_row['intensidad_minima'] = minim_row [1]
    out_sparks_row['tiempo_valle'] = minim_row [2]
    out_sparks_row['intensidad_valle'] = minim_row [3]

    # Calculo del FWHM

    sparks_tiempo_pico50 = []

    for sp in range  (0, cantidad_sparks):
        sp_amp50 = (out_sparks_row['intensidad_maxima'] [sp] + out_sparks_row['intensidad_minima'] [sp])/2   
        x1 = np.asarray (range (int(out_sparks_row['tiempo_minimo'] [sp]), int(out_sparks_row['tiempo_maximo'] [sp]+1))) 
        y1 = np.asarray (list_img_row [sp] [int(out_sparks_row['tiempo_minimo'] [sp]) : int(out_sparks_row['tiempo_maximo'] [sp]+1)])
        ySS = 0
        (amplitudeEst,tauEst) = fitExponent(x1,y1,ySS)
        yEst = amplitudeEst*(exp(-x1/tauEst))+ySS
        sp_ttp50 = (np.log((sp_amp50 -ySS)/ amplitudeEst))*(-tauEst)
        sparks_tiempo_pico50.append (sp_ttp50)

    sparks_tiempo_pico50_2 = []
    for sp in range  (0, cantidad_sparks):
        sp_amp50 = (out_sparks_row['intensidad_maxima'] [sp] + out_sparks_row['intensidad_minima'] [sp])/2
        x2 = np.asarray (range (int(out_sparks_row['tiempo_maximo'] [sp]), int(out_sparks_row['tiempo_valle'] [sp]+1))) 
        y2 = np.asarray (list_img_row [sp] [int(out_sparks_row['tiempo_maximo'] [sp]) : int(out_sparks_row['tiempo_valle'] [sp]+1)])
        (amplitudeEst2,tauEst2) = fitExponent(x2,y2,ySS)  
        yEst2 = amplitudeEst2*(exp(-x2/tauEst2))+ySS
        sp_ttp50_2 = (np.log((sp_amp50 -ySS)/ amplitudeEst2))*(-tauEst2)
        sparks_tiempo_pico50_2.append (sp_ttp50_2)
    out_sparks_row['TTP50'] = sparks_tiempo_pico50 - out_sparks_row['tiempo_minimo']
    full_width = out_sparks_row['tiempo_valle'] - out_sparks_row['tiempo_minimo']
    return full_width, sparks_tiempo_pico50, sparks_tiempo_pico50_2

def analysis_process (list_img_col, list_img_row,x,y,w,h,flag):
    if list_img_col and list_img_row:
        maxim = maximo_spark(list_img_col)
        cantidad_sparks = maxim[0]
        datos_tiempos = maxim[1]
        datos_intensidades = maxim[2]

        Columns = ['Spark_'+ str(x) for x in range(0, cantidad_sparks)]
        out_sparks = pd.DataFrame([datos_tiempos.values(),datos_intensidades.values()], columns = Columns).T
        out_sparks = pd.DataFrame(out_sparks.values, columns = ['tiempo_maximo', 'intensidad_maxima'])

        if 'nan' not in out_sparks['tiempo_maximo']:
            minim = minimo_sparks (cantidad_sparks, list_img_col, out_sparks['tiempo_maximo'])
        else:
            lenth_nan = 'nan'*len(out_sparks['tiempo_maximo'])
            minim = [(lenth_nan),(lenth_nan),(lenth_nan),(lenth_nan)]

        out_sparks['tiempo_minimo'] = minim[0]
        out_sparks['intensidad_minima'] = minim[1]
        out_sparks['tiempo_valle'] = minim[2]
        out_sparks['intensidad_valle'] = minim[3]

        print(out_sparks)
        sparks_amplitud = sparks_amplitude(cantidad_sparks, out_sparks['intensidad_maxima'], out_sparks['intensidad_minima'])
        out_sparks['amplitud'] = sparks_amplitud

        sparks_tiempo_al_pico = time_to_peak (cantidad_sparks, out_sparks['tiempo_maximo'], out_sparks['tiempo_minimo'])
        out_sparks['TTP'] = sparks_tiempo_al_pico

        sparks_tiempo_pico50 = sparks_ttpeak50 (cantidad_sparks, list_img_col, out_sparks['intensidad_maxima'], out_sparks['intensidad_minima'], out_sparks['tiempo_maximo'], out_sparks['tiempo_minimo'])
        out_sparks['TTP50'] = sparks_tiempo_pico50 - out_sparks['tiempo_minimo']

        sparks_tiempo_pico50_2 = sparks_ttpeak50 (cantidad_sparks, list_img_col, out_sparks['intensidad_maxima'], out_sparks['intensidad_valle'], out_sparks['tiempo_maximo'], out_sparks['tiempo_valle'])
        out_sparks['FDHM'] =[A - B for (A, B) in zip(sparks_tiempo_pico50_2, sparks_tiempo_pico50)]

        sp_tau = tau(cantidad_sparks, list_img_col,  out_sparks['tiempo_maximo'], out_sparks['tiempo_valle'])
        out_sparks['tau'] = sp_tau

        out_sparks['(ΔF/F0)/ΔTmax'] = out_sparks['amplitud']/out_sparks['TTP']

        out_sparks['fullDuration'] = out_sparks['tiempo_valle'] - out_sparks['tiempo_minimo']

        full_width = width (list_img_row)[0]
        sparks_tiempo_pico50 = width (list_img_row)[1]
        sparks_tiempo_pico50_2 = width (list_img_row)[2]
        out_sparks['fullWidth'] = full_width
        out_sparks['FWHM'] =[A - B for (A, B) in zip(sparks_tiempo_pico50_2, sparks_tiempo_pico50)]
        out_sparks['pos_x'] = x
        out_sparks['pos_y'] = y
        out_sparks['width'] = w
        out_sparks['high'] = h
        out_sparks['flag'] = flag
        return out_sparks
    else:
        print ('not possible analysis')