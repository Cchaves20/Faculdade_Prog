# Relatório - Trabalho Final INF1022 (OrqLang)

Integrantes: Caio Faria Brito (2410162) e Lucas André Guimarães (2411658)

Fizemos o transpilador em Python com PLY, dividido em lexer (`lexer.py`),
parser (`parser.py`) e gerador (`gerador.py`). Além da gramática inicial e das
extensões obrigatórias, implementamos as duas partes opcionais: os operadores
E/OU/NAO e o bloco PARALELO.

## Lexer

Os tokens são ID, NUM, STR, os símbolos `= ( ) , ->`, os operadores
aritméticos e de comparação e as palavras reservadas.

As palavras reservadas não têm regra própria. Tudo que parece identificador
cai na regra do ID, e depois a gente olha num dicionário se aquela palavra é
reservada. Fizemos assim porque, se cada palavra tivesse sua regra, `INICIOx`
viraria dois tokens (`INICIO` e `x`).

Também tivemos que cuidar dos operadores que são começo de outros (`->` e `-`,
`<=` e `<`, `==` e `=`). Como definimos esses operadores como string, o PLY já
testa primeiro as expressões maiores, então isso se resolve sozinho.

Comentários com `#`, espaços, tabs e o `\r` do Windows são ignorados. A regra
do `\n` atualiza o número da linha, que é usado nas mensagens de erro. Quando
aparece um caractere que não pertence à linguagem, mostramos a linha e o
caractere e marcamos o programa como inválido.

## Gramática final

Copiada das regras do `parser.py`:

```
programa     : INICIO comandos FIM

comandos     : comando comandos
             | comando

comando      : VAR ID ATRIB expr
             | IMPRIMIR expr
             | SERVICO ID ABRE_PAR argumentos FECHA_PAR SETA ID
             | SERVICO ID ABRE_PAR argumentos FECHA_PAR
             | SERVICO ID ABRE_PAR FECHA_PAR SETA ID
             | SERVICO ID ABRE_PAR FECHA_PAR
             | SE expr ENTAO comandos FIM
             | SE expr ENTAO comandos SENAO comandos FIM
             | REPITA expr VEZES comandos FIM
             | PARALELO chamada_par chamadas_par FIM

argumentos   : argumentos VIRGULA expr
             | expr

chamadas_par : chamada_par chamadas_par
             | chamada_par

chamada_par  : SERVICO ID ABRE_PAR argumentos FECHA_PAR SETA ID
             | SERVICO ID ABRE_PAR FECHA_PAR SETA ID

expr         : ID | NUM | STR | VERDADEIRO | FALSO
             | ABRE_PAR expr FECHA_PAR
             | expr MAIS expr | expr MENOS expr
             | expr MULT expr | expr DIV expr
             | expr IGUAL expr | expr DIFERENTE expr
             | expr MENOR expr | expr MENOR_IGUAL expr
             | expr MAIOR expr | expr MAIOR_IGUAL expr
             | MENOS expr %prec UMINUS
             | expr E expr | expr OU expr
             | NAO expr
```

O SERVICO tem duas partes opcionais (o `-> ID` e os argumentos), então
escrevemos as quatro combinações como produções separadas.

A precedência fica na tabela `precedence` do PLY. Da menor para a maior:
OU, E, NAO, comparações, `+ -`, `* /` e o menos unário. Alguns detalhes:

- As comparações são `nonassoc`, então `1 < x < 10` dá erro sintático, como
  o enunciado pede.
- O menos unário usa um token fictício, UMINUS, com `%prec`. Assim o mesmo
  `-` tem precedência maior quando é unário, e `-2 * 3` é lido como `(-2) * 3`.
- Para E/OU/NAO seguimos a sugestão do enunciado. Como o NAO fica abaixo das
  comparações, `NAO x > 3` nega a comparação inteira: `not (x > 3)`.

O `parser.out` não mostra nenhum conflito shift/reduce nem reduce/reduce.

Quando o parser encontra um erro, mostra a linha e o token inesperado. Se o
arquivo acaba antes da hora (quando falta o FIM, por exemplo), avisa isso.
Nesses casos o `main.py` não gera o arquivo e sai com código 1.

## Decisões de tradução

Não montamos uma árvore (AST). Cada regra do parser já devolve o código
Python: as expressões devolvem uma string, e os comandos devolvem uma lista de
linhas. Para os blocos (SE, SENAO, REPITA), pegamos as linhas dos comandos de
dentro e acrescentamos 4 espaços na frente de cada uma (função `identar`). Como
cada bloco recebe as linhas internas já prontas, os blocos aninhados funcionam
sem nenhum tratamento especial. O `gerador.py` só coloca os imports no começo
e junta tudo.

A tradução é bem direta: `VAR x = ...` vira `x = ...`, `IMPRIMIR` vira
`print(...)`, `SERVICO f(a) -> x` vira `x = f(a)` (sem a seta fica só `f(a)`),
VERDADEIRO/FALSO viram True/False e E/OU/NAO viram and/or/not.

Algumas escolhas que valem explicar:

- **Parênteses em toda expressão.** `2 + 3 * 4` vira `(2 + (3 * 4))`. Fica
  feio, mas assim a ordem que o nosso parser decidiu vai junto para o Python,
  e não precisamos confiar que a precedência do Python é igual à nossa.
- **SENAO.** Não teve ambiguidade: cada SE tem o seu próprio FIM, então o
  SENAO sempre fica com o SE que ainda está aberto.
- **REPITA.** Vira `for _repita_contador in range(n):`. O `range(n)` calcula o
  `n` uma vez só, na entrada do laço, que é o que o enunciado pede (o exemplo 09
  testa isso mudando o `n` dentro do laço). Colocamos um `_` no começo do nome
  da variável de controle para diminuir a chance de colidir com alguma variável
  do usuário.

### PARALELO

Esse bloco vira uma chamada ao `executar_paralelo` do runtime do kit:

```python
_paralelo = executar_paralelo([
    ("a", lambda _args=(10,): consultar_sistema_a(*_args)),
    ("b", lambda _args=(10,): consultar_sistema_b(*_args)),
])
a = _paralelo["a"]
b = _paralelo["b"]
```

A parte mais chata foi garantir que os argumentos fossem calculados *antes* de
as threads começarem. Se escrevêssemos só `lambda: f(x)`, o `x` seria lido
quando a thread rodasse, e não quando a lambda foi criada. Por isso passamos os
argumentos como valor padrão da lambda (`_args=...`): o Python calcula o valor
padrão no momento em que cria a lambda. A vírgula em `(10,)` é necessária
porque, sem ela, `(10)` é só o número 10, e não uma tupla.

Depois copiamos os resultados do dicionário para variáveis normais, para que o
resto do programa possa usá-las.

Cada chamada dentro do PARALELO devolve uma tupla (saída, serviço, argumentos).
Isso facilita conferir se duas chamadas usam a mesma variável de saída. Quando
usam, mostramos um erro e rejeitamos o programa. Essa conferência ficou na ação
da regra porque não dá para escrever "nomes diferentes" na gramática. Já a
regra de que só pode haver SERVICO com `->` dentro do bloco, e de que são
pelo menos duas chamadas, ficou na própria gramática.

O exemplo 06 imprime 300 em uns 2 segundos, e não 3, então os serviços estão
rodando ao mesmo tempo.

## Testes

O `testar.py` roda tudo de uma vez: transpila cada exemplo, executa, compara
com o `.esperado.txt` e depois confere se os inválidos são rejeitados. Os
`.esperado.txt` do kit têm o `\n` escrito como texto, então o script trata os
dois formatos.

Além dos exemplos do kit (01 a 07), fizemos estes:

- `08_expressoes`: precedência, associatividade, menos unário, divisão e
  comparações (as contas do enunciado, como `2 + 3 * 4` = 14 e `10 - 3 - 2` = 5)
- `09_blocos_aninhados`: SE/SENAO dentro de REPITA, SE dentro de SENAO,
  `REPITA 0 VEZES` e a contagem sendo calculada uma vez só
- `10_logicos`: E, OU, NAO e a precedência entre eles

E estes inválidos, além dos três do `invalidos.orq.txt` (falta de FIM, falta
de ENTAO e falta de fechar o parêntese):

- `4`: caractere ilegal (`@`)
- `5`: operador sem operando (`VAR x = 1 +`)
- `6`: comparação encadeada (`1 < x < 10`)
- `7`: PARALELO com duas chamadas usando a mesma saída
- `8`: IMPRIMIR dentro do PARALELO
- `9`: PARALELO com uma chamada só
- `10`: NAO sem nada depois

Resultado: 10 de 10 exemplos certos e 10 de 10 inválidos rejeitados.

## Limitações

- Se o usuário usar como nome de variável uma palavra reservada do Python
  (`if`, `for`, `None`...), o código gerado quebra. Nomes como `print` passam,
  mas aí a função original do Python é sobrescrita.
- Uma variável do usuário chamada `_paralelo` ou `_repita_contador` bateria com
  as nossas variáveis auxiliares.
- Depois de um erro léxico, a análise continua, então às vezes aparece também
  um erro sintático logo em seguida. O programa é rejeitado do mesmo jeito, mas
  com duas mensagens.
- As strings não aceitam escape (não dá para ter aspas dentro), e um número
  decimal precisa de dígito antes do ponto (`0.5` funciona, `.5` não).
- Não verificamos tipos nem se a variável existe, já que o enunciado não pede
  isso. Esses erros só aparecem quando o Python gerado roda: por exemplo,
  `REPITA 2.5 VEZES` dá erro no Python, e uma contagem negativa simplesmente
  não executa nenhuma vez.
