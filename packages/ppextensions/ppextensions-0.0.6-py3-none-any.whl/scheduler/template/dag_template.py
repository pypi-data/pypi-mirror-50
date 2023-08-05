"""Copyright (c) 2018, PayPal Inc.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from airflow import DAG
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
from datetime import datetime, timedelta

import configparser
import nbformat
import os

cf = configparser.ConfigParser()
surfix = "_".join(os.path.splitext(os.path.basename(__file__))[0].split('_')[1:])
var_path = os.environ['AIRFLOW_HOME'] + '/variables/var_' + surfix + '.conf'
cf.read(var_path)
dag_id = cf.get("config", "dag_id")
username = cf.get("config", "username")
interval = cf.get("config", "interval")
notebook_path = cf.get("config", "notebook_path")
start = datetime.strptime(cf.get("config", "start"), "%Y-%m-%d %H:%M:%S")
end = datetime.strptime(cf.get("config", "end"), "%Y-%m-%d %H:%M:%S")
emails_failure = cf.get("config", "emails_failure")
emails_success = cf.get("config", "emails_success")
email_on_failure = len(emails_failure) != 0
email_on_success = len(emails_success) != 0
itv = interval.split(" ")
schedule_interval = timedelta(**dict([(itv[1], int(itv[0]))]))


default_args = {
    'owner': username,
    'depends_on_past': False,
    'start_date': start,
    'end_date': end,
    'email': emails_failure.split(","),
    'email_on_failure': email_on_failure,
    'catchup': False,
}


dag = DAG(
    dag_id,
    default_args=default_args,
    schedule_interval=schedule_interval)


def nb_task(ds, **kwargs):
    notebook_dir = os.path.dirname(notebook_path)

    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=21600)
    try:
        out = ep.preprocess(nb, {'metadata': {'path': notebook_dir}})
    except CellExecutionError:
        msg = 'Error executing the notebook "%s".\n\n' % notebook_path
        msg += 'See notebook "%s" for the traceback.' % notebook_path
        print(msg)
        raise
    finally:
        with open(notebook_path, mode='wt') as f:
            nbformat.write(nb, f)


python_operator = PythonOperator(
    task_id='notebook_task',
    provide_context=True,
    python_callable=nb_task,
    dag=dag,
    op_kwargs={'notebook_path': notebook_path},
    run_as_user=username
)

if email_on_success:
    email_operator = EmailOperator(
        task_id='email_task',
        to=emails_success.split(","),
        subject='{} completed successfully'.format(dag_id),
        dag=dag,
        html_content="<p>This job is successfully executed, to customize the email content, please edit dag_template.py</p>"
    )
    email_operator.set_upstream(python_operator)

