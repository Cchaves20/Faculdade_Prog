# testa todos os exemplos e os invalidos
# rodar dentro da pasta INF-1022: python testar.py

import os
import sys
import subprocess

# pro python gerado achar a pasta runtime
ambiente = os.environ.copy()
ambiente["PYTHONPATH"] = "."


def ler(caminho):
    arquivo = open(caminho, encoding="utf-8")
    texto = arquivo.read()
    arquivo.close()
    return texto


# nos esperados do 01 ao 06 o \n ta escrito como texto, so o 07 tem quebra de linha de verdade
def arrumar(texto):
    texto = texto.replace("\\n", "\n")
    texto = texto.replace("\r\n", "\n")
    return texto.strip()


# se o python deu Traceback, o main travou (bug nosso), nao eh rejeicao de verdade
# devolve a ultima linha do erro, que eh a que diz o que aconteceu
def travou(r):
    if "Traceback" in r.stderr:
        return r.stderr.strip().splitlines()[-1]
    return None


print("Exemplos:")
exemplos = sorted(os.listdir("exemplos"))
certos = 0

for nome in exemplos:
    base = nome.replace(".orq", "")
    gerado = "gerado/" + base + ".py"

    # apaga o gerado antigo senao ele pode testar um arquivo velho
    if os.path.exists(gerado):
        os.remove(gerado)

    r = subprocess.run([sys.executable, "main.py", "exemplos/" + nome], capture_output=True, text=True)
    if travou(r):
        print("  TRAVOU", nome, "->", travou(r))
        continue
    if r.returncode != 0:
        print("  ERRO", nome, "->", r.stdout.strip())
        continue

    r = subprocess.run([sys.executable, gerado], capture_output=True, text=True, env=ambiente)
    esperado = ler("testes/" + base + ".esperado.txt")

    if arrumar(r.stdout) == arrumar(esperado):
        print("  ok  ", nome)
        certos = certos + 1
    else:
        print("  ERRO", nome, "-> saida diferente")
        print("       esperado:", arrumar(esperado))
        print("       veio:    ", arrumar(r.stdout), r.stderr.strip())


print()
print("Invalidos (tem que dar erro):")
invalidos = sorted(os.listdir("testes/invalidos"))
rejeitados = 0

for nome in invalidos:
    r = subprocess.run([sys.executable, "main.py", "testes/invalidos/" + nome], capture_output=True, text=True)
    if travou(r):
        print("  TRAVOU", nome, "->", travou(r))
    elif r.returncode != 0:
        print("  ok  ", nome, "->", r.stdout.strip())
        rejeitados = rejeitados + 1
    else:
        print("  ERRO", nome, "-> foi aceito")


print()
print("exemplos:", certos, "de", len(exemplos))
print("invalidos rejeitados:", rejeitados, "de", len(invalidos))
