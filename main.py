import sys
import os

from parser import analisar
from gerador import gerar

# le o programa .orq que foi passado na linha de comando
arquivo = open(sys.argv[1], encoding="utf-8")
codigo = arquivo.read()
arquivo.close()

linhas = analisar(codigo)

if linhas == None:
    sys.exit(1)

# exemplos/01_basico.orq -> gerado/01_basico.py
nome = os.path.basename(sys.argv[1])
nome = nome.replace(".orq", ".py")
saida = os.path.join("gerado", nome)

os.makedirs("gerado", exist_ok=True)
arquivo = open(saida, "w", encoding="utf-8")
arquivo.write(gerar(linhas))
arquivo.close()
print("gerado", saida)