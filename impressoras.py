import socket
import threading
import time
from datetime import datetime

HOST = "0.0.0.0"

# portas simuladas
IMPRESSORAS = {
    "MANTA": 9100,
    "CALIBRACAO": 9101,
    "INSERCAO": 9102
}

ENCODING = "utf-8"


class SimuladorImpressora:
    def __init__(self, nome, porta):
        self.nome = nome
        self.porta = porta

    def salvar_zpl(self, conteudo):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        nome_arquivo = f"{self.nome}_{timestamp}.zpl"

        with open(nome_arquivo, "w", encoding=ENCODING) as f:
            f.write(conteudo)

    def cliente_thread(self, conn, addr):
        print(f"[{self.nome}] Conectado: {addr}")

        dados = b""

        try:
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                dados += chunk

            if dados:
                zpl = dados.decode(ENCODING, errors="ignore")

                print(f"\n[{self.nome}] ===== ZPL RECEBIDO =====")
                print(zpl)
                print(f"[{self.nome}] ========================\n")

                self.salvar_zpl(zpl)

        except Exception as e:
            print(f"[{self.nome}] Erro: {e}")

        finally:
            conn.close()
            print(f"[{self.nome}] Conexão encerrada")

    def iniciar(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((HOST, self.porta))
        servidor.listen()

        print(f"[{self.nome}] Escutando porta {self.porta}")

        while True:
            conn, addr = servidor.accept()

            threading.Thread(
                target=self.cliente_thread,
                args=(conn, addr),
                daemon=True
            ).start()


# =========================
# INICIA IMPRESSORAS
# =========================

for nome, porta in IMPRESSORAS.items():
    sim = SimuladorImpressora(nome, porta)

    threading.Thread(
        target=sim.iniciar,
        daemon=True
    ).start()

print("Simuladores de impressora ativos...")

while True:
    time.sleep(1)
