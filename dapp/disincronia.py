from PIL import Image  # funciones para cargar y manipular imágenes
import numpy as np  # funciones numéricas (arrays, matrices, etc.)
import matplotlib.pyplot as plt  # funciones para representación gráfica

from dapp.image import GreyScaleImage
% matplotlib
inline
import cv2
from matplotlib.pyplot import subplots
from numpy import linspace
from scipy import interpolate
from scipy.signal import argrelextrema
import pandas as pd
from pylab import lstsq
from pylab import matrix
from pylab import exp
from math import log
import random
import csv

def analisis_calcio(path, nombre_foto, cantidad_picos, x_calibracion, min_dist_between_maxs, ancho_corte=5):

    image = GreyScaleImage(path + nombre_foto + ".tif")

    # Select ROI
    fromCenter = False
    showCrosshair = False
    seleted_parameters = cv2.selectROI(image, fromCenter, showCrosshair)

    # Crop image
    x_start = int(seleted_parameters[1])
    x_end = x_start + int(seleted_parameters[3])
    y_start = int(seleted_parameters[0])
    y_end = y_start + int(seleted_parameters[2])

    image.crop_vertical(x_start, x_end)
    image.crop_horizontal(y_start, y_end)
    image.smooth()

    raw_data = image.get_raw_data()
    raw_data = raw_data.split_vertically_by(ancho_corte)
    raw_data.sum_columns()

    peaks_detector = raw_data.get_peaks_detector()

    # Calcula la amplitud de cada pico como la diferencia entre la intensidad máximo y mínimo
    amplitudes = pd.DataFrame()
    for peak in range(0, cantidad_picos):
        amp = intensidades_maximas['Pico_' + str(peak)] - intensidades_minimos['Pico_' + str(peak)]
        amplitudes['Pico_' + str(peak)] = amp

    # Cálculo del tiempo al pico como la diferencia en el tiempo máximo y mínimo

    tiempo_al_pico = pd.DataFrame()
    for peak in range(0, cantidad_picos):
        ttp = tiempos_maximos['Pico_' + str(peak)] - tiempos_minimos['Pico_' + str(peak)]
        tiempo_al_pico['Pico_' + str(peak)] = ttp

    tiempo_al_pico.to_csv(path + 'tiempo_al_pico_' + nombre_foto + '.csv')

    # Calcula el tiempo al 50% del pico de cada pico como la diferencia entre la intensidad máximo y mínimo
    # Lo intenté buscando el valor más cercano a la mitad pero veo que me da valores negativos cuando comparo ese valor comparado con el mínimo
    # Tal vez se debería probar fittear la subida para obtener el valor de la mitad a la subida.

    tiempo_50pico = pd.DataFrame()
    for peak in range(0, cantidad_picos):
        amp50 = (intensidades_maximas['Pico_' + str(peak)] + intensidades_minimos['Pico_' + str(peak)]) / 2
        amp50 = list(amp50.astype(np.int))
        lista_ttp50 = []
        for i in range(0, len(amp50)):
            lista_up = np.asarray(
                list_img_row[i][tiempos_minimos['Pico_' + str(peak)][i]: tiempos_maximos['Pico_' + str(peak)][i]])
            ttp50 = (np.abs(lista_up - amp50[i])).argmin()
            lista_ttp50.append(ttp50)
        tiempo_50pico['Pico_' + str(peak)] = lista_ttp50

    #     '''This function finds a tList in sec yList - measurements ySS - the steady state value of y returns amplitude of exponent tau - the time constant'''

    def fitExponent(tList, yList, ySS=0):
        bList = [log(max(y - ySS, 1e-6)) for y in yList]
        (w, residuals, rank, sing_vals) = lstsq(matrix([[1, t] for t in tList]), matrix(bList).T)
        tau = -1.0 / w[1, 0]
        amplitude = exp(w[0, 0])
        return (amplitude, tau)

    lista_tau = []
    for img_row_sum in list_img_row:
        tau_frame = []
        for peak in range(0, cantidad_picos - 1):
            x = (x_data[tiempos_maximos['Pico_' + str(peak)][0] + 5:tiempos_minimos['Pico_' + str(peak + 1)][
                0]]) * x_calibracion
            tau = 88
            amplitude = 2600
            ySS = 3
            y = np.asarray(
                img_row_sum[tiempos_maximos['Pico_' + str(peak)][0] + 5:tiempos_minimos['Pico_' + str(peak + 1)][0]],
                dtype=np.float64)
            yMeasured = [y + random.normalvariate(0, 0.05) for y in y]
            (amplitudeEst, tauEst) = fitExponent(x, yMeasured, ySS)
            yEst = amplitudeEst * (exp(-x / tauEst)) + ySS
            tau_frame.append(tauEst)
        for peak in range(cantidad_picos - 1):
            tauEst = 'NaN'
            tau_frame.append(tauEst)
        lista_tau.append(tau_frame)

    Columns = ['Pico_' + str(x) for x in range(0, len(tau_frame))]
    taus = pd.DataFrame(lista_tau, columns=Columns)

    # Relación entre la amplitud del pico2 sobre el pico1

    amplitudes_ratio = pd.DataFrame()
    for ratio in range(0, cantidad_picos - 1):
        amp_ratio = amplitudes['Pico_' + str(ratio + 1)] / amplitudes['Pico_' + str(ratio)]
        amplitudes_ratio['Pico_' + str(ratio + 1) + '/Pico_' + str(ratio)] = amp_ratio
    for ratio in range(cantidad_picos - 1):
        amplitudes_ratio[''] = 'NaN'

    tmax_values = tiempos_maximos.values
    tmin_values = tiempos_minimos.values
    int_max_values = intensidades_maximas.values
    int_min_values = intensidades_minimos.values
    amp_values = amplitudes.values
    ratio_amp_values = amplitudes_ratio.values
    tpic_values = tiempo_al_pico.values
    t50pic_values = tiempo_50pico.values
    taus_values = taus.values

    # En esta celda se arma una matriz que tiene por cada feta que se tomo de la imagen,
    # los picos que se midieron en esa feta y para cada pico, un conjunto de metricas
    # que se midieron en celdas anteriores

    feta_por_picos = []
    for index in range(len(tmax_values)):
        # TODO: taus_feta metricas tenia 5 picos en lugar de 6
        # así que se agregó una columna con valores nan
        tmax_feta = tmax_values[index] * x_calibracion
        tmin_feta = tmin_values[index] * x_calibracion
        int_max_feta = int_max_values[index]
        int_min_feta = int_min_values[index]
        amp_feta = amp_values[index]
        ratio_amp_feta = ratio_amp_values[index]
        tpic_feta = tpic_values[index] * x_calibracion
        t50pic_feta = t50pic_values[index] * x_calibracion
        taus_feta = taus_values[index]

        pico_por_mmetricas = []
        for index in range(len(tmax_feta)):
            pico_por_mmetricas.append([
                tmax_feta[index],
                tmin_feta[index],
                int_max_feta[index],
                int_min_feta[index],
                amp_feta[index],
                ratio_amp_feta[index],
                tpic_feta[index],
                t50pic_feta[index],
                taus_feta[index]
            ])

        feta_por_picos.append(pico_por_mmetricas)

    with open(path + 'Tabla_general' + nombre_foto + '.txt', "w") as f:
        wr = csv.writer(f)
        wr.writerows(feta_por_picos)