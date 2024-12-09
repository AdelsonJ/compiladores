import subprocess
import sys

# Confere se os parametros foram digitados corretamente
if len(sys.argv) != 2:
    print("Por favor, informe o nome do arquivo de entrada como argumento")
    sys.exit()

# Copia os valores pras variaveis
entrada = sys.argv[1]


subprocess.run(["python3.12", "lexico.py", entrada])
subprocess.run(["python3.12", "sintatico.py", "tokens.json"])