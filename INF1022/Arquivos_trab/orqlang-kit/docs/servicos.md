# Catálogo de serviços (Python 3.10+)

Todas as funções são importadas de `runtime.servicos`. São determinísticas, exceto pelo tempo de espera explicitamente indicado. Não usam internet nem banco de dados.

| Função | Argumentos | Retorno |
|---|---|---|
| buscar_usuario | usuario_id: int | str |
| usuario_ativo | usuario_id: int | bool |
| buscar_preco | produto_id: int | float |
| verificar_estoque | produto_id: int | int |
| calcular_total | preco: number, quantidade: number | number |
| aplicar_desconto | valor: number, percentual: number | float |
| registrar_pedido | usuario: str, valor: number | bool; imprime PEDIDO |
| ler_temperatura | sensor_id: int | float |
| ler_pressao | sensor_id: int | float |
| verificar_limite | valor: number, limite: number | bool |
| gerar_alerta | mensagem: str | bool; imprime ALERTA |
| carregar_valores | conjunto: str ("a", "b", "vazio") | list |
| contar_valores | valores: list | int |
| somar_valores | valores: list | number |
| calcular_media | valores: list | number (0 se vazio) |
| maior_valor | valores: list | number (0 se vazio) |
| registrar_log | mensagem: str | bool; imprime LOG |
| esperar | segundos: number (0..3) | number; aguarda |
| consultar_sistema_a | numero: number | number; espera 1s |
| consultar_sistema_b | numero: number | number; espera 2s |
| combinar_resultados | a: number, b: number | number |

Usuários válidos: 1 (Ana, ativa), 2 (Bruno, inativo), 3 (Carla, ativa).
Produtos válidos: 10 (100, estoque 5), 20 (250, estoque 3), 30 (40, estoque 0).
Sensores válidos: 101 (28°C, pressão 3.5), 102 (78°C, pressão 7.0).
IDs inválidos podem produzir exceção Python; não é necessário tratá-los no compilador.

## Sintaxe de chamada
O retorno é opcional na DSL: `SERVICO registrar_log("Oi")` descarta o resultado; `SERVICO buscar_usuario(1) -> nome` o armazena. A lista de argumentos pode ser vazia, mesmo que as funções deste catálogo exijam parâmetros.
