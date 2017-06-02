# autofill-sample-database

1. Instale o psycopg2 e o faker
	psycopg2 - http://initd.org/psycopg/docs/install.html
		pip install psycopg2
	faker - https://pypi.python.org/pypi/Faker
		pip install Faker

2. Crie um banco de dados do postgreSQL na sua máquina. 

3. Abra o script autofill-sample-database.py e modifique as primeiras linhas. 
Coloque DBName, DBUser, DBPassword e Host conforme o banco de dados que você criou.

4. Rode o script usando o python 3. O script cria todas tabelas necessarias e da insert em varias tuplas no banco de dados.
	python autofill-sample-database.py

5. Quando o script terminar o banco de dados vai estar cheio de dados. No diretorio do arquivo autofill-sample-database.py serão criados varios arquivos de log com as queries que foram usadas pra criar as tabelas e as tuplas




