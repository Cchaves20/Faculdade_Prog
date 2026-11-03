# Instruções de execução — Projeto de Estruturas Discretas (Grafos)

**Grupo C** — n = 10, p = 0,30, seed = 391

## Requisitos

- Python 3.8 ou superior.
- Nenhuma biblioteca externa: o programa usa apenas módulos da biblioteca padrão
  (`random`, `time`, `argparse`, `collections`).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `projeto_grafos.py` | Programa principal: funções `gerar_grafo`, `graus`, `conexo`, `euleriano`, `circuito_euler`, `valida_circuito` e os dois experimentos |
| `testes.py` | Testes obrigatórios (C4, P4, grafo desconexo, grafo vazio) |
| `saida.txt` | Saída obtida na execução com os parâmetros do grupo |
| `relatorio.md` | Relatório com a implementação, os resultados e a análise |

## Como executar

Na pasta do projeto, rode:

```
python projeto_grafos.py
```

(Em Linux/macOS, se o comando `python` não existir, use `python3`.)

O programa já usa os parâmetros do Grupo C por padrão. Ele:

1. gera grafos aleatórios até encontrar o primeiro com circuito de Euler e mostra
   a matriz de adjacência, as arestas, os graus, a conectividade, o circuito e a validação;
2. gera 1000 grafos com os mesmos n, p e seed e mostra o tempo, o número de grafos
   Eulerianos e a proporção.

Para rodar os testes obrigatórios:

```
python testes.py
```

### Parâmetros opcionais

Os parâmetros podem ser passados pela linha de comando (os valores padrão são os do Grupo C):

```
python projeto_grafos.py --n 10 --p 0.30 --seed 391 --qtd 1000
```

Para salvar a saída em um arquivo:

```
python projeto_grafos.py > saida.txt
```
