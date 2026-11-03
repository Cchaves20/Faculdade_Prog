# Trabalho Final INF1022 - OrqLang

Transpilador de OrqLang (.orq) pra Python, feito com PLY.

Integrantes:
- Caio Faria Brito - 2410162
- Lucas André Guimarães - 2411658

## Instalação

Precisa de Python 3.10 ou mais novo e do PLY:

```
pip install ply
```

## Como rodar

Rode tudo de dentro desta pasta.

Pra transpilar um programa:

```
python main.py exemplos/01_basico.orq
```

Isso cria o arquivo `gerado/01_basico.py`. Se o programa tiver erro, aparece a
mensagem com a linha e o token, e nenhum arquivo é gerado.

Pra executar o Python gerado, a pasta atual precisa estar no PYTHONPATH (por
causa do `from runtime.servicos import *`):

```
# PowerShell
$env:PYTHONPATH = "."
python gerado/01_basico.py

# Linux / Mac
PYTHONPATH=. python gerado/01_basico.py
```

## Testes

```
python testar.py
```

O script transpila e roda cada exemplo da pasta `exemplos/`, compara a saída
com o `.esperado.txt` correspondente em `testes/` e depois confere se todos os
programas de `testes/invalidos/` dão erro. No final ele mostra quantos passaram
(hoje são 10 de 10 nos dois).

Também dá pra testar as partes separadas:

```
python lexer.py exemplos/01_basico.orq    # mostra os tokens
python parser.py exemplos/01_basico.orq   # diz se aceitou e mostra o código gerado
```

## Arquivos

- `lexer.py`, `parser.py` e `gerador.py`: o transpilador em si
- `main.py`: lê o .orq e escreve o .py em `gerado/`
- `testar.py`: script de testes
- `runtime/`: serviços que vieram no kit do professor
- `exemplos/`: os exemplos 01 a 07 vieram do kit; o 08, o 09 e o 10 fizemos nós
- `testes/invalidos/`: os casos 1 a 3 vieram do `invalidos.orq.txt` do kit; os outros fizemos nós
- `RELATORIO.md`: relatório
