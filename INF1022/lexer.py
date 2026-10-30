# Lexer da OrqLang (feito com PLY)

import sys
import ply.lex as lex


# palavras reservadas da linguagem
# o ID consulta esse dicionario pra saber se a palavra eh reservada ou nao
reservadas = {
    "INICIO": "INICIO",
    "FIM": "FIM",
    "VAR": "VAR",
    "SERVICO": "SERVICO",
    "IMPRIMIR": "IMPRIMIR",
    "VERDADEIRO": "VERDADEIRO",
    "FALSO": "FALSO",
    "SE": "SE",
    "ENTAO": "ENTAO",
    "SENAO": "SENAO",
    "REPITA": "REPITA",
    "VEZES": "VEZES",
    "PARALELO": "PARALELO",
    # operadores logicos (opcionais)
    "E": "E",
    "OU": "OU",
    "NAO": "NAO",
}

tokens = [
    "ID", "NUM", "STR",
    "ATRIB", "ABRE_PAR", "FECHA_PAR", "VIRGULA", "SETA",
    "MAIS", "MENOS", "MULT", "DIV",
    "IGUAL", "DIFERENTE", "MENOR", "MENOR_IGUAL", "MAIOR", "MAIOR_IGUAL",
] + list(reservadas.values())


# simbolos e operadores
# obs: o PLY testa primeiro as regex maiores, entao nao tem problema
# de "->" virar "-" e ">", ou "==" virar dois "="
t_SETA        = r"->"
t_IGUAL       = r"=="
t_DIFERENTE   = r"!="
t_MENOR_IGUAL = r"<="
t_MAIOR_IGUAL = r">="
t_MENOR       = r"<"
t_MAIOR       = r">"
t_ATRIB       = r"="
t_MAIS        = r"\+"
t_MENOS       = r"-"
t_MULT        = r"\*"
t_DIV         = r"/"
t_ABRE_PAR    = r"\("
t_FECHA_PAR   = r"\)"
t_VIRGULA     = r","

# espaco, tab e o \r do windows
t_ignore = " \t\r"


# comentario: do # ate o fim da linha, so descarta
def t_COMENTARIO(t):
    r"\#.*"
    pass


# conta as linhas pra mostrar nas mensagens de erro
def t_novalinha(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# numero inteiro ou decimal (10, 2.5)
def t_NUM(t):
    r"\d+(\.\d+)?"
    if "." in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


# string entre aspas duplas
# deixei as aspas no valor porque no python fica igual
def t_STR(t):
    r'"[^"\n]*"'
    return t


# identificador ou palavra reservada
def t_ID(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = reservadas.get(t.value, "ID")
    return t


def t_error(t):
    print("Erro lexico na linha", t.lexer.lineno, "- caractere ilegal:", t.value[0])
    t.lexer.houve_erro = True
    t.lexer.skip(1)


def construir_lexer():
    lexer = lex.lex()
    lexer.houve_erro = False
    return lexer


# pra testar: python lexer.py exemplos/01_basico.orq
if __name__ == "__main__":
    arquivo = open(sys.argv[1], encoding="utf-8")
    codigo = arquivo.read()
    arquivo.close()

    lexer = construir_lexer()
    lexer.input(codigo)

    for tok in lexer:
        print(tok.lineno, tok.type, tok.value)
