# Modelo dos Dados contidos no CSV

> Os nomes devem ser escritos no CSV EXATAMENTE como estão aqui

## Dados de jogadores

| Nome               | Tipo   | Formato          | Min        | Max  | Exemplo      |
| ------------------ | ------ | ---------------- | ---------- | ---- | ------------ |
| player_id          | int    | -                | 1          | -    | 55           |
| nome               | string | "Nome Sobrenome" | -          | -    | "João Silva" |
| username           | string | -                | -          | -    | "joao"       |
| idade              | int    | -                | 16         | 55   | 17           |
| data_nascimento    | string | yyyy-MM-dd       | 2010-01-01 | HOJE | "2025-05-12" |
| genero             | string | -                | -          | -    | "Masculino"  |
| nivel_jogador      | int    | -                | 1          | 100  | 45           |
| data_criacao_conta | string | yyyy-MM-dd       | 2010-01-01 | HOJE | "2023-02-21" |

## Dados geográficos

| Nome   | Tipo   | Formato   | Exemplo |
| ------ | ------ | --------- | ------- |
| cidade | string | -         | Guapó   |
| estado | string | \[Sigla\] | GO      |
| pais   | string | -         | Brasil  |

## Dados de jogo

| Nome        | Tipo   | Formato | Exemplo   |
| ----------- | ------ | ------- | --------- |
| plataforma  | string | -       | Xbox      |
| genero_jogo | string | -       | Simulação |

## Dados de sessão

> o número de sessões pode ser substituído por sessões brutas

> inclusive, nós poderíamos ter todo um modelo de dados só para sessões, não?
com alguns dados do que ocorreu naquela sessão?
ajudaria a criar uma dimensão no data warehouse

| Nome           | Tipo   | Formato    | Min | Max | Exemplo      |
| -------------- | ------ | ---------- | --- | --- | ------------ |
| horas_jogadas  | float  | -          | 1   | -   | 101.4        |
| numero_sessoes | int    | -          | 1   | -   | 450          |
| ultimo_acesso  | string | yyyy-MM-dd | ?   | -   | "2023-02-21" |

## Dados de receita

> valor_gasto pode ser substituído por uma compra bruta também, o que também abre margem pra mais uma possível dimensão no data warehouse

> o último acesso pode ser conseguido na exploração

| Nome               | Tipo  | Formato | Min | Max                        | Exemplo |
| ------------------ | ----- | ------- | --- | -------------------------- | ------- |
| quantidade_compras | int   | -       | 0   | 30                         | 16      |
| valor_gasto        | float | -       | 0   | maior preço \* max compras | 263.4   |