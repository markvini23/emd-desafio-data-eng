{{ config(materialized='table') }}

SELECT codigo_onibus,
       latitude,
       longitude,
       velocidade
from raw.tb_brt_gps