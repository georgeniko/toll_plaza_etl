This mini projects demonstrates a basic ETL procedure of a data pipeline. The goal is to analyze road traffic data from different toll plazas so as to de-congest national highways. In the first part of the project, which is done in the "ETL_toll_data" file, data in different formats (csv,tsv,txt) are collected, transformed and then fitted into a single file of a specific format. The orchestration of the procedure is done with Apache Airflow and the usage of a dag with several tasks. After defining the DAG, it has to be submitted by copying the python file into the AIRFLOW_HOME directory:
"cp ETL_toll_data.py $AIRFLOW_HOME/dags" 
  Then, we can check our dags by running:
 "ariflow dags list|grep "ETL_toll_data""
 
 
The goal of the second part of the project is to create a streaming process of passing cars. As a vehicle passes a toll plaza, the vehicle’s data like vehicle_id,vehicle_type,toll_plaza_id and timestamp are streamed to a Kafka server. After collecting the data, we then load it into a database.

 How to run:
 Make sure you have kafka installed, as well as the modules kafka-python and mysql-connector-python.
 
 Inside the mysql prompt create a database called tolldata and use it. Then, from a different terminal start a zookeeper server and a kafka server. Afterwards, we need to create a sample topic named toll. 
 
 In order to simulate the incoming data from passing vehicles, the toll_traffic_generator.py will be used. Additionally, the straming_data_reader.py is responsible for publishing streaming data from the kafka server to the database. By excecuting the generator we can see at the output of the terminal that it looks like some vehicles are passing the toll plaza. Finally, by excecuting the reader, we can see that the incoming vehicles are inserted into the database. 
 ![alt text](https://github.com/georgeniko/toll_plaza_etl/blob/main/simulator_output.png?raw=true)
 ![alt text](https://github.com/georgeniko/toll_plaza_etl/blob/main/reader_output.png?raw=true)
 This mini project was developed as part of a graded project for the IBM Data Engineering Professional Certificate on Coursera. Source of the dataset: https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz
