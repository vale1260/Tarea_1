def calcular_coeficiente_gini(datos):
    n = len(datos)
    suma_iyi = sum((i + 1) * y for i, y in enumerate(datos))
    suma_yi = sum(datos)

    if suma_yi == 0:
        return 0

    gini = 1 - (2 * suma_iyi) / (n * (n + 1) * suma_yi)

    return gini

# Leer valores de carga del archivo para el sistema casero
with open("data_casero.txt", "r") as archivo_casero:
    carga_casero = [float(linea.strip()) for linea in archivo_casero.readlines()]

# Calcular los coeficientes de Gini
coeficiente_gini_casero = calcular_coeficiente_gini(carga_casero)

# Imprimir los coeficientes de Gini calculados
print("Coeficiente de Gini - Sistema Casero:", coeficiente_gini_casero)
