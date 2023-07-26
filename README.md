# Desafio de Data Engineer - EMD

## Descrição do desafio

Neste desafio você deverá capturar, estruturar, armazenar e transformar dados de uma API instantânea. A API consiste nos dados de GPS do BRT que são gerados na hora da consulta com o último sinal transmitido por cada veículo.

Para o desafio, será necessário construir uma pipeline que captura os dados minuto a minuto e gera um arquivo no formato CSV. O arquivo gerado deverá conter no mínimo 10 minutos de dados capturados (estruture os dados da maneira que achar mais conveniente), então carregue os dados para uma tabela no Postgres. Por fim, crie uma tabela derivada usando o DBT. A tabela derivada deverá conter o ID do onibus, posição e sua a velocidade.

A pipeline deverá ser construída subindo uma instância local do Prefect (em Python). Utilize a versão *0.15.9* do Prefect.

## Solução proposta
 Foi criado um pipeline de dados que faz uma consulta a cada minuto a API de GPS do BRT e gera um arquivo `.json` com a data que foi realizada a consulta e as informações coletadas. A cada 10 arquivos `.json` gerados (representando 10 minutos de dados capturados) será gerado um arquivo `.csv` contendo as informações agregadas. Esse arquivo `.csv` então é carregado numa tabela em um banco de dados PostgreSQL inicializado localmente numa tabela chamada `raw.tb_brt_gps`, e por fim, uma tabela derivada é gerada usando o DBT com o nome `raw.brt_info` 


## Estrutura do projeto
   
- `db/` - Contém todas as informações referente a base de dados e configuração do dbt;
  - `brt_data/` - Contém todos os arquivos relacionados ao dbt
  - `output/` - Diretório onde está armazenado as saídas dos arquivos gerados pela pipeline;
  - `init_db.sql` - Arquivo de inicialização da tabela onde serão armazenados os dados em SQL
  - `docker-compose.yml` - Arquivo de inicialização da instancia docker para o postgres
- `pipeline/` - Contém os arquivos relacionados a execução do pipeline pelo Prefect
  - `flow.py` - Declaração dos flows;
  - `schedules.py` - Declaração dos schedules;
  - `tasks.py` - Declaração das tasks;
  - `constants.py` - Declaração dos valores constantes para o projeto;


## Configuração do ambiente de execução
    
### Requisitos

- Python 3.9.x
- `pip`
- GNU/Linux
- `docker` e `docker-compose`

### Inicialização do ambiente

- Entre no diretório `db/`
- Abra o terminal e execute o comando:
```
docker-compose up -d
```
- Verifique se a instância docker foi executada corretamente com o comando:
```
docker ps
```

## Executando a pipeline

- (Opcional) Crie e ative um ambiente virtual usando venv
- Instale as dependências definidas em `requirements.txt` com o comando:
```
pip install -r requirements.txt
 ```
- Execute o arquivo `main.py` na pasta raiz do projeto:
```
python main.py
```

## Links de referência

- Documentação [Prefect](https://docs-v1.prefect.io/)
- Documentação [DBT](https://docs.getdbt.com/docs/introduction)
- Instalar e configurar o
   [Prefect Server](https://docs.prefect.io/orchestration/getting-started/install.html)
   locamente com um [Docker Agent](https://docs.prefect.io/orchestration/agents/docker.html)
- Construir a pipeline de captura da [API do
   BRT](https://dados.mobilidade.rio/gps/brt)
- Repositório pipelines do [Escritorio de Dados](https://github.com/prefeitura-rio/pipelines)
- Repositório de modelos DBT do [Escritorio de Dados](https://github.com/prefeitura-rio/queries-datario)

