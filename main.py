

def main(codigo):
    # Geração dos tokens
    tokens_gerados = list(tokens.tokenizar(codigo))
    print("="*40)
    print("Tokens Gerados:")
    print("-"*40)
    for token in tokens_gerados:
        print(f"Tipo: {token[0]:<10} | Valor: {token[1]:<10} | Linha: {token[2]}")
    print("="*40)

    # Análise Sintática
    analise = Analisador(tokens_gerados)
    ast = analise.analise()
    print("Árvore Sintática Abstrata (AST):")
    print("-"*40)
    for node in ast:
        print(node)
    print("="*40)

    # Análise Semântica
    analisador_semantico = AnalisadorSemantico()
    for node in ast:
        analisador_semantico.analise(node)

    print("Tabela de Símbolos:")
    print("-"*40)
    for var, valor in analisador_semantico.tabela_simbolos.items():
        print(f"Variável: {var:<10} | Valor: {valor:.2f}")
    print("="*40)

    # Mensagens de entrada/saída
    resultado_saida = ""
    for node in ast:
        if node[0] == 'LEIA':
            # Remover a entrada do terminal
            pass
        elif node[0] == 'IMPRIMA':
            var = node[1][1]
            valor = analisador_semantico.tabela_simbolos.get(var, "Desconhecido")
            resultado_saida += f"Imprimindo {var}: {valor:.2f}\n"

    print("="*40)
    print("Resultado da Expressão:")
    print("-"*40)
    print(resultado_saida)
    print("="*40)
