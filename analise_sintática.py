# analisador.py

import tokens

class Analisador:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos]
    
    def proximo_token(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.token_atual = self.tokens[self.pos]
        else:
            self.token_atual = ('EOF', '')
    
    def esperado(self, tipo_token):
        if self.token_atual[0] == tipo_token:
            self.proximo_token()
        else:
            raise Exception(f'Erro de Sintaxe: esperado {tipo_token}, recebido {self.token_atual[0]}')
    
    def analise(self):
        instrucoes = []
        while self.token_atual[0] != 'EOF':
            instrucoes.append(self.instrucao())
        return instrucoes
    
    def instrucao(self):
        if self.token_atual[0] == 'ID':
            if self.token_atual[1] == 'imprima':
                return self.imprime()
            elif self.token_atual[1] == 'leia':
                return self.leia()
            else:
                return self.atribuicoes()
        else:
            raise Exception(f'Erro de Sintaxe: esperado ID, recebido {self.token_atual[0]}')
    
    def atribuicoes(self):
        var_node = self.fator()
        self.esperado('ASSIGN')  # Token de atribuição ':='
        expr_node = self.expr()
        self.esperado('SEMI')  # Token de finalização ';'
        return ('ASSIGN', var_node, expr_node)
    
    def imprime(self):
        self.esperado('ID')  # Espera o 'imprima'
        id_node = self.token_atual
        self.proximo_token()
        self.esperado('SEMI')  # Espera o ponto e vírgula
        return ('IMPRIMA', id_node)
    
    def leia(self):
        self.esperado('ID')  # Espera o 'leia'
        id_node = self.token_atual
        self.proximo_token()
        self.esperado('SEMI')  # Espera o ponto e vírgula
        return ('LEIA', id_node)
    
    def expr(self):
        node = self.termo()
        while self.token_atual[0] in ('OP',):
            op = self.token_atual
            self.proximo_token()
            node = (op[0], op[1], node, self.termo())
        return node
    
    def termo(self):
        node = self.fator()
        while self.token_atual[0] in ('OP',):
            op = self.token_atual
            self.proximo_token()
            node = (op[0], op[1], node, self.fator())
        return node
    
    def fator(self):
        token = self.token_atual
        if token[0] == 'NUMERO':
            self.proximo_token()
            return ('NUMERO', float(token[1]))
        elif token[0] == 'ID':
            self.proximo_token()
            return ('ID', token[1])
        elif token[0] == 'ESQPAREN':
            self.proximo_token()
            node = self.expr()
            self.esperado('DIRPAREN')
            return node
        else:
            raise Exception(f'Erro de Sintaxe: esperado NUMERO, ID ou ESQPAREN, recebido {token[0]}')
