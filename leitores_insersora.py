import socket
import threading

LEITORES = {
    1: {"nome": "ESQ", "porta": 6001, "fila": []},
    2: {"nome": "DIR", "porta": 6002, "fila": []},
    3: {"nome": "CENTRO", "porta": 6003, "fila": []},
}


def servidor(leitor):
    nome = leitor["nome"]
    porta = leitor["porta"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", porta))
        s.listen()

        print(f"[{nome}] ouvindo porta {porta}")

        while True:
            conn, addr = s.accept()
            print(f"[{nome}] conectado:", addr)

            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    cmd = data.decode().strip()

                    if cmd == "LON":
                        print(f"[{nome}] TRIGGER ON")

                        if leitor["fila"]:
                            codigo = leitor["fila"].pop(0)
                            conn.sendall((codigo + "\r").encode())
                            print(f"[{nome}] enviado:", codigo)
                        else:
                            print(f"[{nome}] sem código (timeout simulado)")

                    elif cmd == "LOFF":
                        print(f"[{nome}] TRIGGER OFF")


def console():
    print("\n=== SIMULADOR SRX300 ===")

    while True:
        try:
            leitor_num = int(input("\nDigite o leitor (1=Esq, 2=Dir, 3=Centro): "))

            if leitor_num not in LEITORES:
                print("leitor inválido")
                continue

            codigo = input("Digite o código lido: ").strip()

            if not codigo:
                print("código vazio")
                continue

            LEITORES[leitor_num]["fila"].append(codigo)

            print(f"[{LEITORES[leitor_num]['nome']}] código adicionado")

        except:
            print("entrada inválida")


# inicia servidores
for leitor in LEITORES.values():
    threading.Thread(target=servidor, args=(leitor,), daemon=True).start()

# inicia console
console()
