from faker import Faker
from datetime import date, timedelta, datetime
from pathlib import Path
from urllib.request import urlretrieve

import random
import csv
import os
import unicodedata
import geonamescache
import pycountry

from babel import Locale

from regras import (
    HOJE,
    gerar_data_nascimento,
    adicionar_anos,
    data_aleatoria,
    criar_username
)

# LOCALIZAÇÃO

LOCALE_POR_PAIS = {
    "BR": "pt_BR",
    "US": "en_US",
    "PT": "pt_PT",
    "ES": "es_ES",
    "FR": "fr_FR",
    "DE": "de_DE",
    "IT": "it_IT",
    "GB": "en_GB",
    "CA": "en_CA",
    "AU": "en_AU",
    "MX": "es_MX",
    "AR": "es_AR"
}


fakers = {
    codigo: Faker(locale)
    for codigo, locale in LOCALE_POR_PAIS.items()
}


# Nomes dos países em português
PORTUGUES = Locale("pt_BR")


# Carrega cidades reais
gc = geonamescache.GeonamesCache(
    min_city_population=1000
)

PAISES = gc.get_countries()

# BASE DE ESTADOS / REGIÕES

PASTA_BASE = Path("base_geografica")

ARQUIVO_ESTADOS = (
    PASTA_BASE / "admin1CodesASCII.txt"
)

URL_ESTADOS = (
    "https://download.geonames.org/export/dump/"
    "admin1CodesASCII.txt"
)


def normalizar_texto(texto):

    texto = unicodedata.normalize(
        "NFKD",
        texto
    )

    texto = "".join(
        caractere
        for caractere in texto
        if not unicodedata.combining(caractere)
    )

    return texto.lower().strip()


def carregar_estados():

    PASTA_BASE.mkdir(
        exist_ok=True
    )

    # Só baixa na primeira vez
    if not ARQUIVO_ESTADOS.exists():

        print(
            "Baixando base de estados/regiões..."
        )

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

                codigo = partes[0]

                nome = partes[1]

                estados[codigo] = nome


    return estados


ESTADOS = carregar_estados()

# SIGLAS DOS ESTADOS

SIGLAS_ESTADOS = {}


for subdivisao in pycountry.subdivisions:

    codigo_pais = subdivisao.country_code

    if codigo_pais in LOCALE_POR_PAIS:

        nome_estado = normalizar_texto(
            subdivisao.name
        )

        # BR-SP -> SP
        # US-CA -> CA
        codigo = subdivisao.code

        if "-" in codigo:

            sigla = codigo.split(
                "-",
                1
            )[1]

        else:

            sigla = codigo


        SIGLAS_ESTADOS[
            (
                codigo_pais,
                nome_estado
            )
        ] = sigla

# CIDADES VÁLIDAS

CIDADES = []


for cidade in gc.get_cities().values():

    codigo_pais = cidade.get(
        "countrycode"
    )

    codigo_estado = cidade.get(
        "admin1code"
    )


    if (
        codigo_pais in LOCALE_POR_PAIS
        and codigo_estado
    ):

        chave = (
            f"{codigo_pais}.{codigo_estado}"
        )

        # Só usa cidades cujo estado/região
        # também existe na base
        if chave in ESTADOS:

            CIDADES.append(
                cidade
            )


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


    # Procura a sigla oficial
    sigla_estado = SIGLAS_ESTADOS.get(
        (
            codigo_pais,
            normalizar_texto(
                nome_estado
            )
        )
    )


    # Caso o país não utilize uma sigla
    # compatível, mantém o nome da região
    estado_final = (
        sigla_estado
        if sigla_estado
        else nome_estado
    )


    pais = PORTUGUES.territories.get(
        codigo_pais,
        PAISES[codigo_pais]["name"]
    )


    return {
        "cidade": cidade["name"],
        "estado": estado_final,
        "pais": pais,
        "codigo_pais": codigo_pais
    }

# GÊNEROS DE JOGO

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


PLATAFORMAS_POR_GENERO = {

    "FPS":
        ["PC", "PlayStation", "Xbox"],

    "RPG":
        ["PC", "PlayStation", "Xbox"],

    "Ação":
        ["PC", "PlayStation", "Xbox"],

    "Aventura":
        ["PC", "PlayStation", "Xbox"],

    "Estratégia":
        ["PC"],

    "Corrida":
        ["PC", "PlayStation", "Xbox"],

    "Esportes":
        ["PC", "PlayStation", "Xbox"],

    "MOBA":
        ["PC", "Mobile"],

    "Simulação":
        ["PC", "PlayStation", "Xbox"],

    "Luta":
        ["PC", "PlayStation", "Xbox"],

    "Survival":
        ["PC", "PlayStation", "Xbox"]
}


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

# GERAR JOGADOR

def gerar_jogador(player_id):

    local = gerar_localizacao()

    fake = fakers[
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


    data_nascimento = (
        gerar_data_nascimento(
            idade
        )
    )


    idade_minima_conta = adicionar_anos(
        data_nascimento,
        13
    )


    inicio_sistema = date(
        2010,
        1,
        1
    )


    data_minima = max(
        idade_minima_conta,
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
        PLATAFORMAS_POR_GENERO[
            genero_jogo
        ]
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


    tempo_minimo, tempo_maximo = (
        TEMPO_SESSAO[
            genero_jogo
        ]
    )


    tempo_medio = random.uniform(
        tempo_minimo,
        tempo_maximo
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
            int(
                horas_jogadas / 25
            ) + 1
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


    inicio_ultimo_acesso = max(
        data_criacao,
        HOJE - timedelta(days=365)
    )


    ultimo_acesso = data_aleatoria(
        inicio_ultimo_acesso,
        HOJE
    )


    return {

        "player_id":
            player_id,

        "nome":
            nome,

        "username":
            username,

        "idade":
            idade,

        "data_nascimento":
            data_nascimento.isoformat(),

        "genero":
            genero,

        "cidade":
            local["cidade"],

        "estado":
            local["estado"],

        "pais":
            local["pais"],

        "plataforma":
            plataforma,

        "genero_jogo":
            genero_jogo,

        "nivel_jogador":
            nivel,

        "data_criacao_conta":
            data_criacao.isoformat(),

        "horas_jogadas":
            horas_jogadas,

        "numero_sessoes":
            numero_sessoes,

        "quantidade_compras":
            compras,

        "valor_gasto":
            valor_gasto,

        "ultimo_acesso":
            ultimo_acesso.isoformat()
    }

# GERAR CSV

def gerar_arquivo_jogadores(
    quantidade
):

    os.makedirs(
        "dados",
        exist_ok=True
    )


    momento = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


    caminho = (
        f"dados/"
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
                    f"{player_id:,} jogadores gerados..."
                )


    return caminho