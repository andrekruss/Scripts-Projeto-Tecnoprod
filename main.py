import subprocess

scripts = [
    "balanca.py",
    "impressoras.py",
    "leitor_calibradora.py",
    "leitores_insersora.py",
    "leitor_gravadora.py"
]

processos = []

for script in scripts:
    p = subprocess.Popen(
        ["cmd", "/c", "start", "cmd", "/k", "python", script]
    )
    processos.append(p)

print("Simuladores iniciados...")

input("Pressione ENTER para parar tudo...")
