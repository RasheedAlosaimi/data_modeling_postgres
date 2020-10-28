# data_modeling_postgres
Project Overview
This project is a part of the Data Engineering Nano Degree, provided Udacity, and its goal is to build a relational database in order to insert their collected data in the right way to maximize the use of it including analysis and modeling. Specifically, the project is to build a database star schema and ETL pipelines.

Tool used:
-	Postgres for managing the DB
-	Python to implement the ETL pipeline 

Project Repository files
The project is provided with two datasets of song dataset that contains details on the songs, and log dataset which provides details on the users and their activities. The project needs to be performed using five files. Three Python script files of sql_queries.py for creating tables and queries, create_tables.py to call the previous created tables and queries, and etl.py file that contains all the functions needed for implementing the ETL pipeline. The other two files are Jupyter Notebook codes files of etl.ipynb and test.ipynb contains codes for queries to test the functionality of the project. 

Database Design
The database for this project is relational consists of five tables including songplays surrounded by the dimension tables of users, songs, artists, and time of which each is related to the fact table by a single join in order to perform analysis. 



ETL Process (pipeline)


How To Run the Project
Running the ".py" files has to be done through the terminal by typing the “filesName.py” followed by [Enter], making sure that all related files are stored in the same destination. In our case, we run create_tables.py which will first drop existing tables then launch the new tables. The same steps should be done for running etl.py which will execute the pipeline and transfer the data from the data file into our created tables.
