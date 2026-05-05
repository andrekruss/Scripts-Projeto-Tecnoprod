import serial
import threading
import time
import sys
import random

# ==========================
# CONFIGURAÇÃO
# ==========================
PORTA = "COM8"
BAUDRATE = 9600
INTERVALO_ENVIO = 0.1  # segundos

# peso alvo (definido pelo usuário)
peso_alvo = 0.0

# peso atual simulado (o que a balança "mede")
peso_simulado = 0.0

lock = threading.Lock()

# parâmetros da simulação
VELOCIDADE_APROX = 0.15     # quão rápido chega no alvo (0.05 = lento, 0.3 = rápido)
RUIDO_MAX = 1          # variação aleatória (kg)
ZONA_ESTAVEL = 0.005       # zona onde praticamente estabiliza


# ==========================
# GERA FRAME PROTOCOLO
# ==========================
def gerar_frame(peso_kg: float) -> bytes:
    valor = int(peso_kg * 100_000_000)
    texto = f"+{valor:011d}"
    return (texto + "\r").encode("ascii")


# ==========================
# THREAD DE ENVIO (RAMPA)
# ==========================
def thread_envio(ser: serial.Serial):
    global peso_simulado, peso_alvo

    while True:
        with lock:
            diferenca = peso_alvo - peso_simulado

            # movimento em rampa (aproximação suave)
            if abs(diferenca) > ZONA_ESTAVEL:
                peso_simulado += diferenca * VELOCIDADE_APROX
            else:
                # quando está muito próximo, praticamente estabiliza
                peso_simulado = peso_alvo

            # adiciona ruído (simula vibração da balança)
            variacao = random.uniform(-RUIDO_MAX, RUIDO_MAX)
            peso_final = max(0, peso_simulado + variacao)

            frame = gerar_frame(peso_final)

        ser.write(frame)
        time.sleep(INTERVALO_ENVIO)


# ==========================
# THREAD DE INPUT
# ==========================
def thread_input():
    global peso_alvo

    while True:
        try:
            valor = input("Digite novo peso alvo (kg): ").strip()

            if valor.lower() == "exit":
                print("Encerrando simulador...")
                sys.exit(0)

            novo_peso = float(valor)

            with lock:
                peso_alvo = novo_peso

            print(f"Novo peso alvo -> {novo_peso} kg")

        except Exception:
            print("Valor inválido.")


# ==========================
# MAIN
# ==========================
def main():
    print("Iniciando simulador de balança (modo rampa)...")

    ser = serial.Serial(
        port=PORTA,
        baudrate=BAUDRATE,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=1
    )

    print(f"Transmitindo na porta {PORTA}")

    threading.Thread(target=thread_envio, args=(ser,), daemon=True).start()
    threading.Thread(target=thread_input, daemon=True).start()

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()