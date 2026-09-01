from jogadores import gerar_arquivo_jogadores


QUANTIDADE = 1_000


arquivo = gerar_arquivo_jogadores(
    QUANTIDADE
)


print()
print("Geração concluída!")
print("Arquivo:", arquivo)