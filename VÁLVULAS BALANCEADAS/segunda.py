import numpy as np
import matplotlib.pyplot as plt

def calcular_seggradiente(presion_objetivo, sg_gas_objetivo):
    # Constantes
    presiones = np.linspace(0, 100, 100)
    sggases = [0.6, 0.65, 0.7, 0.8, 0.9, 1] 
    inicio_fin_rectas = {
        0.6: [(4.65, 200), (25, 1200)],
        0.65: [(5, 200), (28.2, 1200)],
        0.7: [(5.46, 200), (31.5, 1200)],
        0.8: [(5.85, 200), (36, 1200)],
        0.9: [(6.4, 200), (40, 1200)],
        1: [(6.5, 200), (44.8, 1200)],
    }
    
    # Calcular los gradientes para cada valor de SGGAS
    gradientes = {sg_gas: np.interp(presiones, [inicio_fin[0][0], inicio_fin[1][0]], [inicio_fin[0][1], inicio_fin[1][1]]) for sg_gas, inicio_fin in inicio_fin_rectas.items()}

    # Calcular el gradiente
    if sg_gas_objetivo in gradientes:
        gradiente = np.interp(presion_objetivo, [gradientes[sg_gas_objetivo][i] for i in range(len(gradientes[sg_gas_objetivo]))], presiones)
    else:
        keys = sorted(gradientes.keys())
        lower_sggas = max(filter(lambda x: x < sg_gas_objetivo, keys))
        upper_sggas = min(filter(lambda x: x > sg_gas_objetivo, keys))
        lower_grad = np.interp(presion_objetivo, [gradientes[lower_sggas][i] for i in range(len(gradientes[lower_sggas]))], presiones)
        upper_grad = np.interp(presion_objetivo, [gradientes[upper_sggas][i] for i in range(len(gradientes[upper_sggas]))], presiones)
        gradiente = np.interp(sg_gas_objetivo, [lower_sggas, upper_sggas], [lower_grad, upper_grad])
    
    return gradiente

def graficar(presion_objetivo, sg_gas_objetivo, gradiente, inicio_fin_rectas):
    plt.figure(figsize=(8, 6))
    
    # Graficar las líneas de SGGAS
    for sg_gas, inicio_fin in inicio_fin_rectas.items():
        plt.plot(np.linspace(inicio_fin[0][0], inicio_fin[1][0], 100), np.linspace(inicio_fin[0][1], inicio_fin[1][1], 100), label=f'SGGAS {sg_gas}')
    
    # Punto objetivo
    plt.scatter(gradiente, presion_objetivo, color='red', label='Punto objetivo')

    plt.xlabel('GPres')
    plt.ylabel('Psup')
    plt.title('Gráfico de Gradiente vs. Presión de gas y relación de solubilidad')
    plt.legend()
    plt.grid(True)
    plt.show()
