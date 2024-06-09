import numpy as np
import matplotlib.pyplot as plt

def calcular_gradiente(porcentaje_agua_objetivo, API_objetivo):
    # Constantes
    porcentaje_agua = np.linspace(0, 100, 100)
    APIs = [10, 15, 20, 25, 30, 35, 40, 45]  
    inicio_fin_rectas = {
        10: [(0, .432), (100, 0.464)],
        15: [(0, .418), (100, 0.464)],
        20: [(0, .405), (100, 0.464)],
        25: [(0, .392), (100, 0.464)],
        30: [(0, .38), (100, 0.464)],
        35: [(0, .368), (100, 0.464)],
        40: [(2.5, .36), (100, 0.464)],
        45: [(11, .36), (100, 0.464)],
    }
    
    # Calcular los gradientes para cada valor de API
    gradients = {API: np.interp(porcentaje_agua, [inicio_fin[0] for inicio_fin in inicio_fin_rectas[API]], [inicio_fin[1] for inicio_fin in inicio_fin_rectas[API]]) for API in APIs}

    # Calcular el gradiente
    if API_objetivo in gradients:
        gradiente = np.interp(porcentaje_agua_objetivo, porcentaje_agua, gradients[API_objetivo])
    else:
        keys = sorted(gradients.keys())
        lower_API = max(filter(lambda x: x < API_objetivo, keys))
        upper_API = min(filter(lambda x: x > API_objetivo, keys))
        lower_grad = np.interp(porcentaje_agua_objetivo, porcentaje_agua, gradients[lower_API])
        upper_grad = np.interp(porcentaje_agua_objetivo, porcentaje_agua, gradients[upper_API])
        gradiente = np.interp(API_objetivo, [lower_API, upper_API], [lower_grad, upper_grad])
    
    return gradiente

from primera import *
from segunda import *
import numpy as np
import matplotlib.pyplot as plt



"""gradiente_mezcla = calcular_gradiente(porcentaje_agua_objetivo, API_objetivo)
print(f"Gradiente en el punto objetivo para API {API_objetivo}: {gradiente_mezcla}")"""

def calcular_niveles(gradiente_mezcla, NMD, Pws, Pwf):
    NE = NMD - Pws / gradiente_mezcla
    ND = NMD - Pwf / gradiente_mezcla
    return NE, ND


def calcular_Gpres(gradiente_presion, Tfondo, Ts, NMD):
    T_chart = (Ts + (70 + 1.6 * (NMD / 100))) / 2
    T_ac = (Ts + Tfondo) / 2
    Gpres = gradiente_presion * ((T_chart + 459.67) / (T_ac + 459.67))
    return Gpres

def calcular_presion_fondo(Ps, NMD, Gpres):
    Presion_fondo = Ps + (NMD * Gpres /1000)
    return Presion_fondo

def calcular_interseccion(recta1, recta2):
    x1, y1, m1 = recta1
    x2, y2, m2 = recta2
    x_interseccion = (y2 - y1 + m1*x1 - m2*x2) / (m1 - m2)
    y_interseccion = y1 + m1 * (x_interseccion - x1)
    return x_interseccion, y_interseccion

def calcular_ecuacion_recta(p1, p2, nombre):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return m, b


def graficar_recta(m, b, nombre, rango_x):
    x_values = np.linspace(rango_x[0], rango_x[1], 100)
    y_values = m * x_values + b
    plt.plot(x_values, y_values, label=nombre)

def calcular_punto(x, recta):
    m, b = recta
    y = m * x + b
    return x, y


