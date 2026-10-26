import sys
import ply.yacc as yacc

from lexer import tokens, construir_lexer

def p_programa(p):
    """programa : INICIO comandos FIM"""
    pass

def p_comandos(p):
    """comandos : comando comandos
                | comando"""
    pass

def p_comando_var(p):
    """comando : VAR ID ATRIB expr"""
    pass

def p_comando_imprimir(p):
    """comando : IMPRIMIR expr"""
    pass

def p_comando_servico(p):
    """comando : SERVICO ID ABRE_PAR argumentos FECHA_PAR SETA ID
               | SERVICO ID ABRE_PAR argumentos FECHA_PAR
               | SERVICO ID ABRE_PAR FECHA_PAR SETA ID
               | SERVICO ID ABRE_PAR FECHA_PAR"""
    pass

def p_argumentos(p):
    """argumentos : argumentos VIRGULA expr
                  | expr"""
    pass

def p_expr(p):
    """ expr : ID
             | NUM
             | STR
             | VERDADEIRO
             | FALSO """
    pass

houve_erro = False

def p_error(p):
    global houve_erro
    houve_erro = True
    if p is None:
        print("Erro sintatico: fim de arquivo inesperado (falta FIM?)")
    else:
        print("Erro sintatico na linha", p.lineno, "- token inesperado:", p.type, p.value)

parser = yacc.yacc()

# pra testar: python parser.py exemplos/01_basico.orq
if __name__ == "__main__":
    arquivo = open(sys.argv[1], encoding="utf-8")
    codigo = arquivo.read()
    arquivo.close()

    lexer = construir_lexer()
    parser.parse(codigo, lexer=lexer)

    if houve_erro or lexer.houve_erro:
        print("rejeitado")
    else:
        print("aceito")