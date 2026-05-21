import random
import argparse
import matplotlib.pyplot as plt
import numpy as np

# Funciones Auxiliares

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

# Argumentos

parser = argparse.ArgumentParser(
    description='Simulación de ruleta con distintas estrategias de apuesta.',
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument('-c', type=int, default=10,
                    help='Cantidad de corridas (default: 10)')
parser.add_argument('-n', type=int, default=300,
                    help='Cantidad de tiradas por corrida (default: 300)')
parser.add_argument('-e', type=int, default=None,
                    help='Número elegido (0-36). Si se omite, se pregunta el tipo de apuesta.')
parser.add_argument('-s', type=str, choices=['m', 'd', 'f', 'o', 'p'], required=True,
                    help=(
                        'Estrategia de apuesta:\n'
                        '  m = Martingala\n'
                        '  d = D\'Alembert\n'
                        '  f = Fibonacci\n'
                        '  o = Otra\n'
                        '  p = Paroli'
                    ))
parser.add_argument('-a', type=str, choices=['i', 'f'], required=True,
                    help='Tipo de capital:\n  i = infinito\n  f = finito')
parser.add_argument('--capital', type=int, default=1000,
                    help='Capital inicial en pesos/unidades (solo si -a f). Default: 1000')

args = parser.parse_args()

# Validaciones y asignaciones

if args.a == 'f' and args.capital <= 0:
    parser.error("El capital inicial debe ser mayor a 0.")

if args.e is not None and not (0 <= args.e <= 36):
    parser.error("El número elegido debe estar entre 0 y 36.")

cant_corridas  = args.c
cant_tiradas   = args.n
numero_elegido = args.e
estrategia     = args.s
capital_tipo   = args.a
capital_inicial = args.capital if capital_tipo == 'f' else float('inf')

# Tipo de apuesta 

tipo_apuesta = ""
eleccion = ""

if numero_elegido is not None:
    tipo_apuesta = "número"
else:
    print("\n¿Tipo de apuesta? (número / color / docena)")
    tipo_apuesta = input(">> ").strip().lower()

    if tipo_apuesta not in ('número', 'color', 'docena'):
        print("Tipo de apuesta inválido.")
        raise SystemExit(1)

    if tipo_apuesta == "color":
        print("\n¿A qué color apostás? (rojo / negro)")
        eleccion = input(">> ").strip().lower()
        if eleccion not in ('rojo', 'negro'):
            print("Color inválido.")
            raise SystemExit(1)

    elif tipo_apuesta == "docena":
        print("\n¿A qué docena apostás? (primera / segunda / tercera)")
        eleccion = input(">> ").strip().lower()
        if eleccion not in ('primera', 'segunda', 'tercera'):
            print("Docena inválida.")
            raise SystemExit(1)

    elif tipo_apuesta == "número":
        print("\n¿A qué número apostás? (0-36)")
        numero_elegido = int(input(">> ").strip())
        if not (0 <= numero_elegido <= 36):
            print("Número inválido.")
            raise SystemExit(1)

# Resumen

print(f"\nSimulando {cant_corridas} corridas de {cant_tiradas} tiradas cada una...")
print(f"Apuesta: Tipo '{tipo_apuesta}' | Estrategia '{estrategia.upper()}' | Capital '{capital_tipo.upper()}'")

if tipo_apuesta == "número":
    print(f"Número elegido: {numero_elegido}")
else:
    print(f"Elección: {eleccion}")

# Variables Iniciales

saldo_final = []
quiebras = 0

exitos_por_tirada = np.zeros(cant_tiradas)
capital_evolucion = np.zeros(cant_tiradas)
quiebras_tiradas  = np.zeros(cant_tiradas)

fib_seq = fibonacci_seq(100)

# Simulación

# for corrida in range(cant_corridas):
#     saldo = capital_inicial if capital_tipo == 'f' else float('inf')
#     apuesta_inicial = 10
#     apuesta = apuesta_inicial
#     fib_index = 0
#     victorias_consecutivas = 0
#     saldo_corrida = []

#     for tirada in range(cant_tiradas):
#         if capital_tipo == 'f' and saldo <= 0:
#             quiebras += 1
#             quiebras_tiradas[tirada] += 1
#             saldo_corrida += [0] * (cant_tiradas - tirada)
#             break

#         numero = random.randint(0, 36)
#         color  = obtener_color(numero)
#         docena = obtener_docena(numero)

#         gano = False
#         if tipo_apuesta == 'número' and numero == numero_elegido:
#             gano = True
#         elif tipo_apuesta == 'color' and color == eleccion:
#             gano = True
#         elif tipo_apuesta == 'docena' and docena == eleccion:
#             gano = True

#         payout = 35 if tipo_apuesta == 'número' else (2 if tipo_apuesta == 'docena' else 1)

#         if gano:
#             saldo += apuesta * payout
#             if estrategia == 'm':
#                 apuesta = apuesta_inicial
#             elif estrategia == 'd':
#                 if apuesta > apuesta_inicial:
#                     apuesta -= apuesta_inicial
#             elif estrategia == 'f':
#                 fib_index = max(0, fib_index - 2)
#                 apuesta = fib_seq[fib_index] * apuesta_inicial
#             elif estrategia == 'p':
#                 victorias_consecutivas += 1
#                 if victorias_consecutivas == 3:
#                     apuesta = apuesta_inicial
#                     victorias_consecutivas = 0
#                 else:
#                     apuesta = min(saldo, apuesta * 2)
#         else:
#             saldo -= apuesta
#             if estrategia == 'm':
#                 apuesta *= 2
#             elif estrategia == 'd':
#                 apuesta += apuesta_inicial
#             elif estrategia == 'f':
#                 fib_index += 1
#                 apuesta = fib_seq[min(fib_index, len(fib_seq) - 1)] * apuesta_inicial
#             elif estrategia == 'p':
#                 apuesta = apuesta_inicial
#                 victorias_consecutivas = 0

#         saldo_corrida.append(saldo)

#         if gano:
#             exitos_por_tirada[tirada] += 1

#     saldo_final.append(saldo if saldo != float('inf') else capital_inicial)
#     capital_evolucion[:len(saldo_corrida)] += saldo_corrida

# Simulación corregida
for corrida in range(cant_corridas):
    # En infinito empezamos con el capital base pero permitimos saldos negativos
    saldo = args.capital 
    apuesta_inicial = 10
    apuesta = apuesta_inicial
    fib_index = 0
    victorias_consecutivas = 0
    saldo_corrida = []

    for tirada in range(cant_tiradas):
        # El control de quiebra SOLO se ejecuta si el capital es FINITO ('f')
        if capital_tipo == 'f' and saldo <= 0:
            quiebras += 1
            quiebras_tiradas[tirada] += 1
            # Rellenamos el resto de la corrida con 0 porque quebró
            saldo_corrida += [0] * (cant_tiradas - tirada)
            break

        numero = random.randint(0, 36)
        color  = obtener_color(numero)
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
                    # En infinito no hay límite superior por saldo
                    apuesta = apuesta * 2 if capital_tipo == 'i' else min(saldo, apuesta * 2)
        else:
            saldo -= apuesta
            if estrategia == 'm':
                apuesta *= 2
            elif estrategia == 'd':
                apuesta += apuesta_inicial
            elif estrategia == 'f':
                fib_index += 1
                apuesta = fib_seq[min(fib_index, len(fib_seq) - 1)] * apuesta_inicial
            elif estrategia == 'p':
                apuesta = apuesta_inicial
                victorias_consecutivas = 0

        saldo_corrida.append(saldo)
        exitos_por_tirada[tirada] += 1 if gano else 0

    # Guardamos el saldo final de la corrida
    saldo_final.append(saldo)
    # Por cuestiones de tipo convertimos a numpy para que no falle la suma con capital_evolucion que es un array
    vector_saldo = np.array(saldo_corrida, dtype=np.float64)
    capital_evolucion[:len(vector_saldo)] += vector_saldo

# Resultados

saldo_promedio = np.mean(saldo_final)
print("\n--- Resultados ---")
print(f"Saldo promedio final después de {cant_corridas} corridas: {saldo_promedio:.2f}")
print(f"Veces que hubo bancarrota: {quiebras} de {cant_corridas}")

# Graficas 

plt.figure(figsize=(8, 5))
frsa = exitos_por_tirada / cant_corridas
plt.bar(range(1, len(frsa) + 1), frsa, color='red', edgecolor='black')
plt.title('Frecuencia relativa de obtener apuesta favorable (frsa)')
plt.xlabel('Número de tirada (n)')
plt.ylabel('Frecuencia relativa (fr)')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('Frecuencia relativa 1C.png')
plt.close()

plt.figure(figsize=(8, 5))
capital_promedio = capital_evolucion / cant_corridas
plt.plot(range(1, len(capital_promedio) + 1), capital_promedio, color='red', label='fc (flujo de caja)')
plt.axhline(y=capital_inicial if capital_tipo == 'f' else args.capital,
            color='blue', linestyle='--', label='fci (flujo de caja inicial)')

quiebra_indices = np.where(quiebras_tiradas > 0)[0]
for idx in quiebra_indices:
    plt.axvline(x=idx + 1, color='black', linestyle=':', alpha=0.5)

from matplotlib.lines import Line2D
quiebra_line = Line2D([0], [0], color='black', linestyle=':', label='quiebra')

handles, labels = plt.gca().get_legend_handles_labels()
handles.append(quiebra_line)
labels.append('quiebra')
plt.legend(handles, labels)

plt.title('Evolución del capital promedio')
plt.xlabel('Número de tirada (n)')
plt.ylabel('Cantidad de capital (cc)')
plt.grid(True)
plt.tight_layout()
plt.savefig('Promedio 1C.png')
plt.close()