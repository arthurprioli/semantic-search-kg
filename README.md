# semantic-search-kg
Iniciação Científica PIBIC com o objetivo de fazer a implementação de um sistema de busca semântica em títulos de artigos fazendo uso de um banco de dados NoSQL. 

## Configuração do projeto

O projeto foi feito em uma instância do Neo4J AuraDB em nuvem, mas para reproduzir você pode usar os códigos em (https://github.com/arthurprioli/semantic-search-kg/tree/main/src/drafts).

Após clonar o projeto na sua máquina local, faça:

1. Crie o ambiente virtual Python
   
    `python -m venv semantic-search-kg-env`

2. Instale os módulos necessários para a execução do projeto
   
    `pip install -r requirements.txt`

3. Crie uma instância AuraDB do neo4j
   
  <img width="1847" height="73" alt="image" src="https://github.com/user-attachments/assets/bd89990e-c7df-457c-8db1-ae41be275df5" />
   
   Guarde as informações de username, password e uri  e crie um arquivo .env no seguinte formato no diretório principal:
   ```
     NEO4J_USERNAME = nome_de_usuario_neo4j
     NEO4J_PASSWORD = senha_neo4j
     NEO4J_URI = uri_do_banco_neo4j
     MODEL_NAME = nome_modelo_de_embedding (no caso dessa pesquisa 'paraphrase-multilingual-mpnet-base-v2')
   ```

4. Utilização do *cria_kg.ypnb*:

  No cria_kg.ypnb execute o notebook jupyter com a opção 'Run all' para inserir os dados em seu banco e seus embeddings, a execução deve demorar por volta de 3-4 horas para a inserção das mais de 80 mil produções e seus embeddings.

**Os arquivos esperta_kg.ypnb e queries.ypnb foram usados para motivo de pesquisa e não devem ser levados em conta caso o uso seja apenas em teste da ferramenta**

5. Executando o projeto:
   
   Para executar o projeto, ative o ambiente virtual com:
   
   - Linux / macOS
     
      `source activate nome_env/bin/`
   - Windows
     
      `cd nome_env/Scripts`
     
      `activate.bat`

   No diretório **semantic-search-kg** faça:
   
     `streamlit run src/sistema-busca.py`

  A seguinte imagem deve ser apresentada:
  
  <img width="1400" height="763" alt="image" src="https://github.com/user-attachments/assets/b2b8b7f8-0db3-4379-83c1-3be3b4a5c01a" />

  Testando com uma busca:

  <img width="1356" height="435" alt="image" src="https://github.com/user-attachments/assets/2c0573ff-c55b-4d0d-b9d2-d8e0e58cb0a6" />
      
    
