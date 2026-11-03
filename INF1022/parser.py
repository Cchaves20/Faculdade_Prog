import sys
import ply.yacc as yacc

from lexer import tokens, construir_lexer

precedence = (('nonassoc', 'IGUAL', 'DIFERENTE', 'MENOR', 'MENOR_IGUAL', 'MAIOR', 'MAIOR_IGUAL'),
              ('left', 'MAIS', 'MENOS'),
              ('left', 'MULT', 'DIV'),
              ('right', 'UMINUS'))

def identar(linhas):
    novas = list()
    for linha in linhas:
        novas.append("    " + linha)
    return novas

def p_programa(p):
    """programa : INICIO comandos FIM"""
    p[0] = p[2]

def p_comandos(p):
    """comandos : comando comandos
                | comando"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_comando_var(p):
    """comando : VAR ID ATRIB expr"""
    p[0] = [ p[2] + " = " + p[4] ]

def p_comando_imprimir(p):
    """comando : IMPRIMIR expr"""
    p[0] = [ "print(" + p[2] + ")" ]

def p_comando_servico(p):
    """comando : SERVICO ID ABRE_PAR argumentos FECHA_PAR SETA ID
               | SERVICO ID ABRE_PAR argumentos FECHA_PAR
               | SERVICO ID ABRE_PAR FECHA_PAR SETA ID
               | SERVICO ID ABRE_PAR FECHA_PAR"""
    if len(p) == 8:
        p[0] = [p[7] + " = " + p[2] + "(" + p[4] + ")"]
    elif len(p) == 6:
        p[0] = [p[2] + "(" + p[4] + ")"]
    elif len(p) == 7:
        p[0] = [p[6] + " = " + p[2] + "()"]
    elif len(p) == 5:
        p[0] = [p[2] + "()"]

def p_argumentos(p):
    """argumentos : argumentos VIRGULA expr
                  | expr"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + ", " + p[3]

def p_expr(p):
    """ expr : ID
             | NUM
             | STR
             | VERDADEIRO
             | FALSO """
    if p[1] == 'VERDADEIRO':
        p[0] = "True"
    elif p[1] == 'FALSO':
        p[0] = "False"
    else:
        p[0] = str(p[1])

def p_expr_binaria(p):
    """ expr : expr MAIS expr
             | expr MENOS expr
             | expr MULT expr
             | expr DIV expr
             | expr IGUAL expr
             | expr DIFERENTE expr
             | expr MENOR expr
             | expr MENOR_IGUAL expr
             | expr MAIOR expr
             | expr MAIOR_IGUAL expr """
    p[0] = "(" + p[1] + " " + p[2] + " " + p[3] + ")"

def p_expr_menos(p):
    """ expr : MENOS expr %prec UMINUS """
    p[0] = "(-" + p[2] + ")"

def p_expr_parenteses(p):
    """ expr : ABRE_PAR expr FECHA_PAR """
    p[0] = "(" + p[2] + ")"

def p_comando_se(p):
    """ comando : SE expr ENTAO comandos FIM
                | SE expr ENTAO comandos SENAO comandos FIM """
    if len(p) == 6:
        p[0] = ["if " + p[2] + ":"]
        p[0] += identar(p[4])
    else:
        p[0] = ["if " + p[2] + ":"]
        p[0] += identar(p[4])
        p[0] += ["else:"]
        p[0] += identar(p[6])

def p_comando_repita(p):
    """ comando : REPITA expr VEZES comandos FIM """
    p[0] = ["for _repita_contador in range(" + p[2] + "):"]
    p[0] += identar(p[4])

def p_chamada_par(p):
    """ chamada_par : SERVICO ID ABRE_PAR argumentos FECHA_PAR SETA ID
                    | SERVICO ID ABRE_PAR FECHA_PAR SETA ID """
    if len(p) == 8:
        p[0] = (p[7], p[2], p[4])
    else:
        p[0] = (p[6], p[2], "")

def p_chamadas_par(p):
    """ chamadas_par : chamada_par chamadas_par
                     | chamada_par """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_comando_paralelo(p):
    """ comando : PARALELO chamadas_par FIM """
    chamadas = p[2]
    global houve_erro
    nomes = []
    for saida, servico, args in chamadas:
        if saida in nomes:
            print("Erro semantico na linha", p.lineno(1), "- saida repetida no PARALELO:", saida)
            houve_erro = True
        nomes.append(saida)

    p[0] = ["_paralelo = executar_paralelo(["]
    for saida, servico, args in chamadas:
        if args == "":
            tupla = "()"
        else:
            tupla = "(" + args + ",)"
        p[0].append('    ("' + saida + '", lambda _args=' + tupla + ': ' + servico + '(*_args)),')
    p[0].append("])")
    for saida, servico, args in chamadas:
        p[0].append(saida + ' = _paralelo["' + saida + '"]')


houve_erro = False

def p_error(p):
    global houve_erro
    houve_erro = True
    if p is None:
        print("Erro sintatico: fim de arquivo inesperado (falta FIM?)")
    else:
        print("Erro sintatico na linha", p.lineno, "- token inesperado:", p.type, p.value)

parser = yacc.yacc()

# analisa o codigo e devolve a lista de linhas python
# se tiver erro lexico ou sintatico devolve None
def analisar(codigo):
    global houve_erro
    houve_erro = False

    lexer = construir_lexer()
    linhas = parser.parse(codigo, lexer=lexer)

    if houve_erro or lexer.houve_erro:
        return None
    return linhas

# pra testar: python parser.py exemplos/01_basico.orq
if __name__ == "__main__":
    arquivo = open(sys.argv[1], encoding="utf-8")
    codigo = arquivo.read()
    arquivo.close()

    linhas = analisar(codigo)

    if linhas is None:
        print("rejeitado")
    else:
        print("aceito")
        for linha in linhas:
            print(linha)