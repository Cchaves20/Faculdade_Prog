# Projeto de Estruturas Discretas — Grafos

**O robô consegue inspecionar toda a rede?**

INF1631 — 3WB — 2026 — **Grupo C**

Integrantes:
EDUARDO NADAI - 2311248
CAIO FARIA BRITO - 2410162
MARCELO BESSA - 2220426

Parâmetros do grupo: **n = 10**, **p = 0,30**, **seed = 391**

---

## 1. Descrição do problema

A rede de ruas da cidade é modelada como um grafo simples não direcionado: cada
cruzamento é um vértice e cada rua é uma aresta. O robô precisa sair de um cruzamento,
passar por todas as ruas exatamente uma vez e voltar ao ponto de partida. Isso é
exatamente a existência de um **circuito de Euler** no grafo.

O critério usado é o visto na disciplina: um grafo não direcionado possui circuito de
Euler quando

1. todos os vértices de grau não nulo pertencem à mesma componente conexa; e
2. todos esses vértices possuem grau par.

## 2. Implementação

O programa foi escrito em Python, sem bibliotecas de grafos. Usamos apenas módulos da
biblioteca padrão: `random` (gerador de números aleatórios), `time` (medição de tempo),
`argparse` (leitura dos parâmetros) e `collections.deque` (fila da busca em largura).

### Representação

O grafo é representado por uma **matriz de adjacência** `G` de tamanho n × n, em que
`G[u][v] = 1` se existe a rua entre os cruzamentos u e v, e `0` caso contrário. Como o
grafo é não direcionado, a matriz é simétrica; como é simples, a diagonal é nula.
Internamente os vértices vão de 0 a 9, mas são exibidos de 1 a 10, como no enunciado.

### Funções obrigatórias

| Função | Como foi implementada |
|---|---|
| `gerar_grafo(n, p)` | Percorre os 45 pares {u, v} com u < v e inclui a aresta se `random.random() < p`, marcando `G[u][v]` e `G[v][u]`. |
| `graus(G)` | O grau de v é a soma da linha v da matriz. |
| `conexo(G)` | Busca em largura (BFS) a partir do primeiro vértice de grau positivo; depois confere se todos os vértices de grau positivo foram alcançados. Vértices isolados são ignorados, pois não têm ruas. |
| `euleriano(G)` | Aplica explicitamente os dois critérios: `conexo(G)` e todos os vértices de grau não nulo com grau par. Trata o grafo sem arestas como caso especial (ver abaixo). |
| `circuito_euler(G)` | Algoritmo de **Hierholzer** em versão iterativa com pilha (detalhes abaixo). |
| `valida_circuito(G, C)` | Confere que C começa e termina no mesmo vértice, que cada par consecutivo é uma aresta de G, que nenhuma aresta se repete e que todas as arestas de G foram usadas. |

### Algoritmo de Hierholzer

Trabalhamos sobre uma cópia da matriz, removendo cada aresta assim que ela é percorrida.
Começamos com uma pilha contendo um vértice de grau positivo. A cada passo olhamos o
vértice do topo da pilha:

- se ele ainda tem alguma aresta, percorremos essa aresta (removendo-a) e empilhamos o vizinho;
- se ele não tem mais arestas, desempilhamos o vértice e o colocamos no circuito.

Ao final, o circuito (lido em ordem inversa) usa cada aresta exatamente uma vez. Quando o
caminho "fica preso" antes de usar todas as arestas, o algoritmo volta pela pilha até um
vértice que ainda tem arestas livres e começa um novo ciclo a partir dele; esse ciclo é
emendado automaticamente no circuito final.

### Caso do grafo vazio

Em um grafo sem arestas, os dois critérios são verdadeiros por vacuidade (não há vértice
de grau não nulo, e todos os graus são 0, que é par). Porém não existe nenhuma rua para o
robô inspecionar e não há circuito a construir. Por isso a função `euleriano` testa esse
caso **explicitamente** e retorna "não Euleriano": o grafo vazio não é considerado uma
rede adequada para a missão.

### Seed e reprodutibilidade

O gerador é inicializado com `random.seed(391)` no início de cada experimento. Assim,
qualquer execução do programa com os mesmos parâmetros produz exatamente os mesmos grafos.

## 3. Testes obrigatórios

Executados com `python testes.py`:

| Teste | Grafo usado | Graus | Resultado obtido | Esperado |
|---|---|---|---|---|
| Grafo com Euler | Ciclo C4: 1-2-3-4-1 | 2, 2, 2, 2 | Circuito `1 -> 2 -> 3 -> 4 -> 1`, validação OK | Circuito válido ✔ |
| Vértices ímpares | Caminho P4: 1-2-3-4 | 1, 2, 2, 1 | Conexo, mas há graus ímpares → não Euleriano | Sem circuito ✔ |
| Grafo desconexo | Dois triângulos 1-2-3 e 4-5-6 | todos 2 | Graus pares, mas duas componentes → não Euleriano | Sem circuito ✔ |
| Grafo vazio | 4 vértices, nenhuma aresta | todos 0 | Tratado explicitamente → não Euleriano, sem circuito | Caso tratado ✔ |

Também testamos que `valida_circuito` **rejeita** sequências erradas (que não voltam ao
início, que repetem arestas, que usam pares que não são arestas ou que não usam todas as
arestas).

O teste do grafo desconexo é importante porque mostra que a condição dos graus pares
**sozinha não basta**: os dois triângulos têm todos os graus pares e mesmo assim o robô não
consegue passar de uma componente para a outra.

## 4. Resultados

### Experimento 1 — primeiro grafo Euleriano

```
Numero de vertices: 10
Probabilidade p: 0.30
Seed: 391

Grafo Euleriano encontrado!
Numero de grafos gerados: 372

Matriz de adjacencia:
      1  2  3  4  5  6  7  8  9 10
  1:  0  1  0  0  1  1  1  0  0  0
  2:  1  0  0  0  0  0  1  0  0  0
  3:  0  0  0  0  0  1  0  0  1  0
  4:  0  0  0  0  0  0  1  0  0  1
  5:  1  0  0  0  0  0  0  0  0  1
  6:  1  0  1  0  0  0  1  1  0  0
  7:  1  1  0  1  0  1  0  0  1  1
  8:  0  0  0  0  0  1  0  0  0  1
  9:  0  0  1  0  0  0  1  0  0  0
 10:  0  0  0  1  1  0  1  1  0  0

Arestas (15):
(1,2) (1,5) (1,6) (1,7) (2,7) (3,6) (3,9) (4,7) (4,10) (5,10) (6,7) (6,8) (7,9) (7,10) (8,10)

Graus:
v1: 4   v2: 2   v3: 2   v4: 2   v5: 2
v6: 4   v7: 6   v8: 2   v9: 2   v10: 4

Conexo (vertices de grau nao nulo): sim
Todos os graus sao pares: sim
Euleriano: sim

Circuito de Euler:
1 -> 2 -> 7 -> 1 -> 5 -> 10 -> 4 -> 7 -> 6 -> 3 -> 9 -> 7 -> 10 -> 8 -> 6 -> 1
Validacao do circuito: OK
```

### Experimento 2 — 1000 grafos

```
Experimento com 1000 grafos (n = 10, p = 0.30, seed = 391):
Tempo gasto na geracao dos grafos: 0.0067 s
Tempo total (geracao + verificacao): 0.0279 s
Grafos Eulerianos: 1
Proporcao: 0.001
```

(Os tempos variam um pouco a cada execução, dependendo do computador.)

Dados adicionais coletados para apoiar a análise:

| Condição | Grafos (de 1000) |
|---|---|
| Vértices de grau não nulo na mesma componente | 940 |
| Todos os graus pares | 1 |
| Ambas as condições (Euleriano) | 1 |
| Grafos sem arestas | 0 |

| Nº de vértices de grau ímpar | 0 | 2 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|
| Nº de grafos | 1 | 80 | 393 | 430 | 93 | 3 |

## 5. Análise dos resultados

**O grafo Euleriano encontrado.** O primeiro grafo com circuito de Euler tem 15 arestas
(de 45 possíveis, ou seja, cerca de 33%, próximo do esperado para p = 0,30, que daria em
média 13,5 arestas). Todos os 10 vértices têm grau positivo e par: seis vértices de grau
2, três de grau 4 e o vértice 7 com grau 6. A soma dos graus é 30 = 2 × 15, como manda o
Teorema do Aperto de Mãos. O circuito encontrado tem 16 posições (15 arestas + o retorno
ao vértice 1). O vértice 7, de grau 6, aparece 3 vezes no circuito: cada passagem por um
vértice usa duas arestas (uma de chegada e uma de saída), por isso ele precisa ter grau
par. A validação automática confirmou que o circuito usa cada uma das 15 arestas exatamente
uma vez e volta ao ponto de partida.

**Quantidade de grafos até encontrar esse grafo.** Foram necessários **372 grafos**. Esse
número alto já indica que grafos Eulerianos são raros com esses parâmetros: se cerca de 1
em cada algumas centenas de grafos é Euleriano, é natural precisar de centenas de
tentativas.

**Proporção nos 1000 experimentos.** Apenas **1 dos 1000 grafos** foi Euleriano
(proporção **0,001**). Como o experimento usa a mesma seed do primeiro experimento, a
sequência de grafos gerada é a mesma; de fato, o único grafo Euleriano dos 1000 é o
próprio grafo nº 372 encontrado no experimento 1. Com um número tão pequeno de casos
favoráveis, a proporção medida é bastante sensível ao acaso: outra seed poderia dar, por
exemplo, 0 ou 4 grafos Eulerianos. O que o experimento mostra com segurança é a ordem de
grandeza: menos de 1% dos grafos aleatórios com n = 10 e p = 0,30 permite a missão do robô.

**Relação com os graus dos vértices.** A paridade dos graus é claramente o obstáculo
principal. Apenas 1 grafo em 1000 teve todos os graus pares. A tabela de vértices de grau
ímpar mostra que o mais comum é ter 4 ou 6 vértices ímpares, e que o número de vértices
ímpares é **sempre par** (0, 2, 4, 6, 8 ou 10), como garante o Teorema do Aperto de Mãos
(a soma dos graus é o dobro do número de arestas). Intuitivamente, cada um dos 10 vértices
tem grau "par ou ímpar" de forma quase aleatória, e exigir que **todos** sejam pares ao
mesmo tempo é muito restritivo. Mesmo os 80 grafos com apenas 2 vértices ímpares não
servem para a missão: no máximo teriam um *caminho* de Euler (começando em um vértice
ímpar e terminando no outro), mas o robô não voltaria ao ponto inicial.

**Relação com a conectividade.** A conectividade foi uma restrição bem mais fraca: 940
dos 1000 grafos tinham todos os vértices de grau não nulo na mesma componente. Com p =
0,30 cada vértice tem, em média, 0,3 × 9 = 2,7 vizinhos, o que costuma ser suficiente
para ligar a rede. Ainda assim, a conectividade é uma condição necessária e independente
da paridade: o teste com dois triângulos disjuntos mostra um grafo com todos os graus
pares que não tem circuito de Euler, pois o robô não consegue atravessar de uma
componente para a outra. Por outro lado, vértices isolados (grau 0) não atrapalham, porque
não há ruas neles para inspecionar.

**Conclusão.** Com n = 10 e p = 0,30, o robô quase nunca consegue inspecionar toda a rede
nas condições pedidas (proporção observada de 0,001). Nos grafos gerados, o fator que mais
impede a existência de um circuito de Euler é a presença de vértices de grau ímpar; a falta
de conectividade aparece em cerca de 6% dos grafos e é um fator secundário, mas
igualmente necessário de ser verificado.
