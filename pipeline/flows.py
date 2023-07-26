from prefect import Flow

#Schedule and taks import
from pipeline.schedules import minute_brt_data
from pipeline.tasks import (collect_data, transform_data, load_data_to_db, materialize_model)


#Flow initialization
with Flow("collect_brt_data", schedule=minute_brt_data) as flow_1:

    #Extract Task
    collect_data()

    #Transform Task
    transform_file = transform_data()


    #Load Tasks into database
    load_data = load_data_to_db(transform_file, upstream_tasks=[transform_file])

    #Run dbt model
    materialize_model(upstream_tasks=[transform_file, load_data])
