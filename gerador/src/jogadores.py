from faker import Faker
from datetime import date, timedelta, datetime
from pathlib import Path
from urllib.request import urlretrieve

import random
import csv
import unicodedata
import geonamescache
import pycountry

from src.regras import (
    HOJE,
    gerar_data_nascimento,
    adicionar_anos,
    data_aleatoria,
    criar_username
)


# Pasta principal do gerador
# ../
BASE_DIR = Path(__file__).resolve().parent.parent


# Países

PAISES = {
    "BR": {"nome": "Brasil", "locale": "pt_BR"},
    "US": {"nome": "Estados Unidos", "locale": "en_US"},
    "PT": {"nome": "Portugal", "locale": "pt_PT"},
    "ES": {"nome": "Espanha", "locale": "es_ES"},
    "FR": {"nome": "França", "locale": "fr_FR"},
    "DE": {"nome": "Alemanha", "locale": "de_DE"},
    "IT": {"nome": "Itália", "locale": "it_IT"},
    "GB": {"nome": "Reino Unido", "locale": "en_GB"},
    "CA": {"nome": "Canadá", "locale": "en_CA"},
    "AU": {"nome": "Austrália", "locale": "en_AU"},
    "MX": {"nome": "México", "locale": "es_MX"},
    "AR": {"nome": "Argentina", "locale": "es_AR"}
}


# Faker específico para cada país

FAKERS = {
    codigo: Faker(dados["locale"])
    for codigo, dados in PAISES.items()
}


# Localização

gc = geonamescache.GeonamesCache(
    min_city_population=1000
)


PASTA_BASE = BASE_DIR / "data/base_geografica"

ARQUIVO_ESTADOS = (
    # PASTA_BASE / "admin1CodesASCII.txt"
    PASTA_BASE / "codigos_divisoes_administrativas.txt"
)

URL_ESTADOS = (
    "https://download.geonames.org/export/dump/"
    "admin1CodesASCII.txt"
)


def normalizar(texto):

    texto = unicodedata.normalize(
        "NFKD",
        texto
    )

    return "".join(
        letra
        for letra in texto
        if not unicodedata.combining(letra)
    ).lower()


def carregar_estados():

    PASTA_BASE.mkdir(
        exist_ok=True
    )

    # Baixa somente se o arquivo ainda não existir
    if not ARQUIVO_ESTADOS.exists():

        print("Baixando base de estados...")

        urlretrieve(
            URL_ESTADOS,
            ARQUIVO_ESTADOS
        )

    estados = {}

    with open(
        ARQUIVO_ESTADOS,
        "r",
        encoding="utf-8"
    ) as arquivo:

        for linha in arquivo:

            partes = linha.strip().split("\t")

            if len(partes) >= 2:
                estados[partes[0]] = partes[1]

    return estados


ESTADOS = carregar_estados()


# Relaciona estados com suas siglas

SIGLAS_ESTADOS = {}

for estado in pycountry.subdivisions:

    if estado.country_code in PAISES:

        nome = normalizar(
            estado.name
        )

        sigla = estado.code.split(
            "-",
            1
        )[-1]

        SIGLAS_ESTADOS[
            (estado.country_code, nome)
        ] = sigla


# Guarda somente cidades válidas

CIDADES = []

for cidade in gc.get_cities().values():

    codigo_pais = cidade.get(
        "countrycode"
    )

    codigo_estado = cidade.get(
        "admin1code"
    )

    if codigo_pais not in PAISES:
        continue

    if not codigo_estado:
        continue

    chave_estado = (
        f"{codigo_pais}.{codigo_estado}"
    )

    if chave_estado in ESTADOS:
        CIDADES.append(cidade)


def gerar_localizacao():

    cidade = random.choice(
        CIDADES
    )

    codigo_pais = cidade[
        "countrycode"
    ]

    codigo_estado = cidade[
        "admin1code"
    ]

    chave_estado = (
        f"{codigo_pais}.{codigo_estado}"
    )

    nome_estado = ESTADOS[
        chave_estado
    ]

    sigla = SIGLAS_ESTADOS.get(
        (
            codigo_pais,
            normalizar(nome_estado)
        )
    )

    if sigla:
        estado = sigla
    else:
        estado = nome_estado

    return {
        "cidade": cidade["name"],
        "estado": estado,
        "pais": PAISES[codigo_pais]["nome"],
        "codigo_pais": codigo_pais
    }


# Gêneros de jogos

GENEROS_JOGO = [
    "FPS",
    "RPG",
    "Ação",
    "Aventura",
    "Estratégia",
    "Corrida",
    "Esportes",
    "MOBA",
    "Simulação",
    "Luta",
    "Survival"
]


# Plataformas disponíveis para cada gênero

PLATAFORMAS = {
    "FPS": ["PC", "PlayStation", "Xbox"],
    "RPG": ["PC", "PlayStation", "Xbox"],
    "Ação": ["PC", "PlayStation", "Xbox"],
    "Aventura": ["PC", "PlayStation", "Xbox"],
    "Estratégia": ["PC"],
    "Corrida": ["PC", "PlayStation", "Xbox"],
    "Esportes": ["PC", "PlayStation", "Xbox"],
    "MOBA": ["PC", "Mobile"],
    "Simulação": ["PC", "PlayStation", "Xbox"],
    "Luta": ["PC", "PlayStation", "Xbox"],
    "Survival": ["PC", "PlayStation", "Xbox"]
}


# Tempo médio das sessões por gênero

TEMPO_SESSAO = {
    "FPS": (0.4, 2.0),
    "RPG": (1.0, 4.0),
    "Ação": (0.7, 2.5),
    "Aventura": (0.8, 3.0),
    "Estratégia": (0.8, 3.0),
    "Corrida": (0.4, 1.8),
    "Esportes": (0.4, 2.0),
    "MOBA": (0.5, 2.5),
    "Simulação": (1.0, 4.0),
    "Luta": (0.3, 1.5),
    "Survival": (1.0, 4.5)
}


# Gera um jogador

def gerar_jogador(player_id):

    local = gerar_localizacao()

    fake = FAKERS[
        local["codigo_pais"]
    ]


    genero = random.choice([
        "Masculino",
        "Feminino"
    ])


    if genero == "Masculino":

        nome = (
            fake.first_name_male()
            + " "
            + fake.last_name()
        )

    else:

        nome = (
            fake.first_name_female()
            + " "
            + fake.last_name()
        )


    username = (
        criar_username(nome)
        + str(player_id)
    )


    idade = random.randint(
        16,
        55
    )


    nascimento = gerar_data_nascimento(
        idade
    )


    idade_minima = adicionar_anos(
        nascimento,
        13
    )


    inicio_sistema = date(
        2010,
        1,
        1
    )


    data_minima = max(
        idade_minima,
        inicio_sistema
    )


    data_criacao = data_aleatoria(
        data_minima,
        HOJE
    )


    genero_jogo = random.choice(
        GENEROS_JOGO
    )


    plataforma = random.choice(
        PLATAFORMAS[genero_jogo]
    )


    dias_conta = max(
        1,
        (HOJE - data_criacao).days
    )


    max_sessoes = max(
        1,
        int(
            dias_conta
            * random.uniform(
                0.05,
                0.65
            )
        )
    )


    numero_sessoes = random.randint(
        1,
        max_sessoes
    )


    tempo_min, tempo_max = (
        TEMPO_SESSAO[genero_jogo]
    )


    tempo_medio = random.uniform(
        tempo_min,
        tempo_max
    )


    horas_jogadas = round(
        numero_sessoes
        * tempo_medio,
        1
    )


    nivel = min(
        100,
        max(
            1,
            int(horas_jogadas / 25) + 1
        )
    )


    limite_compras = min(
        30,
        max(
            1,
            numero_sessoes // 10
        )
    )


    if random.random() < 0.45:

        compras = 0

    else:

        compras = random.randint(
            1,
            limite_compras
        )


    precos = [
        4.99,
        9.90,
        14.90,
        19.90,
        29.90,
        39.90,
        59.90,
        79.90
    ]


    valor_gasto = round(
        sum(
            random.choice(precos)
            for _ in range(compras)
        ),
        2
    )


    inicio_acesso = max(
        data_criacao,
        HOJE - timedelta(days=365)
    )


    ultimo_acesso = data_aleatoria(
        inicio_acesso,
        HOJE
    )


    return {
        "player_id": player_id,
        "nome": nome,
        "username": username,
        "idade": idade,
        "data_nascimento": nascimento.isoformat(),
        "genero": genero,
        "cidade": local["cidade"],
        "estado": local["estado"],
        "pais": local["pais"],
        "plataforma": plataforma,
        "genero_jogo": genero_jogo,
        "nivel_jogador": nivel,
        "data_criacao_conta": data_criacao.isoformat(),
        "horas_jogadas": horas_jogadas,
        "numero_sessoes": numero_sessoes,
        "quantidade_compras": compras,
        "valor_gasto": valor_gasto,
        "ultimo_acesso": ultimo_acesso.isoformat()
    }


# Salva os jogadores em um CSV

def gerar_arquivo_jogadores(quantidade):

    # Sempre salva dentro da pasta gerador/output
    pasta = BASE_DIR / "output"

    pasta.mkdir(
        exist_ok=True
    )


    # Inclui microssegundos para nunca repetir o nome
    momento = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )


    caminho = pasta / (
        f"jogadores_{quantidade}_"
        f"{momento}.csv"
    )


    colunas = [
        "player_id",
        "nome",
        "username",
        "idade",
        "data_nascimento",
        "genero",
        "cidade",
        "estado",
        "pais",
        "plataforma",
        "genero_jogo",
        "nivel_jogador",
        "data_criacao_conta",
        "horas_jogadas",
        "numero_sessoes",
        "quantidade_compras",
        "valor_gasto",
        "ultimo_acesso"
    ]


    with open(
        caminho,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=colunas
        )

        escritor.writeheader()


        for player_id in range(
            1,
            quantidade + 1
        ):

            jogador = gerar_jogador(
                player_id
            )

            escritor.writerow(
                jogador
            )


            if player_id % 1000 == 0:

                print(
                    player_id,
                    "jogadores gerados..."
                )


    return caminho