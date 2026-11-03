# OrqLang — Kit do Trabalho Final INF1022

Este kit contém os arquivos necessários para o desenvolvimento e teste do trabalho final da disciplina **INF1022 — Analisadores Léxicos e Sintáticos**.

O objetivo do trabalho é desenvolver um **transpilador** para a linguagem OrqLang, capaz de transformar programas escritos nessa linguagem em programas Python equivalentes.

A OrqLang é uma linguagem simplificada para orquestração de tarefas e serviços. Ela permite chamar funções, armazenar resultados em variáveis, realizar operações aritméticas, utilizar condicionais e executar repetições.

Os alunos deverão implementar os analisadores léxico e sintático e a geração de código Python. Para isso, poderão utilizar ferramentas como **PLY (Python Lex-Yacc), Lex/Yacc ou Flex/Bison**.

As funções que serão chamadas pelos programas OrqLang já estão implementadas e são fornecidas pelo professor.

**Requisitos:** Python 3.10 ou superior. A biblioteca de serviços fornecida não possui dependências externas.

---

## 1. Estrutura do kit

```text
orqlang-kit/
│
├── runtime/
│   ├── __init__.py
│   ├── servicos.py
│   └── orqlang_runtime.py
│
├── docs/
│   └── servicos.md
│
├── exemplos/
│   ├── 01_basico.orq
│   ├── 02_loja.orq
│   ├── 03_monitoramento.orq
│   ├── 04_repeticao.orq
│   ├── 05_dados.orq
│   ├── 06_paralelo_bonus.orq
│   └── 07_sem_retorno.orq
│
├── testes/
│   ├── *.esperado.txt
│   ├── invalidos.orq.txt
│   └── test_servicos.py
│
└── README.md
```

### Descrição dos arquivos

- `runtime/servicos.py`: biblioteca de funções Python que poderão ser chamadas pelos programas OrqLang.
- `runtime/orqlang_runtime.py`: biblioteca auxiliar para execução paralela de serviços (funcionalidade bônus).
- `docs/servicos.md`: documentação das funções disponíveis, seus parâmetros e valores retornados.
- `exemplos/`: exemplos de programas escritos em OrqLang.
- `testes/*.esperado.txt`: saídas esperadas para os programas de exemplo.
- `testes/invalidos.orq.txt`: exemplos de programas com erros sintáticos que devem ser rejeitados.
- `testes/test_servicos.py`: testes da biblioteca Python fornecida.

**Importante:** o kit não contém o transpilador. Sua implementação é responsabilidade dos alunos.

---

## 2. O que deve ser desenvolvido

Os alunos deverão implementar um programa que:

1. Receba como entrada um arquivo contendo um programa escrito em OrqLang (`.orq`).
2. Realize a análise léxica do programa.
3. Realize a análise sintática, verificando se o programa segue a gramática da linguagem.
4. Caso o programa seja sintaticamente válido, gere um arquivo Python (`.py`) equivalente.
5. Caso exista um erro léxico ou sintático, apresente uma mensagem de erro, sem gerar um programa Python válido.

A gramática inicial e as extensões obrigatórias estão descritas no PDF do enunciado.

Não é necessário implementar um interpretador para a OrqLang. O programa gerado será executado pelo próprio Python.

---

## 3. Biblioteca de serviços fornecida

O arquivo `runtime/servicos.py` contém funções Python prontas que simulam operações de diferentes sistemas.

Essas funções estão organizadas em cenários como:

- **Loja virtual:** consulta de usuários, produtos, estoque, cálculo de preços e registro de pedidos.
- **Monitoramento:** consulta de sensores, verificação de limites e geração de alertas.
- **Processamento de dados:** carregamento de valores, somatórios, médias e outras operações.
- **Orquestração:** chamadas a sistemas simulados, combinação de resultados e operações com tempo de execução.

Por exemplo, a biblioteca contém a função:

```python
def buscar_usuario(usuario_id):
    return USUARIOS[usuario_id]["nome"]
```

Os alunos poderão chamar essa função por meio de um programa OrqLang:

```text
SERVICO buscar_usuario(1) -> nome
```

O transpilador deverá gerar o código Python equivalente:

```python
nome = buscar_usuario(1)
```

**Os alunos não precisam implementar ou modificar as funções da biblioteca.** Elas já estão prontas para utilização.

A lista completa das funções disponíveis pode ser consultada em `docs/servicos.md`.

---

## 4. Como executar o código Python gerado

O transpilador deverá transformar um programa OrqLang em um programa Python equivalente.

### Exemplo

Considere o seguinte programa OrqLang:

```text
INICIO

SERVICO buscar_usuario(1) -> nome
IMPRIMIR nome

FIM
```

O transpilador deverá produzir um código Python equivalente a:

```python
from runtime.servicos import *

nome = buscar_usuario(1)
print(nome)
```

A primeira linha importa as funções da biblioteca fornecida pelo professor.

### Executando o programa

Suponha que o transpilador tenha gerado o arquivo `gerado/01_basico.py`.

Abra um terminal na pasta `orqlang-kit` e execute:

**Linux/macOS:**

```bash
PYTHONPATH=. python gerado/01_basico.py
```

**Windows (PowerShell):**

```powershell
$env:PYTHONPATH="."
python gerado/01_basico.py
```

O `PYTHONPATH=.` permite que o Python encontre a biblioteca de serviços na pasta `runtime`.

A pasta `gerado` não faz parte do kit original. Ela poderá ser criada pelos alunos para armazenar os programas Python produzidos pelo transpilador.

**Saída esperada:**

```text
Ana
```

Os alunos poderão comparar a saída obtida com os arquivos `.esperado.txt` disponíveis na pasta `testes`.

---

## 5. Chamadas de serviços na OrqLang

A linguagem permite duas formas de chamada de serviços.

### 5.1. Chamada com atribuição de retorno

```text
SERVICO buscar_usuario(1) -> nome
```

Nesse caso, o valor retornado pela função `buscar_usuario` será armazenado na variável `nome`.

Código Python equivalente:

```python
nome = buscar_usuario(1)
```

### 5.2. Chamada sem atribuição de retorno

```text
SERVICO registrar_log("Processamento iniciado")
```

Nesse caso, a função será executada normalmente, mas seu valor de retorno não será armazenado em nenhuma variável.

Código Python equivalente:

```python
registrar_log("Processamento iniciado")
```

**As duas formas são obrigatórias.**

Também devem ser aceitas chamadas de serviços sem argumentos, como:

```text
SERVICO minha_funcao()
```

Nesse caso, a função chamada precisa existir e aceitar zero argumentos para que o programa Python seja executado corretamente.

O transpilador não precisa verificar se a função existe na biblioteca ou se os argumentos são compatíveis. Essas verificações ficam a cargo do Python durante a execução.

---

## 6. Regras importantes da linguagem

As regras completas estão disponíveis no PDF do enunciado. Algumas observações importantes são:

### Variáveis

O comando `VAR` permite atribuir valores a variáveis:

```text
VAR x = 10
VAR y = 20
VAR resultado = x + y
```

O mesmo comando pode ser utilizado para atualizar o valor de uma variável:

```text
VAR x = x + 1
```

Não é necessário implementar declaração de tipos.

### Condicionais

A linguagem permite executar comandos dependendo de uma condição:

```text
SE preco > 100 ENTAO
    IMPRIMIR "Produto caro"
SENAO
    IMPRIMIR "Produto barato"
FIM
```

### Repetição

O comando `REPITA` executa um bloco um determinado número de vezes:

```text
REPITA 3 VEZES
    IMPRIMIR "Executando"
FIM
```

A expressão que determina a quantidade de repetições deverá ser avaliada uma única vez, no início do bloco.

### Expressões

A linguagem deverá suportar operações aritméticas, comparações e parênteses, respeitando a precedência definida no enunciado.

Os operadores lógicos `E`, `OU` e `NAO` são opcionais.

---

## 7. Execução paralela de serviços (bônus)

Como funcionalidade opcional, a OrqLang poderá permitir a execução paralela de serviços.

Exemplo:

```text
INICIO

PARALELO
    SERVICO consultar_sistema_a(10) -> resultado_a
    SERVICO consultar_sistema_b(20) -> resultado_b
FIM

SERVICO combinar_resultados(resultado_a, resultado_b) -> total
IMPRIMIR total

FIM
```

As duas primeiras chamadas poderão ser executadas simultaneamente.

Após a conclusão de ambas, seus resultados estarão disponíveis nas variáveis `resultado_a` e `resultado_b`.

O programa continuará executando normalmente após o bloco `PARALELO`.

### Restrições do bloco PARALELO

Dentro desse bloco, somente serão permitidas chamadas de serviços com atribuição de retorno:

```text
SERVICO nome([argumentos]) -> variavel
```

Cada chamada deverá armazenar seu resultado em uma variável diferente.

**Exemplo válido:**

```text
PARALELO
    SERVICO buscar_preco(10) -> preco
    SERVICO verificar_estoque(10) -> estoque
FIM
```

**Exemplo inválido:**

```text
PARALELO
    SERVICO buscar_preco(10) -> resultado
    SERVICO verificar_estoque(10) -> resultado
FIM
```

O segundo exemplo é inválido porque as duas chamadas tentam armazenar seus resultados na mesma variável, `resultado`.

Além disso, uma chamada não poderá utilizar o resultado produzido por outra chamada dentro do mesmo bloco paralelo.

Para implementar essa funcionalidade, os alunos poderão utilizar o arquivo `runtime/orqlang_runtime.py`, que já fornece os mecanismos necessários para executar funções em paralelo.

Não será necessário implementar threads ou outros mecanismos de concorrência.

---

## 8. Testando a biblioteca fornecida

Antes de implementar o transpilador, os alunos poderão verificar se a biblioteca de serviços está funcionando corretamente.

Para isso, abra um terminal na pasta `orqlang-kit` e execute:

```bash
python -m unittest discover -s testes -p "test_*.py"
```

Esse comando executará os testes Python incluídos no kit.

**Importante:** esses testes verificam apenas a biblioteca fornecida pelo professor. Eles não testam o transpilador desenvolvido pelos alunos.

Para testar o transpilador, os alunos deverão utilizar os programas `.orq` fornecidos e comparar a execução do Python gerado com as saídas esperadas.

---

## 9. Testes do transpilador

A pasta `exemplos` contém programas OrqLang que exercitam diferentes funcionalidades da linguagem.

Os alunos deverão utilizar esses programas para verificar se seus analisadores e gerador de código funcionam corretamente.

Para cada exemplo, recomenda-se:

1. Executar o transpilador utilizando o arquivo `.orq` como entrada.
2. Verificar se o arquivo Python foi gerado corretamente.
3. Executar o programa Python produzido.
4. Comparar sua saída com o arquivo `.esperado.txt` correspondente.

Também deverão ser realizados testes com programas sintaticamente inválidos, verificando se o analisador identifica os erros.

Os alunos poderão criar testes adicionais para validar as extensões obrigatórias da gramática.

---

## 10. Observações finais

- A implementação deve utilizar um gerador de analisadores léxicos e sintáticos, conforme permitido no enunciado.
- Os nomes dos serviços devem ser tratados como identificadores genéricos. O transpilador não deve possuir regras específicas para cada função da biblioteca.
- Não é necessário implementar análise semântica completa, verificação de tipos ou validação da existência das funções Python.
- Não é necessário tratar exceções produzidas pelas funções da biblioteca durante a execução.
- A biblioteca de serviços não deve ser modificada para adaptar seu funcionamento ao transpilador.
- A implementação deve seguir a gramática e os requisitos definidos no PDF do trabalho.

**O objetivo principal é demonstrar o funcionamento dos analisadores léxico e sintático e a capacidade de traduzir programas OrqLang para programas Python executáveis.**