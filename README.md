# nu_project

## Data Model Migration Project
---

### Objective:
	Recreate the original database in the snowflake model and migrate it to the star schema.

### Problem Statements

### Problem Statement 1: Generating SQL queries

In this step we generated a query for the proposed problem of monthly account balances.
The query and the generated csv are stored in the path below:

**\Nubank_Analytics_Engineer_Case_4.0\Problem Statement\1_Problem Statement**

**SGBD -> MySQL (default engine).***

	- Amount_Balance_Account.sql
	- Balance Account Monthly.csv
	- Necessary Inputs.txt

A union of three tables wwas used to create a calculation table (CTE).

	- transfer_ins
	- transfer_outs
	- pix_moviments

This table is linked with the customer and accounts table to bring up the account_id and customer name.
The **Total Transfer In**, **Total Transfer Out** e **Account Monthly Balance** columns are calculated in the CTE and take into account the pix moviments as well.


**Note.: The investment table was not used for this problem solution**

**Query**

![image](https://user-images.githubusercontent.com/49626719/175798981-76f8571d-9e85-4143-9b35-0e15c0a21745.png)

**Result**

![image](https://user-images.githubusercontent.com/49626719/175799145-659eda87-6878-4453-88eb-18f785b8723f.png)


### Problem Statement 2:

***a. Proposal for changing the original data model:***

***Snow Flake***

 ![image](https://user-images.githubusercontent.com/49626719/175799521-74982800-a6b6-46f2-8227-54621aecfb63.png)



  ***Star Schema***
  
 ![image](https://user-images.githubusercontent.com/49626719/175793235-fa3da6f6-927c-46fa-b82d-2f5c9bf37ef6.png)


***b. The snowflake model is not the most recommended because it has a higher level of normalization of the data, wich can be slower due to the process of relationships between tables in the model to achieve a certain type of result.
The idea is to consolidate some tables in the model, creating field aggregation.

### Dimensions proposed for the star model:

**Region dimension:**

	From:
		city,
		state,
		country
	to: 
		***d_region***

**Dimension time:**

	From:
		d_time,
		d_weekday
		d_week
		d_month
		d_year
	to:
		**d_calendar**
		
**Transaction Dimension:**

Generate the types of transactions performed from the transfer_ins, transfer_outs, pix_moviments and investments tables and adds an id to favor the relationship with the **f_transaction** table.

		**d_transaction_type**
	
This dimension will help in creating indicators by transaction type.

![image](https://user-images.githubusercontent.com/49626719/175829704-c85263c4-3c65-44d1-b1f5-054e35b253fa.png)


**Transaction Status Dimension:**

Get all transaction statuses (completed, failed) from the transfer_ins, transfer_outs, pix_moviments and investments tables. Generate a single status dimension. d_status_transaction.

		**d_status_transaction**

**Customers dimension:**

To create the customer table, some information was aggregated from the account table, because as both have unique records, I used this strategy to decrease the number of dimensions and keep the relationship with the fact table with as few foreign keys as possible.

**Creation of the FACT table f_transactions:**

The fact table is the consolidation of the foreign keys of all the dimension tables, always using the primary key of each as a reference. Unification of:

	Transfer_ins
	Transfer_outs
	Pix_moviments
	Investments


## How does this project work?

Below I will present the structure to perform all the action of creating the data model, as well as the collection of the original files in their respective folders to populate the database already with the proper relationships.

### Step by step of how the project works:

#### Project Structure:

![image](https://user-images.githubusercontent.com/49626719/175793587-665a639a-8af3-49f4-91b0-4155c0d553e2.png)

#### Passo 1: Database design

Creation of the configuration files: 

• 	credentials_snow_flake.json
•	credentials_snow_star.json
•	tables.json


**Credentials:**

Contains all the information for creating the database schema:

	  - Host
	  - User
	  - Password
	  - Database

The database argument must be passed in order not to generate an error when creating the data model.

**Tables:**

The tables server configuration file to keep aside the entire table structure of the database, as well as the column names, data type and their respective relationships.

**There are two dictionaries:**

	- Snow_flake_tables (Original)
	- Star_Schema_tables (Modelo proposto)
	- Convert_to_datetime

*Whenever you want to change tables in the data model, change relationships and so on, it is in the **tables.json** file that you will make the adjustments.

***The list convert_to_datetime, serves to map all the date columns that need to be treated to their respective UTCs.***

#### Step 2: Action on the created database

Reading the **raw_tables** folder, to create the database. This part of the process consists of reading each directory looking for specific file types **(csv, xlsx, json)**.


1.	Browse the directories within the raw_tables directory and map the files within each folder and enter them into a directory list.
2.	Uses the list to go through the directory again opening the files and consolidating them, thus generating a single dataset.
3.	Converts the generated dataset into a list and passes it to the function, which splits the data into batches to improve the performance of the database insertion.

**Note: The whole process of collecting the files, and running queries on the snow_flake model to insert into the star model is taking about 12 minutes.**

### Log

The whole process is stored in a log to facilitate error analysis and future performance improvement.

***Part of the log of the process execution in the database.***

![image](https://user-images.githubusercontent.com/49626719/175793986-9269d110-cc64-4e9b-b355-dc4cfd23898d.png)


### É possível reproduzir o projeto usando o arquivo requirements.txt
Existe também um backup das informações do projeto no **GitHub** de forma privada.

### Problem Statement 3: Plano de Migração

Para executar uma migração das informações de um banco para o outro sem que haja impacto na operação é necessário análisar os horários com menor volume de transações no banco de dados, bem como avaliar a capacidade do servidor de lidar com a carga de trabalho oferecida pelo processo.
O intuito é manter todos os seriviços em produção em execução sem gargalos.

É muito importante um alinhamento com as áreas de administração de banco de dados, negócio e outras equipes que possam ser impactadas.
As consultas devem ser otimizadas para onerar o mínimo possível os servidores, sejam eles em nuvem ou onpremise.

O plano de carga também deve ser levado em consideração, qual seria a melhor abordagem, coleta de hora em hora, carga histórica e etc. 
É necessário alinhar a estratégia com a equipe para levantamento de possíveis gaps, dessa forma as chances do processo ser executado sem problemas fica muito mais alta.

Usar uma base de testes para fazer uma análise prévia da performance do fluxo criado com um número controlado de informações, afim de estimar o impacto com o volume
real.

### O plano de migração segue o fluxo abaixo:

1. Alimentar os arquivos de configuração do banco de dados na pasta **\project\settings\**, pois são eles que irão criar a conexão entre os bancos necessários.

2. Ler as informações no banco de dados nu_snow_flake através de consultas sql armazenadas no diretório **\project\model\query** e editá-las afim de melhorar a performance delas, caso seja necessário.
	
3. Conectar-se ao banco de dados nu_star_schema  e executar o insert seguindo a ordem das consultas dentro do diretório de queries, para que os relacionamentos sejam criados corretamente.
	
Scripts desse processo:
	
![image](https://user-images.githubusercontent.com/49626719/175793857-8720c7ac-fceb-4fb5-99a0-49526656180e.png)

São scripts com enfâse em leitura de arquivos em diretório, criação de conexão com dois bancos de dados diferentes e execução de select em um e insert 
no outro.
	
**Exemplo: Esse script é reponsável por inserir as informações retiradas do banco snow_flake, para o modelo star**
	
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

	- Quantidade de transações consolidadas por dia
	- Quantidade de transações consolidadas por mês
	- Percentual de crescimento de transações em relação aos demais produtos (transferências, investimentos e etc)
	- Desempenho em relação a meta

**Exemplo:**

![image](https://user-images.githubusercontent.com/49626719/175800943-6ab0e0bc-ae2d-45b8-9f8a-012a5b4eb1c2.png)


***Visão Analítica***

	- Quantidade de transações por hora
	- Quantidade de transações por minuto
	- Quantidade de transações por segundo

**Exemplo:**

![image](https://user-images.githubusercontent.com/49626719/175800966-a2971a03-6b8c-47e8-8fde-91f733cbe754.png)


***Visão Preditiva***

Essa visão irá conter o resultado da predição dos próximos picos de transações por
Minuto, segundo e hora.

O intuito é efetuar um novo balanceamento dos recursos de servidores para o serviço não ser impactado.

**Exemplo**

![image](https://user-images.githubusercontent.com/49626719/175801058-6e8931ca-23f9-49c0-bef5-d478ee988ce8.png)


### Problem Statement 5: Função para calcular o retorno total de um investimento realizado

Abaixo segue o print do arquivo .csv gerado. 

Contas para serem calculados os retornos de investimento.

![image](https://user-images.githubusercontent.com/49626719/175793467-3d198199-483f-4d5e-90c4-7015f86ad23f.png)

 
Foi usado um script python para a leitura do arquivo investment_accounts_to_send.csv e uma função para ler o json de investimentos investments_json com o intuito de gerar uma tabela e a partir daí usando o framework pandas do Python processar o cruzamento das contas com o arquivo de transações.

Principais arquivos da pasta **return_of_investment**:

![image](https://user-images.githubusercontent.com/49626719/175830229-51c7e0a5-521b-4759-b44c-ca212ea472c6.png)

	- process.py 
	  	Arquivo principal. Executa todas as funções necessárias para a geração do arquivo final.
	- calculate.py
		Efetua os cálculos abaixo:
		 - 𝑀𝑜𝑣𝑒𝑚𝑒𝑛𝑡𝑠 = 𝑃𝑟𝑒𝑣𝑖𝑜𝑢𝑠 𝐷𝑎𝑦 𝐵𝑎𝑙𝑎𝑛𝑐𝑒 + 𝐷𝑒𝑝𝑜𝑠𝑖𝑡 − 𝑊𝑖𝑡ℎ𝑑𝑟𝑎𝑤al
		 - 𝐸𝑛𝑑 𝑜𝑓 𝐷𝑎𝑦 𝐼𝑛𝑐𝑜𝑚𝑒 = 𝑀𝑜𝑣𝑒𝑚𝑒𝑛𝑡𝑠 * 𝐼𝑛𝑐𝑜𝑚𝑒 𝑅𝑎𝑡𝑒
		 - 𝐴𝑐𝑐𝑜𝑢𝑛𝑡 𝐷𝑎𝑖𝑙𝑦 𝐵𝑎𝑙𝑎𝑛𝑐𝑒 = 𝑀𝑜𝑣𝑒𝑚𝑒𝑛𝑡𝑠 + 𝐸𝑛𝑑 𝑜𝑓 𝐷𝑎𝑦 𝐼𝑛𝑐𝑜𝑚𝑒	
	- investment_income.csv
		Arquivo final gerado pelo processo. Traz o saldo diário de cada conta enviada.

***Resultado***

![image](https://user-images.githubusercontent.com/49626719/175830195-3fa06e39-73ec-4307-9a0f-408cc2d5bad1.png)


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
