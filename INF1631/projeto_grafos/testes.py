"""
Testes obrigatorios do projeto (secao 8 do enunciado).

Execute com:  python testes.py
"""

from projeto_grafos import (
    circuito_euler, conexo, euleriano, formata_circuito, grafo_de_arestas,
    graus, valida_circuito,
)


def mostra(nome, G):
    g = graus(G)
    C = circuito_euler(G)
    print(f"== {nome} ==")
    print(f"Graus: {g}")
    print(f"Conexo: {conexo(G)} | Graus pares: {all(d % 2 == 0 for d in g)} | Euleriano: {euleriano(G)}")
    print(f"Circuito: {formata_circuito(C) if C else 'nao existe'}")
    return C


def teste_ciclo_c4():
    # C4: 1-2-3-4-1, todos os vertices com grau 2
    G = grafo_de_arestas(4, [(1, 2), (2, 3), (3, 4), (4, 1)])
    C = mostra("Grafo com Euler (ciclo C4)", G)
    assert euleriano(G)
    assert C is not None and valida_circuito(G, C)
    print("Resultado: circuito valido encontrado -> OK\n")


def teste_caminho_p4():
    # P4: 1-2-3-4, as pontas 1 e 4 tem grau 1 (impar)
    G = grafo_de_arestas(4, [(1, 2), (2, 3), (3, 4)])
    C = mostra("Vertices impares (caminho P4)", G)
    assert conexo(G)
    assert not euleriano(G)
    assert C is None
    print("Resultado: nao possui circuito de Euler -> OK\n")


def teste_desconexo():
    # Dois triangulos disjuntos: 1-2-3-1 e 4-5-6-4. Todos os graus sao pares,
    # mas os vertices de grau nao nulo estao em duas componentes.
    G = grafo_de_arestas(6, [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)])
    C = mostra("Grafo desconexo (duas componentes ciclicas)", G)
    assert all(d % 2 == 0 for d in graus(G))
    assert not conexo(G)
    assert not euleriano(G)
    assert C is None
    print("Resultado: nao possui circuito de Euler -> OK\n")


def teste_grafo_vazio():
    # Sem arestas: tratado explicitamente em euleriano() como rede nao adequada
    G = grafo_de_arestas(4, [])
    C = mostra("Grafo vazio (sem arestas)", G)
    assert sum(graus(G)) == 0
    assert not euleriano(G)
    assert C is None
    assert not valida_circuito(G, C)
    print("Resultado: caso tratado explicitamente (sem ruas, sem circuito) -> OK\n")


def teste_validacao_rejeita_circuitos_errados():
    # Garante que valida_circuito nao aceita qualquer coisa
    G = grafo_de_arestas(4, [(1, 2), (2, 3), (3, 4), (4, 1)])
    print("== Validacao rejeita circuitos invalidos ==")
    assert not valida_circuito(G, [0, 1, 2, 3])        # nao volta ao inicio
    assert not valida_circuito(G, [0, 1, 0])           # repete aresta e nao usa todas
    assert not valida_circuito(G, [0, 2, 1, 3, 0])     # usa pares que nao sao arestas
    assert not valida_circuito(G, [0, 1, 2, 3, 0, 1, 2, 3, 0])  # repete arestas
    assert valida_circuito(G, [0, 3, 2, 1, 0])         # sentido inverso tambem e valido
    print("Resultado: OK\n")


if __name__ == "__main__":
    teste_ciclo_c4()
    teste_caminho_p4()
    teste_desconexo()
    teste_grafo_vazio()
    teste_validacao_rejeita_circuitos_errados()
    print("Todos os testes obrigatorios passaram.")
