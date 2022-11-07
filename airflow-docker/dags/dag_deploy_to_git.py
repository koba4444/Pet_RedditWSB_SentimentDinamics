import datetime
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import os

default_args = {
    "owner": "kok4444",
    "start_date": pendulum.datetime(2021,1,1,tz="Europe/Moscow"),  # запуск день назад
    #"retries": 1,  # запуск таска до 5 раз, если ошибка
    #"retry_delay": datetime.timedelta(minutes=5),  # дельта запуска при повторе 5 минут
    "task_concurency": 1  # одновременно только 1 таск
}

piplines = {'commit_amend_data_to_github': {"schedule": "*/5 * * * *"}
            #'commit_amend_data_to_github': {"schedule": "*/20 15-18 * * *"}
            #"mr_get_reddit_subs1": {"schedule": "/10 * * * *"}
                    }

def init_dag(dag, task_id):
    with dag:
        dt = str(datetime.datetime.now().microsecond)
        filename = os.path.join(f'./streamlit/pages/{dt}.py')
        #print(filename)
        t1 = BashOperator(
            task_id=f"{task_id}",
            bash_command = f'cd  /streamlit; '
                           f'git config --global --add safe.directory /streamlit;'
                            f'git checkout main;'
                            f'python3 ../src/get_reddit_subs.py;'
                            f'python3 ../src/predict_and_loadtoStreamlit.py;'
                            f' git add output.csv;'
                           f'touch flag.txt;'
                            f' echo {dt} > flag.txt;'
                            f' git add flag.txt;'
                            f' git add main.py;'
                            f' git add ./pages/;'  
                             f'git config --global user.email "you@example.com";'
                            f'git config --global user.name "Your Name";'
                           f'git config --global --add safe.directory /streamlit;'
                           f' git commit -m "{dt}" 2>>commiterrors.txt;'
                            f' git remote add origin git@github.com:koba4444/streamlit_test20220914.git;'
                            f' git push origin main; '


        )
        #bash_command=f'python3 "$(pwd)"/src/{task_id}.py')


    return dag

for task_id, params in piplines.items():
    # DAG - ациклический граф
    dag = DAG(task_id,
              schedule_interval=params['schedule'],
              catchup=False, #Не пытаться выполнить пропущенные задания
              max_active_runs=1,
              default_args=default_args
              )
    init_dag(dag, task_id)
    globals()[task_id] = dag
