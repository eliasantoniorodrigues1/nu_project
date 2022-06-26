# nu_project
---

## Projeto de migração de modelo de dados
### Objetivo:
	Recriar o banco de dados original no modelo floco de neve e migra-lo para o esquema estrela.

### Problem Statements

### Problem Statement 1: Gerando consultas SQL

Essa etapa gerar a consulta para o problema proposto de saldo mensal das contas. A consulta e o csv gerado estão armazenados no caminho abaixo:
Nubank_Analytics_Engineer_Case_4.0\Problem Statement\1_Problem Statement
A engine de banco de dados usada é o **MySQL.

•	Amount_Balance_Account.sql
•	Balance Account Monthly.csv
•	Necessary Inputs.txt

Foi utilizado a união de três tabelas para a criação de uma tabela de cálculo (CTE). Essa tabela é ligada com a tabela de clientes para trazer o account_id e o nome do cliente.
As colunas *Total Transfer In*, *Total Transfer Out* e *Account Monthly Balance* são calculadas na CTE e levam em consideração as movimentações do pix também.

**Query**

![image](https://user-images.githubusercontent.com/49626719/175798981-76f8571d-9e85-4143-9b35-0e15c0a21745.png)

**Result**

![image](https://user-images.githubusercontent.com/49626719/175799145-659eda87-6878-4453-88eb-18f785b8723f.png)


### Problem Statement 2:

***a. Proposta para mudança do modelo de dados original:***

***Snow Flake***

 ![image](https://user-images.githubusercontent.com/49626719/175799521-74982800-a6b6-46f2-8227-54621aecfb63.png)



  ***Star Schema***
  
 ![image](https://user-images.githubusercontent.com/49626719/175793235-fa3da6f6-927c-46fa-b82d-2f5c9bf37ef6.png)


***b. O modelo floco de neve não é o mais recomendado pois possui um nível maior de normalização dos dados, o que pode gerar lentidão devido ao acesso de relacionamentos entre tabelas do modelo para alcançar um determinado tipo de resultado.
A ideia é consolidar algumas tabelas do modelo, criando agregação de campos.***

**Dimensão de região:**
	De:
	city,
	state,
	country
para: ***d_region***

**Dimensão tempo:**
	De:
		d_time,
		d_weekday
		d_week
		d_month
		d_year
	para:
		d_calendar
		
Dimensão de Transação:
		Gerar os tipos de transações a partir das tabelas de transfer_ins, transfer_outs, pix_moviments.

		d_transaction_type

Dimesão de Status Transação:

Obter todos os status das transações das tabelas transfer_ins, transfer_outs, pix_moviments e gerar uma única dimensão de status.
		d_status_transaction

Dimesão de Clientes:

Para a criação da tabela de clientes foi agreagdo algumas informações da tabela de contas, pois como ambas possuem registros únicos, usei essa estratégia para 
diminuir o número de dimensóes e manter o relacionamento com a tabela fato com menos chaves estrangeiras.

Criação da tabela Fato:

A tabela fato é a consolidação das chaves estrangeiras de todas as tabelas dimensão, usando sempre como referência a chave primária de cada uma.
Unificação de:

	Transfer_ins
	Transfer_outs
	Pix_moviments
	Investments


## Como esse projeto funciona?

Abaixo irei apresentar a estrutura para executar toda a ação de criação do modelo de dados, bem como a coleta dos arquivos originais em suas respectivas pastas para popular o banco já com os devidos relacionamentos.

### Passo a passo do funcionamento do projeto:

#### Estrutura do Projeto:

![image](https://user-images.githubusercontent.com/49626719/175793587-665a639a-8af3-49f4-91b0-4155c0d553e2.png)

#### Passo 1: Design da base de dados

Criação dos arquivos de configuração: 

•	credentials.json
•	tables.json

Credenciais:
	Contém todas as informações para a criação do esquema de banco de dados.
  - Host
  - User
  - Password
  - Database

O argumento database precisa ser passado para não gerar erro na criação do modelo de dados.

Tables:

O arquivo de configuração das tabelas server para manter a parte toda a estrutura de tabelas do banco, bem como os nomes das colunas, tipo de dados e relacionamentos.

Existem dois dicionários:

•	Snow_flake_tables (Original)
•	Star_Schema_tables (Modelo proposto)
•	Convert_to_datetime

A lista convert_to_datetime, server para mapear todas as colunas de data que precisam de tratamento em seus respectivos UTCs.

#### Passo 2: Ação na base de dados criada

Leitura da pasta raw_tables, para criação do banco de dados.
Essa parte do processo consiste em ler cada diretório buscando por tipos específicos de arquivos (csv, xlsx, json).

1.	Percorrer os diretórios dentro do diretório raw_tables e mapeia os arquivos dentro de cada pasta e os insere em uma lista.
2.	Usa a lista para percorrer o diretório novamente abrindo os arquivos e os consolidando, gerando assim um único dataset.
3.	Converte o dataset gerado em lista e passa para a função, que divide os dados em lotes para melhorar a performance da inserção no banco de dados.

### Log

Todo o processo é armazenado em log para facilitar análise de erros e melhoria de performance.

***Parte do log da execução do processo no banco de dados.***

![image](https://user-images.githubusercontent.com/49626719/175793986-9269d110-cc64-4e9b-b355-dc4cfd23898d.png)


### É possível reproduzir o projeto usando o arquivo requirements.txt

### Problem Statement 3: Plano de Migração

Para executar uma migração das informações de um banco para o outro sem que haja impacto na operação é necessário análisar os horários com menor impacto, sempre
visando manter a performance das bases de produção.
É muito importante um alinhamento com as áreas de administração de banco de dados, negócio e outras equipes que possam ser impactadas.
As consultas devem ser otimizadas para onerar o mínimo possível os servidores, sejam eles em nuvem ou onpremise.
O plano de carga também deve ser levado em consideração, qual seria a melhor abordagem, coleta de hora em hora, carga histórica e etc. É necessário alinhar a estratégia para que tudo corra bem.

Usar uma base de testes para fazer uma análise prévia da performance do fluxo criado com um número controlado de informações, afim de estimar o impacto com o volume
real.

O plano de migração segue o fluxo abaixo:
	1. Alimentar os arquivos de configuração do banco de dados na pasta **\project\settings\**, pois são eles que irão criar a conexão entre os bancos necessários.
	2.Ler as informações no banco de dados nu_snow_flake através de consultas sql armazenadas no diretório **\project\model\query** e editá-las afim de melhorar a performance delas, caso seja necessário.
	
	3. Conectar-se ao banco de dados nu_star_schema  e executar o insert seguindo a ordem das consultas dentro do diretório de queries, para que os relacionamentos sejam criados corretamente.
	
	Scripts desse processo:
	
![image](https://user-images.githubusercontent.com/49626719/175793857-8720c7ac-fceb-4fb5-99a0-49526656180e.png)

	São scripts com enfâse em leitura de arquivos em diretório, criação de conexão com dois bancos de dados diferentes e execução de select em um e insert 
	no outro.
	
**Exemplo:**
	
		def populate_tables(model: str) -> None:
			    # insert data into tables

			    # generate list to ordering insert
			    tbl_names = data_tables[model + '_tables']
			    inserts = []
			    for dict in tbl_names:
				try:
				    name = [tbl_name for tbl_name in dict.keys()]
				    inserts.append(*name)
				except AttributeError:
				    logger.error('You are trying to get key from a list.')

			    if model == 'snow_flake':
				# read raw_tables directory to concat files into just one
				# dataset
				for root, dirs, files in os.walk(RAW_TABLES_DIR):
				    for tbl_name in inserts:
					# searching for all files into directory
					list_paths = db_action.consolidate_path_files(
					    os.path.join(root, tbl_name))
					# receive a pandas dataframe to insert into the table from
					# dir name
					logger.info(f'Inserting data into {tbl_name}...')
					df = db_action.concat_dataset(list_paths)
					for column in df.columns:
					    # convert date in datetime
					    if column in data_tables['convert_to_datetime']:
						df[column] = df[column].apply(
						    dateutil.parser.parse)

					# clean none from transfer_ins and outs
					if tbl_name in ['transfer_ins', 'transfer_outs']:
					    try:
						df['transaction_completed_at'] = df['transaction_completed_at'].replace(
						    'None', 0)
					    except KeyError:
						logger.error("Key doesn't exist.")

					if tbl_name == 'pix_movements':
					    try:
						df['pix_completed_at'] = df['pix_completed_at'].replace(
						    'None', 0)
					    except KeyError:
						logger.error("Key doesn't exist.")

					if tbl_name == 'investments':
					    try:
						df = read_api.get_json_investments(list_paths)
						df['investment_completed_at_timestamp'] = df['investment_completed_at_timestamp'].apply(
						    dateutil.parser.parse)
					    except Exception as e:
						logger.error(f'Error --> {e}')

					# consolidate inserts limit 1000 rows to improve performance
					list_values = df.values.tolist()
					result_list_values = db_action.split_insert(
					    list_values=list_values, begin=0, step=1000)

					# call function to execute insert
					print('Please wait...')
					conn = db_design.db_conn(credentials=credentials_snow)
					db_action.execute_insert(
					    conn,
					    credentials_snow['database'],
					    tbl_name,
					    df.columns.tolist(),
					    result_list_values,
					)
			    else:
				# connect with two databases to performe select and then insert
				snow_conn = db_design.db_conn(credentials=credentials_snow)
				star_conn = db_design.db_conn(credentials=credentials_star)

				# process execution
				db_read_query.execute(snow_conn, star_conn,
						      credentials_star, QUERY_DIR)


### Problem Statement 4: Proposta de KPIs para o Pix

O pix é um produto com uma alta de manda de transações. Para acompanhar o desempenho desse produto eu sugiro a criação dos seguintes indicadores:

Visão Gerencial

•	Quantidade de transações consolidadas por dia
•	Quantidade de transações consolidadas por mês
•	Percentual de crescimento de transações em relação aos demais produtos (transferências, investimentos e etc)
•	Desempenho em relação a meta

**Exemplo:**

![image](https://user-images.githubusercontent.com/49626719/175800943-6ab0e0bc-ae2d-45b8-9f8a-012a5b4eb1c2.png)


Visão Analítica

•	Quantidade de transações por hora
•	Quantidade de transações por minuto
•	Quantidade de transações por segundo

**Exemplo:**

![image](https://user-images.githubusercontent.com/49626719/175800966-a2971a03-6b8c-47e8-8fde-91f733cbe754.png)


Visão Preditiva

•	Essa visão irá conter o resultado da predição dos próximos picos de transações por
Minuto, segundo e hora.

O intuito é efetuar um novo balanceamento dos recursos de servidores para o serviço não ser impactado.

**Exemplo**

![image](https://user-images.githubusercontent.com/49626719/175801058-6e8931ca-23f9-49c0-bef5-d478ee988ce8.png)


### Problem Statement 5: Função para calcular o retorno total de um investimento realizado

Abaixo segue o print do arquivo .csv gerado. 

Contas para serem calculados os retornos de investimento.

![image](https://user-images.githubusercontent.com/49626719/175793467-3d198199-483f-4d5e-90c4-7015f86ad23f.png)

 
Foi usado um script python para a leitura do arquivo investment_accounts_to_send.csv e uma função para ler o json de investimentos investments_json com o intuito de gerar uma tabela e a partir daí usando o framework pandas do Python processar o cruzamento das contas com o arquivo de transações.

***Resultado***

![image](https://user-images.githubusercontent.com/49626719/175798642-32a04cd8-2cc9-4093-bdaa-d52a05b11f95.png)


 ### Script Python para analisar as transações:
 
			 def calculate_movements(list, i):
			    if i == 0:
				previous_d = 0
				deposit = list[i][3]
				withdrawal = list[i][4]
				movement = previous_d + deposit - withdrawal
				end_of_day_income = movement * 0.0001 if previous_d >= 0 else 0
				account_balance = movement + end_of_day_income

				list[i][5] = end_of_day_income
				list[i][6] = account_balance

				return list
			    else:
				previous_d = list[i - 1][6]
				deposit = list[i][3]
				withdrawal = list[i][4]
				movement = previous_d + deposit - withdrawal
				end_of_day_income = movement * 0.0001 if previous_d > 0 else 0
				account_balance = movement + end_of_day_income

				list[i][5] = end_of_day_income
				list[i][6] = account_balance

				return list
