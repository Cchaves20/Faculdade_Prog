"""Biblioteca deterministica fornecida pelo professor. Python 3.10+."""
from __future__ import annotations
import time

USUARIOS = {
    1: {"nome": "Ana", "ativo": True},
    2: {"nome": "Bruno", "ativo": False},
    3: {"nome": "Carla", "ativo": True},
}
PRODUTOS = {
    10: {"preco": 100.0, "estoque": 5},
    20: {"preco": 250.0, "estoque": 3},
    30: {"preco": 40.0, "estoque": 0},
}
LEITURAS = {
    101: {"temperatura": 28.0, "pressao": 3.5},
    102: {"temperatura": 78.0, "pressao": 7.0},
}

def buscar_usuario(usuario_id):
    return USUARIOS[usuario_id]["nome"]

def usuario_ativo(usuario_id):
    return USUARIOS[usuario_id]["ativo"]

def buscar_preco(produto_id):
    return PRODUTOS[produto_id]["preco"]

def verificar_estoque(produto_id):
    return PRODUTOS[produto_id]["estoque"]

def calcular_total(preco, quantidade):
    return preco * quantidade

def aplicar_desconto(valor, percentual):
    return round(valor * (1 - percentual / 100), 2)

def registrar_pedido(usuario, valor):
    print(f"PEDIDO: {usuario} - R$ {valor:.2f}")
    return True

def ler_temperatura(sensor_id):
    return LEITURAS[sensor_id]["temperatura"]

def ler_pressao(sensor_id):
    return LEITURAS[sensor_id]["pressao"]

def verificar_limite(valor, limite):
    return valor > limite

def gerar_alerta(mensagem):
    print(f"ALERTA: {mensagem}")
    return True

def carregar_valores(conjunto):
    dados = {"a": [2, 4, 6], "b": [10, 20, 30], "vazio": []}
    return list(dados[conjunto])

def contar_valores(valores):
    return len(valores)

def somar_valores(valores):
    return sum(valores)

def calcular_media(valores):
    return sum(valores) / len(valores) if valores else 0

def maior_valor(valores):
    return max(valores) if valores else 0

def registrar_log(mensagem):
    print(f"LOG: {mensagem}")
    return True

def esperar(segundos):
    if segundos < 0 or segundos > 3:
        raise ValueError("esperar aceita de 0 a 3 segundos")
    time.sleep(segundos)
    return segundos

def consultar_sistema_a(numero):
    time.sleep(1)
    return numero * 10

def consultar_sistema_b(numero):
    time.sleep(2)
    return numero * 20

def combinar_resultados(a, b):
    return a + b
