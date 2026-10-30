# Gerador: junta as linhas que o parser montou num programa python

# recebe a lista de linhas e devolve o texto do arquivo .py
def gerar(linhas):
    codigo = "from runtime.servicos import *\n\n"
    codigo = codigo + "\n".join(linhas) + "\n"
    return codigo
