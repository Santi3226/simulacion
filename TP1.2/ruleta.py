import random
import sys
import matplotlib.pyplot as plt
import numpy as np

# ------------------ Funciones Auxiliares ------------------

def obtener_color(numero):
    rojos = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    if numero == 0:
        return "verde"
    elif numero in rojos:
        return "rojo"
    else:
        return "negro"

def obtener_docena(numero):
    if 1 <= numero <= 12:
        return "primera"
    elif 13 <= numero <= 24:
        return "segunda"
    elif 25 <= numero <= 36:
        return "tercera"
    else:
        return "ninguna"

def fibonacci_seq(n):
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq

# ------------------ Validar argumentos ------------------

if len(sys.argv) < 7:
    print("Uso incorrecto. Ejemplo de ejecución:")
    print("Si apuestas a número: python programa.py -c <tiradas> -n <corridas> -e <numero_elegido> -s <estrategia> -a <capital>")
    print("Si apuestas a color o docena: python programa.py -c <tiradas> -n <corridas> -s <estrategia> -a <capital>")
    sys.exit(1)

numero_elegido = None
tipo_apuesta = ""
estrategia = ""
capital_tipo = ""
eleccion = ""
capital_inicial = 1000

i = 1
while i < len(sys.argv):
    if sys.argv[i] == "-c":
        cant_tiradas = int(sys.argv[i + 1])
        i += 2
    elif sys.argv[i] == "-n":
        cant_corridas = int(sys.argv[i + 1])
        i += 2
    elif sys.argv[i] == "-e":
        numero_elegido = int(sys.argv[i + 1])
        tipo_apuesta = "número"
        i += 2
    elif sys.argv[i] == "-s":
        estrategia = sys.argv[i + 1].lower()
        i += 2
    elif sys.argv[i] == "-a":
        capital_tipo = sys.argv[i + 1].lower()
        if capital_tipo == "f":
            if i + 2 < len(sys.argv) and sys.argv[i + 2].isdigit():
                capital_inicial = int(sys.argv[i + 2])
                i += 2
            else:
                print("Debe especificar el capital inicial con '-a f <capital_inicial>'.")
                sys.exit(1)
        i += 2
    else:
        print(f"Parámetro desconocido: {sys.argv[i]}")
        sys.exit(1)

if estrategia not in ('m', 'd', 'f', 'o', 'p'):
    print("Estrategia inválida. Opciones: m (Martingala), d (D'Alembert), f (Fibonacci), o (otra), p (Paroli).")
    sys.exit(1)

if capital_tipo not in ('i', 'f'):
    print("Capital inválido. Opciones: i (infinito), f (finito).")
    sys.exit(1)

if tipo_apuesta == "":
    print("\n¿Tipo de apuesta? (número / color / docena)")
    tipo_apuesta = input(">> ").strip().lower()

    if tipo_apuesta not in ('número', 'color', 'docena'):
        print("Tipo de apuesta inválido.")
        sys.exit(1)

    if tipo_apuesta == "color":
        print("\n¿A qué color apuestas? (rojo / negro)")
        eleccion = input(">> ").strip().lower()
        if eleccion not in ('rojo', 'negro'):
            print("Color inválido.")
            sys.exit(1)
    elif tipo_apuesta == "docena":
        print("\n¿A qué docena apuestas? (primera / segunda / tercera)")
        eleccion = input(">> ").strip().lower()
        if eleccion not in ('primera', 'segunda', 'tercera'):
            print("Docena inválida.")
            sys.exit(1)

if tipo_apuesta == "número" and numero_elegido is None:
    print("\n¿A qué número apuestas? (0-36)")
    numero_elegido = int(input(">> ").strip())
    if not (0 <= numero_elegido <= 36):
        print("Número inválido.")
        sys.exit(1)

# ------------------ Variables Iniciales ------------------

print(f"\nSimulando {cant_corridas} corridas de {cant_tiradas} tiradas cada una...")
print(f"Apuesta: Tipo '{tipo_apuesta}' con estrategia '{estrategia.upper()}' y capital '{capital_tipo.upper()}'\n")

if tipo_apuesta == "número":
    print(f"Apuesta sobre el número {numero_elegido}")
else:
    print(f"Apuesta sobre {eleccion}")

saldo_final = []
quiebras = 0

# Variables para gráficas
exitos_por_tirada = np.zeros(cant_tiradas)
capital_evolucion = np.zeros(cant_tiradas)
quiebras_tiradas = np.zeros(cant_tiradas)

fib_seq = fibonacci_seq(100)

# ------------------ Simulación ------------------

for corrida in range(cant_corridas):
    saldo = capital_inicial if capital_tipo == 'f' else float('inf')
    apuesta_inicial = 10
    apuesta = apuesta_inicial
    fib_index = 0
    victorias_consecutivas = 0  # Nuevo: para Paroli
    saldo_corrida = []

    for tirada in range(cant_tiradas):
        if capital_tipo == 'f' and saldo <= 0:
            quiebras += 1
            quiebras_tiradas[tirada] += 1
            saldo_corrida += [0] * (cant_tiradas - tirada)
            break

        numero = random.randint(0, 36)
        color = obtener_color(numero)
        docena = obtener_docena(numero)

        gano = False
        if tipo_apuesta == 'número' and numero == numero_elegido:
            gano = True
        elif tipo_apuesta == 'color' and color == eleccion:
            gano = True
        elif tipo_apuesta == 'docena' and docena == eleccion:
            gano = True

        payout = 35 if tipo_apuesta == 'número' else (2 if tipo_apuesta == 'docena' else 1)

        if gano:
            saldo += apuesta * payout
            if estrategia == 'm':
                apuesta = apuesta_inicial
            elif estrategia == 'd':
                if apuesta > apuesta_inicial:
                    apuesta -= apuesta_inicial
            elif estrategia == 'f':
                fib_index = max(0, fib_index - 2)
                apuesta = fib_seq[fib_index] * apuesta_inicial
            elif estrategia == 'p':
                victorias_consecutivas += 1
                if victorias_consecutivas == 3:
                    apuesta = apuesta_inicial
                    victorias_consecutivas = 0
                else:
                    apuesta = min(saldo, apuesta * 2)
        else:
            saldo -= apuesta
            if estrategia == 'm':
                apuesta *= 2
            elif estrategia == 'd':
                apuesta += apuesta_inicial
            elif estrategia == 'f':
                fib_index += 1
                apuesta = fib_seq[min(fib_index, len(fib_seq)-1)] * apuesta_inicial
            elif estrategia == 'p':
                apuesta = apuesta_inicial
                victorias_consecutivas = 0

        saldo_corrida.append(saldo)

        if gano:
            exitos_por_tirada[tirada] += 1

    saldo_final.append(saldo if saldo != float('inf') else capital_inicial)
    capital_evolucion[:len(saldo_corrida)] += saldo_corrida

# ------------------ Resultados ------------------

saldo_promedio = np.mean(saldo_final)
print("\n--- RESULTADOS ---")
print(f"Saldo promedio final después de {cant_corridas} corridas: {saldo_promedio:.2f}")
print(f"Veces que hubo bancarrota: {quiebras} de {cant_corridas}")

# ------------------ Graficar ------------------

fig, axes = plt.subplots(2, 1, figsize=(10, 12))

# Frecuencia relativa
frsa = exitos_por_tirada / cant_corridas
axes[0].bar(range(1, len(frsa)+1), frsa, color='red', edgecolor='black')
axes[0].set_title('Frecuencia relativa de obtener apuesta favorable (frsa)')
axes[0].set_xlabel('Número de tirada (n)')
axes[0].set_ylabel('Frecuencia relativa (fr)')
axes[0].grid(axis='y')

# Evolución del capital promedio
capital_promedio = capital_evolucion / cant_corridas
axes[1].plot(range(1, len(capital_promedio)+1), capital_promedio, color='red', label='fc (flujo de caja)')
axes[1].axhline(y=capital_inicial, color='blue', linestyle='--', label='fci (flujo de caja inicial)')

# Marcar quiebras
quiebra_indices = np.where(quiebras_tiradas > 0)[0]
for idx in quiebra_indices:
    axes[1].axvline(x=idx+1, color='gray', linestyle=':', alpha=0.5)

# Crear una línea invisible solo para la leyenda de quiebras
from matplotlib.lines import Line2D
quiebra_line = Line2D([0], [0], color='gray', linestyle=':', label='quiebra')

handles, labels = axes[1].get_legend_handles_labels()
handles.append(quiebra_line)
labels.append('quiebra')
axes[1].legend(handles, labels)

axes[1].set_title('Evolución del capital promedio')
axes[1].set_xlabel('Número de tirada (n)')
axes[1].set_ylabel('Cantidad de capital (cc)')
axes[1].grid(True)

plt.tight_layout()
plt.show()
