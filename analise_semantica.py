# analisador_semantico.py

import tokens
import analise_sintática

class AnalisadorSemantico:
    def __init__(self):
        self.tabela_simbolos = {}

    def analise(self, node):
        tipo_node = node[0]

        if tipo_node == 'ASSIGN':
            var_node = node[1]
            expr_node = node[2]
            if var_node[0] != 'ID':
                raise Exception(f"Esperado ID, recebido {var_node[0]}.")
            nome_var = var_node[1]
            valor = self.avaliar_expressao(expr_node)
            self.tabela_simbolos[nome_var] = valor
            return valor  # Retorna o valor atribuído para uso posterior

        elif tipo_node == 'IMPRIMA':
            var_node = node[1]
            if var_node[0] != 'ID':
                raise Exception(f"Esperado ID, recebido {var_node[0]}.")
            nome_var = var_node[1]
            if nome_var not in self.tabela_simbolos:
                raise Exception(f"Variável '{nome_var}' não declarada.")
            valor = self.tabela_simbolos[nome_var]
            print(f"Imprimindo {nome_var}: {valor:.2f}")
            return valor

        elif tipo_node == 'LEIA':
            var_node = node[1]
            if var_node[0] != 'ID':
                raise Exception(f"Esperado ID, recebido {var_node[0]}.")
            nome_var = var_node[1]
            valor = float(input(f"Digite o valor para {nome_var}: "))
            self.tabela_simbolos[nome_var] = valor
            return valor

        elif tipo_node == 'OP':
            esquerda = self.avaliar_expressao(node[2])
            direita = self.avaliar_expressao(node[3])
            return self.aplicar_operacao(node[1], esquerda, direita)

        elif tipo_node == 'NUMERO':
            return float(node[1])

        elif tipo_node == 'ID':
            if node[1] not in self.tabela_simbolos:
                raise Exception(f"Variável '{node[1]}' não declarada.")
            return self.tabela_simbolos[node[1]]

        else:
            raise Exception(f"Tipo de nó não compatível '{tipo_node}'.")

    def avaliar_expressao(self, expr):
        if isinstance(expr, tuple):
            return self.analise(expr)
        else:
            return expr

    def aplicar_operacao(self, op, esquerda, direita):
        if op == '+':
            return esquerda + direita
        elif op == '-':
            return esquerda - direita
        elif op == '*':
            return esquerda * direita
        elif op == '/':
            if direita == 0:
                raise Exception("Divisão por zero.")
            return esquerda / direita
        else:
            raise Exception(f"Operação não suportada '{op}'.")
