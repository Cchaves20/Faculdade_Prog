"""
Projeto de Estruturas Discretas - Grafos (INF1631 - 3WB, 2026)
"O robo consegue inspecionar toda a rede?"

Grupo C: n = 10, p = 0.30, seed = 391

O grafo e representado por uma matriz de adjacencia G (lista de listas),
em que G[u][v] = 1 se existe a aresta {u, v} e 0 caso contrario.
Internamente os vertices sao numerados de 0 a n-1; na saida eles sao
exibidos de 1 a n, como no enunciado (V = {1, 2, ..., 10}).

Nenhuma biblioteca de grafos e utilizada: apenas `random` (gerador de
numeros aleatorios), `time` (medicao de tempo), `argparse` (parametros) e
`collections.deque` (fila da busca em largura).
"""

import argparse
import random
import time
from collections import deque

# Parametros do Grupo C
N = 10
P = 0.30
SEED = 391
QTD_EXPERIMENTO = 1000
MAX_TENTATIVAS = 1_000_000  # evita laco infinito se p tornar impossivel achar um grafo Euleriano


# ---------------------------------------------------------------------------
# Algoritmos obrigatorios
# ---------------------------------------------------------------------------

def gerar_grafo(n, p):
    """Gera um grafo simples nao direcionado com n vertices.

    Para cada par de vertices distintos {u, v} (sao n(n-1)/2 pares), a aresta
    e incluida com probabilidade p. Usa o gerador global `random`, que deve
    ter sido inicializado com a seed do grupo (random.seed(SEED)).
    """
    G = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                G[u][v] = 1
                G[v][u] = 1
    return G


def graus(G):
    """Retorna a lista de graus: grau(v) = soma da linha v da matriz."""
    return [sum(linha) for linha in G]


def conexo(G):
    """Verifica se todos os vertices de grau nao nulo estao na mesma componente.

    Faz uma busca em largura (BFS) a partir do primeiro vertice com grau > 0
    e confere se todos os vertices com grau > 0 foram alcancados.
    Vertices isolados (grau 0) sao ignorados, pois nao ha ruas neles.
    Em um grafo sem arestas nao existe vertice de grau nao nulo, entao a
    condicao e verdadeira por vacuidade (o caso e tratado em euleriano()).
    """
    n = len(G)
    g = graus(G)
    nao_isolados = [v for v in range(n) if g[v] > 0]
    if not nao_isolados:
        return True

    inicio = nao_isolados[0]
    visitado = [False] * n
    visitado[inicio] = True
    fila = deque([inicio])
    while fila:
        u = fila.popleft()
        for v in range(n):
            if G[u][v] and not visitado[v]:
                visitado[v] = True
                fila.append(v)

    return all(visitado[v] for v in nao_isolados)


def euleriano(G):
    """Decide se G possui circuito de Euler usando os criterios da disciplina:

    1. todos os vertices de grau nao nulo pertencem a mesma componente conexa;
    2. todos esses vertices (de grau nao nulo) possuem grau par.

    Caso especial (tratado explicitamente): grafo sem arestas. Os dois
    criterios seriam satisfeitos por vacuidade, mas nao ha nenhuma rua para
    o robo inspecionar e nenhum circuito pode ser construido, entao o grafo
    vazio NAO e considerado uma rede adequada.
    """
    g = graus(G)
    if sum(g) == 0:
        return False

    criterio_conexo = conexo(G)
    criterio_pares = all(d % 2 == 0 for d in g if d > 0)
    return criterio_conexo and criterio_pares


def circuito_euler(G):
    """Constroi um circuito de Euler com o algoritmo de Hierholzer.

    Retorna a lista de vertices do circuito (o primeiro igual ao ultimo),
    ou None se o grafo nao for Euleriano.

    Versao iterativa: anda pelo grafo removendo cada aresta usada (em uma
    copia da matriz). Quando o vertice do topo da pilha nao tem mais arestas,
    ele e movido para o circuito. Isso emenda automaticamente os sub-ciclos.
    """
    if not euleriano(G):
        return None

    n = len(G)
    A = [linha[:] for linha in G]  # copia: as arestas sao removidas ao serem usadas
    inicio = next(v for v in range(n) if any(A[v]))

    pilha = [inicio]
    circuito = []
    while pilha:
        u = pilha[-1]
        v = next((w for w in range(n) if A[u][w]), None)
        if v is None:
            circuito.append(pilha.pop())
        else:
            A[u][v] = 0
            A[v][u] = 0
            pilha.append(v)

    circuito.reverse()
    return circuito


def valida_circuito(G, C):
    """Verifica automaticamente se C e um circuito de Euler valido em G:

    - C comeca e termina no mesmo vertice;
    - cada par consecutivo de C e uma aresta de G;
    - nenhuma aresta e usada mais de uma vez;
    - todas as arestas de G sao usadas.
    """
    if not C or len(C) < 2:
        return False
    n = len(G)
    if any(not (0 <= v < n) for v in C):
        return False
    if C[0] != C[-1]:
        return False

    usadas = set()
    for u, v in zip(C, C[1:]):
        if not G[u][v]:
            return False  # passo que nao corresponde a uma aresta
        aresta = (min(u, v), max(u, v))
        if aresta in usadas:
            return False  # aresta percorrida mais de uma vez
        usadas.add(aresta)

    return usadas == set(arestas(G))  # todas as arestas foram usadas


# ---------------------------------------------------------------------------
# Funcoes auxiliares
# ---------------------------------------------------------------------------

def arestas(G):
    """Lista de arestas (u, v) com u < v, em indices internos (0..n-1)."""
    n = len(G)
    return [(u, v) for u in range(n) for v in range(u + 1, n) if G[u][v]]


def grafo_de_arestas(n, lista):
    """Monta a matriz de adjacencia a partir de arestas numeradas de 1 a n."""
    G = [[0] * n for _ in range(n)]
    for u, v in lista:
        G[u - 1][v - 1] = 1
        G[v - 1][u - 1] = 1
    return G


def formata_arestas(G):
    return " ".join(f"({u + 1},{v + 1})" for u, v in arestas(G))


def formata_circuito(C):
    return " -> ".join(str(v + 1) for v in C)


def formata_matriz(G):
    n = len(G)
    cab = "     " + " ".join(f"{v + 1:>2}" for v in range(n))
    linhas = [cab]
    for u in range(n):
        linhas.append(f"{u + 1:>3}: " + " ".join(f"{x:>2}" for x in G[u]))
    return "\n".join(linhas)


def sim_nao(b):
    return "sim" if b else "nao"


# ---------------------------------------------------------------------------
# Experimentos
# ---------------------------------------------------------------------------

def experimento_primeiro_euleriano(n, p, seed):
    """Gera grafos ate encontrar o primeiro com circuito de Euler."""
    random.seed(seed)
    gerados = 0
    while True:
        G = gerar_grafo(n, p)
        gerados += 1
        if euleriano(G):
            break
        if gerados >= MAX_TENTATIVAS:
            print(f"Nenhum grafo Euleriano encontrado em {gerados} tentativas "
                  f"(n = {n}, p = {p:.2f}, seed = {seed}).")
            return None, gerados

    g = graus(G)
    C = circuito_euler(G)

    print(f"Numero de vertices: {n}")
    print(f"Probabilidade p: {p:.2f}")
    print(f"Seed: {seed}")
    print()
    print("Grafo Euleriano encontrado!")
    print(f"Numero de grafos gerados: {gerados}")
    print()
    print("Matriz de adjacencia:")
    print(formata_matriz(G))
    print()
    print(f"Arestas ({len(arestas(G))}):")
    print(formata_arestas(G))
    print()
    print("Graus:")
    for v in range(n):
        print(f"v{v + 1}: {g[v]}")
    print()
    print(f"Conexo (vertices de grau nao nulo): {sim_nao(conexo(G))}")
    print(f"Todos os graus sao pares: {sim_nao(all(d % 2 == 0 for d in g))}")
    print(f"Euleriano: {sim_nao(euleriano(G))}")
    print()
    print("Circuito de Euler:")
    print(formata_circuito(C))
    print(f"Validacao do circuito: {'OK' if valida_circuito(G, C) else 'FALHOU'}")

    return G, gerados


def experimento_estatistico(n, p, seed, qtd):
    """Gera `qtd` grafos independentes e conta quantos sao Eulerianos.

    O gerador e reinicializado com a mesma seed, para que o experimento seja
    reproduzivel. Alem do total exigido, conta separadamente as condicoes
    (graus pares / conexidade) para apoiar a analise do relatorio.
    """
    random.seed(seed)

    qtd_euler = 0
    qtd_pares = 0
    qtd_conexo = 0
    qtd_vazios = 0
    impares = {}  # numero de vertices de grau impar -> quantos grafos
    tempo_geracao = 0.0

    inicio_total = time.perf_counter()
    for _ in range(qtd):
        t0 = time.perf_counter()
        G = gerar_grafo(n, p)
        tempo_geracao += time.perf_counter() - t0

        if euleriano(G):
            qtd_euler += 1
        g = graus(G)
        if sum(g) == 0:
            qtd_vazios += 1
        if all(d % 2 == 0 for d in g):
            qtd_pares += 1
        if conexo(G):
            qtd_conexo += 1
        k = sum(d % 2 for d in g)
        impares[k] = impares.get(k, 0) + 1
    tempo_total = time.perf_counter() - inicio_total

    proporcao = qtd_euler / qtd

    print(f"Experimento com {qtd} grafos (n = {n}, p = {p:.2f}, seed = {seed}):")
    print(f"Tempo gasto na geracao dos grafos: {tempo_geracao:.4f} s")
    print(f"Tempo total (geracao + verificacao): {tempo_total:.4f} s")
    print(f"Grafos Eulerianos: {qtd_euler}")
    print(f"Proporcao: {proporcao:.3f}")
    print()
    print("Detalhamento (para a analise):")
    print(f"  Grafos com todos os graus pares: {qtd_pares}")
    print(f"  Grafos com vertices de grau nao nulo conexos: {qtd_conexo}")
    print(f"  Grafos sem arestas: {qtd_vazios}")
    print("  Numero de vertices de grau impar por grafo:")
    for k in sorted(impares):
        print(f"    {k:>2} vertices impares: {impares[k]} grafos")

    return qtd_euler, proporcao


def main():
    parser = argparse.ArgumentParser(
        description="Projeto de Estruturas Discretas - circuito de Euler em grafos aleatorios")
    parser.add_argument("--n", type=int, default=N, help=f"numero de vertices (padrao {N})")
    parser.add_argument("--p", type=float, default=P, help=f"probabilidade de cada aresta (padrao {P})")
    parser.add_argument("--seed", type=int, default=SEED, help=f"semente do gerador (padrao {SEED})")
    parser.add_argument("--qtd", type=int, default=QTD_EXPERIMENTO,
                        help=f"grafos no experimento computacional (padrao {QTD_EXPERIMENTO})")
    args = parser.parse_args()

    experimento_primeiro_euleriano(args.n, args.p, args.seed)
    print("--------------------------------")
    experimento_estatistico(args.n, args.p, args.seed, args.qtd)


if __name__ == "__main__":
    main()
