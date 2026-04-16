import serial
import threading
import time
import sys

# ==========================
# CONFIGURAÇÃO
# ==========================
PORTA = "COM8"      # porta que seu sistema vai ler
BAUDRATE = 9600
INTERVALO_ENVIO = 0.1  # segundos entre frames

# peso atual em kg
peso_atual = 0.0
lock = threading.Lock()


# ==========================
# GERA FRAME PROTOCOLO PRT2
# ==========================
def gerar_frame(peso_kg: float) -> bytes:
    """
    Sua balança envia peso * 10^8
    """
    valor = int(peso_kg * 100_000_000)

    # exemplo: +00012.340
    texto = f"+{valor:011d}"

    # adiciona CR
    return (texto + "\r").encode("ascii")


# ==========================
# THREAD DE ENVIO CONTÍNUO
# ==========================
def thread_envio(ser: serial.Serial):
    global peso_atual

    while True:
        with lock:
            frame = gerar_frame(peso_atual)

        ser.write(frame)
        time.sleep(INTERVALO_ENVIO)


# ==========================
# THREAD DE INPUT DO USUÁRIO
# ==========================
def thread_input():
    global peso_atual

    while True:
        try:
            valor = input("Digite novo peso (kg): ").strip()

            if valor.lower() == "exit":
                print("Encerrando simulador...")
                sys.exit(0)

            novo_peso = float(valor)

            with lock:
                peso_atual = novo_peso

            print(f"Peso atualizado -> {novo_peso} kg")

        except Exception:
            print("Valor inválido.")


# ==========================
# MAIN
# ==========================
def main():
    print("Iniciando simulador de balança...")

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
