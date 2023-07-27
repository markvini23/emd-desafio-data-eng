# Modelo DBT brt_data 

Diretório com os arquivos referente a uma instancia local do DBT

- Na pasta `models/` contém o arquivo `.sql` referente a criação do modelo de tabela derivada
- Os arquivos `profiles.yml` e `dbt_project.yml` contém as informação necessárias de configuração e execução do modelo
- Para executar a instância local do projeto, execute o comando:
```
dbt run --profile-dir .
```
- Para gerar a documentação do modelo execute o comando: 
```
dbt docs generate
```
- Para inicializar um webserver na porta 8080 e servir a documentação localmente, execute o comando:
```
dbt docs serve --profiles-dir .
```