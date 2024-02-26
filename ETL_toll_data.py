from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

#DAG arguments

default_args = {
    'owner': 'Michael Scott',
    'start_date': days_ago(0),
    'email': ['Michael@Scott.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

#DAG definition
dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

#Tasks definition

unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='tar -xzf /home/project/tolldata.tgz -C /home/project/airflow/dags/finalassignment/staging',
    dag=dag,
)

#Extract the fields Rowid, Timestamp, Anonymized Vehicle number and Vehicle type from the vehicle-data.csv file
# and then save them into a file named csv_data.csv.
extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='awk \'{print $1","$2","$3","$4}\' vehicle-data.csv > csv_data.csv',
    dag=dag,
)

#Extract the fields Number of axles, Tollplaza id and Tollplaza code from the tollplaza-data.tsv file and then save it into
# a file named tsv_data.csv.
extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut  -f 5,6,7  tollplaza-data.tsv > tsv_data.csv',
    dag=dag,
)

#Extract the fields Type of Payment code and Vehicle Code from the fixed width file payment-data.txt and save it into a file
# named fixed_width_data.csv.
extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='cut  -c 59-62,63-68  payment-data.txt > fixed_width_data.csv',
    dag=dag,
)

#Combine data 
consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste csv_data.csv tsv_data.csv fixed_width_data.csv> extracted_data.csv',
    dag=dag,
)

#Transform the vehicle_type field in extracted_data.csv into capital letters
transform_data = BashOperator(
    task_id='transform_data',
    bash_command='tr "$4""[a-z]" "[A-Z]"<extracted_data.csv> transformed_data.csv',
    dag=dag,
)

#Final Pipeline
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data
