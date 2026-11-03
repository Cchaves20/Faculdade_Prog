"""Auxiliar opcional para blocos PARALELO (bonus)."""
from concurrent.futures import ThreadPoolExecutor

def executar_paralelo(tarefas):
    """Recebe lista de pares (nome_saida, callable_sem_argumentos).
    Executa todas as tarefas em paralelo, espera todas terminarem e
    devolve dicionario {nome_saida: resultado}, na ordem de entrada.
    Exemplo: executar_paralelo([("a", lambda: funcao(1)), ...]).
    """
    nomes = [nome for nome, _ in tarefas]
    if len(nomes) != len(set(nomes)):
        raise ValueError("Saidas duplicadas no bloco paralelo")
    with ThreadPoolExecutor(max_workers=max(1, len(tarefas))) as executor:
        futuros = [executor.submit(funcao) for _, funcao in tarefas]
        return {nome: futuro.result() for nome, futuro in zip(nomes, futuros)}
