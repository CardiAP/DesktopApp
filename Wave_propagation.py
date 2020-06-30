{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 55,
   "metadata": {},
   "outputs": [],
   "source": [
    "path = 'C:/Users/Leand/OneDrive/Documentos/Lean/Analizador_imagenes_calcio/Imagenes_confocal/Rata/C071112/'\n",
    "nombre_foto = 'c3ack000'\n",
    "x_calibracion = 4.5\n",
    "ancho_corte = 3"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "metadata": {},
   "outputs": [
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "How many peaks do you want to analyse? 1\n"
     ]
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "from PIL import Image             # funciones para cargar y manipular imágenes\n",
    "import numpy as np                # funciones numéricas (arrays, matrices, etc.)\n",
    "import matplotlib.pyplot as plt   # funciones para representación gráfica\n",
    "%matplotlib inline\n",
    "import cv2\n",
    "from matplotlib.pyplot import subplots\n",
    "from numpy import linspace\n",
    "from scipy import interpolate\n",
    "from scipy.signal import argrelextrema\n",
    "import pandas as pd\n",
    "from pylab import lstsq\n",
    "from pylab import matrix\n",
    "from pylab import exp\n",
    "from math import log\n",
    "import random\n",
    "import  csv\n",
    "\n",
    "\n",
    "if __name__ == '__main__' :\n",
    "# Read image\n",
    "    imag = cv2.imread(path + nombre_foto + \".tif\")\n",
    "\n",
    "    if imag is None:\n",
    "        print(\"Check file path\")\n",
    "    else:\n",
    "        cv2.imshow ('image', imag)\n",
    "        cv2.waitKey(0)\n",
    "        cv2.destroyAllWindows()\n",
    "        cantidad_picos = int(input ('How many peaks do you want to analyse?'))\n",
    "\n",
    "    if cantidad_picos == 0:\n",
    "        pass\n",
    "    else:\n",
    "        # Select ROI\n",
    "        fromCenter = False\n",
    "        showCrosshair = False\n",
    "        r = cv2.selectROI(imag, fromCenter, showCrosshair)\n",
    "\n",
    "        # Crop image\n",
    "        imCrop = imag[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]\n",
    "        up = int(r[1])\n",
    "        down = int(r[1]+r[3])\n",
    "        left = int(r[0])\n",
    "        right = int(r[0]+r[2])\n",
    "\n",
    "#########################\n",
    "#- Creating a log file -#\n",
    "log_path = path + 'logfile.txt'\n",
    "\n",
    "with open(log_path, 'a') as my_file:\n",
    "    my_file.write('selected area pict: '+ nombre_foto + '\\n' +'up: ' + str(up) + '\\n'+'down: ' + str(down) + '\\n'+'left: ' + str(left) + '\\n'+'right: ' + str(right) + '\\n')\n",
    "\n",
    "# Display cropped image\n",
    "cv2.imshow(\"Image\", imCrop)\n",
    "cv2.waitKey(0)\n",
    "cv2.destroyAllWindows()\n",
    "\n",
    "\n",
    "################################\n",
    "### PREPARACIÓN DE LA IMAGEN ###\n",
    "################################\n",
    "\n",
    "I = Image.open(path + nombre_foto + \".tif\")\n",
    "a=np.asarray(I,dtype=np.float32)  # convierte el objeto I en una matriz de tipo float32\n",
    "Image.fromarray(a.astype(np.uint8)).save(\"prueba.jpg\")  # primero convierte \"a\" a uint8, y luego a un objeto \"imagen\"\n",
    "\n",
    "\n",
    "######################################################################################################\n",
    "###HACE CORTES DE LA IMAGEN CADA INTERVALOS DE PIXELES Y LUEGO HACE UN HISTOGRAMA DE CADA INTERVALO###\n",
    "######################################################################################################\n",
    "\n",
    "## Genera una imagen en escala de grises con la que se trabaja\n",
    "\n",
    "#             plt.figure()\n",
    "#             plt.subplot(121)\n",
    "#             plt.imshow(a,cmap='gray',interpolation='nearest')\n",
    "#             plt.title('Imagen') \n",
    "a = cv2.bilateralFilter(a,20,300,300)\n",
    "\n",
    "## Corta en porciones la imagen haciendo un histograma de cada una\n",
    "x_data = np.asarray(range(up,down),dtype=np.float64)\n",
    "list_img_row = []\n",
    "\n",
    "whole_cell_SI = Image.fromarray(a[up:down, left:right].astype(np.uint8))\n",
    "whole_cell_data = np.sum(whole_cell_SI,axis=1).tolist()\n",
    "for i in range (left, right, ancho_corte):\n",
    "    #recorte de la imagen en los límites del objeto\n",
    "    seleccion=a[up:down,i:i + ancho_corte]\n",
    "    #análisis de cada franja\n",
    "    SI = Image.fromarray(seleccion.astype(np.uint8))\n",
    "    img_row_sum = np.sum(SI,axis=1).tolist() #lista de datos del histograma\n",
    "    list_img_row.append (img_row_sum)\n",
    "#gráfico de cada franja\n",
    "#             plt.subplot(122)\n",
    "#             plt.imshow(seleccion,cmap='gray',interpolation='nearest')\n",
    "#             plt.title('Subframe') \n",
    "#             plt.show()\n",
    "#gráfico de histograma\n",
    "plt.plot(img_row_sum)\n",
    "plt.title(nombre_foto)\n",
    "plt.xlabel(\"time\")\n",
    "plt.ylabel(\"Intensity\")\n",
    "plt.savefig('img_row_sum')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "metadata": {},
   "outputs": [
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Time between peaks? 400\n"
     ]
    }
   ],
   "source": [
    "# Función que da la posición de los picos máximos\n",
    "\n",
    "min_distancia = input ('Time between peaks?')\n",
    "def maximo_peak (vector):\n",
    "    import numpy as np\n",
    "    from peakutils.peak import indexes\n",
    "    import peakutils\n",
    "    indexes = indexes(np.array(vector), thres=1.0/max(vector), min_dist=min_distancia)\n",
    "    kk = list(indexes)\n",
    "    tiempos = []\n",
    "    intensidades = []\n",
    "    for j in kk:\n",
    "        if vector[j]> (sum(vector) / len(vector)):\n",
    "            tiempos.append (j)\n",
    "            intensidades.append (vector[j])\n",
    "    return tiempos,intensidades\n",
    "\n",
    "# Aplico la función sobre los datos de la célula entera, y devuelve valores de tiempos e intensidades de los máximos\n",
    "\n",
    "\n",
    "whole_cell_picos = maximo_peak (whole_cell_data)\n",
    "whole_cell_tiempos_maximos = whole_cell_picos [0]\n",
    "whole_cell_intensidades_maximos = whole_cell_picos [1]\n",
    "\n",
    "cantidad_total_picos = int (len(whole_cell_picos[0]))                             \n",
    "Columns = ['Transient_'+ str(x) for x in range(0, cantidad_total_picos)]\n",
    "wc = pd.DataFrame([whole_cell_tiempos_maximos,whole_cell_intensidades_maximos], columns = Columns)\n",
    "\n",
    "# Aplico la función sobre los datos, y devuelve valores de tiempos e intensidades de los máximos\n",
    "\n",
    "datos_tiempos = {}\n",
    "datos_intensidades = {}  \n",
    "\n",
    "for i in range (0,len(list_img_row)):\n",
    "\n",
    "    picos = maximo_peak (list_img_row[i])\n",
    "    datos_tiempos [i] = picos [0]\n",
    "    datos_intensidades [i] = picos [1]\n",
    "\n",
    "df_tiempos = pd.DataFrame(list(datos_tiempos.items()),columns = ['Rows','Picos'])\n",
    "df_intensidades = pd.DataFrame(list(datos_intensidades.items()),columns = ['Rows','Picos'])\n",
    "Columns = ['Pico_'+ str(x) for x in range(0, cantidad_total_picos)]\n",
    "tiempos_maximos = pd.DataFrame(df_tiempos.Picos.tolist(), columns=Columns)\n",
    "intensidades_maximas = pd.DataFrame(df_intensidades.Picos.tolist(), columns=Columns)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### MEDIDA DE LA VELOCIDAD DE PROPAGACIÓN DE WAVES"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "-1.5104936457664446 445.19570966794015\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "<matplotlib.collections.PathCollection at 0x18f629e2160>"
      ]
     },
     "execution_count": 59,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "wp = pd.DataFrame()\n",
    "wp ['tiempo']= tiempos_maximos ['Pico_0']\n",
    "wp ['distancia'] = range (0,ancho_corte*len (tiempos_maximos ['Pico_0']),ancho_corte)\n",
    "\n",
    "x = list(wp ['distancia'])\n",
    "y = list(wp ['tiempo'])\n",
    "\n",
    "(m, b) = np.polyfit(x, y, 1)\n",
    "print(m, b)\n",
    "\n",
    "yp = np.polyval([m, b], x)\n",
    "plt.plot(x, yp)\n",
    "plt.grid(True)\n",
    "plt.scatter(x,y)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
