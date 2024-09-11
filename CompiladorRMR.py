import tokens
from tokens import tokenizar
from analise_sintática import Analisador
from analise_semantica import AnalisadorSemantico


class CompiladorRMR:
    def __init__(self):
        self.tabela_simbolos = {}

    def exemplo_codigo(self):
        return (
            "-- Exemplo de código:\n\n"
            "\033[1m"
            "leia b;\n"
            "leia c;\n"
            "a := (b + c) * (c - b);\n"
            "imprima a;\n\n"
            "\033[0m"
            "-- O código deve a sintaxe da linguagem RMR.\n"
            "-- 'leia' é usado para entrada de variáveis.\n"
            "-- 'imprima' é usado para exibir valores.\n"
            "-- Use ':=' para atribuição.\n"
            "-- Use '+' para adição, '-' para subtração, '*' para multiplicação e '/' para divisão.\n"
            "-- Parênteses são usados para agrupar expressões.\n"
        )

    def solicitar_entrada(self, variavel):
        try:
            return float(input(f"Digite o valor para {variavel}: "))
        except ValueError:
            return None

    def ler_codigo(self):
        print("Digite o código linha por linha. Pressione Enter em uma linha vazia para finalizar.")
        codigo = []
        while True:
            linha = input()  # Ler uma linha do usuário
            if linha == "":
                break  # Se a linha estiver vazia, terminamos a entrada
            codigo.append(linha)
        # Combina as linhas em uma única string separadas por "\n"
        return "\n".join(codigo)

    def analisar_codigo(self, codigo):
        # Geração dos tokens
        tokens_gerados = list(tokens.tokenizar(codigo))

        # Análise Sintática
        try:
            analise = Analisador(tokens_gerados)
            ast = analise.analise()
        except Exception as e:
            print(f"Erro de Análise Sintática: {e}")
            return

        # Inicialização do Analisador Semântico
        analisador_semantico = AnalisadorSemantico()

        # Primeiramente, processar os nós de 'LEIA'
        for node in ast:
            if node[0] == 'LEIA':
                variavel = node[1][1]
                valor = self.solicitar_entrada(variavel)
                if valor is not None:
                    analisador_semantico.tabela_simbolos[variavel] = valor
                else:
                    print(f"Erro: Valor para {variavel} não fornecido.")
                    return  # Para evitar continuar com valores inválidos

        # Análise Semântica dos outros nós
        for node in ast:
            if node[0] != 'LEIA':
                try:
                    analisador_semantico.analise(node)
                except Exception as e:
                    print(f"Erro de Análise Semântica: {e}")
                    return

        return tokens_gerados, ast, analisador_semantico.tabela_simbolos

    def executar(self):
        print("Exemplo de código:")
        print(self.exemplo_codigo())
        codigo = self.ler_codigo()
        modo = input(
            "Somente resultado (1) ou compilador completo (2)? (digite 1 ou 2): ")

        tokens_gerados, ast, tabela_simbolos = self.analisar_codigo(codigo)
        if modo == "2":
            print("="*40 + "\nTokens Gerados:")
            for token in tokens_gerados:
                print(
                    f"Tipo: {token[0]:<10} | Valor: {token[1]:<10} | Linha: {token[2]}")
            print("="*40 + "\nÁrvore Sintática Abstrata (AST):")
            for node in ast:
                print(node)
            print("="*40 + "\nTabela de Símbolos:")
            for var, valor in tabela_simbolos.items():
                print(f"Variável: {var:<10} | Valor: {valor:.2f}")
            print("="*40)

        # Impressão dos resultados finais
        for node in ast:
            if node[0] == 'IMPRIMA':
                variavel = node[1][1]
                valor = tabela_simbolos.get(variavel, 'Desconhecido')
                if isinstance(valor, str):
                    print(f"Resultado de {variavel}: {valor}")
                else:
                    print(f"Resultado de {variavel}: {valor:.2f}")


if __name__ == "__main__":
    compilador = CompiladorRMR()
    compilador.executar()
