import socket

IP = "127.0.0.1"   # IP do seu sistema
PORTA = 5001       # mesma porta do LeitorHRX500WB
ENCODING = "ascii"

print("=== Simulador HRX500WB ===")

while True:
    codigo = input("\nDigite o código (ou 'sair'): ").strip()

    if codigo.lower() == "sair":
        break

    if not codigo:
        continue

    try:
        print("Conectando...")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((IP, PORTA))

            mensagem = (codigo + "\r\n").encode(ENCODING)
            s.sendall(mensagem)

            print(f"Código enviado: {codigo}")

    except Exception as e:
        print(f"Erro: {e}")

print("Simulador finalizado.")
