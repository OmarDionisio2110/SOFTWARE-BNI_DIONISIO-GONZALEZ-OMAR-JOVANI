import matplotlib.pyplot as plt
import numpy as np
from primera import *
from segunda import *


porcentaje_agua_objetivo = 0
API_objetivo = 35
Pso = 800 
sg_gas_objetivo = .65
NMD = 8000
Pwf = 2050
Pws = 2500
Ts = 100 
Tfondo = 180  
gradiente_fluido = 0.45  
Pwh = 250


gradiente_mezcla = calcular_gradiente(porcentaje_agua_objetivo, API_objetivo)
#print(f"Gradiente en el punto objetivo para API {API_objetivo}: {gradiente_mezcla}")


NE, ND = calcular_niveles(gradiente_mezcla,NMD,Pws,Pwf)

"""print(f"EL NIVEL ESTATICO ES: {NE}")
print(f"El NIVEL DINAMICO ES: {ND}")"""

gradiente_presion = calcular_seggradiente(Pso, sg_gas_objetivo)
#print(f"Gradiente en el punto objetivo para SGGAS {sg_gas_objetivo}: {gradiente_presion}")

delta_presion = calcular_Gpres(gradiente_presion, Tfondo, Ts, NMD)
Pvo = calcular_presion_fondo(Pso, NMD, delta_presion)

print(Pvo)
"""print("delta_presion:", delta_presion)
print("Presión de fondo:", Pvo)
"""


Pdisp = Pso + 100
Pdisp_NMD = calcular_presion_fondo(Pdisp, NMD, delta_presion)

Pso = (Pso,0)
Pvo = (Pvo, (-1)*NMD)
ND = (0,ND*(-1))
NE = (0,NE*(-1))
Pdisp = (Pdisp, 0)
Pdisp_nmd = (Pdisp_NMD, (-1)*NMD)
Pws = (Pws,(-1)*NMD)
Pwf = (Pwf, (-1)*NMD)
Pwh = (Pwh, 0)
Pwhp = Pwh[0]
Gradf = 0.45
ProfND= ND[1]
Prof = Pvo[1]/2


# Obtener las coordenadas de los puntos que forman la recta Pso-Pvo
x1 = Pso[0]
y1 = Pso[1]
x2 = Pvo[0]
y2 = Pvo[1]
m = (y2 - y1) / (x2 - x1)
b = y1 - m*x1
recta_Pso_Pvo = (m, b)


# Obtener las coordenadas de los puntos que forman la recta RV1
x1 = Pdisp[0]
y1 = Pdisp[1]
x2 = Pdisp_nmd[0]
y2 = Pdisp_nmd[1]
m = (y2 - y1) / (x2 - x1)
b = y1 - m*x1
recta_RV1 = (m, b)

RV2 = lambda x: m_rv1*(x-25) + b_rv1

# Obtener las coordenadas de los puntos que forman la recta EcNE
x1 = NE[0]
y1 = NE[1]
x2 = Pws[0]
y2 = Pws[1]
m = (y2 - y1) / (x2 - x1)
b = y1 - m*x1
recta_EcNE = (m, b)

# Obtener las coordenadas de los puntos que forman la recta EcND
x1 = ND[0]
y1 = ND[1]
x2 = Pwf[0]
y2 = Pwf[1]
m = (y2 - y1) / (x2 - x1)
b = y1 - m*x1
recta_EcND = (m, b)


# Ecuación de la recta Pso-Pvo
m1 = (Pvo[1] - Pso[1]) / (Pvo[0] - Pso[0])
b1 = Pso[1] - m1 * Pso[0]

# Ecuación de la recta EcND
m2 = (Pwf[1] - ND[1]) / (Pwf[0] - ND[0])
b2 = ND[1] - m2 * ND[0]

# Punto de intersección de las rectas
x = (b2 - b1) / (m1 - m2)
y = m1 * x + b1

# Punto de balance
x_pob, y_pob = (x, y)
PuntoBalance = (x_pob,y_pob)
print("El punto de balance es:", (x_pob, y_pob))

# Al eje x del "Punto de balance" restale 100 y traza una línea vertical y obten su ecuación de la recta y llamala "VertPo"
x_VertPo = PuntoBalance[0] - 100
VertPo = "x = " + str(x_VertPo)

# Calcula el punto de intersección entre la recta "EcND" y la recta "VertPo" y el punto de intersección guárdalo como "Poi"
x_poi = (x_VertPo)
y_poi = ((recta_EcND[0]*x_VertPo)+recta_EcND[1])
poi = (x_poi, y_poi)
print("El punto op iny:", (x_poi, y_poi))

# Guarda el punto denominado "Grad" con eje x = Pwhp + Gradf*ProfNE, y eje y = ProfNE
x_Grad = (Pwhp+(-Gradf*(Prof)))
Grad = (x_Grad, Prof)


# Traza una recta entre el punto "Pwh" y "Grad" y calcula la ecuación de la recta y llamala "RGrad1"
m_RGrad1 = (Grad[1] - Pwh[1])/(Grad[0] - Pwh[0])
n_RGrad1 = Grad[1] - m_RGrad1*Grad[0]
RGrad1 = "y = " + str(m_RGrad1) + "x + " + str(n_RGrad1)
x_min = min(Grad[0], Pwh[0]) - 1
x_max = max(Pdisp[0], Grad[0]) + 1
x_RGrad1 = [x_min, x_max]
y_RGrad1 = [m_RGrad1*x_i + n_RGrad1 for x_i in x_RGrad1]



x_Ptpd = (Pwh[0]+200)
y_Ptpd = (0)
Ptpd = (x_Ptpd, y_Ptpd)



# Traza una recta entre el punto "Ptpd" y el punto "Poi", calcula su ecuación de la recta y llamala "RPTP"
m_RPTP = (poi[1] - Ptpd[1])/(poi[0] - Ptpd[0])
n_RPTP = poi[1] - m_RPTP*poi[0]
RPTP = "y = " + str(m_RPTP) + "x + " + str(n_RPTP)
x_min = min(poi[0], Ptpd[0]) - 1
x_max = max(poi[0], Ptpd[0]) + 1
x = [x_min, x_max]
y = [m_RPTP*x_i + n_RPTP for x_i in x]
plt.plot(x, y)

# Traza una recta entre el punto "Pwh" y el punto "Poi", calcula su ecuación de la recta y llamala "RecVal"
m_RecVal = (poi[1] - Pwh[1])/(poi[0] - Pwh[0])
n_RecVal = poi[1] - m_RecVal*poi[0]
RecVal = "y = " + str(m_RecVal) + "x + " + str(n_RecVal)
x_min = min(poi[0], Pwh[0]) - 1
x_max = max(poi[0], Pwh[0]) + 1
x = [x_min, x_max]
y = [m_RecVal*x_i + n_RecVal for x_i in x]
plt.plot(x, y)

# Intersección entre RV1 y RGrad1
m_rv1 = (Pdisp_nmd[1]-Pdisp[1])/(Pdisp_nmd[0]-Pdisp[0])
b_rv1 = Pdisp_nmd[1] - m_rv1*Pdisp_nmd[0]

m_rgrad1 = (Pwh[1]-Grad[1])/(Pwh[0]-Grad[0])
b_rgrad1 = Pwh[1] - m_rgrad1*Pwh[0]

x_valvula1 = (b_rgrad1-b_rv1)/(m_rv1-m_rgrad1)
y_valvula1 = m_rv1*x_valvula1 + b_rv1
Valvula1 = (x_valvula1, y_valvula1)


# Recta horizontal apartir del eje x del punto “Valvula1”
#VALVULA2
Horva1 = lambda x: y_valvula1

x_min = int((y_valvula1-n_RPTP)/m_RPTP)
x_max = int(Valvula1[0])
x_Horva1 = [i for i in range(x_min, x_max+1)]
y_Horva1 = [Horva1(x_i) for x_i in x_Horva1]


# Punto de intersección entre las rectas RPTP y Horva1
x_pv1 = (y_valvula1-n_RPTP)/(m_RPTP)
y_pv1 = y_valvula1
Pv1 = (x_pv1, y_pv1)


#R2
x1 = Pdisp[0]
y1 = Pdisp[1]
x2 = Pdisp_nmd[0]
y2 = Pdisp_nmd[1]
m = (y2 - y1) / ((x2) - (x1))
b = y1 - m*(x1-100)
recta_RV2 = ((m), (b))
x = np.linspace(0, x2)
y = m * x + b
plt.plot(x, y)


#RGrad2
m_RGrad2 = (m_RGrad1)
n_RGrad2 = ((m_RGrad1*(-x_pv1))+y_pv1)
RGrad2 = (m, b)
x_min = min(Pv1[0], Pvo[0]) - 1
x_max = max(Pv1[0], x_pob) + 1
x_RGrad2 = [x_min, x_max]
y_RGrad2 = [m_RGrad2*x_i + n_RGrad2 for x_i in x_RGrad2]

# Punto de intersección entre RV2 y RGrad2
x_valvula2 = ((recta_RV2[1]-n_RGrad2)/(-recta_RV2[0]+m_RGrad2))
y_valvula2 = (m_RGrad2*x_valvula2)+n_RGrad2
Valvula2 = (x_valvula2, y_valvula2)

#Valvula 3
# Recta horizontal apartir del eje x del punto “Valvula2”
Horva2 = lambda x: y_valvula2
x_min = int((y_valvula2-n_RPTP)/m_RPTP)
x_max = int(Valvula2[0])
x_Horva2 = [i for i in range(x_min, x_max+1)]
y_Horva2 = [Horva2(x_i) for x_i in x_Horva2]


# Punto de intersección entre las rectas RPTP y Horva2
x_pv2 = (y_valvula2-n_RPTP)/(m_RPTP)
y_pv2 = y_valvula2
Pv2 = (x_pv2, y_pv2)


#R3
x1 = Pdisp[0]
y1 = Pdisp[1]
x2 = Pdisp_nmd[0]
y2 = Pdisp_nmd[1]
m = (y2 - y1) / ((x2) - (x1))
b = y1 - m*(x1-100)
recta_RV3 = ((m), (b))
x = np.linspace(0, x2)
y = m * x + b
plt.plot(x, y)

#RGrad3
m_RGrad3 = (m_RGrad2)
n_RGrad3 = ((m_RGrad2*(-x_pv2))+y_pv2)
RGrad3 = (m, b)
x_min = min(Pv2[0], Pvo[0]) - 1
x_max = max(Pv2[0], x_pob) + 1
x_RGrad3 = [x_min, x_max]
y_RGrad3 = [m_RGrad3*x_i + n_RGrad3 for x_i in x_RGrad3]


# Punto de intersección entre RV3 y RGrad3
x_valvula3 = ((recta_RV3[1]-n_RGrad3)/(-recta_RV3[0]+m_RGrad3))
y_valvula3 = (m_RGrad3*x_valvula3)+n_RGrad3
Valvula3 = (x_valvula3, y_valvula3)


#Valvula 4
# Recta horizontal apartir del eje x del punto “Valvula2”
Horva3 = lambda x: y_valvula3
x_min = int((y_valvula3-n_RPTP)/m_RPTP)
x_max = int(Valvula3[0])
x_Horva3 = [i for i in range(x_min, x_max+1)]
y_Horva3 = [Horva3(x_i) for x_i in x_Horva3]


# Punto de intersección entre las rectas RPTP y Horva2
x_pv3 = (y_valvula3-n_RPTP)/(m_RPTP)
y_pv3 = y_valvula3
Pv3 = (x_pv3, y_pv3)


#R4
x1 = Pdisp[0]
y1 = Pdisp[1]
x2 = Pdisp_nmd[0]
y2 = Pdisp_nmd[1]
m = (y2 - y1) / ((x2) - (x1))
b = y1 - m*(x1-100)
recta_RV4 = ((m), (b))
x = np.linspace(0, x2)
y = m * x + b
plt.plot(x, y)

#RGrad4
m_RGrad4 = (m_RGrad3)
n_RGrad4 = ((m_RGrad3*(-x_pv3))+y_pv3)
RGrad4 = (m, b)
x_min = min(Pv3[0], Pvo[0]) - 1
x_max = max(Pv3[0], x_pob) + 1
x_RGrad4 = [x_min, x_max]
y_RGrad4 = [m_RGrad4*x_i + n_RGrad4 for x_i in x_RGrad4]


# Punto de intersección entre RV3 y RGrad3
x_valvula4 = ((recta_RV4[1]-n_RGrad4)/(-recta_RV4[0]+m_RGrad4))
y_valvula4 = (m_RGrad4*x_valvula4)+n_RGrad4
Valvula4 = (x_valvula4, y_valvula4)

#Valvula 5
# Recta horizontal apartir del eje x del punto “Valvula2”
Horva4 = lambda x: y_valvula4
x_min = int((y_valvula4-n_RPTP)/m_RPTP)
x_max = int(Valvula4[0])
x_Horva4 = [i for i in range(x_min, x_max+1)]
y_Horva4 = [Horva4(x_i) for x_i in x_Horva4]


# Punto de intersección entre las rectas RPTP y Horva2
x_pv4 = (y_valvula4-n_RPTP)/(m_RPTP)
y_pv4 = y_valvula4
Pv4 = (x_pv4, y_pv4)


#R5
x1 = Pdisp[0]
y1 = Pdisp[1]
x2 = Pdisp_nmd[0]
y2 = Pdisp_nmd[1]
m = (y2 - y1) / ((x2) - (x1))
b = y1 - m*(x1-100)
recta_RV5 = ((m), (b))
x = np.linspace(0, x2)
y = m * x + b
plt.plot(x, y)

#RGrad5
m_RGrad5 = (m_RGrad4)
n_RGrad5 = ((m_RGrad4*(-x_pv4))+y_pv4)
RGrad5 = (m, b)
x_min = min(Pv4[0], Pvo[0]) - 1
x_max = max(Pv4[0], x_pob) + 1
x_RGrad5 = [x_min, x_max]
y_RGrad5 = [m_RGrad5*x_i + n_RGrad5 for x_i in x_RGrad5]


# Punto de intersección entre RV3 y RGrad3
x_valvula5 = ((recta_RV5[1]-n_RGrad5)/(-recta_RV5[0]+m_RGrad5))
y_valvula5 = (m_RGrad5*x_valvula5)+n_RGrad5
Valvula5 = (x_valvula5, y_valvula5)

#Valvula 6
# Recta horizontal apartir del eje x del punto “Valvula2”
Horva5 = lambda x: y_valvula5
x_min = int((y_valvula5-n_RPTP)/m_RPTP)
x_max = int(Valvula5[0])
x_Horva5 = [i for i in range(x_min, x_max+1)]
y_Horva5 = [Horva5(x_i) for x_i in x_Horva5]


# Punto de intersección entre las rectas RPTP y Horva2
x_pv5 = (y_valvula5-n_RPTP)/(m_RPTP)
y_pv5 = y_valvula5
Pv5 = (x_pv5, y_pv5)


#R6
x1 = Pdisp[0]
y1 = Pdisp[1]
x2 = Pdisp_nmd[0]
y2 = Pdisp_nmd[1]
m = (y2 - y1) / ((x2) - (x1))
b = y1 - m*(x1-100)
recta_RV6 = ((m), (b))
x = np.linspace(0, x2)
y = m * x + b
plt.plot(x, y)

#RGrad6
m_RGrad6 = (m_RGrad5)
n_RGrad6 = ((m_RGrad5*(-x_pv5))+y_pv5)
RGrad6 = (m, b)
x_min = min(Pv5[0], Pvo[0]) - 1
x_max = max(Pv5[0], x_pob) + 1
x_RGrad6 = [x_min, x_max]
y_RGrad6 = [m_RGrad6*x_i + n_RGrad6 for x_i in x_RGrad6]


x_valvula6 = ((recta_RV6[1]-n_RGrad6)/(-recta_RV6[0]+m_RGrad6))
y_valvula6 = (m_RGrad6*x_valvula6)+n_RGrad6
Valvula6 = (x_valvula6, y_valvula6)

#Valvula 7
# Recta horizontal apartir del eje x del punto “Valvula2”
Horva6 = lambda x: y_valvula6
x_min = int((y_valvula6-n_RPTP)/m_RPTP)
x_max = int(Valvula6[0])
x_Horva6 = [i for i in range(x_min, x_max+1)]
y_Horva6 = [Horva6(x_i) for x_i in x_Horva6]


# Punto de intersección entre las rectas RPTP y Horva2
x_pv6 = (y_valvula6-n_RPTP)/(m_RPTP)
y_pv6 = y_valvula6
Pv6 = (x_pv6, y_pv6)


#R7
x1 = Pdisp[0]
y1 = Pdisp[1]
x2 = Pdisp_nmd[0]
y2 = Pdisp_nmd[1]
m = (y2 - y1) / ((x2) - (x1))
b = y1 - m*(x1-100)
recta_RV7 = ((m), (b))
x = np.linspace(0, x2)
y = m * x + b
plt.plot(x, y)

#RGrad7
m_RGrad7 = (m_RGrad6)
n_RGrad7 = ((m_RGrad6*(-x_pv6))+y_pv6)
RGrad7 = (m, b)
x_min = min(Pv6[0], Pvo[0]) - 1
x_max = max(Pv6[0], x_pob) + 1
x_RGrad7 = [x_min, x_max]
y_RGrad7 = [m_RGrad7*x_i + n_RGrad7 for x_i in x_RGrad7]


x_valvula7 = ((recta_RV7[1]-n_RGrad7)/(-recta_RV7[0]+m_RGrad7))
y_valvula7 = (m_RGrad7*x_valvula7)+n_RGrad7
Valvula7 = (x_valvula7, y_valvula7)

#Valvula 8
# Recta horizontal apartir del eje x del punto “Valvula2”
Horva7 = lambda x: y_valvula7
x_min = int((y_valvula7-n_RPTP)/m_RPTP)
x_max = int(Valvula7[0])
x_Horva7 = [i for i in range(x_min, x_max+1)]
y_Horva7 = [Horva7(x_i) for x_i in x_Horva7]


# Punto de intersección entre las rectas RPTP y Horva2
x_pv7 = (y_valvula7-n_RPTP)/(m_RPTP)
y_pv7 = y_valvula7
Pv7 = (x_pv7, y_pv7)


#R8
x1 = Pdisp[0]
y1 = Pdisp[1]
x2 = Pdisp_nmd[0]
y2 = Pdisp_nmd[1]
m = (y2 - y1) / ((x2) - (x1))
b = y1 - m*(x1-100)
recta_RV8 = ((m), (b))
x = np.linspace(0, x2)
y = m * x + b
plt.plot(x, y)

#RGrad8
m_RGrad8 = (m_RGrad7)
n_RGrad8 = ((m_RGrad7*(-x_pv7))+y_pv7)
RGrad8 = (m, b)
x_min = min(Pv7[0], Pvo[0]) - 1
x_max = max(Pv7[0], x_pob) + 1
x_RGrad8 = [x_min, x_max]
y_RGrad8 = [m_RGrad8*x_i + n_RGrad8 for x_i in x_RGrad8]


x_valvula8 = ((recta_RV8[1]-n_RGrad8)/(-recta_RV8[0]+m_RGrad8))
y_valvula8 = (m_RGrad8*x_valvula8)+n_RGrad8
Valvula8 = (x_valvula8, y_valvula8)

#Valvula 9
# Recta horizontal apartir del eje x del punto “Valvula2”
Horva8 = lambda x: y_valvula8
x_min = int((y_valvula8-n_RPTP)/m_RPTP)
x_max = int(Valvula8[0])
x_Horva8 = [i for i in range(x_min, x_max+1)]
y_Horva8 = [Horva8(x_i) for x_i in x_Horva8]


# Punto de intersección entre las rectas RPTP y Horva2
x_pv8 = (y_valvula8-n_RPTP)/(m_RPTP)
y_pv8 = y_valvula8
Pv8 = (x_pv8, y_pv8)


#R9
x1 = Pdisp[0]
y1 = Pdisp[1]
x2 = Pdisp_nmd[0]
y2 = Pdisp_nmd[1]
m = (y2 - y1) / ((x2) - (x1))
b = y1 - m*(x1-100)
recta_RV9 = ((m), (b))
x = np.linspace(0, x2)
y = m * x + b
plt.plot(x, y)

#RGrad9
m_RGrad9 = (m_RGrad8)
n_RGrad9 = ((m_RGrad8*(-x_pv8))+y_pv8)
RGrad9 = (m, b)
x_min = min(Pv8[0], Pvo[0]) - 1
x_max = max(Pv8[0], x_pob) + 1
x_RGrad9 = [x_min, x_max]
y_RGrad9 = [m_RGrad9*x_i + n_RGrad9 for x_i in x_RGrad9]


x_valvula9 = ((recta_RV9[1]-n_RGrad9)/(-recta_RV9[0]+m_RGrad9))
y_valvula9 = (m_RGrad9*x_valvula9)+n_RGrad9
Valvula9 = (x_valvula9, y_valvula9)

#Valvula 10
# Recta horizontal apartir del eje x del punto “Valvula2”
Horva9 = lambda x: y_valvula9
x_min = int((y_valvula9-n_RPTP)/m_RPTP)
x_max = int(Valvula9[0])
x_Horva9 = [i for i in range(x_min, x_max+1)]
y_Horva9 = [Horva9(x_i) for x_i in x_Horva9]


# Punto de intersección entre las rectas RPTP y Horva2
x_pv9 = (y_valvula9-n_RPTP)/(m_RPTP)
y_pv9 = y_valvula9
Pv9 = (x_pv9, y_pv9)


#R10
x1 = Pdisp[0]
y1 = Pdisp[1]
x2 = Pdisp_nmd[0]
y2 = Pdisp_nmd[1]
m = (y2 - y1) / ((x2) - (x1))
b = y1 - m*(x1-100)
recta_RV10 = ((m), (b))
x = np.linspace(0, x2)
y = m * x + b
plt.plot(x, y)

#RGrad10
m_RGrad10 = (m_RGrad9)
n_RGrad10 = ((m_RGrad9*(-x_pv9))+y_pv9)
RGrad10 = (m, b)
x_min = min(Pv9[0], Pvo[0]) - 1
x_max = max(Pv9[0], x_pob) + 1
x_RGrad10 = [x_min, x_max]
y_RGrad10 = [m_RGrad10*x_i + n_RGrad10 for x_i in x_RGrad10]


x_valvula10 = ((recta_RV10[1]-n_RGrad10)/(-recta_RV10[0]+m_RGrad10))
y_valvula10 = (m_RGrad10*x_valvula10)+n_RGrad10
Valvula10 = (x_valvula10, y_valvula10)


print("Coordenadas de Valvula1:", Valvula1)

plt.plot([Pso[0], Pvo[0]], [Pso[1], Pvo[1]])
plt.plot([Pdisp[0], Pdisp_nmd[0]], [Pdisp[1], Pdisp_nmd[1]])
plt.plot([ND[0], Pwf[0]], [ND[1], Pwf[1]])
plt.plot([NE[0], Pws[0]], [NE[1], Pws[1]], label="EcND")
plt.plot(x_pob, y_pob, 'o',markersize=5,markerfacecolor='r', markeredgecolor='r')
plt.plot(x_poi, y_poi, 'o',markersize=5,markerfacecolor='r', markeredgecolor='r')
plt.plot(x_valvula1, y_valvula1, 'o',markersize=5,markerfacecolor='r', markeredgecolor='b')
plt.plot(x_RGrad1, y_RGrad1)
plt.plot(x_Horva1, y_Horva1)
plt.plot(x_RGrad2, y_RGrad2)
plt.plot(x_valvula2, y_valvula2, 'o',markersize=5,markerfacecolor='r', markeredgecolor='b')
print("Coordenadas de Valvula2:", Valvula2)

import matplotlib.pyplot as plt

# Definición de coordenadas y puntos de ejemplo
y_poi = y_poi
valvulas = [
    (x_Horva2, y_Horva2, x_RGrad3, y_RGrad3, x_valvula3, y_valvula3, 'Valvula3', Valvula3),
    (x_Horva3, y_Horva3, x_RGrad4, y_RGrad4, x_valvula4, y_valvula4, 'Valvula4', Valvula4),
    (x_Horva4, y_Horva4, x_RGrad5, y_RGrad5, x_valvula5, y_valvula5, 'Valvula5', Valvula5),
    (x_Horva5, y_Horva5, x_RGrad6, y_RGrad6, x_valvula6, y_valvula6, 'Valvula6', Valvula6),
    (x_Horva6, y_Horva6, x_RGrad7, y_RGrad7, x_valvula7, y_valvula7, 'Valvula7', Valvula7),
    (x_Horva7, y_Horva7, x_RGrad8, y_RGrad8, x_valvula8, y_valvula8, 'Valvula8', Valvula8),
    (x_Horva8, y_Horva8, x_RGrad9, y_RGrad9, x_valvula9, y_valvula9, 'Valvula9', Valvula9),
    (x_Horva9, y_Horva9, x_RGrad10, y_RGrad10, x_valvula10, y_valvula10, 'Valvula10', Valvula10)
]

valvula_operante = None


# Graficar e imprimir las válvulas que cumplen la condición
for valvula in valvulas:
    x_Horva, y_Horva, x_RGrad, y_RGrad, x_valvula, y_valvula, nombre_valvula, coordenadas_valvula = valvula
    if y_valvula > y_poi:
        plt.plot(x_Horva, y_Horva)
        plt.plot(x_RGrad, y_RGrad)
        plt.plot(x_valvula, y_valvula, 'o', markersize=5, markerfacecolor='r', markeredgecolor='b')
        print(f"Coordenadas de {nombre_valvula}: {coordenadas_valvula}")
    else:
        valvula_operante = (coordenadas_valvula[0], coordenadas_valvula[1])
        print(f"La válvula operante es la {nombre_valvula}")
        print("Coordenadas de la válvula operante:", valvula_operante)
        break

# Si se encontró una válvula operante, graficarla también
if valvula_operante:
    plt.plot(valvula_operante[0], valvula_operante[1], 'o', markersize=5, markerfacecolor='g', markeredgecolor='b')



"""if y_valvula2 > y_poi:
    plt.plot(x_Horva2, y_Horva2)
    plt.plot(x_RGrad3, y_RGrad3)
    plt.plot(x_valvula3, y_valvula3, 'o',markersize=5,markerfacecolor='r', markeredgecolor='b')
    print("Coordenadas de Valvula3:", Valvula3)
else:
    print("La válvula operante es la válvula 2")
    valvulaop = (Valvula2[0], Valvula2[1])
    print("Coordenadas de la válvula operante:", valvulaop)
    

if y_valvula3 > y_poi:
    plt.plot(x_Horva3, y_Horva3)
    plt.plot(x_RGrad4, y_RGrad4)
    plt.plot(x_valvula4, y_valvula4, 'o',markersize=5,markerfacecolor='r', markeredgecolor='b')
    print("Coordenadas de Valvula4:", Valvula4)
else:
    print("La válvula operante es la válvula 3")
    valvulaop = (Valvula3[0], Valvula3[1])
    print("Coordenadas de la válvula operante:", valvulaop)


if y_valvula4 > y_poi:
    plt.plot(x_Horva4, y_Horva4)
    plt.plot(x_RGrad5, y_RGrad5)
    plt.plot(x_valvula5, y_valvula5, 'o',markersize=5,markerfacecolor='r', markeredgecolor='b')
    print("Coordenadas de Valvula5:", Valvula5)
else:
    print("La válvula operante es la válvula 4")
    valvulaop = (Valvula4[0], Valvula4[1])
    print("Coordenadas de la válvula operante:", valvulaop)

if y_valvula5 > y_poi:
    plt.plot(x_Horva5, y_Horva5)
    plt.plot(x_RGrad6, y_RGrad6)
    plt.plot(x_valvula6, y_valvula6, 'o',markersize=5,markerfacecolor='r', markeredgecolor='b')
    print("Coordenadas de Valvula6:", Valvula6)
else:
    print("La válvula operante es la válvula 5")
    valvulaop = (Valvula5[0], Valvula5[1])
    print("Coordenadas de la válvula operante:", valvulaop)
    
if y_valvula6 > y_poi:
    plt.plot(x_Horva6, y_Horva6)
    plt.plot(x_RGrad7, y_RGrad7)
    plt.plot(x_valvula7, y_valvula7, 'o',markersize=5,markerfacecolor='r', markeredgecolor='b')
    print("Coordenadas de Valvula7:", Valvula7)
else:
    print("La válvula operante es la válvula 6")
    valvulaop = (Valvula6[0], Valvula6[1])
    print("Coordenadas de la válvula operante:", valvulaop)

if y_valvula7 > y_poi:
    plt.plot(x_Horva7, y_Horva7)
    plt.plot(x_RGrad8, y_RGrad8)
    plt.plot(x_valvula8, y_valvula8, 'o',markersize=5,markerfacecolor='r', markeredgecolor='b')
    print("Coordenadas de Valvula8:", Valvula8)
else:
    print("La válvula operante es la válvula 7")
    valvulaop = (Valvula7[0], Valvula7[1])
    print("Coordenadas de la válvula operante:", valvulaop)

if y_valvula8 > y_poi:
    plt.plot(x_Horva8, y_Horva8)
    plt.plot(x_RGrad9, y_RGrad9)
    plt.plot(x_valvula9, y_valvula9, 'o',markersize=5,markerfacecolor='r', markeredgecolor='b')
    print("Coordenadas de Valvula9:", Valvula9)
else:
    print("La válvula operante es la válvula 8")
    valvulaop = (Valvula8[0], Valvula8[1])
    print("Coordenadas de la válvula operante:", valvulaop)

if y_valvula9 > y_poi:
    plt.plot(x_Horva9, y_Horva9)
    plt.plot(x_RGrad10, y_RGrad10)
    plt.plot(x_valvula10, y_valvula10, 'o',markersize=5,markerfacecolor='r', markeredgecolor='b')
    print("Coordenadas de Valvula10:", Valvula10)
else:
    print("La válvula operante es la válvula 9")
    valvulaop = (Valvula9[0], Valvula9[1])
    print("Coordenadas de la válvula operante:", valvulaop)"""



plt.grid()

plt.legend()
plt.ylim(ymax=0, ymin=-8000)
plt.title('Valvúlas Desbalanceadas')
plt.savefig('grafica_problema2_desbalanceadas.pdf')

plt.show()





