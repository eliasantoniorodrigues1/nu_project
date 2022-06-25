# nu_project
---

## Projeto de migração de modelo de dados
### Objetivo:
	Criar o banco de dados original (floco de neve) e migra-lo para o esquema estrela.

a. Proposta para mudança do modelo de dados original:	

Snow Flake

 ![image](https://user-images.githubusercontent.com/49626719/175793233-99e58a5c-bc10-466f-9b3a-37651e86b53f.png)


  Star Schema
 ![image](https://user-images.githubusercontent.com/49626719/175793235-fa3da6f6-927c-46fa-b82d-2f5c9bf37ef6.png)



b.	O modelo floco de neve não é o mais recomendado pois possui um nível maior de normalização dos dados, o que pode gerar lentidão devido ao acesso de relacionamentos entre tabelas do modelo para alcançar um determinado tipo de resultado.
A ideia é consolidar algumas tabelas do modelo, criando agregação de campos.

Dimensão de região:
De:
city,
state,
country
para:
d_region
	Dimensão tempo:
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
As tabelas customers e accounts será mantida da forma em que se encontra.
Criação da tabela Fato:
A tabela fato pode ser uma consolidação de todas as movimentações de uma conta. Ela seria a unificação de:
	Transfer_ins
	Transfer_outs
	Pix_moviments
	Investments


Como esse projeto funciona?
Abaixo irei apresentar a estrutura para executar toda a ação de criação do modelo de dados, bem como a coleta dos arquivos originais em suas respectivas pastas para popular o banco já com os devidos relacionamentos.

Passo a passo do funcionamento do projeto:
Passo 1: Design da base de dados
Criação dos arquivos de configuração: 
•	credentials.json
•	tables.json
Credenciais:
	Contém todas as informações para a criação do esquema de banco de dados.
	Host
	User
	Password
	Database
O argumento database precisa ser passado para não gerar erro na criação do modelo de dados.

Tables:
O arquivo de configuração das tabelas server para manter a parte toda a estrutura de tabelas do banco, bem como os nomes das colunas, tipo de dados e relacionamentos.
Existem dois dicionários:
•	Snow_flake_tables (Original)
•	Star_Schema_tables (Modelo proposto)
•	Convert_to_datetime
A lista convert_to_datetime, server para mapear todas as colunas de data que precisam de tratamento em seus respectivos UTCs.
Passo 2: Ação na base de dados criada
Leitura da pasta raw_tables, para criação do banco de dados.
Essa parte do processo consiste em ler cada diretório buscando por tipos específicos de arquivos (csv, xlsx, json).
1.	Percorrer os diretórios dentro do diretório raw_tables e mapeia os arquivos dentro de cada pasta e os insere em uma lista.
2.	Usa a lista para percorrer o diretório novamente abrindo os arquivos e os consolidando, gerando assim um único dataset.
3.	Converte o dataset gerado em lista e passa para a função, que divide os dados em lotes para melhorar a performance da inserção no banco de dados.
Log
Todo o processo é armazenado em log para facilitar análise de erros e melhoria de performance.

É possível reproduzir o projeto usando o arquivo requirements.txt

Problem Statements

Problem Statement 1: Gerando consultas SQL
Essa etapa gerar a consulta para o problema proposto de saldo mensal das contas. A consulta e o csv gerado estão armazenados no caminho abaixo:
Nubank_Analytics_Engineer_Case_4.0\Problem Statement\1_Problem Statement
A engine de banco de dados usada é o MySQL.
•	Amount_Balance_Account.sql
•	Balance Account Monthly.csv
•	Necessary Inputs.txt

Problem Statement 4: Proposta de KPIs para o Pix
O pix é um produto com uma alta de manda de transações. Para acompanhar o desempenho desse produto eu sugiro a criação dos seguintes indicadores:
Visão Gerencial
•	Quantidade de transações consolidadas por dia
•	Quantidade de transações consolidadas por mês
•	Percentual de crescimento de transações em relação aos demais produtos (transferências, investimentos e etc)
•	Desempenho em relação a meta

Visão Analítica
•	Quantidade de transações por hora
•	Quantidade de transações por minuto
•	Quantidade de transações por segundo
Visão Preditiva
•	Essa visão irá conter o resultado da predição dos próximos picos de transações por
Minuto, segundo e hora.
O intuito é efetuar um novo balanceamento dos recursos de servidores para o serviço não ser impactado.

Problem Statement 5: Função para calcular o retorno total de um investimento realizado
Abaixo segue o print do arquivo .csv gerado. 
Contas para serem calculados os retornos de investimento.
 
Foi usado um script python para a leitura do arquivo investment_accounts_to_send.csv e uma função para ler o json de investimentos investments_json com o intuito de gerar uma tabela e a partir daí usando o framework pandas do Python processar o cruzamento das contas com o arquivo de transações.
 
