# Gerador de dados
## Dependencia que tem que instalar para rodar o gerador 

pip install faker geonamescache pycountry Babel

## Estrutura de diretórios

.venv
gerador
├── data
│   └── base_geografica
├── main.py
└── src
    ├── jogadores.py
    ├── partidas.py
    └── regras.py

- src: Código principal
- data: Dados pré-carregados utilizados pelo código
- output*: Arquivos gerados pelo código
- .venv*: Arquivos do ambiente virtal python

* Está no .gitignore
