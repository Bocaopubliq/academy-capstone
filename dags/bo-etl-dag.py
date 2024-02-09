from conveyor.operators import ConveyorContainerOperatorV2
from datetime import datetime, timedelta
from airflow import DAG
role = "JOBROLE-{{ macros.conveyor.env() }}"
# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'bo-cap-dag_v2',
    default_args=default_args,
    description='Ingest airquality data from s3 and load to snowflake',
    schedule_interval="@daily",
    start_date=datetime(2024,2,7),
    catchup=True,
) as dag:
    bo_etl_task = ConveyorContainerOperatorV2(
        task_id="bo-etl-task",
        aws_role="capstone_conveyor",
        instance_type='mx.micro')
    bo_etl_task