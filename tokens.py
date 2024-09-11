# tokens.py
import re

# Definição dos tokens usando expressões regulares
especificacao_token = [
    ('NUMERO',     r'\d+(\.\d*)?'),  # Números inteiros ou decimais
    ('ID',         r'[a-zA-Z_]\w*'),  # Identificadores
    ('ASSIGN',     r':='),           # Operador de atribuição
    ('OP',         r'[+\-*/]'),      # Operadores aritméticos
    ('ESQPAREN',   r'\('),           # Parênteses esquerdo
    ('DIRPAREN',   r'\)'),           # Parênteses direito
    ('SEMI',       r';'),            # Ponto e vírgula
    ('NOVALINHA',  r'\n'),           # Nova linha
    ('ESPACO',     r'[ \t]+'),       # Espaços e tabulações
    ('LEIA',       r'leia'),         # Comando de leitura
    ('IMPRIMA',    r'imprima'),      # Comando de impressão
    ('OUTROCHAR',  r'.'),            # Qualquer outro caractere
]

# Compilação das expressões regulares
token_re = '|'.join(
    f'(?P<{pair[0]}>{pair[1]})' for pair in especificacao_token)
captura_token = re.compile(token_re).match

# Função geradora que irá produzir os tokens
def tokenizar(codigo):
    numero_linha = 1
    start_linha = 0
    match = captura_token(codigo)
    while match is not None:
        tipo = match.lastgroup
        if tipo == 'NOVALINHA':
            numero_linha += 1
        elif tipo != 'ESPACO':
            valor = match.group(tipo)
            yield tipo, valor, numero_linha
        start_linha = match.end()
        match = captura_token(codigo, start_linha)
    if start_linha != len(codigo):
        # Caractere inesperado encontrado
        raise RuntimeError(f'Carácter Inesperado {codigo[start_linha]} na linha {numero_linha}')
    yield 'EOF', '', numero_linha
